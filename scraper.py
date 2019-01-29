from bs4 import BeautifulSoup
import pprint
from newspaper import Article
import re

pp = pprint.PrettyPrinter()

def main():
	notes = import_bookmarks("data/articles_without_content.enex")
	notes = get_notes_content(notes)
	export_updated_bookmarks(notes, "data/articles_with_content.enex")
	print('Done!')


def import_bookmarks(source_file):
	''' Given the path to an evernote XML source file,
	extracts and returns a list of notes within that file.
	'''
	print('Parsing {}...'.format(source_file))

	try:
		with open(source_file) as file:
			soup = BeautifulSoup(file, "xml")
			notes = soup.find_all('note')
			return notes
	except:
		return []


def get_notes_content(notes):
	''' Given a list of notes, 
	returns an updated list of notes with the note content attribute 
	set to the body content of the article (if it was successfully scraped).
	'''
	for i, note in enumerate(notes):

		print("Processing article {} of {}".format(i+1, len(notes)))

		# find the article url
		url_markup = note.find('source-url')
		if url_markup:
			url = url_markup.get_text().strip()

			# download and get the article content
			article = Article(url, keep_article_html=True)
			try:
				article.download()
				article.parse()
				content = build_content_html(article)
				content_obj = BeautifulSoup(content, "html.parser")

				# add the content to the note object
				note.content.clear()
				note.content.append(content_obj)
			except:
				print('- Could not process article')

	return notes


def build_content_html(article):
	''' Given a parsed article object,
	returns HTML with the article title and body html.
	'''
	# evernote needs content to be wrapped in CDATA and the <en-note> tag
	content_xml = '<![CDATA[<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>'

	if article.title:
		content_xml += "<h1>{}</h1>\n".format(article.title)

	if article.text:
		text_lines = [line for line in article.text.splitlines() if line]
		for line in text_lines:
			# line = line.replace("\"", "__").replace("\'", "_")
			content_xml += "<p>{}</p>".format(line.strip())

	content_xml += '</en-note>]]>'

	return content_xml


def export_updated_bookmarks(notes, filepath):
	''' Given a list of notes as bs4 objects,
	write out an updated evernote XML bookmark file to the given filepath.
	'''
	print('Exporting to {}...'.format(filepath))

	output_xml = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd"><en-export export-date="20190128T190645Z" application="Evernote" version="Evernote Mac 7.8 (457453)">'

	for note in notes:
		note_html = note.prettify(formatter="html")
		output_xml += note_html

	output_xml += '</en-export>'

	# strip problematic line breaks and whitespace out – breaks evernote import
	output_xml = re.sub(r'\n\s*', '', output_xml)

	# write out to disk
	with open(filepath, 'w', encoding='utf8') as export_file:
		export_file.write(output_xml)


if __name__ == '__main__':
	main()