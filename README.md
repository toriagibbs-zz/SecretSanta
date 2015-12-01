# Secret Santa
#### by Toria Gibbs and Justin Michel

A simple python script for Secret Santa gift assignments. The script creates a cycle of all users in random order and emails the assignments to each user from a specified gmail account.

BONUS: Cat Mode! The script supports two 'types' of Secret Santa:

1. simple: Assigns only a name, intended for in-person Secret Santa exchanges (no mailing address, due date, additional notes)
2. cats: Your assignee is 1 or more cats! Originally written for Etsy's Cats@ Secret Santa 2015, this mode supports cats' names, mailing location, and additional notes from the recipient cats' owner.

## Setup

It's simple! Download (cut and paste or git clone/fork) the SecretSanta.py file and make the following preparations:
* Create a CSV file (Excel, Google Spreadsheets, etc. can export to CSV format) with your participants information. See examples in the [examples](https://github.com/toriagibbs/SecretSanta/blob/master/examples) directory.
  * Each row has the format [name, email, cats' names, address, notes]
  * For a 'simple' Secret Santa, only name and email are required
* Consider asking a friend to send the emails, as they will show up in the sender's outbox!

## Usage
```
usage: SecretSanta.py [-h] [-m {test,longtest,exec}] [-t {simple,cats}]
                      [-e EMAIL] [-u USERNAME] [-p PASSWORD] [-r {gmail}]
                      [-d DUE_DATE]
                      participants_file

Secret Santa

positional arguments:
  participants_file     CSV file containing participant info

optional arguments:
  -h, --help            show this help message and exit
  -m {test,longtest,exec}, --mode {test,longtest,exec}
  -t {simple,cats}, --type {simple,cats}
  -e EMAIL, --email EMAIL
                        email address to send from
  -u USERNAME, --username USERNAME
                        username for email account
  -p PASSWORD, --password PASSWORD
                        password for email account
  -r {gmail}, --provider {gmail}
                        email provider
  -d DUE_DATE, --due-date DUE_DATE
                        due date in YYYY-MM-DD format
```

The `username` and `password` arguments can be omitted and will be prompted for if necessary.
For example, `./SecretSanta.py -e secretsanta@gmail.com -d 2015-12-15 -m exec -t cats 2015_secret_santa.csv`

* Runs with **mode=test**, **type=simple**, and **provider=gmail** by default
* Trouble authenticating with Google SMTP? Try [enabling less secure apps](https://www.google.com/settings/u/1/security/lesssecureapps).

| Mode     | Description                                                |
|----------|------------------------------------------------------------|
| test     | Test mode: prints simple 1-line assignments to console     |
| longtest | Test mode: prints complete constructed emails to console   |
| exec     | Execute mode: sends email assignments, no print to console |

| Type   | Description                                                                                             |
|--------|---------------------------------------------------------------------------------------------------------|
| simple | Simple Secret Santa assigns by name                                                                     |
| cats   | Cats Secret Santa assigns by cats and includes owner's name, mailing location, and notes about the cats |

