# Instagram Network Tool

Collection of scripts to build and analyze instagram-networks from account-data.

**Currently includes**
- Script to convert the relevant HTML section to a json file
- A tool wich interprets search querries to filter all users in network by who does or doesn't follow them.


## How To Use

This section includes a quick summary on how to use each script.

### Read Network

The script `read_network.py` converts html list of users followed by the target user and generates an entry in the network-file (json format).

**1. Get the HTML**\
Make sure you are signed into your Instagram Account. Open your browser, go to the Instagram4-rofile you want to scrape and click on "Following".
A list of accounts should open up. Scroll to the bottom of that list to dynamically load in all accounts and then hover you mouse above a user.
Press F12 to inspect the element and find the container which contains all users.\
Copy the element and paste the html into a text file. Make sure to copy the filepath of the html file.

**2. Convert To JSON**\
Then open up your console, go to the folder containing the scripts and execute the conversion script:
```sh
python3 read_network.py [path to html] [path to network file] [usertag]
```

If the provided network file does not exist it will be created. If it already exists the data will be appended or updated.

## Filter Network

With `database_search.py` you can filter the network for users according to who follows these accounts.

```sh
python3 database_search.py [network file] [search expression]
```

The search expression gets fed through a custom built interpreter.\
**Example**: `"(a or b) and not (c or d)"`\
Returns all accounts followed by a or b but excludes all accounts followed by c or d

Use `-d` for list of scraped accounts or `-h` for help.

Network files are json-formatted and should have the following format:
```json
{
  "account 1": {
    "display": "<display name, not strictly required>",
    "follows": ["account a", "account b", "..."]
  },

  "account 2":{
    "display": "<display name, not strictly required>",
    "follows": ["see above"]
  },
  ...
}
```
