import json
import csv
import boto3

import dyndb

class DynamoExporter():
    def __init__(self, table_name, region):
        self.resource = boto3.resource('dynamodb', region_name=region)
        self.table_name = table_name
        self.region = region
        self.table = self.resource.Table(table_name)

    def __get_keys(self, data):
        keys = set([])
        for item in data:
            keys = keys.union(set(item))
        return keys

    def __convert_rawdata_to_stringvalue(self, data):
        """
        Convert raw data to string value.
        :param data: List of dictionary
        :return: String value.
        """
        ret = []
        for item in data:
            obj = {}
            for k, v in item.items():
                obj[k] = str(v)
            ret.append(obj)
        return ret

    def get_data(self):
        keys = []

        for item in self.table.attribute_definitions:
            keys.append(item['AttributeName'])

        keys_set = set(keys)

        item_count = self.table.item_count

        raw_data = self.table.scan()
        if not raw_data:
            return None

        items = raw_data['Items']
        fieldnames = set([]).union(self.__get_keys(items))

        cur_total = (len(items) + raw_data['Count'])
        if cur_total > item_count:
            percents = 99.99
        else:
            percents = cur_total * 100 / item_count

        print("{} records ..... {:02.0f}%".format(raw_data['Count'], percents), end='\r')

        while raw_data.get('LastEvaluatedKey'):
            print('Downloading ', end='')
            raw_data = self.table.scan(ExclusiveStartKey=raw_data['LastEvaluatedKey'])
            items.extend(raw_data['Items'])
            fieldnames = fieldnames.union(self.__get_keys(items))
            cur_total = (len(items) + raw_data['Count'])
            if cur_total > item_count:
                percents = 99.99
            else:
                percents = cur_total * 100 / item_count

            print("{} records ..... {:02.0f}%".format(raw_data['Count'], percents), end='\r')

        print("\nTotal downloaded records: {}".format(len(items)))

        for fieldname in fieldnames:
            if fieldname not in keys:
                keys.append(fieldname)

        return {'items': items, 'keys': keys}

    def write_to_json_file(self, data, filename):
        """
        Write to a json file
        :param data: Dictionary
        :param filename: output file name.
        :return: None
        """
        if data is None:
            return

        print("Writing to json file.")
        with open(filename, 'w') as f:
            f.write(json.dumps(self.__convert_rawdata_to_stringvalue(data['items'])))

    def write_to_csv_file(self, data, filename):
        """
        Write to a csv file.
        :param data:
        :param filename:
        :return: True
        """
        if data is None:
            return

        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=data['keys'], quotechar='"')
            writer.writeheader()
            writer.writerows(data['items'])

        print(f"\nSucccessfully exported {len(data['items'])} item(s) from '{filename}'\n")
        return True