import time
import requests
import json
import re
from tqdm import tqdm
import utils
from tqdm import tqdm
import logging

logging.basicConfig(filename='monitor_rate_limit.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
headers = utils.get_header()

def get_java_repositories_with_stars(headers, stars_lower_bound, stars_upper_bound, page):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:java stars:{stars_lower_bound}..{stars_upper_bound}",
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": "100"
    }
    response = requests.get(url, params=params, headers=headers)
    monitor_rate_limit(response)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print("Error: Failed to fetch repositories")
        return []
    
def get_commit_count_with_regex(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # logging.info(response.text)
        # Check if the response is successful
        if response.status_code == 200:
            # Use regular expression to find the commit count
            match = re.search(r'"commitCount":"([\d,]+)"', response.text)
            if match:
                # Extract the commit count and remove commas
                commit_count = match.group(1).replace(',', '')
                commit_count_number = int(commit_count)
            else:
                commit_count_number = "Commit count not found in the file."
            return commit_count_number
        else:
            return f"Failed to get response from the URL, status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def size_filter(repo):
    if repo["size"] > 1000 and repo["size"] < 1000000:
        return True
    return False

def commit_count_filter(repo):
    url = repo['html_url']
    commit_count = get_commit_count_with_regex(url)
    if type(commit_count) == int and commit_count >= 500:
        return commit_count
    return -1

def has_pom_file_filter(repo):
    url = repo["contents_url"].replace("{+path}", "")
    response = requests.get(url)
    # monitor_rate_limit(response)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file["name"] == "pom.xml":
                return True
    return False

# add new filter here

def monitor_rate_limit(response):
    logging.info(response.headers)

if __name__ == "__main__":
    start_time = time.time()
    repositories = []

    # cause only 1k repos could be scraped once, so use stars_bound to control the number of repos.
    # make sure the number of repos in the stars_cound is less than 1k.
    # This section can be rewritten to obtain automatically if really needed >_<
    stars_bound = [(4000, 1000000), (2000, 4000), (1500, 2000), (1200, 1500), (1000, 1200), 
                   (800, 1000), (700, 800), (600, 700), (500, 600), (450, 500), (400, 450), (350, 400), 
                   (320, 350), (300, 320), (270, 300), (250, 270), (230, 250), (210, 230), (200, 210), 
                   (190, 200), (180, 190), (170, 180), (160, 170), (150, 160), (145, 150), (140, 145),
                   (135, 140), (130, 135), (125, 130), (120, 125), (115, 120), (110, 115), (105, 110), (100, 105)]
    
    for i in range(len(stars_bound)):
        stars_lower_bound = stars_bound[i][0]
        stars_upper_bound = stars_bound[i][1]
        print(f"epoch {i}: stars range {stars_lower_bound}..{stars_upper_bound - 1}")
        headers = utils.get_header()
        temp_repos = []
        for page in tqdm(range(1, 11), desc="Getting repositories"):
            try:
                per_search = get_java_repositories_with_stars(headers, stars_lower_bound, stars_upper_bound, page)
            except e:
                logging.info("When Getting repositories, something maybe connection error occured, sleep 3s and retry, details:")
                logging.info(e)
                time.sleep(3)
                page -= 1
                continue
            if len(per_search) == 0:
                break
            temp_repos.extend(per_search)
        if len(temp_repos) == 0: # this always means current token is banned temporarily
            headers = utils.get_header()
            i -= 1
            continue
        filtered_repos = []
        gather_repos = []
        for j in tqdm(range(len(temp_repos)), desc="Filtering repositories"):
            try:
                commit_count = commit_count_filter(temp_repos[j])
                has_pom_file = has_pom_file_filter(temp_repos[j])
                # add new filter here
            except Exception as e:
                logging.info("When Filtering repositories, somethingmaybe connection error occured, sleep 3s and retry, details:")
                logging.info(e)
                time.sleep(3)
                j -= 1
                continue
            if commit_count != -1 and has_pom_file: # add new filter here
                filtered_repos.append(temp_repos[j])
                content = {'project_name': temp_repos[j]['name'], 'url': temp_repos[j]['html_url'], 'stars': temp_repos[j]['stargazers_count'], 'size': temp_repos[j]['size'], 'commit_count': commit_count}
                gather_repos.append(content)
        print("Number of repos:", len(filtered_repos))
        utils.save_to_file(filtered_repos, "original_result.json")
        utils.save_to_file(gather_repos, "gather_result.json")
        repositories.extend(filtered_repos)
        if len(repositories) >= 3000:
            break

    url_repos = utils.handle_repos(repositories)
    utils.save_to_file(url_repos, "url_data.json")

    print("Total repositories:", len(repositories))
    end_time = time.time()
    print("Time cost:", end_time - start_time, "seconds")
