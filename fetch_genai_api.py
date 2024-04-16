import json

import requests

STUDIO_API_URL = "https://genai.pt-df.inday.io/api/"
STUDIO_ACCESS_TOKEN = "eyJ1c2VySWQiOiJqZXNzaWNhLmxpIiwiYXBpS2V5IjoiMzczYjFiMzMtNmY0Yi00NWIxLTlmMDctZTM1YjA1YTdkOTE0In0="

PROMPT_ID = "MWZiZGM0ODYtNWM2Yi00NzYzLWE1ZGItODU4MDljZjg4NDM1OjpqZXNzaWNhLmxp"
# prompt is here: https://genai.pt-df.inday.io/?p=MWZiZGM0ODYtNWM2Yi00NzYzLWE1ZGItODU4MDljZjg4NDM1OjpqZXNzaWNhLmxp


def fetch_prediction_from_genai(prompt_id, payload):
    headers = {
        "api_key": STUDIO_ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Wd-Tenant": "super",
        "Wd-Tenant-Override": "super",
        "Wd-Environment": "vndly",
        "Wd-Origin": "vndly",
        "x-tenant": "super",
        "x-wd-request-id": "vndly-0001"
    }

    url = f"{STUDIO_API_URL}v1alpha/prediction/generate/{prompt_id}"
    response = requests.post(url, json=payload, headers=headers)
    return response.text


def get_predictions(prompt_id, question, contexts, variables, extra_prompts):
    # Define the request body from question, contexts, variables and extra prompts
    body = {
        "inputArgs": variables,
        "promptItems": [{"type": "user", "content": question}] + [{"type": "user", "content": p} for p in extra_prompts] + [{"type": "context", "content": p} for p in contexts]
    }

    response = fetch_prediction_from_genai(prompt_id, body)
    result = json.loads(response)['rawStrings'][0]
    print(result)
    return result

if __name__ == "__main__":
    get_predictions(PROMPT_ID, "why timesheet hours is not correct", ["time is in time_entries_clockedtime table for TI/TO, there's one row id=242389, its entry_date is March 13, 2024, while clock_out_date is March 16, 2024, that's why that day it's 74 hours. ", "it's because these line items are not invoiced yet. Their invoice number are all empty. The Previous BC and Current BC are  joined with InvoiceMaster.billing_cycle_id, which is null for these uninvoiced line items."], {}, [])