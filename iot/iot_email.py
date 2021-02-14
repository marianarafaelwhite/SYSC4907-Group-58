"""
iot_email.py

Roughly follows this tutorial:
https://bc-robotics.com/tutorials/sending-
email-using-python-raspberry-pi/

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import argparse
import logging
import smtplib
import constants as c


def send_email(recipients, subject, content):
    """
    Sends an email to recipient(s)

    Parameters
    ----------
    recipients : list
    subject : str
    content : str
    """
    if not recipients:
        logging.debug('No recipients specified')
        return

    # Connect to Gmail Server
    session = smtplib.SMTP(c.SMTP_SERVER, c.SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    # Login to Gmail
    session.login(c.GMAIL_USERNAME, c.GMAIL_PASSWORD)

    # General email headers
    from_header = 'From: {}'.format(c.GMAIL_USERNAME)
    subject_header = 'Subject: {}'.format(subject)
    mime_header = 'MIME-Version: 1.0'
    type_header = 'Content-Type: text/html'

    # Iterate through recipients
    for r in recipients:
        # Create recipient specific email header
        to_header = 'To: {}'.format(r)
        headers = [from_header, subject_header, to_header,
                   mime_header, type_header]
        headers = '\r\n'.join(headers)

        # Send Email
        logging.debug('Sending an email to: {}'.format(r))
        session.sendmail(c.GMAIL_USERNAME, r, headers + '\r\n\r\n' + content)

    # Exit
    session.quit


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', help='print debug messages')
    parser.add_argument(
        '-a', '--address',
        required=True,
        help='email address to send to')
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.v else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    # Email Contents
    recipients = [args.address]
    email_subject = 'COVID Risk Alert Test'
    email_content = 'This is a test'

    send_email(recipients, email_subject, email_content)
