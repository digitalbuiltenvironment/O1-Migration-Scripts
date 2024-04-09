import time
import math
import os
import html
import shutil
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Configuration
MAX_WAIT_TIME = 60
MAX_WAIT_TIME2 = 1200
BASE_URL = "https://construction.bentley.com/"
USERNAME = 'xianghui_zhang_from.tp@optimus-pw.com'
PASSWORD = 'S81681652z/asd123'
TARGET_PROJECT = ['275f4768-427f-461e-92b9-105566693bee','acf330cd-780f-4707-befb-e7c55f65e93f','403a12f5-7aec-41d7-a8c4-01931f61efc1','9843956a-56e1-421e-bff0-2ef25fc0adc8']
REVERSE_DOWNLOAD = True

# Folders
OUTPUT_FOLDER = 'Selenium_Outputs/'

# Make the download directory the same as the script directory
DOWNLOAD_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "\\" + OUTPUT_FOLDER
CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_experimental_option('prefs', {
    'download.default_directory': DOWNLOAD_DIRECTORY,
    'download.directory_upgrade': True,
})

# global variables
project_name = ""
current_project = 0
pagetracker = 0

def get_project_name(driver):
    global project_name
    wait_for_element(driver, (By.XPATH, "//h2[contains(@class, 'iui-text-subheading') and contains(@class, 'btn-my-work-header')]"))
    div_element = driver.find_element(By.CLASS_NAME, "bnt-hc-project-fullname")
    span_element = div_element.find_element(By.TAG_NAME, "span")
    text_with_entities = span_element.text
    project_name = html.unescape(text_with_entities)
    #print("\nProject Name: " + project_name)


def create_project_folder(driver):
    global project_name
    get_project_name(driver)
    os.makedirs(OUTPUT_FOLDER + project_name, exist_ok=True)


def download_required_checker(directory_path, total_items):
    global pagetracker
    counter = 0
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            counter += 1
        elif os.path.isdir(item_path):
            counter += 1
        # print(str(counter) + " - " + item)

    if counter == total_items:
        return True
    else:
        pagetracker = math.ceil(int(counter)/25) - 1
        return False


def do_zip_files(title):
    global project_name
    matching_zip_file = None
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        if filename.endswith(".zip") and "SYNCHRO_export" in filename:
            matching_zip_file = os.path.join(DOWNLOAD_DIRECTORY, filename)
            break

    if matching_zip_file:
        output_directory = os.path.join(OUTPUT_FOLDER, project_name, title)

        # Unzip the contents to the output directory
        with zipfile.ZipFile(matching_zip_file, 'r') as zip_ref:
            zip_ref.extractall(output_directory)

        # Remove the ZIP file Don't remove yet
        os.remove(matching_zip_file)
    else:
        pass

    # Move all PDFs to the correct folder
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        if filename.endswith(".pdf"):
            shutil.move(DOWNLOAD_DIRECTORY + "/" + filename, OUTPUT_FOLDER + project_name + "/" + title + "/" + filename)


def wait_for_element_to_disappear(driver, locator, max_wait_time=MAX_WAIT_TIME2):
    WebDriverWait(driver, max_wait_time).until_not(EC.presence_of_element_located(locator))
    time.sleep(0.25)


def wait_for_element(driver, locator, max_wait_time=MAX_WAIT_TIME):
    WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located(locator))
    time.sleep(0.25)


def unzip_file(file_path):
    for filename in os.listdir(file_path):
        if filename.endswith(".zip") and "SYNCHRO_export" in filename:
            zip_file_path = os.path.join(file_path, filename)

            # Create a directory to extract the contents (you can customize the directory name)
            extraction_dir = os.path.join(file_path, "extracted_contents")
            os.makedirs(extraction_dir, exist_ok=True)

            # Extract the contents of the ZIP file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_dir)

            print(f"Extracted contents from {filename} to {extraction_dir}")


def login(driver):
    driver.get(BASE_URL+"/all-projects/my-projects")
    wait_for_element(driver, (By.XPATH, "//div[@class='ping-input-container']"))

    driver.find_element(By.ID, "identifierInput").send_keys(USERNAME)
    driver.find_element(By.ID, "sign-in-button").click()
    wait_for_element(driver, (By.XPATH, "//div[@class='ping-input-container password-container']"))

    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "sign-in-button").click()

    print(RED + "Authorise PingID" + RESET)

    wait_for_element(driver, (By.XPATH, "//table[contains(@class, 'bnt-hc-tables-table') and contains(@class, 'bnt-hc-tables-tweaked')]"), 90)
    wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-large')]"))
    print(GREEN + "Logged in" + RESET)


