import pytest
import addict
from pathlib import Path

from gregor_anvil_automation.utils.email import send_email, Email, SMTPCredentials


@pytest.fixture(name="valid_config")
def fixture_valid_config():
    config = addict.Dict(
        sender="u253196@bcm.edu",
        recipients="u253196@bcm.edu",
    )
    return config


@pytest.fixture(name="invalid_config")
def fixture_invalid_config():
    config = addict.Dict(
        sender="",
        recipients="",
    )
    return config


def test_send_email_valid(valid_config):
    """Test that send_email successfully sends an email"""
    subject = "Test Email"
    body = "This is a test email."
    attachments = []
    credentials = SMTPCredentials()
    email = Email(credentials)
    email.build_message(subject, body, valid_config.sender, valid_config.recipients)
    assert send_email(valid_config, subject, body, attachments) == email.send()


def test_send_email_valid_attachment(valid_config):
    """Test that send_email successfully sends an email with an attachment"""
    subject = "Test Email"
    body = "This is a test email."
    attachments = [Path("tests/utils/test_files/email_control.csv")]
    credentials = SMTPCredentials()
    email = Email(credentials)
    email.build_message(subject, body, valid_config.sender, valid_config.recipients)
    assert send_email(valid_config, subject, body, attachments) == email.send()


def test_send_email_valid_empty(valid_config):
    """Test that send_email successfully sends a blank email"""
    subject = ""
    body = ""
    attachments = []
    credentials = SMTPCredentials()
    email = Email(credentials)
    email.build_message(subject, body, valid_config.sender, valid_config.recipients)
    assert send_email(valid_config, subject, body, attachments) == email.send()


def test_send_email_invalid(invalid_config):
    """Test that send_email fails to send an email"""
    subject = "Test Email"
    body = "This is a test email."
    attachments = []
    credentials = SMTPCredentials()
    email = Email(credentials)
    email.build_message(subject, body, invalid_config.sender, invalid_config.recipients)
    assert send_email(invalid_config, subject, body, attachments) == email.send()
