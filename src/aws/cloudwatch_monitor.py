#!/usr/bin/env python3
"""
CloudWatch Monitoring and Logging Utilities
Enhanced CloudWatch integration for the Python DevOps project
"""

import boto3

# Removed unused imports
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, NoCredentialsError
import click
from typing import List, Dict, Optional


class CloudWatchMonitor:
    """CloudWatch monitoring and logging utilities"""

    def __init__(self, region: str = "us-east-1"):
        """Initialize CloudWatch monitor"""
        try:
            self.logs_client = boto3.client("logs", region_name=region)
            self.cloudwatch_client = boto3.client("cloudwatch", region_name=region)
            self.lambda_client = boto3.client("lambda", region_name=region)
            self.region = region
            click.echo(click.style("✓ CloudWatch Monitor initialized", fg="green"))
        except NoCredentialsError:
            click.echo(
                click.style(
                    "✗ AWS credentials not found. Please configure AWS credentials.",
                    fg="red",
                )
            )
            exit(1)
        except ClientError as e:
            click.echo(
                click.style(
                    f"✗ Error initializing CloudWatch Monitor: {str(e)}", fg="red"
                )
            )
            exit(1)

    def get_lambda_logs(self, function_name: str, hours: int = 24) -> List[Dict]:
        """Get Lambda function logs from CloudWatch"""
        try:
            log_group_name = f"/aws/lambda/{function_name}"

            # Calculate start time
            start_time = int(
                (datetime.now() - timedelta(hours=hours)).timestamp() * 1000
            )

            # Get log streams
            response = self.logs_client.describe_log_streams(
                logGroupName=log_group_name,
                orderBy="LastEventTime",
                descending=True,
                limit=10,
            )

            logs = []
            for stream in response["logStreams"]:
                # Get log events from each stream
                events_response = self.logs_client.get_log_events(
                    logGroupName=log_group_name,
                    logStreamName=stream["logStreamName"],
                    startTime=start_time,
                )

                for event in events_response["events"]:
                    logs.append(
                        {
                            "timestamp": datetime.fromtimestamp(
                                event["timestamp"] / 1000
                            ),
                            "message": event["message"],
                            "stream": stream["logStreamName"],
                        }
                    )

            return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

        except ClientError as e:
            click.echo(click.style(f"✗ Error getting logs: {str(e)}", fg="red"))
            return []

    def get_lambda_metrics(self, function_name: str, hours: int = 24) -> Dict:
        """Get Lambda function CloudWatch metrics"""
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)

            metrics = {}

            # Get invocation count
            invocations = self.cloudwatch_client.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Invocations",
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour
                Statistics=["Sum"],
            )

            # Get error count
            errors = self.cloudwatch_client.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Errors",
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=["Sum"],
            )

            # Get duration
            duration = self.cloudwatch_client.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Duration",
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=["Average", "Maximum"],
            )

            metrics["invocations"] = sum(
                point["Sum"] for point in invocations["Datapoints"]
            )
            metrics["errors"] = sum(point["Sum"] for point in errors["Datapoints"])
            metrics["avg_duration"] = (
                sum(point["Average"] for point in duration["Datapoints"])
                / len(duration["Datapoints"])
                if duration["Datapoints"]
                else 0
            )
            metrics["max_duration"] = (
                max(point["Maximum"] for point in duration["Datapoints"])
                if duration["Datapoints"]
                else 0
            )

            return metrics

        except ClientError as e:
            click.echo(click.style(f"✗ Error getting metrics: {str(e)}", fg="red"))
            return {}

    def create_custom_metric(
        self, namespace: str, metric_name: str, value: float, unit: str = "Count"
    ):
        """Create custom CloudWatch metric"""
        try:
            self.cloudwatch_client.put_metric_data(
                Namespace=namespace,
                MetricData=[
                    {
                        "MetricName": metric_name,
                        "Value": value,
                        "Unit": unit,
                        "Timestamp": datetime.now(),
                    }
                ],
            )
            click.echo(
                click.style(f"✓ Custom metric {metric_name} created", fg="green")
            )
            return True
        except ClientError as e:
            click.echo(click.style(f"✗ Error creating metric: {str(e)}", fg="red"))
            return False

    def get_lambda_function_info(self, function_name: str) -> Optional[Dict]:
        """Get detailed Lambda function information"""
        try:
            response = self.lambda_client.get_function(FunctionName=function_name)
            return {
                "name": response["Configuration"]["FunctionName"],
                "arn": response["Configuration"]["FunctionArn"],
                "runtime": response["Configuration"]["Runtime"],
                "handler": response["Configuration"]["Handler"],
                "state": response["Configuration"]["State"],
                "last_modified": response["Configuration"]["LastModified"],
                "code_size": response["Configuration"]["CodeSize"],
                "memory_size": response["Configuration"]["MemorySize"],
                "timeout": response["Configuration"]["Timeout"],
            }
        except ClientError as e:
            click.echo(
                click.style(f"✗ Error getting function info: {str(e)}", fg="red")
            )
            return None


