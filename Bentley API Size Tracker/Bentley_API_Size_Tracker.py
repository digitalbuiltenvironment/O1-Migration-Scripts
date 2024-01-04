import os
from time import sleep

import requests
import json

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

TARGETED_PROJECTS = ["Infra @ Tukang Estate", "Infra @ TWC", "Reclamation @TWC",
                     "Infra @ Seletar Aerospace Avenue and Road 3", "Infra @ Jalan Buroh"]

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

HEADERS = {
    'Prefer': 'return=representation',
    'Accept': 'application/vnd.bentley.itwin-platform.v1+json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkJlbnRsZXlJTVNfMjAyMyIsInBpLmF0bSI6ImE4bWUifQ.eyJzY29wZSI6WyJmb3JtczpyZWFkIiwiZm9ybXM6bW9kaWZ5Il0sImNsaWVudF9pZCI6Iml0d2luLWRldmVsb3Blci1jb25zb2xlIiwiYXVkIjpbImh0dHBzOi8vaW1zLmJlbnRsZXkuY29tL2FzL3Rva2VuLm9hdXRoMiIsImh0dHBzOi8vaW1zb2lkYy5iZW50bGV5LmNvbS9hcy90b2tlbi5vYXV0aDIiLCJodHRwczovL2ltc29pZGMuYmVudGxleS5jb20vcmVzb3VyY2VzIiwiYmVudGxleS1hcGktbWFuYWdlbWVudCJdLCJzdWIiOiJmNzk0NTg2YS1jMzk2LTRmYTktODY2OC00ZTY5ZWYzZDJjOWUiLCJyb2xlIjoiUHJvamVjdCBNYW5hZ2VyIiwib3JnIjoiYTI2MDE4NzUtYTg3NC00ZmVjLTlmNzMtMjBkMWY0ZmU4NDUzIiwic3ViamVjdCI6ImY3OTQ1ODZhLWMzOTYtNGZhOS04NjY4LTRlNjllZjNkMmM5ZSIsImlzcyI6Imh0dHBzOi8vaW1zLmJlbnRsZXkuY29tIiwiZW50aXRsZW1lbnQiOlsiTUFOQUdFRF9TRVJWSUNFUyIsIlNFTEVDVCJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwiZ2l2ZW5fbmFtZSI6IlhpYW5nSHVpIiwic2lkIjoiUTlYVHRUZEZENmcyNXJvUDFZbjdmSko0NFY4LlNVMVRMVUpsYm5Sc1pYa3RVMGMuSE9CaC41d0Jud0pwVFdNS3lzTVZXQ2ZtcGxCUzRVIiwibmJmIjoxNjk2MzkxMDIyLCJ1bHRpbWF0ZV9zaXRlIjoiMTAwNDA4NTQ3OSIsInVzYWdlX2NvdW50cnlfaXNvIjoiU0ciLCJhdXRoX3RpbWUiOjE2OTYzOTEzMjIsIm5hbWUiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwib3JnX25hbWUiOiJKVEMgQ29ycG9yYXRpb24iLCJmYW1pbHlfbmFtZSI6IlpoYW5nIiwiZW1haWwiOiJ4aWFuZ2h1aV96aGFuZ19mcm9tLnRwQG9wdGltdXMtcHcuY29tIiwiZXhwIjoxNjk2Mzk0OTI0fQ.J0sm8sKXi03JdS3pkPbzLT7MyIa_5e1mnzKg8QfOORye_mZOXgwzuw3D9VEJRBTh24Br325bAn-viYy-3GQq0NEtG1OXKKRaScHl2t2ogaoJZ6Q3j5GHBGWRbIcJ-33LXya1VDJDhK3IuhXSGokNslGr1no6OYfS9vLr_8EbumkTH5xjp1MeTcNGgTQRQx2JqZK9bDjYPu3WqsciEHC7_nLewdA7R9HuOHqKyfdj-2rvFR3tjetfySTxQ4i4o0Cq58Ks0uphz3zNJJvKDTaV6OVd6s2dIFFhmlP2H6Cn14zpHUeQULsHhcp72LoCE9iNlgErwpduvkfCVKN8VLmDWw'
}


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
        print(f"\t{YELLOW}Downloading PDF: {form_name}.pdf{RESET}")
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
                print(f"\t{YELLOW}Downloading Attachment: {attachment_name}{RESET}")
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
        print(f"\t{YELLOW}Downloading Audit Logs for Form: {form_name}.json{RESET}")
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
        print(f"\t{YELLOW}Downloading Comments Logs for Form: {form_name}.json{RESET}")
        with open(comment_logs_path, 'w') as comment_logs_file:
            json.dump(comment_logs_data, comment_logs_file, indent=4)


