from Amazon.aws import DynamoDB
import os


def handler(event):
    tableName = os.getenv('TABLE_NAME')
    dynamodb = DynamoDB(tableName)

    dynamodb.status_database()

    dynamodb.update_item(event)


if __name__ == "__main__":
    event = {
        "provider": "Amazon",
        "mask": 8,
        "range": "10.0.0.0"
    }
    print(handler(event))