import pytest
import tempfile

from gregor_anvil_automation.utils.email import send_email


@pytest.mark.integration
def test_send_email_valid_no_attachment(config):
    """Test that send_email successfully sends an email"""
    subject = "Gregor Test Email"
    body = "This is a Gregor automation test email."
    result = send_email(config, subject, body, [])
    assert result == 0


@pytest.mark.integration
def test_send_email_valid_attachment(valid_config):
    """Test that send_email successfully sends an email with an attachment"""
    subject = "Gregor Test Email"
    body = "This is a Gregor automation test email."
    test_file = tempfile.TemporaryFile()
    test_file.writelines("This is a Gregor test file.")
    result = send_email(valid_config, subject, body, test_file)
    assert result == 0
