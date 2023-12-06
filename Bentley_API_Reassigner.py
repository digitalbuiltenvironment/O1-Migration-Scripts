import os
from time import sleep

import requests
import json

# Constants
BASE_URL = "https://api.bentley.com"
FORMS_ENDPOINT = "/forms/"
PROJECT_ENDPOINT = "/projects/"
DOWNLOAD_PDF_ENDPOINT = "/download?fileType=pdf&includeHeader=true"

ISSUES_ENDPOINT = "/issues"
IMODELS_ENDPOINT = "/imodels"
STORAGE_ENDPOINT = "/storage/folders/"

ATTACHMENTS_ENDPOINT = "/attachments"
COMMENTS_ENDPOINT = "/comments"
OUTPUT_FOLDER = "Outputs/"

REASSIGN_LIST = ["Hamzah Ali", "William Lim", "Mohan Kannaiyan", "Tong Kwang Lim"]
CHANGED_LIST = []


# def generate_auth_headers():
#     # Your client ID and client secret
#     client_id = 'service-TWoDsHSXkpUxst90rlqNu0rqP'
#     client_secret = 'EIVv1WJy4DBt+Rwi3VkkqAoE3ywmz0rQBcC1ORKTAisuNLhszEw7HiC6EnAxNzP4Q8+SJN8FytcepeQokrcQcg=='
#     scope = 'issues:modify email profile insights:read organization itwinjs synchronization:modify synchronization:read transformations:read transformations:modify forms:modify imodels:read imodels:modify changedelements:modify forms:read insights:modify designelementclassification:modify openid changedelements:read webhooks:modify library:modify library:read projects:modify realitydata:read storage:modify storage:read users:read projects:read realitydata:modify designelementclassification:read webhooks:read issues:read'

#     Url = "https://ims.bentley.com/connect/token"
#     Data = {'grant_type': 'client_credentials',
#             'client_id': client_id,
#             'client_secret': client_secret,
#             'scope': scope}
#     Response = requests.post(Url, Data)

#     auth_header = f"{Response.json()['token_type']} {Response.json()['access_token']}"
#     return {
#         'Prefer': 'return=representation',
#         'Accept': 'application/vnd.bentley.itwin-platform.v1+json',
#         'Authorization': auth_header
#     }


# HEADERS = generate_auth_headers()


HEADERS = {
    "Prefer": "return=representation",
    "Accept": "application/vnd.bentley.itwin-platform.v1+json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkJlbnRsZXlJTVNfMjAyNCIsInBpLmF0bSI6ImE4bWUifQ.eyJzY29wZSI6WyJmb3JtczpyZWFkIiwiZm9ybXM6bW9kaWZ5Il0sImNsaWVudF9pZCI6Iml0d2luLWRldmVsb3Blci1jb25zb2xlIiwiYXVkIjpbImh0dHBzOi8vaW1zLmJlbnRsZXkuY29tL2FzL3Rva2VuLm9hdXRoMiIsImh0dHBzOi8vaW1zb2lkYy5iZW50bGV5LmNvbS9hcy90b2tlbi5vYXV0aDIiLCJodHRwczovL2ltc29pZGMuYmVudGxleS5jb20vcmVzb3VyY2VzIiwiYmVudGxleS1hcGktbWFuYWdlbWVudCJdLCJzdWIiOiJmNzk0NTg2YS1jMzk2LTRmYTktODY2OC00ZTY5ZWYzZDJjOWUiLCJyb2xlIjoiUHJvamVjdCBNYW5hZ2VyIiwib3JnIjoiYTI2MDE4NzUtYTg3NC00ZmVjLTlmNzMtMjBkMWY0ZmU4NDUzIiwic3ViamVjdCI6ImY3OTQ1ODZhLWMzOTYtNGZhOS04NjY4LTRlNjllZjNkMmM5ZSIsImlzcyI6Imh0dHBzOi8vaW1zLmJlbnRsZXkuY29tIiwiZW50aXRsZW1lbnQiOlsiTUFOQUdFRF9TRVJWSUNFUyIsIlNFTEVDVCJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwiZ2l2ZW5fbmFtZSI6IlhpYW5nSHVpIiwic2lkIjoiUTlYVHRUZEZENmcyNXJvUDFZbjdmSko0NFY4LlNVMVRMVUpsYm5Sc1pYa3RVMGMuWFdwRS5hVmV4amg3THpEWlNMbm9yYTNJWUhqdEx0IiwibmJmIjoxNzAwNjQ0MDc3LCJ1bHRpbWF0ZV9zaXRlIjoiMTAwNDA4NTQ3OSIsInVzYWdlX2NvdW50cnlfaXNvIjoiU0ciLCJhdXRoX3RpbWUiOjE3MDA2NDQzNzcsIm5hbWUiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwib3JnX25hbWUiOiJKVEMgQ29ycG9yYXRpb24iLCJmYW1pbHlfbmFtZSI6IlpoYW5nIiwiZW1haWwiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwiZXhwIjoxNzAwNjQ3OTgwfQ.Lvj9VjFNcM9_KSAbq9vlV1Pe35xs9HRz5ulLDQCcmgFQn8SibDkTaF6lzxNh_mDiF2ZZGPnlT3dXm5juhCP1EPN-yv2rWdVsm4gswstkufzD_yFwroDCBPvwJ8d_pm3m2QeE6YArj6JrpzbD1LPZ7yVDADcersYtROLY4FBaGqOTv2_sdPK0rzjeQ8_ybbeUiBYUSgL7l9zR6Ybewslqvl5-T2oKgg2UMuWZR4YCn-yp4HEDfCJQHWVvKJZHqS_-OMkENMyw1JsFnsDUY-XubJffkoiD1QIuk1VjHfi8y6MHk5vp36aoFuAz8hIoOPQkCCtop50ZHObKjagHtTsGKA",
}


