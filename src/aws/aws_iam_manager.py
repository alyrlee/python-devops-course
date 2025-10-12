#!/usr/bin/env python3
"""
AWS IAM Role and Policy Management Script
Creates Cloud9 service role with AWSCloud9ServiceRolePolicy and attaches to user
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError, NoCredentialsError
import click
from typing import Optional, List


class AWSIAMManager:
    """AWS IAM Manager for creating roles, policies, and user attachments"""

    def __init__(self, region: str = "us-east-1"):
        """Initialize the AWS IAM Manager"""
        try:
            self.iam_client = boto3.client("iam", region_name=region)
            self.sts_client = boto3.client("sts", region_name=region)
            self.region = region
            click.echo(
                click.style("✓ AWS IAM Manager initialized successfully", fg="green")
            )
        except NoCredentialsError:
            click.echo(
                click.style(
                    "✗ AWS credentials not found. Please configure AWS credentials.",
                    fg="red",
                )
            )
            sys.exit(1)
        except ClientError as e:
            click.echo(
                click.style(f"✗ Error initializing AWS IAM Manager: {str(e)}", fg="red")
            )
            sys.exit(1)

    def get_account_id(self) -> str:
        """Get the AWS account ID"""
        try:
            response = self.sts_client.get_caller_identity()
            return response["Account"]
        except ClientError as e:
            click.echo(click.style(f"✗ Error getting account ID: {str(e)}", fg="red"))
            sys.exit(1)

    def create_cloud9_trust_policy(self) -> dict:
        """Create trust policy for Cloud9 service role"""
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "cloud9.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
        return trust_policy

    def create_cloud9_role(self, role_name: str) -> bool:
        """Create Cloud9 service role"""
        try:
            # Check if role already exists
            try:
                self.iam_client.get_role(RoleName=role_name)
                click.echo(
                    click.style(f"✓ Role '{role_name}' already exists", fg="yellow")
                )
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] != "NoSuchEntity":
                    raise
            except (ValueError, KeyError, AttributeError) as e:
                if "NoSuchEntity" not in str(e):
                    raise

            # Create the role
            trust_policy = self.create_cloud9_trust_policy()
            self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Cloud9 service role for development environment",
                Tags=[
                    {"Key": "Purpose", "Value": "Cloud9ServiceRole"},
                    {"Key": "Environment", "Value": "Development"},
                ],
            )

            click.echo(
                click.style(f"✓ Created Cloud9 service role: {role_name}", fg="green")
            )
            return True

        except ClientError as e:
            click.echo(click.style(f"✗ Error creating role: {str(e)}", fg="red"))
            return False

    def attach_managed_policies(self, role_name: str, policy_arns: List[str]) -> bool:
        """Attach AWS managed policies to the role"""
        try:
            for policy_arn in policy_arns:
                try:
                    self.iam_client.attach_role_policy(
                        RoleName=role_name, PolicyArn=policy_arn
                    )
                    policy_name = policy_arn.split("/")[-1]
                    click.echo(
                        click.style(f"✓ Attached policy: {policy_name}", fg="green")
                    )
                except ClientError as e:
                    if e.response["Error"]["Code"] == "EntityAlreadyExists":
                        policy_name = policy_arn.split("/")[-1]
                        click.echo(
                            click.style(
                                f"⚠ Policy {policy_name} already attached", fg="yellow"
                            )
                        )
                    else:
                        click.echo(
                            click.style(
                                f"✗ Error attaching policy {policy_arn}: {str(e)}",
                                fg="red",
                            )
                        )
                        return False
            return True
        except ClientError as e:
            click.echo(click.style(f"✗ Error attaching policies: {str(e)}", fg="red"))
            return False

    def create_user(self, username: str) -> bool:
        """Create IAM user if it doesn't exist"""
        try:
            # Check if user exists
            try:
                self.iam_client.get_user(UserName=username)
                click.echo(
                    click.style(f"✓ User '{username}' already exists", fg="yellow")
                )
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] != "NoSuchEntity":
                    raise
            except (ValueError, KeyError, AttributeError) as e:
                if "NoSuchEntity" not in str(e):
                    raise

            # Create the user
            self.iam_client.create_user(
                UserName=username, Tags=[{"Key": "Purpose", "Value": "Cloud9User"}]
            )
            click.echo(click.style(f"✓ Created user: {username}", fg="green"))
            return True

        except ClientError as e:
            click.echo(click.style(f"✗ Error creating user: {str(e)}", fg="red"))
            return False

    def attach_role_to_user(self, username: str, role_name: str) -> bool:
        """Attach role to user by creating an inline policy that allows assuming the role"""
        try:
            account_id = self.get_account_id()
            role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

            # Create inline policy for assuming the role
            assume_role_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "sts:AssumeRole",
                        "Resource": role_arn,
                    }
                ],
            }

            policy_name = f"{role_name}AssumeRolePolicy"

            # Check if policy already exists
            try:
                self.iam_client.get_user_policy(
                    UserName=username, PolicyName=policy_name
                )
                click.echo(
                    click.style(
                        f"✓ Policy {policy_name} already attached to user", fg="yellow"
                    )
                )
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] != "NoSuchEntity":
                    raise
            except (ValueError, KeyError, AttributeError) as e:
                if "NoSuchEntity" not in str(e):
                    raise

            # Attach the policy
            self.iam_client.put_user_policy(
                UserName=username,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(assume_role_policy),
            )

            click.echo(
                click.style(
                    f"✓ Attached role {role_name} to user {username}", fg="green"
                )
            )
            return True

        except ClientError as e:
            click.echo(
                click.style(f"✗ Error attaching role to user: {str(e)}", fg="red")
            )
            return False

    def create_access_key(self, username: str) -> Optional[dict]:
        """Create access key for the user"""
        try:
            response = self.iam_client.create_access_key(UserName=username)
            access_key = response["AccessKey"]
            click.echo(
                click.style(f"✓ Created access key for user {username}", fg="green")
            )
            return access_key
        except ClientError as e:
            click.echo(click.style(f"✗ Error creating access key: {str(e)}", fg="red"))
            return None

    def setup_cloud9_environment(self, role_name: str, username: str) -> bool:
        """Complete setup for Cloud9 environment"""
        try:
            # AWS managed policies for Cloud9
            cloud9_policies = [
                "arn:aws:iam::aws:policy/AWSCloud9ServiceRolePolicy",
                "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
                "arn:aws:iam::aws:policy/AmazonS3FullAccess",
                "arn:aws:iam::aws:policy/AmazonVPCFullAccess",
            ]

            # Create role
            if not self.create_cloud9_role(role_name):
                return False

            # Attach policies
            if not self.attach_managed_policies(role_name, cloud9_policies):
                return False

            # Create user
            if not self.create_user(username):
                return False

            # Attach role to user
            if not self.attach_role_to_user(username, role_name):
                return False

            return True

        except ClientError as e:
            click.echo(
                click.style(
                    f"✗ Error setting up Cloud9 environment: {str(e)}", fg="red"
                )
            )
            return False


