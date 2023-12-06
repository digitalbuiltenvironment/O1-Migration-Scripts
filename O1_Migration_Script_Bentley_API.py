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
OUTPUT_FOLDER = 'Outputs/'


def generate_auth_headers():
    # Your client ID and client secret
    client_id = 'service-TWoDsHSXkpUxst90rlqNu0rqP'
    client_secret = 'EIVv1WJy4DBt+Rwi3VkkqAoE3ywmz0rQBcC1ORKTAisuNLhszEw7HiC6EnAxNzP4Q8+SJN8FytcepeQokrcQcg=='
    scope = 'issues:modify email profile insights:read organization itwinjs synchronization:modify synchronization:read transformations:read transformations:modify forms:modify imodels:read imodels:modify changedelements:modify forms:read insights:modify designelementclassification:modify openid changedelements:read webhooks:modify library:modify library:read projects:modify realitydata:read storage:modify storage:read users:read projects:read realitydata:modify designelementclassification:read webhooks:read issues:read'

    Url = "https://ims.bentley.com/connect/token"
    Data = {'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope}
    Response = requests.post(Url, Data)

    auth_header = f"{Response.json()['token_type']} {Response.json()['access_token']}"
    return {
        'Prefer': 'return=representation',
        'Accept': 'application/vnd.bentley.itwin-platform.v1+json',
        'Authorization': auth_header
    }


HEADERS = generate_auth_headers()


# HEADERS = {
#     'Prefer': 'return=representation',
#     'Accept': 'application/vnd.bentley.itwin-platform.v1+json',
#     'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkJlbnRsZXlJTVNfMjAyMyIsInBpLmF0bSI6ImE4bWUifQ.eyJzY29wZSI6WyJmb3JtczpyZWFkIiwiZm9ybXM6bW9kaWZ5Il0sImNsaWVudF9pZCI6Iml0d2luLWRldmVsb3Blci1jb25zb2xlIiwiYXVkIjpbImh0dHBzOi8vaW1zLmJlbnRsZXkuY29tL2FzL3Rva2VuLm9hdXRoMiIsImh0dHBzOi8vaW1zb2lkYy5iZW50bGV5LmNvbS9hcy90b2tlbi5vYXV0aDIiLCJodHRwczovL2ltc29pZGMuYmVudGxleS5jb20vcmVzb3VyY2VzIiwiYmVudGxleS1hcGktbWFuYWdlbWVudCJdLCJzdWIiOiJmNzk0NTg2YS1jMzk2LTRmYTktODY2OC00ZTY5ZWYzZDJjOWUiLCJyb2xlIjoiUHJvamVjdCBNYW5hZ2VyIiwib3JnIjoiYTI2MDE4NzUtYTg3NC00ZmVjLTlmNzMtMjBkMWY0ZmU4NDUzIiwic3ViamVjdCI6ImY3OTQ1ODZhLWMzOTYtNGZhOS04NjY4LTRlNjllZjNkMmM5ZSIsImlzcyI6Imh0dHBzOi8vaW1zLmJlbnRsZXkuY29tIiwiZW50aXRsZW1lbnQiOlsiTUFOQUdFRF9TRVJWSUNFUyIsIlNFTEVDVCJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwiZ2l2ZW5fbmFtZSI6IlhpYW5nSHVpIiwic2lkIjoieVFWUTlHMFdCTFNJVGRDcWdSYzVxc0laMjAwLlNVMVRMVUpsYm5Sc1pYa3RVMGMuOXRVMC5ZUXJZWHlxbHl1NmNTRW5TaFNRTmM4MTgyIiwibmJmIjoxNjkzOTA4MTc3LCJ1bHRpbWF0ZV9zaXRlIjoiMTAwNDA4NTQ3OSIsInVzYWdlX2NvdW50cnlfaXNvIjoiU0ciLCJhdXRoX3RpbWUiOjE2OTM5MDg0NzcsIm5hbWUiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwib3JnX25hbWUiOiJKVEMgQ29ycG9yYXRpb24iLCJmYW1pbHlfbmFtZSI6IlpoYW5nIiwiZW1haWwiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwiZXhwIjoxNjkzOTEyMDc5fQ.DMTQy-_Ztbmo6tTvispuEAZBjOdo_3VwX0kp5WZCmNZvQ2bQelkn6WJtKrBI9-En7Xwk9f0ygNo5k1jLYzYbQnW_S4iEElKIrHW_Y7kbD6ZD1N89CBdr0Xp-8kc_HqZQCuLCDm6Jil6amzv5gS6abrytCTSM2rLCpSA8-9LJ7QNb8d1A9KfQmIJ8G9JJWGN1KnjFb3n78V3dGGIv3eM-hi4SRhUcs0K0uA0yb51BKF8AApVrDLlhyGRKzsjBrX2BgRcpR-nc8eRa18SIRHaJUUgaN6JAy0zPDa3G4gg4b2vAsJwT32qmeHMKlp3lpBgOKaXTw3dR4d8JykUeUbEw9Q'
# }


def get_continuation_token(data_string):
    try:
        #json_object = json.loads(data_string)
        continuation_token = (data_string["_links"]['next']['href'].split("continuationToken=")[-1]).split('"')[0]
        return continuation_token
    except:
        return ""


# Function to download a PDF
def download_pdf(form_id, form_name):
    pdf_url = BASE_URL + FORMS_ENDPOINT + form_id + DOWNLOAD_PDF_ENDPOINT
    response = requests.get(pdf_url, headers=HEADERS)
    if response.status_code == 200:
        pdf_data = response.content
        pdf_folder = os.path.join(OUTPUT_FOLDER, form_name)
        os.makedirs(pdf_folder, exist_ok=True)
        pdf_path = os.path.join(pdf_folder, form_name + ".pdf")
        # if not os.path.exists(pdf_path):
        print(f"\tDownloading PDF: {form_name}.pdf")
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_data)


