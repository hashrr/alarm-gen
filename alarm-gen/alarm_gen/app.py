import json
import boto3

ec2_client = boto3.client("ec2")


def lambda_handler(event, context):
    instance_ids = []
    try:
        # this is based on the event sent by EventBridge
        # TODO: better to create a separate function to fetch the instance ID

        instance_id = event["detail"]["requestParameters"]["responseElements"][
            "instancesSet"
        ]["items"][0]["instanceId"]
        instance_ids.append(instance_id)
    except Exception as e:
        print(e)
        return

    result = ec2_client.describe_instances(InstanceIds=instance_ids)
    print(json.dumps(result, indent=4, default=str))