@click.command()
@click.option(
    "--role-name", default="Cloud9ServiceRole", help="Name of the Cloud9 service role"
)
@click.option("--username", default="cloud9-user", help="Name of the IAM user")
@click.option("--region", default="us-east-1", help="AWS region")
@click.option(
    "--create-access-key", is_flag=True, help="Create access key for the user"
)
def main(role_name: str, username: str, region: str, create_access_key: bool):
    """AWS IAM Manager - Create Cloud9 service role and attach to user"""

    click.echo(
        click.style("🚀 Starting AWS IAM setup for Cloud9...", fg="blue", bold=True)
    )

    # Initialize AWS IAM Manager
    iam_manager = AWSIAMManager(region)

    # Setup Cloud9 environment
    if iam_manager.setup_cloud9_environment(role_name, username):
        click.echo(
            click.style(
                "✅ Cloud9 environment setup completed successfully!",
                fg="green",
                bold=True,
            )
        )

        if create_access_key:
            access_key = iam_manager.create_access_key(username)
            if access_key:
                click.echo(
                    click.style("\n🔑 Access Key Details:", fg="blue", bold=True)
                )
                click.echo(f"Access Key ID: {access_key['AccessKeyId']}")
                click.echo(f"Secret Access Key: {access_key['SecretAccessKey']}")
                click.echo(
                    click.style(
                        "\n⚠️  IMPORTANT: Save these credentials securely!",
                        fg="red",
                        bold=True,
                    )
                )
    else:
        click.echo(
            click.style("❌ Cloud9 environment setup failed!", fg="red", bold=True)
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
