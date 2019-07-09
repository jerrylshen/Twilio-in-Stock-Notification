from urllib.request import urlopen
import bs4
import requests
import send_sms

class ProductScraper:
	
	def __init__(self):
		#boolean to see if sold out or not
		self.sold_out = True
	
	def _check_product_availabilty(self):
		base_url = "https://www.holotaco.com/products/holo-taco-launch-collection"
		
		open_page = requests.get(base_url)
		soup = bs4.BeautifulSoup(open_page.content, "html.parser")
		
		
		table = soup.find('div', attrs = {'class': 'price'})
		search_term = '<span class="price-item price-item--regular" data-regular-price="">'
		
		#boolean set to True when found first instance of the above html tag line
		bool_set = False
		
		table = table.prettify().split('\n')
		#print(type(table), len(table))
		
		for term in table:
			term = term.strip(" ").strip("\t")
			
			try:
				if term == search_term:
					bool_set = True
					continue
			except:
				continue
				
			#once found the html tag line, this statement will go through
			if bool_set:
				if term != "Sold out":
					send_sms.send_alert()
					self.sold_out = False
					
				
	def output_result(self):
		self._check_product_availabilty();
		return self.sold_out


if __name__ == "__main__":
	ps = ProductScraper()
	output = ps.output_result()
	
	#print(output)
