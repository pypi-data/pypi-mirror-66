import os
import click
import boto3
from dyndb import DynamoExporter, DynamoImporter

@click.group()
def main():
    pass

@main.command('export')
@click.option('-t', '--table', help='DynamoDB table to export', required=True)
@click.option('-r', '--region', help='AWS region', default='eu-central-1')
@click.option('-f', '--format', help='Format file [csv/json].', type=click.Choice(['json','csv']), default='csv')
@click.option('-o', '--output', help='Output directory', type=click.Path(), default=os.path.join(os.getcwd(),'out'))
def exp(table, region, format, output):
    """
    Export data from DynamoDB table
    """
    clz = DynamoExporter(table_name=table, region=region)

    data = clz.get_data()

    if not os.path.isdir(output):
        os.makedirs(output)

    if data:        
        if format == 'json':
            clz.write_to_json_file(data, os.path.join(output, '{}.json'.format(table)))
        else:
            clz.write_to_csv_file(data, os.path.join(output, '{}.csv'.format(table)))
    else:
        click.echo('No data to export')

@main.command('import')
@click.option('-t', '--table', help='DynamoDB table to export')
@click.option('-r', '--region', help='AWS region', default='eu-central-1')
@click.option('-f', '--file', help='File', type=click.Path(), required=True)
def imp(table, region, file):
    """
    Import data into DynamoDB table
    """
    base = os.path.splitext(os.path.basename(file))
    format = base[1][1:]

    if not table:
        table = base[0]

    clz = DynamoImporter(table_name=table, region=region)

    clz.import_file(file, format=format)

@main.command()
@click.option('-r', '--region', help='AWS region', default='eu-central-1')
@click.option('-l', '--limit', help='A maximum number of table names to return', default=100)
def list(region, limit):
    """
    List all available DynamoDB tables
    """
    client = boto3.client('dynamodb', region_name=region)

    response = client.list_tables(
        Limit = limit
    )

    click.echo('\nFound {} DynamoDB tables in region {}.\n'.format(len(response['TableNames']),region))

    for t in response['TableNames']:
        click.echo(' - {}'.format(t))


@main.command('truncate')
@click.option('-t', '--table', help='DynamoDB table to export', required=True)
@click.option('-r', '--region', help='AWS region', default='eu-central-1')
def trunc(table, region):
    """
    Truncate all items from DynamoDB table
    """
    click.confirm("About to truncate table '{}'. Are you sure?".format(table), abort=True)

    resource = boto3.resource('dynamodb', region_name=region)

    table = resource.Table(table)

    keys = []

    for item in table.attribute_definitions:
        keys.append(item['AttributeName'])

    scan = table.scan()

    with table.batch_writer() as batch:
        for item in scan['Items']:
            batch.delete_item(
                Key = { k: v for k, v in item.items() if k in keys}
            )