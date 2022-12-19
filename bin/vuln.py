import io
import json
import os
import sys
from datetime import datetime

import boto3
import requests
import yaml
from requests import packages

# Silence insecure request warning
requests.packages.urllib3.disable_warnings()


def get_wui_creds():
    """Gets the WUI credentials from the config file

    Returns:
        dict: WUI credentials
    """
    with open("/usr/share/wazuh-dashboard/data/wazuh/config/wazuh.yml", "r") as file:
        config = yaml.safe_load(file)
        password1 = config["hosts"][0]["default"]["password"]
        user1 = config["hosts"][0]["default"]["username"]

        return {"password": password1, "user": user1}


# TODO: Create a dictionary of Wazuh API endpoints to be used as a quick reference when calling
# wazuh_api()

wazuh_base_url = 'https://localhost:55000'


def get_jwt_token():
    url = f'{wazuh_base_url}/security/user/authenticate'

    response = requests.get(url, auth=(get_wui_creds()["user"], get_wui_creds()["password"]), verify=False)
    return response.json()['data']['token']


def wazuh_api():
    headers = {
        "Authorization": "Bearer {}".format(get_jwt_token())
    }

    response = requests.get(f"{wazuh_base_url}/agents", headers=headers, verify=False)

    return response.json()


def get_vuln_reports(agent_id: int):
    headers = {
        "Authorization": "Bearer {}".format(get_jwt_token())
    }

    response = requests.get(f"{wazuh_base_url}/vulnerabilities/{agent_id}", headers=headers, verify=False)

    return response.json()


agents = [x["id"] for x in wazuh_api()["data"]["affected_items"]]


def main():
    vulns = []
    try:
        for ids in agents:
            if get_vuln_reports(ids)["detail"] == "404: Not Found":
                print(f"No vulnerabilities for agent {ids}")
                sys.exit(1)
            else:
                vulns.append(get_vuln_reports(ids))
    except Exception as e:
        print(e)

    return vulns


if __name__ == "__main__":
    report = io.BytesIO(bytes(json.dumps(main()), encoding="utf-8"))

    s3 = boto3.resource('s3')
    s3.meta.client.upload_fileobj(report, os.getenv("export EXAMPLE_VARIABLE='example value'"),
                                  f"{datetime.now()}-vulnerability-report")