@click.command()
@click.option(
    "--function-name", default="python-devops-lambda", help="Lambda function name"
)
@click.option("--region", default="us-east-1", help="AWS region")
@click.option("--hours", default=24, help="Hours to look back for logs/metrics")
@click.option("--logs", is_flag=True, help="Show recent logs")
@click.option("--metrics", is_flag=True, help="Show metrics")
@click.option("--info", is_flag=True, help="Show function information")
def main(
    function_name: str, region: str, hours: int, logs: bool, metrics: bool, info: bool
):
    """CloudWatch monitoring for Lambda functions"""

    click.echo(click.style("🔍 CloudWatch Lambda Monitor", fg="blue", bold=True))

    # Initialize monitor
    monitor = CloudWatchMonitor(region)

    # Show function information
    if info:
        click.echo(click.style("\n📊 Function Information:", fg="blue", bold=True))
        function_info = monitor.get_lambda_function_info(function_name)
        if function_info:
            for key, value in function_info.items():
                click.echo(f"  {key}: {value}")

    # Show metrics
    if metrics:
        click.echo(
            click.style(f"\n📈 Metrics (last {hours} hours):", fg="blue", bold=True)
        )
        metrics_data = monitor.get_lambda_metrics(function_name, hours)
        if metrics_data:
            click.echo(f"  Invocations: {metrics_data.get('invocations', 0)}")
            click.echo(f"  Errors: {metrics_data.get('errors', 0)}")
            click.echo(f"  Avg Duration: {metrics_data.get('avg_duration', 0):.2f} ms")
            click.echo(f"  Max Duration: {metrics_data.get('max_duration', 0):.2f} ms")
        else:
            click.echo("  No metrics data available")

    # Show logs
    if logs:
        click.echo(
            click.style(f"\n📝 Recent Logs (last {hours} hours):", fg="blue", bold=True)
        )
        logs_data = monitor.get_lambda_logs(function_name, hours)
        if logs_data:
            for log in logs_data[:10]:  # Show last 10 logs
                timestamp = log["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                click.echo(f"  [{timestamp}] {log['message'].strip()}")
        else:
            click.echo("  No logs available")

    # If no specific options, show all
    if not any([info, metrics, logs]):
        click.echo(click.style("\n📊 Function Information:", fg="blue", bold=True))
        function_info = monitor.get_lambda_function_info(function_name)
        if function_info:
            click.echo(f"  Name: {function_info['name']}")
            click.echo(f"  State: {function_info['state']}")
            click.echo(f"  Runtime: {function_info['runtime']}")
            click.echo(f"  Last Modified: {function_info['last_modified']}")

        click.echo(click.style(f"\n📈 Quick Metrics:", fg="blue", bold=True))
        metrics_data = monitor.get_lambda_metrics(function_name, 1)  # Last hour
        if metrics_data:
            click.echo(f"  Recent Invocations: {metrics_data.get('invocations', 0)}")
            click.echo(f"  Recent Errors: {metrics_data.get('errors', 0)}")

        click.echo(click.style(f"\n📝 Recent Logs:", fg="blue", bold=True))
        logs_data = monitor.get_lambda_logs(function_name, 1)  # Last hour
        if logs_data:
            for log in logs_data[:3]:  # Show last 3 logs
                timestamp = log["timestamp"].strftime("%H:%M:%S")
                click.echo(f"  [{timestamp}] {log['message'].strip()}")
        else:
            click.echo("  No recent logs")


if __name__ == "__main__":
    main()
