# Very basic and barebones app to automatically create github commits into a public repository updating a counter.

import datetime
import random
import github
import os
import json
import time

import argparse

import requests
parser = argparse.ArgumentParser(description="GitCommit is a script that automatically pushes a random number of commits to a counter file on github for the user.")

parser.add_argument("--edit", "-e", action='store_true', help="Skips the actual running of the script while also forcing the setup sequence to run. This still requires the user login, to read and check information.")
parser.add_argument("--reset", "-r", action='store_true', help="Overrites the token json file with a fresh one. (Will remove all data)")

args = parser.parse_args()

if os.path.exists("token.json") and not args.reset: # setup is kind of broken but works enough
    with open("token.json", "r") as f:
        token = json.loads(f.read())
else:
    userToken = "Enter token"

    if not args.reset:
        print("> Need help? Press enter for more info.")
        userToken = input("< Github PAT (Key) (Classic): ")

        if userToken == "":
            print("\n\n> This program requires a Github Personal Access Token (PAT), this is found in settings.\n This token is only used to automatically create / update files within the selected repo.\n Please restart and enter your token to continue the setup.")
            exit(0)
    elif os.path.exists("token.json"):
        os.remove("token.json")

    with open("token.json", "x") as f:
        f.write('{\n"token" : "' + userToken + '",\n"repository-id" : "Do not touch this",\n"filename" : "Do not touch this",\n"counter": 0,\n"commit-message-link" : "https://raw.githubusercontent.com/PineappleJohn/GitCommit/refs/heads/main/update-names.txt"\n}')

    print("> Check token.json to ensure it is correct, then restart.")
    exit(-1)

try:
    auth = github.Auth.Token(token["token"])
    git = github.Github(auth=auth)
    user = git.get_user()
    publicRepos = user.get_repos(visibility="public")


    print("\n\n" + # this is incredibly messy but not a big deal
    r' dP""b8 88 888888     dP""b8  dP"Yb  8b    d8 8b    d8 88 888888' + "\n" +
    r'dP   `" 88   88      dP   `" dP   Yb 88b  d88 88b  d88 88   88  ' + "\n" +
    r'Yb  "88 88   88      Yb      Yb   dP 88YbdP88 88YbdP88 88   88  ' + "\n" +
    r' YboodP 88   88       YboodP  YbodP  88 YY 88 88 YY 88 88   88  '
    )
    print(f"\n> User {user.login} ({user.name}) logged in successfully.\n> ...")
except Exception as e:
    print("> An error occurred while trying to authenticate with GitHub. Please check your token and internet then try again.")
    input("< Press enter for more info")
    print(e)
    exit(-1)

commitMesages = [line.strip() for line in requests.get(token["commit-message-link"]).text.splitlines() if line.strip() != ""]

def setup():
    print("> Program not configured, running setup...")
    includeOthers = input("< Include other users repositories? (y/n)").lower() == "y"

    for i, repo in enumerate(publicRepos): # If the user name isn't removed it looks much worse, it's really only needed on other users repositories, ex. BananaFrank/FooBar -> FooBar
        if i > 99: break # at this point printing them would be silly
        name = repo.full_name
        if user.login in repo.full_name and not includeOthers:
            name = name.removeprefix(user.login + "/")
            
        print(f"[{i}] | {" " if i > 9 else "  "}{name}") # add padding so text doesn't look bad

    print(f"[-1] Create new repo\n")

    print("===============================")
 
    try:
        selectedRepo = int(input("<- #"))
    except:
        print("> Invalid input")
        exit(-1)

    if selectedRepo == -1:
        repoName = input("< Repo name: ")
        repoDesc = input("< Repo description: ")
        try:
            newRepo = user.create_repo(repoName, description=repoDesc, private=False)
            print(f"> Id: {newRepo.id}")
            token["repository-id"] = newRepo.id
        except Exception as e:
            print(f"An error occurred while trying to create the repo: {e}")
            exit(-1)

        print("> Repo created successfully.")

    if publicRepos[selectedRepo] is None:
        print("> Invalid input")
        exit(-1)



    try:
        for i, repo in enumerate(publicRepos):
            if selectedRepo == i:
                token["repository-id"] = repo.id
                token["filename"] = input("< Filename: ")
                repo.create_file(token["filename"] + ".txt", "Initial commit", str(token["counter"]), branch="main") # fun fact: if you want to make it more inconspicous you can make the filename variable a path and hides the file making the counter commit look larger
    except Exception as e:
        print("=== An unknown error occured! ===")
        print(f"More details: {e}")
        exit(-1)

    json.dump(token, open("token.json", "w"))
    print("> Setup complete")

if token["repository-id"] == "Do not touch this" or token["filename"] == "Do not touch this" or args.edit:
    setup()

    if args.edit:
        exit(1)

print("> Ready")

try:
    for i in range(random.randrange(1, 6)):
        try:
            repo = git.get_repo(token["repository-id"]) # updates the counter and updates the file
            token["counter"] = int(token["counter"]) + 1
            repo.update_file(token["filename"] + ".txt", random.choice(commitMesages), str(token["counter"]), repo.get_contents(token["filename"] + ".txt").sha, branch="main")
            json.dump(token, open("token.json", "w"))
        except KeyboardInterrupt:
            print("> Unable to exit at this moment, skipped this commit.")
            continue
        try:
            waitTime = random.randrange(30, 900)
            print("> Commit successful!")
            print(f"> Waiting {waitTime} seconds before next commit... ({(datetime.datetime.now() + datetime.timedelta(seconds=waitTime)).strftime('%H:%M')})\n> ...")

            time.sleep(waitTime) # takes some time to avoid rate limits and such
        except KeyboardInterrupt:
            print("> Exiting safely...")
            exit(0)
except Exception as e:
    print(f"> An error occurred while trying to update the repo: {e}")
    exit(-1)


git.close()
