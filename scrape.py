from lxml import html
import requests
from bs4 import BeautifulSoup
import json
from api_sync import WP_API_Sync
import re
from sarkari_result import SarkariResult
from urllib.parse import urlparse
import traceback, pickle, os

GLOB_DATA = dict()

class EGScraper:

	"""docstring for EGScraper"""
	def __init__( self ):
		self.wpapi = WP_API_Sync()

	def traverse_sr_attributes( self ):
		attributes = [ 
			( "Result", "http://www.sarkariresult.com/result.php" ),
			( "Admit_Card", "https://www.sarkariresult.com/admitcard.php" ),
			( "Latest_Jobs", "https://www.sarkariresult.com/latestjob.php" )
		]

		for attribute, link in attributes:
			if not attribute or attribute == "" or not link or link == "":
				continue
			attribute = attribute.replace( "_", " " )
			if attribute == "" or not attribute:
				continue

			# Set global data to cache links 
			# with current attribute if not set yet
			if attribute not in GLOB_DATA:
				GLOB_DATA[attribute] = []

			self.scrape_sarkari_result( attribute.strip(), link )
			# break

	def scrape_sarkari_result( self, attr, link ):
		if not attr or attr == "" or not link or link == "":
			return
		page = requests.get( link )
		tree = page.content

		soup 		= BeautifulSoup( tree, 'lxml' )
		results 	= soup.find( "div", { "id" : "post" } ).find_all( 'ul' )
		link_count 	= 0 
		for li in  results :
			if not li:
				continue

			linkAnchor 		= li.find_all( 'a' )[1]['href'].strip()
			if not linkAnchor or linkAnchor == '':
				continue

			parsed_uri 	= urlparse(linkAnchor)
			domain 		= '{uri.netloc}'.format(uri=parsed_uri)
			if 'sarkariresult' not in domain:
				continue

			linkAnchor = self.clean_html_tags_and_attrs( linkAnchor )
			if not linkAnchor or linkAnchor == '':
				continue
			
			if GLOB_DATA[attr] and linkAnchor in GLOB_DATA[attr]:
				print( '================> Locally Skipped' )
				continue

			print( linkAnchor )
			link_status = self.wpapi.is_cached( linkAnchor, attr )
			if link_status and link_status == 'category_no_found':
				data = {
					"categories" 	: [ attr ],
					"link_to_check"	: linkAnchor
				}
				self.wpapi.update_post( data )
				continue
			elif link_status and link_status != 'category_no_found':
				print( "======================> Skipped" )
				continue

			result_detail 	= requests.get( linkAnchor )
			if result_detail.status_code == 404:
				continue

			# Update link's cache
			GLOB_DATA[attr].append( linkAnchor )

			response_json 	= self.extract_and_post_details( result_detail.content, linkAnchor, attr )
			# break

	def clean_html_tags_and_attrs( self, link_str ):
		if not link_str or link_str == '':
			return link_str
		
		regex = re.compile(
	        r'^(?:http|ftp)s?://' # http:// or https://
	        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
	        r'localhost|' #localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?' # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		if re.match( regex, link_str ):
			return link_str

		cleanr = re.compile( '<.*?>' )
		cleantext = re.sub( cleanr, '', link_str )
		cleantext = cleantext.split( '.php' )
		if cleantext[0] and cleantext[0] != '':
			link_str = cleantext[0] + ".php"

		return link_str

	def extract_and_post_details( self, result_detail, linkAnchor, category ):
		sr_ob = SarkariResult( linkAnchor )
		detail_soup = sr_ob.filter_extracted_content( BeautifulSoup( result_detail, 'html5lib' ), category )
		self.wpapi.create_new_post( detail_soup );

	def direct_call_to_source( self, link ):
		result_detail 	= requests.get( link )
		if result_detail.status_code == 404:
			return
		response_json 	= self.extract_and_post_details( result_detail.content, link, "Admit Card" )

if __name__ == "__main__":
	try:
		if os.path.exists('GLOB_DATA.dat') and os.path.getsize( 'GLOB_DATA.dat' ) > 0:
			with open('GLOB_DATA.dat', 'rb') as f:
				GLOB_DATA = pickle.load(f)
		egscraper = EGScraper()
		egscraper.traverse_sr_attributes()
		# egscraper.direct_call_to_source( "http://sarkariresult.net/page/andhrabankpo.php" )
	finally:
		with open('error.log', 'a') as f:
			f.write(traceback.format_exc())
		with open('GLOB_DATA.dat', 'wb') as f:
			pickle.dump(GLOB_DATA, f)
