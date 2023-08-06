import pytest
import vcr
from click.testing import CliRunner

from smokeur.cli import upload_file


def test_upload_random_file():
    runner = CliRunner()
    result = runner.invoke(upload_file, ["--file", "/tmp/random-1234-abcdef"],)

    assert result.exit_code == 1
    assert (
        str(result.exception)
        == "[Errno 2] No such file or directory: '/tmp/random-1234-abcdef'"
    )


@pytest.mark.vcr()
def test_upload_invalid_token(monkeypatch):
    monkeypatch.setenv("SMOKEUR_API_TOKEN", "!@#$")
    runner = CliRunner()
    with vcr.use_cassette("tests/cassettes/test_upload_invalid_token.yaml"):
        result = runner.invoke(upload_file, ["--file", "tests/fixtures/text_file.txt"],)

    assert result.exit_code == 1
    assert str(result.output) == "The access token is invalid.\n"


def test_upload_file():
    runner = CliRunner()
    with vcr.use_cassette("tests/cassettes/test_upload_file.yaml"):
        result = runner.invoke(upload_file, ["--file", "tests/fixtures/text_file.txt"],)

    assert "Your file is available on:" in str(result.output)
    assert result.exit_code == 0
