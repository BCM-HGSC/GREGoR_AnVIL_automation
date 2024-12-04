import os
import smtplib
import ssl
import logging
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from traceback import format_exception
from typing import List

import addict

logger = logging.getLogger(__name__)


class SMTPCredentials:
    """Class for SMTP credentials"""

    def __init__(self) -> None:
        self.host = os.environ.get("EMAIL_HOST")
        self.port = os.environ.get("EMAIL_PORT")
        self.username = os.environ.get("EMAIL_USERNAME")
        self.password = os.environ.get("EMAIL_PASSWORD")

    def __repr__(self):
        return f"SMTPCredentials(host={self.host}, port={self.port}, username={self.username})"


class Email:
    """Email class"""

    def __init__(self, credentials: SMTPCredentials) -> None:
        self.credentials = credentials
        self.message = MIMEMultipart()

    def add_attachments(self, attachments: List[Path]) -> None:
        """Adds attachments to email message"""
        for attachment in attachments:
            with open(attachment, "r", encoding="utf-8") as fin:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(fin.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", "attachment", filename=attachment.name
                )
                self.message.attach(part)

    def build_message(
        self, subject: str, body: str, sender: str, recipients: List[str]
    ) -> None:
        """Builds email message"""
        self.message.attach(MIMEText(body, "html"))
        self.message["Subject"] = subject
        self.message["From"] = sender
        self.message["To"] = ", ".join(recipients)

    def send(self) -> int:
        """Sends email"""
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(self.credentials.host, self.credentials.port) as server:
                if self.credentials.username and self.credentials.password:
                    server.starttls(context=context)
                    server.login(self.credentials.username, self.credentials.password)
                server.send_message(self.message)
        except Exception:
            logger.exception("Unable to send email")
            return 1
        return 0


def build_traceback_message():
    """Builds a message to send via email that contains traceback"""
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback = format_exception(exc_type, exc_value, exc_tb)
    traceback = "".join([t.replace("\n", "<br>") for t in traceback if "\n" in t])
    return UNABLE_TO_PROCESS_MSG_BODY.format(traceback=traceback)


def build_manifest_traceback_message(body, provided_lists):
    """Builds a message to send via email that contains traceback"""
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback = format_exception(exc_type, exc_value, exc_tb)
    traceback = "".join([t.replace("\n", "<br>") for t in traceback if "\n" in t])
    html_provided_lists = get_list_html(provided_lists)
    return body.format(output=html_provided_lists, traceback=traceback)


def send_email(
    email_config: addict.Dict, subject: str, body: str, attachments: List[Path] = None
) -> int:
    """Sends an email"""
    if attachments is None:
        attachments = []
    credentials = SMTPCredentials()
    email = Email(credentials)
    logger.info("Creating Email Message")
    email.build_message(
        subject=subject,
        body=body,
        sender=email_config.sender,
        recipients=email_config.recipients,
    )
    if attachments:
        logger.info("Adding Email Attachments")
        email.add_attachments(attachments)
    return email.send()


def get_email_body(
    email_body: str, passing_samples: List[str], failed_samples: List[str], **kwargs
) -> str:
    """Generates the string message to be sent as an email."""
    return email_body.format(
        success=get_list_html(passing_samples),
        failed=get_list_html(failed_samples),
        **kwargs,
    )


def get_list_html(list_of_samples: list[str]) -> str:
    """Returns an string of HTML text for email body"""
    if list_of_samples:
        return "".join(f"<li>{sample}</li>" for sample in list_of_samples)
    return "None"


##################
# Email Messages #
##################
# Already made messages that the application can chose from depending on the situation

UNABLE_TO_PROCESS_MSG_BODY = """
<html>
    <head></head>
    <body>
        <p>An exception was encountered when processing the files.
        <p> Exception </p>
        <blockquote>
        {traceback}
        </blockquote>

        <p><i>This is an automated message. Do not reply.</i>
    </body>
</html>
"""


ATTACHED_ISSUES_MSG_BODY = """
<html>
    <head></head>
    <body>
        <p>Issues were encountered when processing records. A CSV file
        with encountered issues is attached. Please investigate.

        <p><i>This is an automated message. Do not reply.</i>
    </body>
</html>
"""


SUCCESS_MSG_BODY = """
<html>
    <head></head>
    <body>
        <p>A TSV file containing information of the successfully submitted
        samples is attached.

        <p><i>This is an automated message. Do not reply.</i>
    </body>
</html>
"""
