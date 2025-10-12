# AWS IAM Role and Policy Management

This script creates an AWS IAM role with Cloud9 service role policy and attaches it to a user for development environments.

## Features

- ✅ Creates Cloud9 service role with proper trust policy
- ✅ Attaches AWS managed policies (AWSCloud9ServiceRolePolicy, EC2, S3, VPC)
- ✅ Creates IAM user and attaches role
- ✅ Optional access key creation
- ✅ Comprehensive error handling and logging
- ✅ Tagging for resource management

## Prerequisites

1. **AWS Credentials**: Configure AWS credentials using one of these methods:
   ```bash
   # Option 1: AWS CLI
   aws configure
   
   # Option 2: Environment variables
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   
   # Option 3: IAM role (if running on EC2)
   ```

2. **Python Dependencies**: Install required packages:
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage
```bash
python aws_iam_manager.py
```

### Custom Parameters
```bash
python aws_iam_manager.py \
  --role-name MyCloud9Role \
  --username my-dev-user \
  --region us-west-2 \
  --create-access-key
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--role-name` | `Cloud9ServiceRole` | Name of the Cloud9 service role |
| `--username` | `cloud9-user` | Name of the IAM user |
| `--region` | `us-east-1` | AWS region |
| `--create-access-key` | `False` | Create access key for the user |

## What the Script Does

### 1. Creates Cloud9 Service Role
- **Role Name**: Configurable (default: `Cloud9ServiceRole`)
- **Trust Policy**: Allows Cloud9 service to assume the role
- **Tags**: Purpose and Environment tags for resource management

### 2. Attaches AWS Managed Policies
- `AWSCloud9ServiceRolePolicy` - Core Cloud9 permissions
- `AmazonEC2FullAccess` - EC2 instance management
- `AmazonS3FullAccess` - S3 bucket access
- `AmazonVPCFullAccess` - VPC configuration

### 3. Creates IAM User
- **Username**: Configurable (default: `cloud9-user`)
- **Tags**: Purpose tag for identification

### 4. Attaches Role to User
- Creates inline policy allowing user to assume the Cloud9 role
- Policy name: `{role_name}AssumeRolePolicy`

### 5. Optional Access Key Creation
- Creates AWS access key for programmatic access
- **Important**: Save credentials securely!

## Example Output

```
🚀 Starting AWS IAM setup for Cloud9...
✓ AWS IAM Manager initialized successfully
✓ Created Cloud9 service role: Cloud9ServiceRole
✓ Attached policy: AWSCloud9ServiceRolePolicy
✓ Attached policy: AmazonEC2FullAccess
✓ Attached policy: AmazonS3FullAccess
✓ Attached policy: AmazonVPCFullAccess
✓ Created user: cloud9-user
✓ Attached role Cloud9ServiceRole to user cloud9-user
✅ Cloud9 environment setup completed successfully!

🔑 Access Key Details:
Access Key ID: AKIAIOSFODNN7EXAMPLE
Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

⚠️  IMPORTANT: Save these credentials securely!
```

## Security Considerations

1. **Principle of Least Privilege**: The script uses AWS managed policies which provide broad permissions. Consider creating custom policies with minimal required permissions for production use.

2. **Access Key Security**: 
   - Store access keys securely (AWS Secrets Manager, environment variables)
   - Rotate access keys regularly
   - Use IAM roles instead of access keys when possible

3. **Role Assumption**: Users can assume the Cloud9 role but cannot directly access AWS services without assuming the role first.

## Troubleshooting

### Common Issues

1. **Credentials Not Found**
   ```
   ✗ AWS credentials not found. Please configure AWS credentials.
   ```
   **Solution**: Configure AWS credentials using `aws configure` or environment variables.

2. **Insufficient Permissions**
   ```
   ✗ Error creating role: Access Denied
   ```
   **Solution**: Ensure your AWS credentials have IAM permissions to create roles, users, and policies.

3. **Role Already Exists**
   ```
   ✓ Role 'Cloud9ServiceRole' already exists
   ```
   **Solution**: This is informational - the script will continue with existing role.

### Debug Mode
For detailed error information, check AWS CloudTrail logs or use AWS CLI to verify permissions:

```bash
aws sts get-caller-identity
aws iam list-roles --query 'Roles[?RoleName==`Cloud9ServiceRole`]'
```

## Cleanup

To remove the created resources:

```bash
# Delete access key (if created)
aws iam delete-access-key --user-name cloud9-user --access-key-id AKIAIOSFODNN7EXAMPLE

# Delete user policy
aws iam delete-user-policy --user-name cloud9-user --policy-name Cloud9ServiceRoleAssumeRolePolicy

# Delete user
aws iam delete-user --user-name cloud9-user

# Detach policies from role
aws iam detach-role-policy --role-name Cloud9ServiceRole --policy-arn arn:aws:iam::aws:policy/AWSCloud9ServiceRolePolicy

# Delete role
aws iam delete-role --role-name Cloud9ServiceRole
```

## Next Steps

After running the script:

1. **Configure Cloud9 Environment**: Use the created role when setting up Cloud9 environments
2. **Test Permissions**: Verify that the user can assume the role and access required services
3. **Monitor Usage**: Use AWS CloudTrail to monitor role usage and access patterns
4. **Set Up MFA**: Consider enabling MFA for additional security

## Support

For issues or questions:
1. Check AWS IAM documentation
2. Verify AWS credentials and permissions
3. Review CloudTrail logs for detailed error information
