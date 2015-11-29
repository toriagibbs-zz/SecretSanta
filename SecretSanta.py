#!/usr/bin/python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Based on Justin's Secret Santa Program by Justin Michel #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import random
import smtplib
import getpass

names = [("Example User 1", "email_1@gmail.com"), \
         ("Example User 2", "email_2@gmail.com"), \
         ("Example User 3", "email_3@gmail.com"), \
         ("Example User 4", "email_4@gmail.com")]

numNames = len(names) - 1

fromaddr = "your_secret_santa_email@gmail.com"
username = "your_secret_santa_email"
password = "********"

def shuffle(x, y):
    first = names[x]
    names[x] = names[y]
    names[y] = first

def buildEmail(toAddr, toName, secretName):
    msg = """From: Secret Santa <your_secret_santa_email@gmail.com>
To: %s <%s>
Subject: Your Secret Santa Assignment!

Greetings %s! Using a very carefully derived formula (and a little bit of magic), the Secret Santa Program has picked you to be the Secret Santa for %s!!!

Have a nice day!
--Santa's Helper""" % (toAddr, toName, toName, secretName)

    return msg;

def randomize():
    count = 0
    while count < 100000:
        x = random.randint(0, numNames)
        y = random.randint(0, numNames)
        shuffle(x, y)
        count = count + 1

def main():
    randomize()

    password = getpass.getpass()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    for i in range(len(names)):
        santa = names[i][0]
        santaEmail = names[i][1]
        nextIndex = i+1
        if i == numNames:
            nextIndex = 0
        secret = names[nextIndex][0]
        msg = buildEmail(santaEmail, santa, secret)
        server.sendmail(fromaddr, santaEmail, msg)

    server.quit()

    return 0

if __name__ == '__main__':
    status = main()

