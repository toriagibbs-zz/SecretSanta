#!/usr/bin/python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Based on Justin's Secret Santa Program by Justin Michel #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import getopt
import random
import smtplib
import getpass

names = [("Joe", "joe@gmail.com", "Fluffy", "the Brooklyn office", "Fluffy is crazy for catnip!"), \
        ("Mike", "mike@gmail.com", "Fish and Chips", "the Hudson office", "Fish and Chips are tearing up my furniture, they need a scratching post."), \
        ("Anne", "anne@gmail.com", "Naga and Momo", "the Brooklyn office", "Naga and Momo love toys with feathers."), \
        ("Sally", "sally@gmail.com", "Romeow", "123 State Street, Seattle, WA  00123", "Romeow likes toys that dangle from strings.")]

numNames = len(names) - 1

dueDate = "Tues Dec 15"

fromAddr = "your_secret_santa_email@gmail.com"
username = "your_secret_santa_email"
password = "********"

def randomize():
    count = 0
    while count < 100000:
        x = random.randint(0, numNames)
        y = random.randint(0, numNames)
        shuffle(x, y)
        count = count + 1

def shuffle(x, y):
    first = names[x]
    names[x] = names[y]
    names[y] = first

def setupMailServer():
    password = getpass.getpass()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    return server

def buildEmail(toAddr, toName, secretName):
    msg = """From: Secret Santa <%s>
To: %s <%s>
Subject: Your Secret Santa Assignment!

Greetings %s! Using a very carefully derived formula (and a little bit of magic), the Secret Santa Program has picked you to be the Secret Santa for %s!!!

Have a nice day!
--Santa's Helper""" % (fromAddr, toName, toAddr, toName, secretName)
    return msg

def buildCatsEmail(toAddr, toName, secretName, secretCats, secretAddress, secretNotes):
    msg = """From: Secret Santa <%s>
To: %s <%s>
Subject: Your Secret Santa Assignment!

Greetings %s! Using a very carefully derived formula (and a little bit of magic), the Secret Santa Program has picked you to be the Secret Santa for %s!!!

Proud owner, %s, says: %s

Please mail your gift to %s at %s by %s.

Have a nice day!
--Santa's Helper""" % (fromAddr, toName, toAddr, toName, secretCats, secretName, secretNotes, secretName, secretAddress, dueDate)
    return msg

def main(argv):
    mode = 'test'
    type = 'simple'
    try:
        opts, args = getopt.getopt(argv,"m:t:",["mode=","type="])
    except getopt.GetoptError:
        print 'SecretSanta.py [-m <test|longtest|exec>] [-t <simple|cats>] '
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            arg = arg.lower()
            if arg == 'test' or arg == 'longtest' or arg == 'exec':
                mode = arg
            else:
                print '%s is not a valid mode, please use "test" or "longtest" or "exec"' % (arg)
                sys.exit(2)
        elif opt in ("-t", "--type"):
            arg = arg.lower()
            if arg == 'simple' or arg == 'cats':
                type = arg
            else:
                print '%s is not a valid type, please use "simple" or "cats"' % (arg)
                sys.exit(2)

    print 'Running in %s mode' % (mode)
    if mode != 'exec':
        print 'Use -m exec to run in execute mode'

    server = ''
    if mode == 'exec':
        server = setupMailServer()

    randomize()
    for i in range(len(names)):
        santa = names[i][0]
        santaEmail = names[i][1]
        nextIndex = i+1
        if i == numNames:
            nextIndex = 0
        secret = names[nextIndex][0]

        if type == 'cats':
            secretCats = names[nextIndex][2]
            secretAddress = names[nextIndex][3]
            secretNotes = names[nextIndex][4]
            msg = buildCatsEmail(santaEmail, santa, secret, secretCats, secretAddress, secretNotes)
        else:
            msg = buildEmail(santaEmail, santa, secret)

        if mode == 'exec':
            server.sendmail(fromAddr, santaEmail, msg)
        elif mode == 'longtest':
            print '------------------------'
            print msg
        else:
            print '%s -> %s' % (santa, secret)

    if mode == 'exec':
        server.quit()

    return 0

if __name__ == '__main__':
    status = main(sys.argv[1:])

