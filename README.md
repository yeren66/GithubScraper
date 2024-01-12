# GithubScraper
Scrape github repository under custom conditions.

use this command run the script
```
python scraper.py
```

### Conditions Setting

#### search conditions

Modify `get_java_repositories_with_stars` method in `scraper.py`.

The original params is like this
```
params = {
        "q": f"language:java stars:{stars_lower_bound}..{stars_upper_bound}",
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": "100"
    }
```
You can add query conditions in value of key"q", change language and so on. But Carefully change things related to method input params, unless you know how to deal with.

#### filter conditions

Modify method with suffix "filter" or add new filter method to make fine-grained filters.

Current filter contains `size_filter`, `commit_count_filter`, `has_pom_file_filter`.

If you want to add new filter, fill the place with comment `# add new filter here`.

<details>
  <summary>Here are a repo's info to refer</summary>
    
```
{
    "id": 22790488,
    "node_id": "MDEwOlJlcG9zaXRvcnkyMjc5MDQ4OA==",
    "name": "java-design-patterns",
    "full_name": "iluwatar/java-design-patterns",
    "private": false,
    "owner": {
        "login": "iluwatar",
        "id": 582346,
        "node_id": "MDQ6VXNlcjU4MjM0Ng==",
        "avatar_url": "https://avatars.githubusercontent.com/u/582346?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/iluwatar",
        "html_url": "https://github.com/iluwatar",
        "followers_url": "https://api.github.com/users/iluwatar/followers",
        "following_url": "https://api.github.com/users/iluwatar/following{/other_user}",
        "gists_url": "https://api.github.com/users/iluwatar/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/iluwatar/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/iluwatar/subscriptions",
        "organizations_url": "https://api.github.com/users/iluwatar/orgs",
        "repos_url": "https://api.github.com/users/iluwatar/repos",
        "events_url": "https://api.github.com/users/iluwatar/events{/privacy}",
        "received_events_url": "https://api.github.com/users/iluwatar/received_events",
        "type": "User",
        "site_admin": false
    },
    "html_url": "https://github.com/iluwatar/java-design-patterns",
    "description": "Design patterns implemented in Java",
    "fork": false,
    "url": "https://api.github.com/repos/iluwatar/java-design-patterns",
    "forks_url": "https://api.github.com/repos/iluwatar/java-design-patterns/forks",
    "keys_url": "https://api.github.com/repos/iluwatar/java-design-patterns/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/iluwatar/java-design-patterns/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/iluwatar/java-design-patterns/teams",
    "hooks_url": "https://api.github.com/repos/iluwatar/java-design-patterns/hooks",
    "issue_events_url": "https://api.github.com/repos/iluwatar/java-design-patterns/issues/events{/number}",
    "events_url": "https://api.github.com/repos/iluwatar/java-design-patterns/events",
    "assignees_url": "https://api.github.com/repos/iluwatar/java-design-patterns/assignees{/user}",
    "branches_url": "https://api.github.com/repos/iluwatar/java-design-patterns/branches{/branch}",
    "tags_url": "https://api.github.com/repos/iluwatar/java-design-patterns/tags",
    "blobs_url": "https://api.github.com/repos/iluwatar/java-design-patterns/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/iluwatar/java-design-patterns/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/iluwatar/java-design-patterns/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/iluwatar/java-design-patterns/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/iluwatar/java-design-patterns/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/iluwatar/java-design-patterns/languages",
    "stargazers_url": "https://api.github.com/repos/iluwatar/java-design-patterns/stargazers",
    "contributors_url": "https://api.github.com/repos/iluwatar/java-design-patterns/contributors",
    "subscribers_url": "https://api.github.com/repos/iluwatar/java-design-patterns/subscribers",
    "subscription_url": "https://api.github.com/repos/iluwatar/java-design-patterns/subscription",
    "commits_url": "https://api.github.com/repos/iluwatar/java-design-patterns/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/iluwatar/java-design-patterns/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/iluwatar/java-design-patterns/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/iluwatar/java-design-patterns/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/iluwatar/java-design-patterns/contents/{+path}",
    "compare_url": "https://api.github.com/repos/iluwatar/java-design-patterns/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/iluwatar/java-design-patterns/merges",
    "archive_url": "https://api.github.com/repos/iluwatar/java-design-patterns/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/iluwatar/java-design-patterns/downloads",
    "issues_url": "https://api.github.com/repos/iluwatar/java-design-patterns/issues{/number}",
    "pulls_url": "https://api.github.com/repos/iluwatar/java-design-patterns/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/iluwatar/java-design-patterns/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/iluwatar/java-design-patterns/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/iluwatar/java-design-patterns/labels{/name}",
    "releases_url": "https://api.github.com/repos/iluwatar/java-design-patterns/releases{/id}",
    "deployments_url": "https://api.github.com/repos/iluwatar/java-design-patterns/deployments",
    "created_at": "2014-08-09T16:45:18Z",
    "updated_at": "2024-01-11T17:05:49Z",
    "pushed_at": "2024-01-09T06:06:16Z",
    "git_url": "git://github.com/iluwatar/java-design-patterns.git",
    "ssh_url": "git@github.com:iluwatar/java-design-patterns.git",
    "clone_url": "https://github.com/iluwatar/java-design-patterns.git",
    "svn_url": "https://github.com/iluwatar/java-design-patterns",
    "homepage": "https://java-design-patterns.com",
    "size": 31545,
    "stargazers_count": 85212,
    "watchers_count": 85212,
    "language": "Java",
    "has_issues": true,
    "has_projects": false,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "has_discussions": false,
    "forks_count": 25902,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 238,
    "license": {
        "key": "other",
        "name": "Other",
        "spdx_id": "NOASSERTION",
        "url": null,
        "node_id": "MDc6TGljZW5zZTA="
    },
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [
        "awesome-list",
        "design-patterns",
        "hacktoberfest",
        "java",
        "principles",
        "snippets",
        "snippets-collection",
        "snippets-library"
    ],
    "visibility": "public",
    "forks": 25902,
    "open_issues": 238,
    "watchers": 85212,
    "default_branch": "master",
    "permissions": {
        "admin": false,
        "maintain": false,
        "push": false,
        "triage": false,
        "pull": true
    },
    "score": 1.0
}
```
</details>

### Token Setting

You should add a file named `tokens.txt` to record **Github Personal Access Token** to accelerate speed and avoid [rate limit](https://docs.github.com/en/graphql/overview/rate-limits-and-node-limits-for-the-graphql-api#exceeding-the-rate-limit).

A `token.txt` file like this
```
ghp_tMLAziHRsOCMqJil********IOxSuC0hJMDl
ghp_iOOxByUrE58frqSy********lHRG2E049ZpN
ghp_8q69yCA8OHJSwIsa********k5em3q0MECTG
```

Script will use these tokens recursively.

You can find detailed tutorial [Here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to get **Github Personal Access Token**.

> Note: Although multiple tokens could be applied by one account, the rate limit is shared.