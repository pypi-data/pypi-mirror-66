import click
import random
import string
import itertools
import click

from utils.storage import Session, Storage
from utils.models import User
from utils import readable_passwd, encrypt_password, decrypt_hash, check_encrypted_password, read_config, read_key
from getpass import getpass


@click.group()
def cli():
    pass


storage = Storage()


@cli.command()
@click.option(
    '--length', '-l',
    default=12,
    help='Length of password',
)
@click.option(
    '--words-only', '-w',
    help='Words only',
    is_flag=True,
    type=bool
)
@click.option(
    '--numbers-only', '-n',
    help='Numbers only',
    is_flag=True,
    type=bool
)
@click.option(
    '--readable', '-r',
    is_flag=True,
    help='Readable password generation',
    type=bool
)
@click.option(
    '--uppercase', '-u',
    is_flag=True,
    help='Readable password generation',
    type=bool
)
@click.option(
    '--lowercase', '-low',
    is_flag=True,
    help='Readable password generation',
    type=bool
)
@click.option(
    '--save', '-s',
    is_flag=True,
    help='Save to account',
    default=False,
    type=bool
)
def generate(length, words_only, numbers_only, readable, uppercase, lowercase, save):
    generated = ''
    if uppercase:
        if words_only:
            generated = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase) for _ in range(length))
        else:
            generated = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(length))
    elif lowercase:
        if words_only:
            generated = ''.join(random.SystemRandom().choice(
                string.ascii_lowercase) for _ in range(length))
        else:
            generated = ''.join(random.SystemRandom().choice(
                string.ascii_lowercase + string.digits) for _ in range(length))
    elif numbers_only:
        generated = ''.join(random.SystemRandom().choice(
            string.digits) for _ in range(length))
    elif readable:
        generated = ''.join(itertools.islice(readable_passwd(), length))
    else:
        generated = ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))
    session = Session()
    if save:
        exist = storage.redis.exists('login')
        if not exist:
            return print("You aren't logged in!")
        else:
            id = storage.redis.get('login')
            user = session.query(User).filter(User.id == id).first()
            if user is None:
                return print('Something went wrong, try loging in again.')
            name = input('Name of password: ')
            url = input('URL (none = no url): ')
            user.saved_passwords.append({
                'name': name,
                'url': None if str.lower(url) == 'none' or str.lower(url) == '' else url,
                'password': encrypt_password(generated)
            })
            session.query(User).filter(User.id == id).update(
                {'saved_passwords': user.saved_passwords})
            session.commit()
            return print(f'Saved password to {name}')

    return print(generated)


@cli.command()
def login():
    exist = storage.redis.exists('login')
    if exist:
        return print("You are already logged in, you can logout and log in to a different account.")

    username = input("What is your username: ")
    password = getpass("What is your password: ")

    session = Session()

    user = session.query(User).filter(User.username == username).first()

    storage.redis.setex('login', read_config()['login_expiration'], user.id)

    if user is None:
        print("No user found, try again later.")
    else:
        check = check_encrypted_password(password, user.authorization)
        if check:
            print("Logged in successfully!")
        else:
            print("Try again, was your password correct?")


@cli.command()
def logout():
    exist = storage.redis.exists('login')
    id = storage.redis.get('login')

    if not exist:
        return print("You aren't logged in yet!")

    storage.redis.delete('login')

    session = Session()

    user = session.query(User).filter(User.id == id).first()
    return print(f'You have logged out of {user.username}!')


@cli.command()
@click.option(
    '--show-all', '-s',
    is_flag=True,
    help='Show all passwords, un-censored',
    default=False,
    type=bool
)
def passwords(show_all):
    exist = storage.redis.exists('login')
    id = storage.redis.get('login')
    if not exist:
        return print("You are not logged in.")

    session = Session()

    user = session.query(User).filter(User.id == id).first()

    if user is None:
        return print('Something went wrong, try loging in again.')
    s = ""
    for x in user.saved_passwords:
        format = ""
        if show_all:
            consent = input(
                'Are you sure that you want to see your passwords? (Y/n): ')
            if not str.lower(consent) == 'y':
                format = f'{x["name"]}: {"".join("*" for _ in range(len(decrypt_hash(x["password"]))))}'
            else:
                format = f'{x["name"]}: {decrypt_hash(x["password"])}'
        else:
            # if not x['url']:
            format = f'{x["name"]}: {"".join("*" for _ in range(len(decrypt_hash(x["password"]))))}'
        s += format + "\n"
    return print(s)


@cli.command()
def signup():
    username = input("What is your username: ")
    password = getpass("What is your password: ")
    encrypted = encrypt_password(password)

    session = Session()
    existing = session.query(User).filter(User.username == username).first()
    if existing:
        return print("User exists already...")
    user = User(id=int(''.join(random.SystemRandom().choice(
        string.digits) for _ in range(14))), username=username, authorization=encrypted, saved_passwords=[])

    session.add(user)
    session.commit()
    print(username, encrypted)


@cli.command()
def store():
    password = getpass('What will be the password: ')
    session = Session()
    exist = storage.redis.exists('login')
    if not exist:
        return print("You aren't logged in!")
    else:
        id = storage.redis.get('login')
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            return print('Something went wrong, try loging in again.')
        name = input('Name of password: ')
        url = input('URL (none = no url): ')
        user.saved_passwords.append({
            'name': name,
            'url': None if str.lower(url) == 'none' or str.lower(url) == '' else url,
            'password': encrypt_password(password)
        })
        session.query(User).filter(User.id == id).update(
            {'saved_passwords': user.saved_passwords})
        session.commit()
        return print(f'Saved password to {name}')


if __name__ == '__main__':
    cli()
