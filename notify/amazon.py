# import modules
import boto3   # Amazon web services
import json


def send_sms(phone_number, message, aws_access_key_id=None, aws_secret_access_key=None):
    """
    Send a simple message service (sms), what is commonly known as a text message, using Amazon's Simple Notification
    Service.
    :param phone_number: Ten digit domestic phone number.
    :param message: Message to send to phone - must be less than 160 characters.
    :return:
    """

    # if credentials are manually provided
    if aws_access_key_id and aws_secret_access_key:

        # # create an AWS session object using the provided credentials
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-east-1'
        )

    # if credentials are not manually provided
    else:

        # open the configuration file with the credentials
        credentials_file = open('resources/credentials.json').read()
        credentials_all = json.loads(credentials_file)
        credentials = credentials_all['aws_sns']

        # create an AWS session object
        session = boto3.session.Session(
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],
            region_name='us-east-1'
        )

    # create a simple notification service client object
    sns = session.client('sns')

    # send the message
    sns.publish(
        PhoneNumber=phone_number,
        Message=message
    )
