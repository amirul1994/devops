def lambda_handler(event, context):
    if event["name"] == "KodeKloud":
        return "Successful"