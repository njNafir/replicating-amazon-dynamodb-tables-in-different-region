# Copyright (C) 2018 Dineshkarthik Raveendran

from __future__ import print_function  # Python 2/3 compatibility
import boto3
import argparse


def replicate(table_name, existing_region, new_region, new_table_name):
    """
    Replicate table in new region.

    Creates a new table with existing KeySchema and AttributeDefinitions
    read and write capacity untis are set to 5. Change it as required.


    Parameters
    ----------
    table_name: string
        Name of the existing table to be replicated.
    existing_region: string
        Region in which the table is present.
    new_region: string
        Region in which the table needs to be replicated.
    new_table_name: string
        Name for the new table to be created, if not given
        existing table name is used.
    """

    existing_table = boto3.resource(
        'dynamodb', region_name=existing_region).Table(table_name)
    items = existing_table.scan()['Items']

    dynamodb = boto3.resource('dynamodb', region_name=new_region)

    print("Creating table '{0}' in region '{1}'".format(
        new_table_name, new_region))

    table = dynamodb.create_table(
        TableName=new_table_name,
        KeySchema=existing_table.key_schema,
        AttributeDefinitions=existing_table.attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        })
    print("Table status:", table.table_status)

    table.wait_until_exists()
    table.reload()

    print("Table status:", table.table_status)
    print("Updating table with data...")
    if table.table_status == 'ACTIVE':
        for item in items:
            response = table.put_item(Item=item)
            print("PutItem status:",
                  response['ResponseMetadata']['HTTPStatusCode'])

    print("Total items created:", table.scan()['Count'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--table_name',
        type=str,
        required=True,
        help="Name of the table to be replicated in new region")
    parser.add_argument(
        '-r',
        '--region',
        type=str,
        required=True,
        help="Region in which the table is present")
    parser.add_argument(
        '-nr',
        '--new_region',
        type=str,
        required=True,
        help="Region in which the table needs to be replicated")
    parser.add_argument(
        '-nt',
        '--new_table_name',
        type=str,
        help="Name for the new table [Optional], Old table name will be used")
    args = parser.parse_args()
    if args.new_table_name is None:
        args.new_table_name = args.table_name

    replicate(args.table_name, args.region, args.new_region,
              args.new_table_name)