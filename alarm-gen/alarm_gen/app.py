import json


def fetch_instance_details(eb_event) -> list:
    """Parses the EventBridge event to get the instance details"""
    instances = []
    event_details = eb_event.get("detail", {})
    if not event_details:
        return instances

    try:
        instances = (
            event_details.get("responseElements", {})
            .get("instancesSet", {})
            .get("items", [])
        )
        return instances
    except Exception as e:
        print(e)
        return []


def lambda_handler(event, context):
    return_msg = {}
    instances = fetch_instance_details(event)
    if not instances:
        # log the event for debugging
        print(json.dumps(event, indent=4, default=str))

        return_msg["statusCode"] = "500"
        return_msg["body"] = {"message": "No instances found"}
        return return_msg

    for instance in instances:
        instance_id = instance.get("instanceId", "")
        tags = instance.get("tagSet", {})

        return_msg["statusCode"] = "200"
        return_msg["body"] = {
            "message": "instance found",
            "instanceId": instance_id,
            "tags": tags,
        }
        return return_msg
