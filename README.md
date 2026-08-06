# GitCommit
Automatically updates a file with a counter based on some information. Basically activity spoofing for GitHub
## Setup
Setup is simple, provide token, select repository, and then type a filename, in this case check ```counter-example.txt```.<br>
You can view all of the stored data in token.json. The link leads to ```update-names.txt``` which is a list of fake commit messages.
## Roadmap
For the future this script will have a list of repositories and a file for each, possibly even multiple files to make it more realistic. Plus the in-script setup
will be removed, its clunky, broken, and it doesn't make sense for the future.
<br><br>

As of now the default json looks like this:
```json
{
  "token" : "Insert token",
  "repository-id" : "Do not touch this",
  "filename" : "Do not touch this",
  "counter": 0,
  "commit-message-link" : "https://raw.githubusercontent.com/PineappleJohn/GitCommit/refs/heads/main/update-names.txt"
}
```
But it will look like this:

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
