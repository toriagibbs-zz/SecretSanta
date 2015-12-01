#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Based on Justin's Secret Santa Program by Justin Michel #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import argparse
import csv
import collections
import datetime
import getpass
import random
import smtplib


class StringEnum(object):
    @classmethod
    def choices(cls):
        return [v for (k, v) in vars(cls).iteritems() if not k.startswith('_')]


class Mode(StringEnum):
    TEST = 'test'
    LONGTEST = 'longtest'
    EXEC = 'exec'


class Type(StringEnum):
    SIMPLE = 'simple'
    CATS = 'cats'


class Provider(StringEnum):
    GMAIL = 'gmail'


ProviderInfo = collections.namedtuple('ProviderInfo', ['hostname', 'port', 'ssl'])


PROVIDER_INFO = {
    Provider.GMAIL: ProviderInfo('smtp.gmail.com', 465, True),
}


EMAIL_TEMPLATE = """From: Secret Santa <{from_addr}>
To: {to_name} <{to_email}>
Subject: Your Secret Santa Assignment!

Greetings {to_name}! Using a very carefully derived formula (and a little bit of magic), the Secret Santa Program has picked you to be the Secret Santa for {secret_name}!!!
{cats}
Have a nice day!
--Santa's Helper"""


CATS_TEMPLATE = """

Proud owner, {secret_name}, says: {secret_notes}

Please mail your gift to {secret_name} at {secret_address} by {due_date}.

"""


DEFAULT_DUE_DATE = datetime.date.today().replace(month=12, day=15)


Participant = collections.namedtuple('Participant', ['name', 'email', 'cats', 'address', 'notes'])
Participant.__new__.__defaults__ = (None, None, None)


def read_participants(participants_file):
    with open(participants_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        return [Participant(*row) for row in reader]


def setup_mail_server(username, password, provider):
    info = PROVIDER_INFO[provider]
    server = smtplib.SMTP_SSL(info.hostname, info.port) \
             if info.ssl else smtplib.SMTP(info.hostname, info.port)
    server.login(username, password)
    return server


def pair_up(values):
    return zip(values, values[1:] + values[:1])


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def main():

    parser = argparse.ArgumentParser(description='Secret Santa')
    parser.add_argument('-m', '--mode', choices=Mode.choices(), default=Mode.TEST)
    parser.add_argument('-t', '--type', choices=Type.choices(), default=Type.SIMPLE)
    parser.add_argument('-e', '--email', type=str, help='email address to send from')
    parser.add_argument('-u', '--username', type=str, help='username for email account')
    parser.add_argument('-p', '--password', type=str, help='password for email account')
    parser.add_argument('-r', '--provider', choices=Provider.choices(),
                        default=Provider.GMAIL, help='email provider')
    parser.add_argument('-d', '--due-date', type=parse_date, default=DEFAULT_DUE_DATE,
                        help='due date in YYYY-MM-DD format')
    parser.add_argument('participants_file', help='CSV file containing participant info')

    args = parser.parse_args()
    mode = args.mode
    type = args.type
    email = args.email
    due_date = args.due_date.strftime('%a %b %-d')
    participants = read_participants(args.participants_file)

    print 'Running in %s mode' % (mode)
    if mode != Mode.EXEC:
        print 'Use -m {} to run in execute mode'.format(Mode.EXEC)

    # setup SMTP server if necessary
    server = None
    if mode == Mode.EXEC:
        username = args.username if args.username else raw_input('Username: ')
        password = args.password if args.password else getpass.getpass('Password: ')
        server = setup_mail_server(username, password, args.provider)

    random.shuffle(participants)

    for (santa, secret) in pair_up(participants):
        if type == Type.CATS:
            cats = CATS_TEMPLATE.format(secret_name=secret.name,
                                        secret_notes=secret.notes,
                                        secret_address=secret.address,
                                        due_date=due_date)
            msg = EMAIL_TEMPLATE.format(from_addr=email,
                                        to_name=santa.name,
                                        to_email=santa.email,
                                        secret_name=secret.cats,
                                        cats=cats)
        else:
            msg = EMAIL_TEMPLATE.format(from_addr=email,
                                        to_name=santa.name,
                                        to_email=santa.email,
                                        secret_name=secret.name,
                                        cats='')

        if mode == Mode.EXEC:
            server.sendmail(email, santa.email, msg)
        elif mode == Mode.LONGTEST:
            print '{0:-<30}'.format('')
            print msg
        else:
            print '{} -> {}'.format(santa.name, secret.name)

    if mode == Mode.EXEC:
        server.quit()

    return 0

if __name__ == '__main__':
    main()

