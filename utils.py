import json
import os

def find_tokens():
    with open('tokens.txt', 'r') as f:
        tokens = f.readlines()
    f = lambda x: x.replace('\n', '')
    tokens = list(map(f, tokens))
    return tokens

def save_to_file(content, filename="result.json"):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(content, f, indent=4)
    else:
        with open (filename, 'r') as f:
            data = json.load(f)
        data.extend(content)
        data = list(set(data))
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

def get_header():
    """
    Return a header with a token recursively.
    """
    global index
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token ' + tokens[index],
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
    index = (index + 1) % len(tokens)
    return headers

def handle_repos(repos):
    url_repos = []
    for repo in repos:
        url_repos.append(repo['html_url'])
    return url_repos

# init
tokens = find_tokens()
index = 0