# Function to download attachments
def download_attachments(form_id, form_name):
    attachments_url = BASE_URL + FORMS_ENDPOINT + form_id + ATTACHMENTS_ENDPOINT
    response = requests.get(attachments_url, headers=HEADERS)
    if response.status_code == 200:
        attachments_data = response.json()
        attachments_folder = os.path.join(OUTPUT_FOLDER, form_name, 'Attachments')
        os.makedirs(attachments_folder, exist_ok=True)
        for attachment in attachments_data.get('attachments', []):
            attachment_id = attachment.get('id')
            attachment_name = attachment.get('fileName')
            attachment_url = attachments_url + f'/{attachment_id}'
            response = requests.get(attachment_url, headers=HEADERS)
            if response.status_code == 200:
                attachment_data = response.content
                attachment_path = os.path.join(attachments_folder, attachment_name)
                # if not os.path.exists(attachment_path):
                print(f"\tDownloading Attachment: {attachment_name}")
                with open(attachment_path, 'wb') as attachment_file:
                    attachment_file.write(attachment_data)


# Function to download audit logs
def download_audit_logs(form_id, form_name):
    audit_logs_url = BASE_URL + FORMS_ENDPOINT + form_id + "/auditTrailEntries"
    response = requests.get(audit_logs_url, headers=HEADERS)
    if response.status_code == 200:
        audit_logs_data = response.json()
        audit_logs_path = os.path.join(OUTPUT_FOLDER, form_name, f'{form_name}-Audit_Log.json')
        # if not os.path.exists(audit_logs_path):
        print(f"\tDownloading Audit Logs for Form: {form_name}.json")
        with open(audit_logs_path, 'w') as audit_logs_file:
            json.dump(audit_logs_data, audit_logs_file, indent=4)


# Function to download comments log
def download_comments(form_id, form_name):
    comment_logs_url = BASE_URL + FORMS_ENDPOINT + form_id + COMMENTS_ENDPOINT
    response = requests.get(comment_logs_url, headers=HEADERS)
    if response.status_code == 200:
        comment_logs_data = response.json()
        comment_logs_path = os.path.join(OUTPUT_FOLDER, form_name, f'{form_name}-Comments_Log.json')
        # if not os.path.exists(comment_logs_path):
        print(f"\tDownloading Comments Logs for Form: {form_name}.json")
        with open(comment_logs_path, 'w') as comment_logs_file:
            json.dump(comment_logs_data, comment_logs_file, indent=4)


def check_for_comments(form_name):
    comment_logs_path = os.path.join(OUTPUT_FOLDER, form_name, f'{form_name}-Comments_Log.json')
    if os.path.exists(comment_logs_path):
        return True
    else:
        return False

testlist = []
counterx = 0
countery = 0
counterz = 0

# Function to process forms
def process_forms(data):
    global counterx, countery, counterz
    forms_data = data.get('formDataInstances', [])
    continuation_token = get_continuation_token(data)
    for form in forms_data:
        form_id = form.get('id')
        form_name = form.get('number')
        if not check_for_comments(form_name):
            print(f"\nProcessing Form: {form_name}")
            download_pdf(form_id, form_name)
            download_attachments(form_id, form_name)
            download_audit_logs(form_id, form_name)
            download_comments(form_id, form_name)
        else:
            print(f"Skipping Form: {form_name}")
    return continuation_token


# Main function
def main():
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        target_url = BASE_URL + FORMS_ENDPOINT + "?projectId=d83ff104-0204-43c0-b94b-8a497d7aaf82"
        response = requests.get(target_url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            continuation_token = process_forms(data)
            while continuation_token != "":
                response = requests.get(target_url + "&continuationToken=" + continuation_token, headers=HEADERS)
                if response.status_code == 200:
                    data = response.json()
                    continuation_token = process_forms(data)
        else:
            print("Failed to retrieve data from API.")
            print("Error: " + str(response.status_code), response.reason + ": " + response.content.decode("utf-8"))
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
