#!/usr/bin/env python3
"""
AWS Lambda Deployment Script
Deploys the lambda function to AWS
"""

import boto3
import zipfile
import os
import json
from botocore.exceptions import ClientError, NoCredentialsError
import click


class LambdaDeployer:
    """AWS Lambda deployment manager"""
    
    def __init__(self, region='us-east-1'):
        """Initialize the Lambda deployer"""
        try:
            self.lambda_client = boto3.client('lambda', region_name=region)
            self.iam_client = boto3.client('iam', region_name=region)
            self.region = region
            click.echo(click.style("✓ AWS Lambda Deployer initialized", fg="green"))
        except NoCredentialsError:
            click.echo(click.style("✗ AWS credentials not found. Please configure AWS credentials.", fg="red"))
            exit(1)
        except Exception as e:
            click.echo(click.style(f"✗ Error initializing Lambda deployer: {str(e)}", fg="red"))
            exit(1)
    
    def create_deployment_package(self, function_name):
        """Create deployment package for Lambda function"""
        try:
            # Create a temporary directory for the package
            package_dir = f"lambda_packages/{function_name}"
            os.makedirs(package_dir, exist_ok=True)
            
            # Copy the lambda function
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
            return zip_path
            
        except Exception as e:
            click.echo(click.style(f"✗ Error creating deployment package: {str(e)}", fg="red"))
            return None
    
    def create_lambda_role(self, role_name):
        """Create IAM role for Lambda function"""
        try:
            # Check if role exists
            try:
                self.iam_client.get_role(RoleName=role_name)
                click.echo(click.style(f"✓ Role '{role_name}' already exists", fg="yellow"))
                return f"arn:aws:iam::{self.get_account_id()}:role/{role_name}"
            except ClientError as e:
                if e.response['Error']['Code'] != 'NoSuchEntity':
                    raise
            
            # Create trust policy
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            # Create the role
            response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Lambda execution role'
            )
            
            # Attach basic execution policy
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
            )
            
            click.echo(click.style(f"✓ Created Lambda role: {role_name}", fg="green"))
            return response['Role']['Arn']
            
        except ClientError as e:
            click.echo(click.style(f"✗ Error creating Lambda role: {str(e)}", fg="red"))
            return None
    
    def get_account_id(self):
        """Get AWS account ID"""
        try:
            sts_client = boto3.client('sts')
            response = sts_client.get_caller_identity()
            return response['Account']
        except Exception as e:
            click.echo(click.style(f"✗ Error getting account ID: {str(e)}", fg="red"))
            return None
    
    def deploy_lambda_function(self, function_name, zip_path, role_arn):
        """Deploy Lambda function"""
        try:
            # Read the zip file
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            
            # Check if function exists
            try:
                self.lambda_client.get_function(FunctionName=function_name)
                # Function exists, update it
                response = self.lambda_client.update_function_code(
                    FunctionName=function_name,
                    ZipFile=zip_content
                )
                click.echo(click.style(f"✓ Updated Lambda function: {function_name}", fg="green"))
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceNotFoundException':
                    raise
                
                # Function doesn't exist, create it
                response = self.lambda_client.create_function(
                    FunctionName=function_name,
                    Runtime='python3.9',
                    Role=role_arn,
                    Handler='lambda_function.lambda_handler',
                    Code={'ZipFile': zip_content},
                    Description='Python DevOps Lambda function'
                )
                click.echo(click.style(f"✓ Created Lambda function: {function_name}", fg="green"))
            
            return response['FunctionArn']
            
        except ClientError as e:
            click.echo(click.style(f"✗ Error deploying Lambda function: {str(e)}", fg="red"))
            return None
    
    def test_lambda_function(self, function_name):
        """Test the deployed Lambda function"""
        try:
            test_event = {
                "name": "Python DevOps"
            }
            
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(test_event)
            )
            
            result = json.loads(response['Payload'].read())
            click.echo(click.style(f"✓ Lambda test successful: {result['body']}", fg="green"))
            return True
            
        except ClientError as e:
            click.echo(click.style(f"✗ Error testing Lambda function: {str(e)}", fg="red"))
            return False


@click.command()
@click.option('--function-name', default='python-devops-lambda', help='Lambda function name')
@click.option('--region', default='us-east-1', help='AWS region')
def main(function_name, region):
    """Deploy Lambda function to AWS"""
    
    click.echo(click.style("🚀 Starting Lambda deployment...", fg="blue", bold=True))
    
    # Initialize deployer
    deployer = LambdaDeployer(region)
    
    # Create deployment package
    zip_path = deployer.create_deployment_package(function_name)
    if not zip_path:
        return
    
    # Create Lambda role
    role_name = f"{function_name}-role"
    role_arn = deployer.create_lambda_role(role_name)
    if not role_arn:
        return
    
    # Deploy function
    function_arn = deployer.deploy_lambda_function(function_name, zip_path, role_arn)
    if not function_arn:
        return
    
    # Test function
    if deployer.test_lambda_function(function_name):
        click.echo(click.style("✅ Lambda deployment completed successfully!", fg="green", bold=True))
        click.echo(click.style(f"Function ARN: {function_arn}", fg="blue"))
    else:
        click.echo(click.style("❌ Lambda deployment failed!", fg="red", bold=True))


if __name__ == '__main__':
    main()
