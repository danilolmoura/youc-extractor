import logging
import pdb

from bs4 import BeautifulSoup
import click
import requests


logger = logging.getLogger()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--word', type=str)
def extract(word):
    logger.info('Start extraction')
    url = 'https://www.youtube.com/results?search_query=curso+de+{}'

    ses = requests.Session()
    res = ses.get(url.format(word))

    soup = BeautifulSoup(res.content, 'html.parser')


if __name__ == '__main__':
    cli()
