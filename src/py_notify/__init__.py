__title__ = "py-notify"
__version__ = "1.0.1"
__author__ = "Joel McCune (https://github.com/knu2xs)"
__license__ = "Apache 2.0"
__copyright__ = "Copyright 2023 by Joel McCune (https://github.com/knu2xs)"

__all__ = ["send_pushover", "send_sms"]

import importlib.util
import logging
import os
import re
from typing import Optional, Union

import requests
from azure.communication.sms import SmsClient, SmsSendResult

# if in development environment, load environment variables from .env file
if importlib.util.find_spec("dotenv"):
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())


def _validate_phone_number(phone_number: str) -> str:
    """Ensure and clean up phone number string for sending SMS messages, ``+133344455555``."""
    # pluck out all the numbers
    matches = re.findall(r"\d+", phone_number)

    # combine all the numbers
    if len(matches):
        phone_number = "".join(matches)

    # if the phone number is not 10 to 12 digits, cannot use
    if (len(phone_number) < 10) or (len(phone_number) > 12):
        raise ValueError(
            f"""The phone number provided "{phone_number}", is not between 10 and 12 digits."""
        )

    # if does not include the 1 US country code, add it
    elif len(phone_number) == 10:
        phone_number = "1" + phone_number

    # add the plus prefix
    phone_number = "+" + phone_number

    return phone_number


def send_sms(
    body: str, recipients: Optional[Union[str, list[str]]] = None
) -> list[SmsSendResult]:
    """
    Send simple text messages to phone numbers using Azure Communication Services' SMS SDK.

    .. note::

        This requires purchasing ($2/month for toll-free) a phone number in Azure Communication Services.

    Args:
        body: Text message to send.
        recipients: Single phone number or list of phone numbers to send to.
    """
    # if recepients not provided, try to read from environment variable
    if recipients is None:
        recipients = os.environ.get("SMS_NUMBER")

    # if still do not have an sms number, cannot send a message
    if recipients is None:
        raise ValueError("Please provide recipient phone number(s).")

    # format the phone numbers to send to
    if isinstance(recipients, str):
        recipients = _validate_phone_number(recipients)
    else:
        recipients = [_validate_phone_number(ph) for ph in recipients]

    # load the SMS connection string from environment variables
    azure_sms_connection_string = os.environ.get("AZURE_SMS_CONNECTION_STRING")

    if azure_sms_connection_string is None:
        raise EnvironmentError(
            "Cannot load Azure SMS connection string from environment variables."
        )

    # get the SMS number used for sending messages
    azure_sms_number = os.environ.get("AZURE_SMS_NUMBER")

    if azure_sms_number is None:
        raise EnvironmentError(
            "Cannot load Azure SMS number from environment variables."
        )

    # format the azure phone number, the number used for sending
    azure_sms_number = _validate_phone_number(azure_sms_number)

    # create the client to use for sending messages
    sms_client: SmsClient = SmsClient.from_connection_string(
        azure_sms_connection_string
    )

    # use the client to send the message
    sms_responses = sms_client.send(from_=azure_sms_number, to=recipients, message=body)

    # ensure all messages were successful, and notify if not
    for resp in sms_responses:
        if not resp.successful:
            logging.error(
                f"""Encountered error while sending SMS message to "{resp.to}": {resp.error_message}"""
            )
        else:
            logging.debug(f"""SMS Message "{body}" successfully sent to "{resp.to}".""")

    return sms_responses


def send_pushover(
    message: str,
    api_token: Optional[str] = None,
    user_key: Optional[str] = None,
) -> requests.Response:
    """
    Send notifications using Pushover platform.

    Args:
        message: Text message to send.
        api_token: Pushover API token. If not provided, will try to retrieve from ``PUSHOVER_API_KEY`` environment
          variable.
        user_key: Pushover user key. If not provided, will try to retrieve from ``PUSHOVER_USER_KEY`` environment
          variable.
    """
    # try to retrieve credentials from environment variables
    if user_key is None:
        user_key = os.environ.get("PUSHOVER_USER_KEY")
        logging.debug("Using Pushover user key from environment variables.")
    else:
        logging.debug("Using Pushover user key provided via input parameter.")

    if api_token is None:
        api_token = os.environ.get("PUSHOVER_API_KEY")
        logging.debug(f"Using Pushover API token from environment variables.")
    else:
        logging.debug(f"Using Pushover API token provided via input parameter.")

    # format parameters
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": api_token,
        "user": user_key,
        "message": message,
        "sound": "bugle",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # make post call to submit message send request
    res = requests.post(url, headers=headers, data=payload)

    # handle response if an error is encountered
    if res.status_code != requests.codes.ok:
        logging.error(
            f"""Pushover API encountered an error, returned status code {res.status_code}: {res.json().get("error")}"""
        )
    else:
        logging.debug("Message successfully sent via Pushover.")

    # provide the response back, which can be handled if necessary
    return res
