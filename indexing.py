# -*- coding: utf-8 -*-
import sys
import jinja2
import codecs
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# Define namespaces dictionary to make ET.find() or ET.findall() more simple
namespace = {'wp':'http://wordpress.org/export/1.2/',
			 'content':'http://purl.org/rss/1.0/modules/content/'}


# loop through every element in the article with the tag wp:postmeta
# and save necessary data to the dictionary
def getMetaData(dict, article):
	for metaObject in article.findall('wp:postmeta', namespace):
		# If the text in the meta_key tag is "production_id" 
		# save the meta_value tag text in our dictionary as "production_id"
		if metaObject.find('wp:meta_key', namespace).text == "production_id":
			dict['production_id'] = metaObject.find('wp:meta_value', namespace).text
		# Otherwise, if the text in the meta_key tag is "hospital_name"
		# save the text of meta_value tag in our dictionary as "affiliation"
		elif metaObject.find('wp:meta_key', namespace).text == "hospital_name":
			dict['affiliation'] = metaObject.find('wp:meta_value', namespace).text
	return dict

# save xml file with specified title that contains `text`
def renderAndSave(text, title):
	templateLoader = jinja2.FileSystemLoader( searchpath="/" )
	templateEnv = jinja2.Environment( loader=templateLoader )
	TEMPLATE_FILE = "/home/russell/Desktop/indexing/JOMI-8.xml"
	template = templateEnv.get_template( TEMPLATE_FILE )
	file = codecs.open('files/' + title + '.xml', 'w', encoding='utf8')
	file.write( text )
	file.close()



# Use ET to define the xml file
tree = ET.ElementTree(file="/home/russell/Desktop/indexing/jomi.wordpress.2015-06-11.xml")
# For each article in the xml file
for elem in tree.iterfind('channel/item'):
	if elem.find('wp:status', namespace).text == 'preprint':
		continue
	# Initialize an empty dictionary that will be appended
	# to hold all of the data that we parse
	data = {}
	# Save the title, link, and pubdate of the article as dictionary entries
	data['title'] = elem.find('title').text
	data['link'] = elem.find('link').text
	data['pubdate'] = elem.find('pubDate').text
	data = getMetaData(data, elem)
	
	# get the author's JoMI username (use findall() if multiple authors exist?)
	author_username = elem.find('category[@domain="author"]').text
	# loop through author listings at beginning of xml doc
	for i in tree.iterfind('channel/wp:author', namespace):
		if i.find('wp:author_login', namespace).text == author_username:
			 data['author'] = i.find('wp:author_display_name', namespace).text

	# content = ET.fromstring( '<?xml version="1.0" encoding="UTF-8" ?>\n' + '<body>\n' + \
	# 		elem.find('content:encoded', namespace).text.encode('utf-8') + '</body>' )	
	# for tag in content.iterfind('h4'):
	# 	print tag.text

	renderAndSave( template.render( data ), data['production_id'] )


# parse the necessary data into a dictionary
	# tough part of this is the actual content
	# thinking about actually switching over to pulling data straight from MySQL
	# the xml file that WordPress generates contains an entire xml doc of formatted
		# text in the contents section
	# Would need to find a way to generate bullet points or numbered lists for 
		# <ul> and <ol> respectively
	# Here's a possible solution I see: filter through the content to get rid 
		# of unwanted sections
	# Feed this data into an xml to plain-text converter
	# Still need to make arrays of titles and corresponding text to feed into the template engine
# render an xml file with the dictionary as the argument
# save file with unique name in specific folder


# Notes: 
# The text for both the Main Text and the Procedure Outline would be appropriate.
# Do not include the citations, comments, disclosures, or statement of consent.
# Each document will need a unique identifier.  In the example, I used
	# “JOMI-“ along with your identifier.  Adding “JOMI-“ before your
	#  article ID will ensure there is no conflict with any other content we index.
# The section headings are not required, but many times they are themselves informative.
# You should provide a URL for linking.