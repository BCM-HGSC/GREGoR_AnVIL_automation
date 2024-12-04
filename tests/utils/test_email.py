import pytest

from gregor_anvil_automation.utils.email import send_email


@pytest.mark.integration
def test_send_email_valid_no_attachment(config, tmp_path):
    """Test that send_email successfully sends an email"""
    subject = "Gregor Test Email"
    body = "This is a Gregor automation test email."
    config.env_file = tmp_path / ".test.env"
    result = send_email(config.email, subject, body, [])
    assert result == 0


@pytest.mark.integration
def test_send_email_valid_attachment(config, tmp_path):
    """Test that send_email successfully sends an email with an attachment"""
    subject = "Gregor Test Email"
    body = "This is a Gregor automation test email."
    config.env_file = tmp_path / ".test.env"
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a Gregor test file.")
    result = send_email(config.email, subject, body, [test_file])
    assert result == 0
