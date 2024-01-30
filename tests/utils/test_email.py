import os
import pytest
import addict

from gregor_anvil_automation.utils.email import send_email, Email, SMTPCredentials


@pytest.fixture(name="valid_config")
def fixture_valid_config():
    config = addict.Dict(
        ("sender", "hgsc-submit@bcm.edu"), ("recipients", "hgsc-submit@bcm.edu")
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


def test_send_email_valid(valid_config):
    """Test that send_email successfully sends an email"""
    subject = "Test Email"
    body = "This is a test email."
    attachments = []
    credentials = SMTPCredentials()
    email = Email(credentials)
    email.build_message(subject, body, valid_config.sender, valid_config.recipients)
    assert send_email(valid_config, subject, body, attachments) == email.send()
