#! /usr/bin/env python3
"""
Smokeur CLI (https://gitlab.com/c0x6a/smokeur-cli)

A command line interface to interact with
Smokeur Server (https://gitlab.com/c0x6a/smokeur)
"""
import os
import sys

import click
import pyperclip
import requests

VERSION = "1.0.0"


@click.group()
def smokeur_cli():
    """Click grouper for smokeur commands"""
    ...


@smokeur_cli.command()
@click.option(
    "--file",
    prompt="File to upload",
    help="Relative or absolute path of file to be uploaded",
)
def upload_file(file):
    """Upload a file to Smokeur"""
    try:
        smokeur_server = os.environ["SMOKEUR_SERVER"]
    except KeyError:
        print(
            "Please set 'SMOKEUR_SERVER' environment variable before using this tool."
        )
        sys.exit(1)

    try:
        smokeur_api_token = os.environ["SMOKEUR_API_TOKEN"]
    except KeyError:
        print(
            "Please set 'SMOKEUR_API_TOKEN' environment variable before using this tool."
        )
        sys.exit(1)

    smokeur_headers = {
        "User-Agent": "Smokeur CLI/{version}".format(version=VERSION),
        "X-Token": smokeur_api_token,
    }
    with open(file, "rb") as file_to_upload:
        data = {"file": file_to_upload}

        try:
            response = requests.post(
                url=smokeur_server, files=data, headers=smokeur_headers,
            )
        except requests.exceptions.ConnectionError as ex:
            print(str(ex))
            sys.exit(1)

    if response.ok:
        result_url = response.json().get("result")
        pyperclip.copy(result_url)
        print(f"Your file is available on: {result_url}")
        print("The URL has been copied to the clipboard too.")
    else:
        try:
            print(response.json()["detail"])
        except (KeyError, AttributeError):
            print(response.reason)
        sys.exit(1)


cli = click.CommandCollection(sources=[smokeur_cli])  # pylint: disable=invalid-name

if __name__ == "__main__":
    cli()
