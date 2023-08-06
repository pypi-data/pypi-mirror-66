#! /usr/bin/env python3
"""
Smokeur CLI (https://gitlab.com/c0x6a/smokeur-cli)

A command line interface to interact with
Smokeur Server (https://gitlab.com/c0x6a/smokeur)
"""
import os
import sys

import pyperclip
import requests

VERSION = "0.1.8"


def upload_file():
    """Upload a file to Smokeur"""
    try:
        SMOKEUR_SERVER = os.environ["SMOKEUR_SERVER"]
    except KeyError:
        print(
            "Please set 'SMOKEUR_SERVER' environment variable before using this tool."
        )
        sys.exit(1)

    try:
        SMOKEUR_API_TOKEN = os.environ["SMOKEUR_API_TOKEN"]
    except KeyError:
        print(
            "Please set 'SMOKEUR_API_TOKEN' environment variable before using this tool."
        )
        sys.exit(1)

    try:
        file_name = sys.argv[1]
    except IndexError:
        print(
            "You have to give the file path to upload; e.g.:\n"
            "$ smokeur somefile.jpg\n"
            "or\n"
            "$ smokeur /path/to/somefile.png"
        )
        sys.exit(1)

    smokeur_headers = {
        "User-Agent": "Smokeur CLI/{version}".format(version=VERSION),
        "X-Token": SMOKEUR_API_TOKEN,
    }
    with open(file_name, "rb") as file:
        data = {"file": file}

        try:
            response = requests.post(
                url=SMOKEUR_SERVER, files=data, headers=smokeur_headers,
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


if __name__ == "__main__":
    upload_file()
