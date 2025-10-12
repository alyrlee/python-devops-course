#!/usr/bin/env python3
"""
Deploy Lambda with specific role ARN
"""

import boto3
import zipfile
import os
import json
from botocore.exceptions import ClientError, NoCredentialsError
import click


@click.command()
@click.option('--function-name', default='python-devops-lambda', help='Lambda function name')
@click.option('--region', default='us-east-1', help='AWS region')
def main(function_name, region):
    """Deploy Lambda function with Lambda_Service role"""
    
    # Use the specific role ARN found in your account
    role_arn = "arn:aws:iam::699300400361:role/Lambda_Service"
    
    click.echo(click.style(f"🚀 Deploying Lambda with role: {role_arn}", fg="blue", bold=True))
    
    try:
        lambda_client = boto3.client('lambda', region_name=region)
        
        # Create deployment package
        package_dir = f"lambda_packages/{function_name}"
        os.makedirs(package_dir, exist_ok=True)
        
        lambda_code = """
import json

def lambda_handler(event, context):
    '''
    Basic AWS Lambda function example.
    '''
    name = event.get("name", "World")
    message = f"Hello, {name}! Welcome to AWS Lambda."

    # Log something
    print(f"Greeting generated for: {name}")

    return {
        "statusCode": 200,
        "body": message
    }
"""
        
        with open(f"{package_dir}/lambda_function.py", "w") as f:
            f.write(lambda_code)
        
        # Create zip file
        zip_path = f"{package_dir}.zip"
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(f"{package_dir}/lambda_function.py", "lambda_function.py")
        
        click.echo(click.style(f"✓ Created deployment package: {zip_path}", fg="green"))
        
        # Read the zip file
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        # Check if function exists
        try:
            lambda_client.get_function(FunctionName=function_name)
            # Function exists, update it
            response = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            click.echo(click.style(f"✓ Updated Lambda function: {function_name}", fg="green"))
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceNotFoundException':
                raise
            
            # Function doesn't exist, create it
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Description='Python DevOps Lambda function'
            )
            click.echo(click.style(f"✓ Created Lambda function: {function_name}", fg="green"))
        
        # Test the function
        test_event = {"name": "Python DevOps"}
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(test_event)
        )
        
        result = json.loads(response['Payload'].read())
        click.echo(click.style(f"✓ Lambda test successful: {result['body']}", fg="green"))
        
        # Get the function ARN from the function configuration
        function_response = lambda_client.get_function(FunctionName=function_name)
        function_arn = function_response['Configuration']['FunctionArn']
        
        click.echo(click.style("✅ Lambda deployment completed successfully!", fg="green", bold=True))
        click.echo(click.style(f"Function ARN: {function_arn}", fg="blue"))
        
    except NoCredentialsError:
        click.echo(click.style("✗ AWS credentials not found. Please configure AWS credentials.", fg="red"))
    except ClientError as e:
        click.echo(click.style(f"✗ Error deploying Lambda: {str(e)}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"✗ Unexpected error: {str(e)}", fg="red"))


if __name__ == '__main__':
    main()
