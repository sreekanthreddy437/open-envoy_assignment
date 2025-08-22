#!/usr/bin/env python3
import sys
import boto3
from botocore.exceptions import NoRegionError, NoCredentialsError, ClientError

def list_ec2(region):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances()
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance["InstanceId"])
    return instances if instances else ["No EC2 instances found."]

def list_s3(region):
    # S3 is global but boto3 requires a region
    s3 = boto3.client("s3", region_name=region)
    response = s3.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])] or ["No S3 buckets found."]

def list_dynamodb(region):
    dynamodb = boto3.client("dynamodb", region_name=region)
    response = dynamodb.list_tables()
    return response.get("TableNames", []) or ["No DynamoDB tables found."]

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 list_resources.py <service> <region>")
        print("Example: python3 list_resources.py ec2 us-east-1")
        sys.exit(1)

    service = sys.argv[1].lower()
    region = sys.argv[2]

    try:
        if service == "ec2":
            resources = list_ec2(region)
            print(f"\nEC2 Instances in {region}:")
        elif service == "s3":
            resources = list_s3(region)
            print(f"\nS3 Buckets (Global, showing in {region}):")
        elif service == "dynamodb":
            resources = list_dynamodb(region)
            print(f"\nDynamoDB Tables in {region}:")
        else:
            print(f"❌ Unsupported service '{service}'. Supported: ec2, s3, dynamodb.")
            sys.exit(1)

        for r in resources:
            print(f" - {r}")

    except NoRegionError:
        print("❌ Error: AWS region not specified or invalid.")
    except NoCredentialsError:
        print("❌ Error: AWS credentials not found. Run `aws configure` first.")
    except ClientError as e:
        print(f"❌ AWS Client error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
