__title__ = "py-notify"
__version__ = "1.0.0"
__author__ = "Joel McCune (https://github.com/knu2xs)"
__license__ = "Apache 2.0"
__copyright__ = "Copyright 2023 by Joel McCune (https://github.com/knu2xs)"

__all__ = ["send_email", "send_pushover"]

import logging
import re
from typing import Optional, Union

import requests
from azure.communication.sms import SmsClient, SmsSendResult

from .utils.credentials import (
    get_azure_sms_connection_string,
    get_azure_sms_number,
    get_sms_number,
    get_pushover_credentials,
)


def validate_phone_number(phone_number: str) -> str:
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
    Send simple text messages to phone numbers.
    
    Args:
        body: Text message to send.
        recipients: Single phone number or list of phone numbers to send to.
    """
    # if recepients not provided, read from environment variables
    if recipients is None:
        recipients = get_sms_number()

    # format the phone numbers to send to
    if isinstance(recipients, str):
        recipients = validate_phone_number(recipients)
    else:
        recipients = [validate_phone_number(ph) for ph in recipients]

    # load the SMS connection string from environment variables
    azure_sms_connection_string = get_azure_sms_connection_string()
    azure_sms_number = get_azure_sms_number()

    # format the azure phone number, the number used for sending
    azure_sms_number = validate_phone_number(azure_sms_number)

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
            logging.debug(f"""SMS Message successfully sent to "{resp.to}".""")

    return sms_responses


def send_pushover(
    message: str, user_key: Optional[str] = None, api_token: Optional[str] = None
) -> requests.Response:
    """
    Send notifications using Pushover platform.

    Args:
        message: Text message to send.
        user_key: Pushover user key. If not provided, will try to retrieve from ``PUSHOVER_USER_KEY`` environment
          variable.
        api_token: Pushover API token. If not provided, will try to retrieve from ``PUSHOVER_API_TOKEN`` environment
          variable.
    """
    if user_key is not None and api_token is None:
        _, api_key = get_pushover_credentials()
        logging.debug(
            f"Using provided Pushover api_token with user_key from environment variables."
        )
    elif api_token is None and user_key is None:
        user_key, api_token = get_pushover_credentials()
        logging.debug("Using Pushover credentials from environment variables.")
    else:
        logging.debug("Using Pushover credentials from input parameters.")

    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": api_token,
        "user": user_key,
        "message": message,
        "sound": "bugle",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post(url, headers=headers, data=payload)

    if res.status_code != requests.codes.ok:
        logging.error(
            f"""Pushover API encountered an error, returned status code {res.status_code}: {res.json().get("error")}"""
        )
    else:
        logging.debug("Message successfully sent via Pushover.")

    return res
