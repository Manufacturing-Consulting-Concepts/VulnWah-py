import io
import json
import os
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

    response = requests.get(f"{wazuh_base_url}/vulnerability/{agent_id}", headers=headers, verify=False)
    return response.json()


agents = [x["id"] for x in wazuh_api()["data"]["affected_items"]]


def main():
    vulns = []
    try:
        for ids in agents:
            if get_vuln_reports(ids)["data"]["total_affected_items"] == 0:
                print(f"No vulnerabilities for agent {ids}")
                pass
            else:
                block = "{ " + f"{ids}" + ":" + f"{get_vuln_reports(ids)}" + " }"
                vulns.append(block)
    except Exception as e:
        print(e)

    return vulns


if __name__ == "__main__":
    if not main():
        print("No vulnerabilities found...")

    else:
        report = io.StringIO(json.dumps(main()))

        s3 = boto3.resource('s3')
        s3.meta.client.put_object(Body=report.getvalue(), Bucket=os.getenv("S3_BUCKET_NAME"),
                                  Key=f"{datetime.now()}-vulnerability-report.json")


