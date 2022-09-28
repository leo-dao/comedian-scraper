from itemadapter import ItemAdapter
import json

class ComedianScraperPipeline:
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        
        # get average number of siblings
        for comedian in spider.comedian_list:
            if comedian.get('num_siblings'):
                spider.comedian_list[0]['average number of siblings'] += comedian['num_siblings']
        
        spider.comedian_list[0]['average number of siblings'] = spider.comedian_list[0]['average number of siblings'] / spider.comedian_list[0]['total youngest']
        
        spider.comedian_list[0]['average number of siblings'] = round(spider.comedian_list[0]['average number of siblings'], 2)

        
        with open('youngest_comedian.json', 'w') as f:
            json.dump(spider.comedian_list, f)