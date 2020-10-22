import boto3
import botocore.exceptions

class DynamoDB:
    def __init__(self, tableName):
        self.dynamodb = boto3.client('dynamodb')
        self.tableName = tableName

    def status_database(self):
        table_status = self._table_status()
        if not table_status:
            self._create_db()

        return 'ok'

    def _table_status(self):
        try:
            response = self.dynamodb.describe_table(
                TableName=self.tableName
            )
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                return False
            else:
                raise Exception(f'Failed in check DB: {err}')
        except Exception as err:
            raise Exception(f'Failed in check DB: {err}')

        return response['Table']['TableStatus']

    def _create_db(self):
        try:
            response = self.dynamodb.create_table(
                TableName=self.tableName,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'provider',
                        'AttributeType': 'S'
                     },
                    {
                        'AttributeName': 'network',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'mask',
                        'AttributeType': 'S'
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'provider',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'network',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'mask',
                        'KeyType': 'HASH'
                    }
                ],
            )

            # Wait table to be available
            response.wait_until_exists()
        except Exception as err:
            raise Exception(f'Failed in create DB: {err}')

        return response['TableDescription']['TableStatus']

    def update_item(self, event):
        response = self.dynamodb.put_item(
            TableName=self.tableName,
            Item={**event}
        )
        pass