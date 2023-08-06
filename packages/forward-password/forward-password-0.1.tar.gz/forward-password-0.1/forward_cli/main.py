import click
import random
import string
import itertools
import click

from utils.loader import load_from_directory


@click.group()
def main():
    pass


if __name__ == "__main__":
    load_from_directory("commands", main)
    main()