def enter_project(driver):
    global project_name, current_project
    
    for i in range(len(TARGET_PROJECT)):
        driver.get(BASE_URL+"/"+TARGET_PROJECT[i]+"/home")
        create_project_folder(driver)
        print("\nProject Name: " + GREEN + project_name + RESET + " " + str(i+1) + "/" + str(len(TARGET_PROJECT)))
        click_links_and_export(driver)
        time.sleep(1)
    print(GREEN + "All projects downloaded!!!!" + RESET)
    return False


def download_excel(driver, title, title_end_space_checker):
    container_div_for_button = driver.find_element(By.XPATH,"//div[contains(@class, 'iui-root iwn-hc-adaptive-bar') and contains(@class, 'bnt-hc-forms-wsg-grid-bar-buttons')]")
    buttons = container_div_for_button.find_elements(By.XPATH, ".//span[contains(@class, 'iui-button-icon')]")
    buttons[-1].click()
    time.sleep(1.5)
    loop = True
    if driver.find_elements(By.XPATH, "//span[contains(@class, 'bnt-hc-archived')]"):
        loop = False
    while loop:
        try:
            time.sleep(1)
            find_dropdown_element = driver.find_element(By.XPATH,"//li[contains(@class, 'iui-menu-item ') and contains(@class, 'iwn-hc-adaptive-menu-item-enabled')]")
            if find_dropdown_element:
                loop = False
                dropdown_buttons = find_dropdown_element.find_elements(By.XPATH, "//div[@class='iui-menu-label']")
                time.sleep(0.5)
                dropdown_buttons[-1].click()
        except:
            time.sleep(0.5)
            container_div_for_button = driver.find_element(By.XPATH,"//div[contains(@class, 'iui-root iwn-hc-adaptive-bar') and contains(@class, 'bnt-hc-forms-wsg-grid-bar-buttons')]")
            buttons = container_div_for_button.find_elements(By.XPATH, ".//span[contains(@class, 'iui-button-icon')]")
            buttons[-1].click()
            time.sleep(0.5)

    while True:
        time.sleep(0.5)
        if title_end_space_checker:
            files = os.listdir(DOWNLOAD_DIRECTORY)
            if any(file.endswith(".xlsx") for file in files):
                break
        else:
            if os.path.exists(DOWNLOAD_DIRECTORY + "/" + title + ".xlsx"):
                break


def download_pdf(driver):
    if driver.find_elements(By.XPATH, "//div[contains(@class, 'bnt-hc-table-container-scroll-wrapper')]"):

        container_for_checkbox = driver.find_element(By.XPATH,"//th[contains(@class, 'bnt-hc-tables-select-iwn-header-cell')]")
        checkbox = container_for_checkbox.find_element(By.XPATH, ".//input[contains(@class, 'iui-checkbox')]")
        checkbox.click()
        loop = True

        if driver.find_elements(By.XPATH, "//span[contains(@class, 'bnt-hc-archived')]"):
            while True:
                try:
                    time.sleep(1.5)
                    container_div_for_button = driver.find_element(By.XPATH,"//div[contains(@class, 'iui-root iwn-hc-adaptive-bar') and contains(@class, 'bnt-hc-forms-wsg-grid-bar-buttons')]")
                    buttons = container_div_for_button.find_elements(By.XPATH, ".//span[contains(@class, 'iui-button-icon')]")
                    buttons[-3].click()
                    time.sleep(3)
                    if export_pdf_checkbox_clicker(driver):
                        break
                except:
                    pass
        else:
            time.sleep(0.25)
            container_div_for_button = driver.find_element(By.XPATH,"//div[contains(@class, 'iui-root iwn-hc-adaptive-bar') and contains(@class, 'bnt-hc-forms-wsg-grid-bar-buttons')]")
            buttons = container_div_for_button.find_elements(By.XPATH, ".//span[contains(@class, 'iui-button-icon')]")
            buttons[-1].click()
            time.sleep(1.5)
            while loop:
                try:
                    find_dropdown_element = driver.find_element(By.XPATH,"//li[contains(@class, 'iui-menu-item ') and contains(@class, 'iwn-hc-adaptive-menu-item-enabled')]")
                    if find_dropdown_element:
                        dropdown_buttons = find_dropdown_element.find_elements(By.XPATH, "//div[@class='iui-menu-label']")
                        time.sleep(0.5)
                        # click on download PDF
                        dropdown_buttons[-3].click()

                        # wait export modal to load
                        wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-large')]"))
                        loop = False

                except:
                    time.sleep(0.5)
                    container_div_for_button = driver.find_element(By.XPATH,"//div[contains(@class, 'iui-root iwn-hc-adaptive-bar') and contains(@class, 'bnt-hc-forms-wsg-grid-bar-buttons')]")
                    buttons = container_div_for_button.find_elements(By.XPATH, ".//span[contains(@class, 'iui-button-icon')]")
                    buttons[-1].click()

            export_pdf_checkbox_clicker(driver)


