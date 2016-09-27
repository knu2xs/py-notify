# import modules
import smtplib
import json
from email.mime.text import MIMEText


def send_gmail(address_to, subject, body, importance='normal', address_from=None, password=None):
    """
    Send an email using Gmail.
    :param address_to: Target address.
    :param subject: Email subject.
    :param body: The message...the meat.
    :param importance: Importance set to high, normal, or low.
    :param address_from: Optional Gmail address of the sender.
    :param password: Optional password for sender's Gmail account.
    """
    # if the username and password are not provided as input
    if not address_from and not password:

        # open the configuration file with the credentials
        credentials_file = open('resources/credentials.json').read()
        credentials_all = json.loads(credentials_file)
        credentials = credentials_all['gmail']

        # save the Gmail credentials into variables
        address_from = credentials['username']
        password = credentials['password']

    # create a MIME object to work with, with the body text already populated
    message = MIMEText(body)

    # add header information header
    message['Subject'] = subject
    message['From'] = address_from
    message['To'] = address_to

    # ensure importance is all lowercase
    importance = importance.lower()

    # check for valid values in importance
    if importance == 'high':
        message['Importance'] = importance
    elif importance.lower() == 'low':
        message['Importance'] = importance
    else:
        message['Importance'] = 'normal'

    # create an email server object
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # get the connection opened
    server.ehlo()
    server.starttls()

    # login to the server using the credentials
    server.login(address_from, password)

    # send the email
    server.send_message(
        msg=message,
        from_addr=address_from,
        to_addrs=address_to
    )

    # close the server connection
    server.quit()
