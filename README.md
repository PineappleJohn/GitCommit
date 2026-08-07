# GitCommit
Automatically updates a file with a counter based on some information. Basically activity spoofing for GitHub
## Setup
Setup is simple, provide token, add repositories and filenames, in this case check ```counter-example.txt```.<br>
You can view all of the stored data in ```updated-token.json```. The link leads to ```update-names.txt``` which is a list of fake commit messages.
## Usage
Simply run the script with data filled out and it will automatically pick a few random repos to update every few minutes. You can replace the filename with something like ```folder1/folder2/filename``` to embed it into folders.

As of now the default json looks like this:
```json
{
    "token" : "insert-token",
    "commit-message-link": "https://raw.githubusercontent.com/PineappleJohn/GitCommit/refs/heads/main/update-names.txt",
    "repositories" : [
        {
            "repository-name" : "insert-repository-name",
            "filename" : "insert-filename",
            "counter": 0
        }
    ],
    "config": {
        "min-commit-wait-time": 30,
        "max-commit-wait-time": 900,
        "min-commit-count": 1,
        "max-commit-count": 9
    }
}
```
The legacy app is no longer supported but kept due to its setup functionality rather than the new one which just parses a user created json file.
