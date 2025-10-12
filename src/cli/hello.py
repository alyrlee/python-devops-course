import click
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


@click.command()
@click.option('--region', default='us-east-1', help='AWS region')
def buckets(region):
    """This is a commandline tool that lists all the buckets in an AWS account"""
    try:
        s3 = boto3.client('s3', region_name=region)
        all_buckets = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in all_buckets['Buckets']]
        click.echo(
            click.style(f"Available buckets: {bucket_names}", bg="yellow", fg="blue")
        )
    except NoCredentialsError:
        click.echo(click.style("✗ AWS credentials not found. Please configure AWS credentials.", fg="red"))
    except ClientError as e:
        click.echo(click.style(f"✗ Error accessing S3: {str(e)}", fg="red"))


if __name__ == "__main__":
    buckets()    