import logging
import json
import pdb


from bs4 import BeautifulSoup
import click
import requests

logger = logging.getLogger()

@click.group()
def cli():
    pass

URL_YOUTUBE_BASE = 'https://www.youtube.com'
URL_YOUTUBE_PLAYLIST = URL_YOUTUBE_BASE + '/playlist?list={}'
URL_YOUTUBE_SEARCH = 'https://www.youtube.com/results?search_query=curso+de+{}&sp=EgIQAw%3D%3D'
OUTPUT_FORMAT = '| [{}]({}) | {} | [{}]({})'

def extact(word):
	language = 'Portuguese'
	logger.info('Starting with word {}'.format(word))
	columns = []

	ses = requests.Session()
	res = ses.get(URL_YOUTUBE_SEARCH.format(word))

	soup = BeautifulSoup(res.content, 'html.parser')

	body = soup.body

	initial_pos = str(body.find_all('script')[1]).find('{"responseContext"')
	final_pos = str(body.find_all('script')[1]).find('{"apmUserPreference":{}}};') + 25

	res_json = json.loads(str(body.find_all('script')[1])[initial_pos:final_pos])

	contents = res_json['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

	for content in contents:
		try:
			playlist_link = content['playlistRenderer']['playlistId']
			playlist_title = content['playlistRenderer']['title']['simpleText']
			
			channel_name = content['playlistRenderer']['shortBylineText']['runs'][0]['text']
			channel_link = content['playlistRenderer']['shortBylineText']['runs'][0]['navigationEndpoint']['browseEndpoint']['canonicalBaseUrl']

			columns.append(OUTPUT_FORMAT.format(
				playlist_title,
				URL_YOUTUBE_PLAYLIST.format(playlist_link),
				language,
				channel_name,
				URL_YOUTUBE_BASE + channel_link
			))
		except Exception as e:
			pass

	columns.sort()
	for column in columns:
		print(column)

@cli.command()
@click.option('--word', type=str, required=True)
def test(word):
    response = extact(word)

if __name__ == '__main__':
    cli()
