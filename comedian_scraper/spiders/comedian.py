import scrapy
import re

class ComedianScraper(scrapy.Spider):
    name = 'comedians'
    comedian_list = [{
        'total scraped': 0,
        'total youngest': 0,
        'average number of siblings': 0,
    }]

    comedians_wiki_url = 'https://en.wikipedia.org/wiki/List_of_comedians'

    def start_requests(self):
        yield scrapy.Request(url=self.comedians_wiki_url, callback=self.parse_wiki)


    def parse_wiki(self, response):

        # get all div with classname 'div-col'
        divs = response.css('div.div-col')
        # click every link per list item in ul
        for div in divs:
            for a in div.css('li a'):
                yield response.follow(a, callback=self.parse_wiki_bio)

    def parse_wiki_bio(self, response):

        self.comedian_list[0]['total scraped'] += 1

        page = response.css('div#mw-content-text')

        name = response.url.split('/')[-1].replace('_', ' ')
        
        paragraphs = page.css('p')
        for paragraph in paragraphs:
            
            if re.search(r'youngest of', paragraph.get()):
                
                num_siblings_int = re.search(r'the youngest of (\d+)', paragraph.get())
                num_siblings_str = re.search(r'the youngest of (\w+)', paragraph.get())

                if num_siblings_int:
                    num_siblings = int(num_siblings_int.group(1)) - 1

                elif num_siblings_str:  

                    # replace string with number
                    num_siblings = num_siblings_str.group(1).replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace('ten', '10').replace('eleven', '11').replace('twelve', '12')

                    num_siblings = int(num_siblings) - 1
                else:
                    num_siblings = None

                if num_siblings:
                    
                    self.comedian_list[0]['total youngest'] += 1
                    
                    # ignoring html tags
                    text = re.sub('<[^<]+?>', '', paragraph.get())
                    self.comedian_list.append({
                        'name': name,
                        'bio': text,
                        'url': response.url,
                        'num_siblings': num_siblings,
                    })
                break
            