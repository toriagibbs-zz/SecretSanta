#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Based on Justin's Secret Santa Program by Justin Michel #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import argparse
import collections
import datetime
import getpass
import random
import smtplib


class Enum(object):
    @classmethod
    def choices(cls):
        return [v for (k, v) in vars(cls).iteritems() if not k.startswith('_')]


class Mode(Enum):
    TEST = 'test'
    LONGTEST = 'longtest'
    EXEC = 'exec'


class Type(Enum):
    SIMPLE = 'simple'
    CATS = 'cats'


class Provider(Enum):
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


PARTICIPANTS = [
        ("Joe", "joe@gmail.com", "Fluffy", "the Brooklyn office", "Fluffy is crazy for catnip!"), \
        ("Mike", "mike@gmail.com", "Fish and Chips", "the Hudson office", "Fish and Chips are tearing up my furniture, they need a scratching post."), \
        ("Anne", "anne@gmail.com", "Naga and Momo", "the Brooklyn office", "Naga and Momo love toys with feathers."), \
        ("Sally", "sally@gmail.com", "Romeow", "123 State Street, Seattle, WA 00123", "Romeow likes toys that dangle from strings.")
]


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
    parser.add_argument('-u', '--username', type=str, required=False,
                        help='username for email account')
    parser.add_argument('-p', '--password', type=str, required=False,
                        help='password for email account')
    parser.add_argument('-r', '--provider', choices=Provider.choices(), default=Provider.GMAIL,
                        help='email provider')
    parser.add_argument('-d', '--due-date', type=parse_date, default=DEFAULT_DUE_DATE)

    args = parser.parse_args()
    mode = args.mode
    type = args.type
    email = args.email
    due_date = args.due_date.strftime('%a %b %-d')

    print 'Running in %s mode' % (mode)
    if mode != Mode.EXEC:
        print 'Use -m {} to run in execute mode'.format(Mode.EXEC)

    # setup SMTP server if necessary
    server = None
    if mode == Mode.EXEC:
        username = args.username if args.username else raw_input('Username: ')
        password = args.password if args.password else getpass.getpass('Password: ')
        server = setup_mail_server(username, password, args.provider)

    participants = PARTICIPANTS # TODO: load from CSV file
    random.shuffle(participants)

    for (santa, secret) in pair_up(participants):
        santa_name = santa[0]
        santa_email = santa[1]
        secret_name = secret[0]

        if type == Type.CATS:
            secret_cats = secret[2]
            secret_address = secret[3]
            secret_notes = secret[4]
            cats = CATS_TEMPLATE.format(secret_name=secret_name,
                                        secret_notes=secret_notes,
                                        secret_address=secret_address,
                                        due_date=due_date)
            msg = EMAIL_TEMPLATE.format(from_addr=email,
                                        to_name=santa_name,
                                        to_email=santa_email,
                                        secret_name=secret_name,
                                        cats=cats)
        else:
            msg = EMAIL_TEMPLATE.format(from_addr=email,
                                        to_name=santa_name,
                                        to_email=santa_email,
                                        secret_name=secret_name,
                                        cats='')

        if mode == Mode.EXEC:
            server.sendmail(email, santa_email, msg)
        elif mode == Mode.LONGTEST:
            print '{0:-<30}'.format('')
            print msg
        else:
            print '{} -> {}'.format(santa_name, secret_name)

    if mode == Mode.EXEC:
        server.quit()

    return 0

if __name__ == '__main__':
    main()

