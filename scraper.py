from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os

from job import Job

JOBS_FILE = "sent_jobs.json"

def scrape_job(driver, index):

    """ Scrape all of the data needed for the email and return a job object"""
    company_elem = driver.find_element(By.XPATH, f'//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[3]/div[2]/div/div[2]/article/markdown-accessiblity-table/table/tbody/tr[{index}]/td[1]/strong')
    company = company_elem.text.strip()
    role_elem = driver.find_element(By.XPATH, f'//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[3]/div[2]/div/div[2]/article/markdown-accessiblity-table/table/tbody/tr[{index}]/td[2]')
    role = role_elem.text.strip()
    location_elem = driver.find_element(By.XPATH, f'//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[3]/div[2]/div/div[2]/article/markdown-accessiblity-table/table/tbody/tr[{index}]/td[3]')
    location = location_elem.text.strip()
    link_elem = driver.find_element(By.XPATH, f'//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[3]/div[2]/div/div[2]/article/markdown-accessiblity-table/table/tbody/tr[{index}]/td[4]/a[1]')
    link = link_elem.get_attribute("href")
    date_elem = driver.find_element(By.XPATH, f'//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[3]/div[2]/div/div[2]/article/markdown-accessiblity-table/table/tbody/tr[{index}]/td[5]')
    date = date_elem.text.strip()

    return Job(company, role, location, link, date)

def save_scraped_jobs(jobs):
    """ Save scraped jobs so that we do not repeat jobs """

    file_path = os.path.join(os.getcwd(), JOBS_FILE)

    json_jobs = [job.getJSON() for job in jobs]
    with open(file_path, "w") as f:
        json.dump(json_jobs, f, indent=4)

def load_sent_jobs():

    """ Load sents jobs so we can check against saved jobs """
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, "r") as f:
            return json.load(f)
    return []

def gather_data():
    """ Main scraper logic """
    base_url = "https://github.com/SimplifyJobs/Summer2025-Internships?tab=readme-ov-file"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(base_url)

    sent_jobs = load_sent_jobs()

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.repository-content"))
        )
        jobs = []
        """ If first time running program, get first ten jobs available """
        if not sent_jobs:
            jobs = [scrape_job(driver, index) for index in range(1, 11)]
        else:
            first_job = Job(sent_jobs[0]['company'], sent_jobs[0]['role'], sent_jobs[0]['location'], sent_jobs[0]['link'], sent_jobs[0]['date'])
            index = 1
            while True:
                curr_job = scrape_job(driver, index)
                """ Only send job if it has not already been sent"""
                if (curr_job == first_job):
                    break
                jobs.append(curr_job)
                index += 1

        for job in jobs:
            print(job)
    
    except TimeoutException:
        print('Page took too long to load.')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        driver.quit()

    if jobs: #Only save if we scraped jobs
        save_scraped_jobs(jobs)

    return jobs