def export_pdf_checkbox_clicker(driver):
    # export all pdf and attachments
    time.sleep(0.2)
    container_for_export = driver.find_element(By.XPATH,
                                               "//div[contains(@class, 'bnt-hc-popover-border') and contains(@class, 'bnt-modal-border')]")
    export_checkbox = container_for_export.find_elements(By.XPATH, ".//input[contains(@class, 'iui-checkbox')]")
    try:
        for checkbox in export_checkbox:
            checkbox.click()
            time.sleep(0.1)
    except:
        pass
    container_for_export_button = driver.find_element(By.XPATH, "//div[contains(@class, 'bnt-hc-toolbar')]")
    export_button = container_for_export_button.find_element(By.XPATH, ".//button[contains(@class, 'iui-button')]")
    export_button.click()

    return True


def click_links_and_export(driver):
    work_element = driver.find_element(By.XPATH, "//li[@title='Work']")
    work_element.click()

    container_div = driver.find_element(By.CSS_SELECTOR, ".bnt-hc-side-navigation-child-item-container")
    link_wrappers = container_div.find_elements(By.CSS_SELECTOR, ".bnt-link-wrapper")
    if(REVERSE_DOWNLOAD):
        for x in range(len(link_wrappers)-1, -1, -1):
            container_div = driver.find_element(By.CSS_SELECTOR, ".bnt-hc-side-navigation-child-item-container")
            link_wrappers = container_div.find_elements(By.CSS_SELECTOR, ".bnt-link-wrapper")
            href = link_wrappers[x].get_attribute("href")
            if "tasks" not in href:
                link_wrappers[x].click()
                time.sleep(1)

                # Wait for the page to load
                wait_for_element(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-empty-page-icon') or contains(@class, 'bnt-hc-grid-and-form-information')]"))
                wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                element_title = driver.find_element(By.XPATH, "//h3[@class='bnt-hc-text-title bnt-hc-one-line-overflow']")
                title = html.unescape(element_title.text)
                title_end_space_checker = False
                title2 = ''
                if title[-1] == ' ':
                    title2 = title
                    title_end_space_checker = True
                    title = title[:-1]
                form_folder = os.path.join(OUTPUT_FOLDER, project_name, title)
                os.makedirs(form_folder, exist_ok=True)
                extra_pages = False

                if driver.find_elements(By.XPATH, "//div[contains(@class, 'bnt-hc-table-container-scroll-wrapper')]"):
                    # get title and total items
                    try:
                        element_pagination = driver.find_element(By.CLASS_NAME, "btn-hc-pagination-page-tracker")
                        total_items = element_pagination.text
                        total_items = total_items.split(" ")[-1]
                        extra_pages = True
                    except NoSuchElementException:
                        container_for_table = driver.find_element(By.XPATH,"//table[contains(@class, 'bnt-hc-tables-table') and contains(@class, 'bnt-hc-tables-tweaked') and contains(@class, 'bnt-hc-tables-fixed')]")
                        total_items = len(container_for_table.find_elements(By.XPATH, ".//tr[contains(@class, 'bnt-hc-tables-row')]"))
                        extra_pages = False
                    total_pages = math.ceil(int(total_items)/25)

                    if not download_required_checker(form_folder, int(total_items)+1):
                        try:
                            print("\tDownloading " + GREEN + "Excel" + RESET + " for " + GREEN + title + RESET)
                            download_excel(driver, title, title_end_space_checker)

                            for i in range(0, total_pages):
                                if i < pagetracker:
                                    continue
                                if extra_pages:
                                    wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                    time.sleep(0.5)
                                    container_for_pagination = driver.find_element(By.XPATH, "//div[contains(@class, 'bnt-hc-pagination')]")
                                    active_page = container_for_pagination.find_element(By.XPATH, ".//span[contains(@class, 'active')]")
                                    active_page = int(active_page.text)
                                else:
                                    active_page = 1
                                if active_page != (i+1):
                                    loop2 = True
                                    while loop2:
                                        wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                        time.sleep(0.5)
                                        container_for_pagination = driver.find_element(By.XPATH, "//div[contains(@class, 'bnt-hc-pagination')]")
                                        total_pages_elements = container_for_pagination.find_elements(By.XPATH, ".//span[contains(@class, 'bnt-hc-pagination-page-item')]")
                                        for page_element in total_pages_elements:
                                            if page_element.text == str(i+1):
                                                page_element.click()
                                                wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                                loop2 = False
                                                time.sleep(1)
                                                break
                                        if loop2:
                                            total_pages_elements[-2].click()
                                            wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))

                                print("\tDownloading " + YELLOW + "PDFs" + RESET + ": " + str(i+1) + "/" + str(total_pages) + " page(s) for " + GREEN + title + RESET)
                                time.sleep(0.5)
                                download_pdf(driver)

                                # Move the excel file to the correct folder
                                if title_end_space_checker:
                                    files = os.listdir(DOWNLOAD_DIRECTORY)
                                    for file in files:
                                        if file.endswith(".xlsx"):
                                            source_path = os.path.join(DOWNLOAD_DIRECTORY, file)
                                            destination_path = str(OUTPUT_FOLDER + project_name + "/" + title + "/" + title + ".xlsx")
                                            shutil.move(source_path, destination_path)
                                            break
                                else:
                                    if os.path.exists(DOWNLOAD_DIRECTORY + "/" + title + ".xlsx"):
                                        shutil.move(DOWNLOAD_DIRECTORY + "/" + title + ".xlsx", OUTPUT_FOLDER + project_name + "/" + title + "/" + title + ".xlsx")

                                wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-in-progress-title-bar')]"))

                                # Check if next page is needed
                                # if i != total_pages - 1:
                                #     next_page_button = driver.find_element(By.XPATH, "//i[contains(@class, 'svg-icon') and contains(@class, 'btn-hc-pagination-next-page-button')]")
                                #     next_page_button.click()
                                #     wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                while True:
                                    time.sleep(0.5)
                                    files = os.listdir(DOWNLOAD_DIRECTORY)
                                    if any(file.endswith((".zip", ".pdf")) for file in files):
                                        break
                                time.sleep(1)
                                do_zip_files(title)
                                time.sleep(2)
                        except Exception as e:
                            print(e)
                            pass
                        time.sleep(2)

    else:
        for x in range(0, len(link_wrappers)):
            container_div = driver.find_element(By.CSS_SELECTOR, ".bnt-hc-side-navigation-child-item-container")
            link_wrappers = container_div.find_elements(By.CSS_SELECTOR, ".bnt-link-wrapper")
            href = link_wrappers[x].get_attribute("href")
            if "tasks" not in href:
                link_wrappers[x].click()
                time.sleep(1)

                # Wait for the page to load
                wait_for_element(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-empty-page-icon') or contains(@class, 'bnt-hc-grid-and-form-information')]"))
                wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                element_title = driver.find_element(By.XPATH, "//h3[@class='bnt-hc-text-title bnt-hc-one-line-overflow']")
                title = html.unescape(element_title.text)
                title_end_space_checker = False
                title2 = ''
                if title[-1] == ' ':
                    title2 = title
                    title_end_space_checker = True
                    title = title[:-1]
                form_folder = os.path.join(OUTPUT_FOLDER, project_name, title)
                os.makedirs(form_folder, exist_ok=True)
                extra_pages = False

                if driver.find_elements(By.XPATH, "//div[contains(@class, 'bnt-hc-table-container-scroll-wrapper')]"):
                    # get title and total items
                    try:
                        element_pagination = driver.find_element(By.CLASS_NAME, "btn-hc-pagination-page-tracker")
                        total_items = element_pagination.text
                        total_items = total_items.split(" ")[-1]
                        extra_pages = True
                    except NoSuchElementException:
                        container_for_table = driver.find_element(By.XPATH,"//table[contains(@class, 'bnt-hc-tables-table') and contains(@class, 'bnt-hc-tables-tweaked') and contains(@class, 'bnt-hc-tables-fixed')]")
                        total_items = len(container_for_table.find_elements(By.XPATH, ".//tr[contains(@class, 'bnt-hc-tables-row')]"))
                        extra_pages = False
                    total_pages = math.ceil(int(total_items)/25)

                    if not download_required_checker(form_folder, int(total_items)+1):
                        try:
                            print("\tDownloading " + GREEN + "Excel" + RESET + " for " + GREEN + title + RESET)
                            download_excel(driver, title, title_end_space_checker)

                            for i in range(0, total_pages):
                                if i < pagetracker:
                                    continue
                                if extra_pages:
                                    wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                    time.sleep(0.5)
                                    container_for_pagination = driver.find_element(By.XPATH, "//div[contains(@class, 'bnt-hc-pagination')]")
                                    active_page = container_for_pagination.find_element(By.XPATH, ".//span[contains(@class, 'active')]")
                                    active_page = int(active_page.text)
                                else:
                                    active_page = 1
                                if active_page != (i+1):
                                    loop2 = True
                                    while loop2:
                                        wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                        time.sleep(0.5)
                                        container_for_pagination = driver.find_element(By.XPATH, "//div[contains(@class, 'bnt-hc-pagination')]")
                                        total_pages_elements = container_for_pagination.find_elements(By.XPATH, ".//span[contains(@class, 'bnt-hc-pagination-page-item')]")
                                        for page_element in total_pages_elements:
                                            if page_element.text == str(i+1):
                                                page_element.click()
                                                wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                                loop2 = False
                                                time.sleep(1)
                                                break
                                        if loop2:
                                            total_pages_elements[-2].click()
                                            wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))

                                print("\tDownloading " + YELLOW + "PDFs" + RESET + ": " + str(i+1) + "/" + str(total_pages) + " page(s) for " + GREEN + title + RESET)
                                time.sleep(0.5)
                                download_pdf(driver)

                                # Move the excel file to the correct folder
                                if title_end_space_checker:
                                    files = os.listdir(DOWNLOAD_DIRECTORY)
                                    for file in files:
                                        if file.endswith(".xlsx"):
                                            source_path = os.path.join(DOWNLOAD_DIRECTORY, file)
                                            destination_path = str(OUTPUT_FOLDER + project_name + "/" + title + "/" + title + ".xlsx")
                                            shutil.move(source_path, destination_path)
                                            break
                                else:
                                    if os.path.exists(DOWNLOAD_DIRECTORY + "/" + title + ".xlsx"):
                                        shutil.move(DOWNLOAD_DIRECTORY + "/" + title + ".xlsx", OUTPUT_FOLDER + project_name + "/" + title + "/" + title + ".xlsx")

                                wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-in-progress-title-bar')]"))

                                # Check if next page is needed
                                # if i != total_pages - 1:
                                #     next_page_button = driver.find_element(By.XPATH, "//i[contains(@class, 'svg-icon') and contains(@class, 'btn-hc-pagination-next-page-button')]")
                                #     next_page_button.click()
                                #     wait_for_element_to_disappear(driver, (By.XPATH, "//div[contains(@class, 'bnt-hc-spinner-container')]"))
                                while True:
                                    time.sleep(0.5)
                                    files = os.listdir(DOWNLOAD_DIRECTORY)
                                    if any(file.endswith((".zip", ".pdf")) for file in files):
                                        break
                                time.sleep(1)
                                do_zip_files(title)
                                time.sleep(2)
                        except Exception as e:
                            print(e)
                            pass
                        time.sleep(2)


def main():
    global current_project
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(YELLOW + "Starting Selenium Script..." + RESET)

    main_loop = True
    while main_loop:
        driver = webdriver.Chrome(options=CHROME_OPTIONS)
        try:
            login(driver)
            main_loop = enter_project(driver)
        except Exception as e:
            print(e)
            current_project = current_project - 1
            continue
        finally:
            driver.quit()


if __name__ == "__main__":
    main()