def get_continuation_token(data_string):
    try:
        # json_object = json.loads(data_string)
        continuation_token = (
            data_string["_links"]["next"]["href"].split("continuationToken=")[-1]
        ).split('"')[0]
        return continuation_token
    except:
        return ""


reassign_counter = 0


def reassign(form_id , form_name):
    global reassign_counter
    reassign_counter += 1
    # target_url = BASE_URL + FORMS_ENDPOINT + 'aafMRy_f7UOvD6EGpap2wnmuzFtt-0tLoVGbfsprVoA'
    target_url = BASE_URL + FORMS_ENDPOINT + form_id
    
    payload = {
        "status": "Review by SO",
        "assignee": {
            "displayName": "SO - SO Rep",
            "id": "2d905313-f0df-4795-b1c2-15fdb173c305",
        }
    }

    response = requests.patch(target_url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"\tReassigned Form: {form_name} Success!")
        CHANGED_LIST.append(form_name)
    else:
        print("Failed to retrieve data from API.")
        print(
            "Error: " + str(response.status_code),
            response.reason + ": " + response.content.decode("utf-8"),
        )


# Function to process forms
def process_forms(data):
    global counterx, countery, counterz
    forms_data = data.get("formDataInstances", [])
    continuation_token = get_continuation_token(data)
    for form in forms_data:
        form_id = form.get("id")
        form_name = form.get("number")
        form_status = form.get("status")
        if form_status == "Verify by RSS":
            form_assignee = form.get("assignee").get("displayName")
            if form_assignee in REASSIGN_LIST:
                print(f"\nProcessing Form: {form_name}, {form_status}, {form_assignee}")
                reassign(form_id, form_name)
        # else:
        #     print(f"Skipping Form: {form_name}")
    return continuation_token


# Main function
def main():
    global reassign_counter
    try:
        target_url = (
            BASE_URL
            + FORMS_ENDPOINT
            + "?projectId=47cca769-df2f-43ed-af0f-a106a5aa76c2"
        )
        response = requests.get(target_url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            continuation_token = process_forms(data)
            while continuation_token != "":
                response = requests.get(
                    target_url + "&continuationToken=" + continuation_token,
                    headers=HEADERS,
                )
                if response.status_code == 200:
                    data = response.json()
                    continuation_token = process_forms(data)
        else:
            print("Failed to retrieve data from API.")
            print(
                "Error: " + str(response.status_code),
                response.reason + ": " + response.content.decode("utf-8"),
            )
    except Exception as e:
        print(f"Error: {str(e)}")

    print(f"\nReassigned {reassign_counter} forms.")
    # Specify the file path
    file_path = "reassign_list.txt"

    # Open the file in write mode
    with open(file_path, "w") as file:
        file.write(f"Reassigned Forms ({reassign_counter}):\n")
        # Write each element of the list to a new line in the file
        for item in CHANGED_LIST:
            file.write(f"{item}\n")

    print(f"The list has been written to {file_path}")


if __name__ == "__main__":
    main()