def check_for_comments(form_name):
    comment_logs_path = os.path.join(OUTPUT_FOLDER, form_name, f'{form_name}-Comments_Log.json')
    if os.path.exists(comment_logs_path):
        return True
    else:
        return False

# Function to process forms
def process_forms(data):
    global OUTPUT_FOLDER
    forms_data = data.get('formDataInstances', [])
    continuation_token = get_continuation_token(data)
    for form in forms_data:
        form_id = form.get('id')
        form_name = form.get('number')
        form_display_name = form.get('displayName')
        form_project_title = form.get('properties', {}).get('Project__x0020__Name')

        if form_project_title:
            # Convert form_project_title to lowercase
            form_project_title_lower = form_project_title.lower()
            if form_display_name == "Safety Observation Form" and form_project_title_lower.replace(" ", "") in [project.lower().replace(" ", "") for project in TARGETED_PROJECTS]:

                if form_project_title.replace(" ", "") == "Infra @ Tukang Estate".replace(" ", ""):
                    OUTPUT_FOLDER = 'Outputs/Infra @ Tukang Estate'
                    os.makedirs(os.path.join(OUTPUT_FOLDER), exist_ok=True)
                elif form_project_title.replace(" ", "") == "Infra @ TWC".replace(" ", ""):
                    OUTPUT_FOLDER = 'Outputs/Infra @ TWC'
                    os.makedirs(os.path.join(OUTPUT_FOLDER), exist_ok=True)
                elif form_project_title.replace(" ", "") == "Reclamation @TWC".replace(" ", ""):
                    OUTPUT_FOLDER = 'Outputs/Reclamation @TWC'
                    os.makedirs(os.path.join(OUTPUT_FOLDER), exist_ok=True)
                elif form_project_title.replace(" ", "") == "Infra @ Seletar Aerospace Avenue and Road 3".replace(" ", ""):
                    OUTPUT_FOLDER = 'Outputs/Infra @ Seletar Aerospace Avenue and Road 3'
                    os.makedirs(os.path.join(OUTPUT_FOLDER), exist_ok=True)
                elif form_project_title.replace(" ", "") == "Infra @ Jalan Buroh".replace(" ", ""):
                    OUTPUT_FOLDER = 'Outputs/Infra @ Jalan Buroh'
                    os.makedirs(os.path.join(OUTPUT_FOLDER), exist_ok=True)
                else:
                    OUTPUT_FOLDER = 'Outputs/'
                if not check_for_comments(form_name):
                    print(f"\n{GREEN}Processing Form: {form_name} - {form_project_title}{RESET}")
                    download_pdf(form_id, form_name)
                    download_attachments(form_id, form_name)
                    download_audit_logs(form_id, form_name)
                    download_comments(form_id, form_name)
                else:
                    print(f"\n{GREEN}Skipping Form: {form_name} - {form_project_title} Already Exists{RESET}")
                    pass

            else:
                print(f"\n{RED}Skipping Form: {form_name} - {form_project_title} not in project target{RESET}")
                pass
    return continuation_token


# Main function
def main():
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        target_url = BASE_URL + FORMS_ENDPOINT + "?projectId=3d9a1bea-2a42-46b1-9377-7f35a5ae4949"
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
            print(RED+"Failed to retrieve data from API."+RESET)
            print(RED+"Error: " + str(response.status_code), response.reason + ": " + response.content.decode("utf-8")+RESET)
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")


if __name__ == "__main__":
    main()
