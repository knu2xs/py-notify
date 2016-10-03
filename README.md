# Py-Notify

This package enables sending email and text messages from a Python script. This enables sending email or a text message as part of a processing workflow, typically for either emergency notification, or simply to know when a long running workflow is complete.

## Use

There are two methods available in the notify package, one for sending a notification email through gmail, and another for sending a text message using the simple message service (SMS) protocol using the Amazon Web Services Simple Notification Service.

### notify.send_gmail

```
notify.send_gmail(address_to, subject, body, importance='normal', address_from=None, password=None)
    :param address_to: Target address.
    :param subject: Email subject.
    :param body: The message...the meat.
    :param importance: Importance set to high, normal, or low.
    :param address_from: Optional Gmail address of the sender.
    :param password: Optional password for sender's Gmail account.
```

This method, not surprisingly, is used to send a message via Gmail. If a credentials file is created as part of the setup detailed below, it is not necessary to provide more than a recipient address, subject, and body text. Importance (low, normal, or high) is optional. If an email and password are provided, they will be used instead of anything provided in a configuration file.

### notify.send_sms
```
send_sms(phone_number, message, aws_access_key_id=None, aws_secret_access_key=None):
    :param phone_number: Ten digit domestic phone number.
    :param message: Message to send to phone - must be less than 160 characters.
```

This method is used to send a message, a text, using the simple message service (SMS) protocol through Amazon Web Service's (AWS) Simple Notification Service (SNS).

The phone number *must* be in the +12348876390 format with no spaces, or the message will not work. Currently the script does not have formatting or error catching to account for this. It will just silently fail.

Messages are limited to 160 characters. Anything more will be truncated.

### notify.get_short_url

```
Get shortened url using bit.ly.
    :param long_url: Long url to be shortened.
    :param login: Bitly login for api.
    :param api_key: Bitly api key corresponding to the login.
    :return: Strung shortened url.
```

This method is included as a helper since many times, if a hyperlink is to be included in a text message, the hyperlink needs to be shortened. This does require credentials for bit.ly.

## Configuration

While the included methods can be invoked directly, passing credentials into the script at runtime, it is a little easier and more reusable to create a configuration file containing the credentials. Start by creating a directory called `resources` inside the `notify` package directory. Inside the `resources` directory, create a file called `credentials.json`. This file should contain the following verbatium - except replacing the values with the email/password for gmail, the Amazon Web Services access key ID and secret access key for sending text messages, and the bit.ly login and api_key.

```
{
  "gmail": {
    "username": "secommteam@gmail.com",
    "password": "P@$$W0rd...or something"
  },
  "aws_sns": {
    "aws_access_key_id": "GIBBERISHACCESSKEY",
    "aws_secret_access_key": "EVENMOREGIBBERISHSECRETACCESSKEY"
  },
  "bitly": {
    "login": "o_sweet05login",
    "api_key": "R_g1bb3r1shg1bb3r1shg1bb3r1sh"
  }
}
```

## Included Packages

Three packages, `boto3`, `botocore`, `jmespath`, and `bitly_api` are included as part of this repository. If these are installed on your system using a package manager, you do not need them in this directory. They are dependencies included for the sake of simplicity of use.