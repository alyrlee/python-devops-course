#!/usr/bin/env python3
"""
Test script for AWS IAM Manager
Tests the functionality of the AWS IAM role and policy management
"""

import pytest
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "aws"))
try:
    from aws_iam_manager import AWSIAMManager
except ImportError:
    # Fallback for pylint static analysis
    AWSIAMManager = None


class TestAWSIAMManager:
    """Test cases for AWS IAM Manager"""

    @patch("boto3.client")
    def test_init_success(self, mock_boto_client):
        """Test successful initialization"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        manager = AWSIAMManager("us-east-1")
        assert manager.iam_client == mock_iam
        assert manager.sts_client == mock_sts
        assert manager.region == "us-east-1"

    @patch("boto3.client")
    def test_get_account_id(self, mock_boto_client):
        """Test getting AWS account ID"""
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {"Account": "123456789012"}
        mock_boto_client.return_value = mock_sts

        manager = AWSIAMManager()
        account_id = manager.get_account_id()
        assert account_id == "123456789012"

    def test_create_cloud9_trust_policy(self):
        """Test Cloud9 trust policy creation"""
        with patch.object(AWSIAMManager, "get_account_id", return_value="123456789012"):
            manager = AWSIAMManager()
            trust_policy = manager.create_cloud9_trust_policy()

            assert trust_policy["Version"] == "2012-10-17"
            assert "Statement" in trust_policy
            assert len(trust_policy["Statement"]) == 1
            assert trust_policy["Statement"][0]["Effect"] == "Allow"
            assert (
                trust_policy["Statement"][0]["Principal"]["Service"]
                == "cloud9.amazonaws.com"
            )

    @patch("boto3.client")
    def test_create_cloud9_role_success(self, mock_boto_client):
        """Test successful Cloud9 role creation"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {"Account": "123456789012"}
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        # Mock role doesn't exist
        mock_iam.get_role.side_effect = ClientError(
            {"Error": {"Code": "NoSuchEntity", "Message": "Role not found"}}, 
            "GetRole"
        )
        mock_iam.create_role.return_value = {"Role": {"RoleName": "test-role"}}

        manager = AWSIAMManager()
        result = manager.create_cloud9_role("test-role")

        assert result is True
        mock_iam.create_role.assert_called_once()

    @patch("boto3.client")
    def test_create_cloud9_role_exists(self, mock_boto_client):
        """Test Cloud9 role creation when role already exists"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        # Mock role exists
        mock_iam.get_role.return_value = {"Role": {"RoleName": "test-role"}}

        manager = AWSIAMManager()
        result = manager.create_cloud9_role("test-role")

        assert result is True
        mock_iam.create_role.assert_not_called()

    @patch("boto3.client")
    def test_attach_managed_policies_success(self, mock_boto_client):
        """Test successful policy attachment"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        manager = AWSIAMManager()
        policies = [
            "arn:aws:iam::aws:policy/AWSCloud9ServiceRolePolicy",
            "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
        ]

        result = manager.attach_managed_policies("test-role", policies)

        assert result is True
        assert mock_iam.attach_role_policy.call_count == 2

    @patch("boto3.client")
    def test_create_user_success(self, mock_boto_client):
        """Test successful user creation"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        # Mock user doesn't exist
        mock_iam.get_user.side_effect = ClientError(
            {"Error": {"Code": "NoSuchEntity", "Message": "User not found"}}, 
            "GetUser"
        )
        mock_iam.create_user.return_value = {"User": {"UserName": "test-user"}}

        manager = AWSIAMManager()
        result = manager.create_user("test-user")

        assert result is True
        mock_iam.create_user.assert_called_once()

    @patch("boto3.client")
    def test_create_user_exists(self, mock_boto_client):
        """Test user creation when user already exists"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        # Mock user exists
        mock_iam.get_user.return_value = {"User": {"UserName": "test-user"}}

        manager = AWSIAMManager()
        result = manager.create_user("test-user")

        assert result is True
        mock_iam.create_user.assert_not_called()

    @patch("boto3.client")
    def test_attach_role_to_user_success(self, mock_boto_client):
        """Test successful role attachment to user"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {"Account": "123456789012"}
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        # Mock policy doesn't exist
        mock_iam.get_user_policy.side_effect = ClientError(
            {"Error": {"Code": "NoSuchEntity", "Message": "Policy not found"}}, 
            "GetUserPolicy"
        )
        mock_iam.put_user_policy.return_value = {}

        manager = AWSIAMManager()
        result = manager.attach_role_to_user("test-user", "test-role")

        assert result is True
        mock_iam.put_user_policy.assert_called_once()

    @patch("boto3.client")
    def test_create_access_key_success(self, mock_boto_client):
        """Test successful access key creation"""
        mock_iam = Mock()
        mock_sts = Mock()
        mock_boto_client.side_effect = [mock_iam, mock_sts]

        mock_access_key = {
            "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
            "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        }
        mock_iam.create_access_key.return_value = {"AccessKey": mock_access_key}

        manager = AWSIAMManager()
        result = manager.create_access_key("test-user")

        assert result == mock_access_key
        mock_iam.create_access_key.assert_called_once_with(UserName="test-user")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
