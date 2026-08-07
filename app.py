import datetime
import random
import github
import os
import json
import time

import requests

tokenPath = "updated-token.json"

if os.path.exists(tokenPath):
    with open(tokenPath, "r") as f:
        token = json.load(f)
else:
    token = None
    exit(f"Token file not found. Please ensure '{tokenPath}' exists, you can get the contents from the git repo")

auth = None
git = None
commitMessages = None

try:
    auth = github.Auth.Token(token["token"])
    git = github.Github(auth=auth)
    commitMessages = requests.get(token["commit-message-link"]).text.splitlines()

    print("Login complete")
except Exception as e:
    print("Something went wrong. " + str(e))
    exit(-1)

def GetReposByName(repos: list[github.Repository], name: str) -> github.Repository:
    for repo in repos:
        if repo.name == name:
            return repo
    return None

commits = random.randint(token["config"]["min-commit-count"], token["config"]["max-commit-count"])
for i in range(commits):
    repositoryIndex = random.randint(0, len(token["repositories"]) - 1)
    repoName = token["repositories"][repositoryIndex]["repository-name"]
    repo: github.Repository = GetReposByName(git.get_user().get_repos(visibility="public"), repoName)
    assert repo is not None, f"Repo {repoName} not found. Please ensure the repository exists and is public."

    print("Found repo" if repo is not None else "No repo")

    counter = int(token["repositories"][repositoryIndex]["counter"]) + 1

    repo.update_file(token["repositories"][repositoryIndex]["filename"] + ".txt", random.choice(commitMessages), str(counter), sha=repo.get_contents(token["repositories"][repositoryIndex]["filename"] + ".txt").sha, branch="main")

    token["repositories"][repositoryIndex]["counter"] = str(counter)

    with open(tokenPath, "w") as f:
        json.dump(token, f)
        print("JSON dumped.")

    wait = random.randint(int(token["config"]["min-commit-wait-time"]), int(token["config"]["max-commit-wait-time"]))
    print("Waiting " + str(wait))
    time.sleep(wait)

git.close()
