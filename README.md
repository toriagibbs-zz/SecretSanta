# Secret Santa
#### by Toria Gibbs and Justin Michel

A simple python script for Secret Santa gift assignments. The script creates a cycle of all users in random order and emails the assignments to each user from a specified gmail account.

BONUS: Cat Mode! The script supports two 'types' of Secret Santa:

1. simple: Assigns only a name, intended for in-person Secret Santa exchanges (no mailing address, due date, additional notes)
2. cats: Your assignee is 1 or more cats! Originally written for Etsy's Cats@ Secret Santa 2015, this mode supports cats' names, mailing location, and additional notes from the recipient cats' owner.

## Setup

It's simple! Download (cut and paste or git clone/fork) the SecretSanta.py file and make the following updates:
* Add your users to the names array
  * Each row has the format [name, email, cats' names, address, notes]
  * For a 'simple' Secret Santa, only fill out name and email
* Update the fromAddr, username, password variables for the gmail account which will send the assignments
* Consider asking a friend to send the emails, as they will show up in the sender's outbox!

## Usage
`./SecretSanta.py [-m <test|longtest|exec>] [-t <simple|cats>]`

* Runs with **mode=test** and **type=simple** by default
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


