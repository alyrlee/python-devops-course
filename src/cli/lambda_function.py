import json

def lambda_handler(event, context):
    """
    Basic AWS Lambda function example.
    """
    name = event.get("name", "World")
    message = f"Hello, {name}! Welcome to AWS Lambda."

    # Log something
    print(f"Greeting generated for: {name}")

    return {
        "statusCode": 200,
        "body": message
    }
