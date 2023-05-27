import scrapy
from bs4 import BeautifulSoup
import json


class BestSpider(scrapy.Spider):
    name = 'best'
    # allowed_domains = ['bestbuy.com']
    # start_urls = ['http://bestbuy.com/']


    def start_requests(self):
        url = "https://www.bestbuy.com/site/lg-70-class-up7070-series-led-4k-uhd-smart-webos-tv/6452990.p?skuId=6452990"
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
        

        a={"intl_splash":False,
          "CTT":"310edc5fc5b7ed0792c8ce8a4abcc09c",
          "SID":"dfd626e2-2517-4f64-9187-1894ff01e337",
          "_abck":"8DA499868F7F288DDFCD9573C42E95D3~-1~YAAQxQHVFxEYeHCHAQAAdrVFngmF4kidxHF7+ziH+3IrP6Lid+F3/IJIhGhV7WiLuplWH7+HiFhWhBEBg5uxW/eUWjFdif66DkE15PhvoQyhjUI8Glr0qCzNLb5gp5/8mvIhJ+drR6F+4j/k2RSlO4iDXhB4wx5hkQrx5RbPC0WFvqJyUSzr4jqVRKXLaj5H1Q7n0HesQGD7o+yz2ytyboGG6SkpVXLTUIqSfDynZqAlCusUuHvX5gFBbQ/ro9DWFoudjJ4B4y7K7n5PR+i3a990RgJ9Fk5YyoUZihCPeB31V9zwXfhH0vRPxBqnEvVjS6ksZ935Exo5mjROYpts+fC0jL/A3hDPJ4TrZLnDtAi3Eo2dfuDD49aZLNL1hdq+c7q6elVpFn3Lwv53q1RiSr01fi9HYI3vCMLRFOqMrzcQBJ7c18N1e0maPzwQsjlT~0~-1~-1",
            "bby_cbc_lb":"p-browse-e",
            "bby_rdp":"l",
            "bm_sz" :"7B7600251B98A65181450B8ACCDCFE96~YAAQngHVF2BXQnOHAQAAzAQunhNOD5KoRC3x6PWES3N4ZFpTANVf64UyRj4sOfVR8dwWw7Uxm2Pn7LGi1Plt77heUo+Da1fJAyH4FwR5rDI/WyF9RO8ZgZ7A3fx6eMOyZQQLkNyECkQwYVtxic2b2P0E9Xzso5nUHsyf7PCcK7yYMGCPRPoSONgP10ObvlndUA4vh5ByhKvhWVFJwb17HQZzSmd1EzBp05os5WM2orTtDAiYp8J0Ttv947fntQB6VgoeQT95YRJg4Gx+eXxEwgMbGzSKXpteRLsdAKOVRRhIYuIzkN+4o6slc6K2hA+EGZq2wSqVg9Cc6y8KHdIKzYpBXPXvSUW8UPMwfOECkQkOZCIoOxXoHHAFyTgjaWU++qs=~4534838~3289140",
            "ltc":"%20",
            "vt":"f77f32bc-df66-11ed-b597-0a16d1138605"}


        yield scrapy.Request(url,method="GET",headers=headers,cookies=a,callback=self.parse)
       


    def parse(self, response):
        with open("bsc.html","w",encoding="utf-8")as a:
            a.write(response.text)
        name = response.xpath("//div[@class='sku-title']//h1/text()").get()
        model = response.xpath("//div[@class='title-data lv']/descendant::div[2]/span[2]/text()").get()
        SKU = response.xpath("//div[@class='title-data lv']/descendant::div[3]/span[2]/text()").get()
        price = response.xpath("//div[@class='pricing-price'][1]/descendant::div[4]/div/div/div/span[1]/text()").get()
        ratings_reviews_details = response.xpath("//span[@class='c-reviews order-2']/preceding-sibling::span[1]/parent::div/p/text()").get()
        reviews = response.xpath("//span[2][contains(text(),'Reviews')]/text()").get()
        rating = response.xpath("//span[@class='c-reviews order-2']/preceding-sibling::span[1]/text()").get()
        all_images = response.xpath("//div[@class='app-container']//ul[@class='seo-list'][1]/descendant::a/@href").getall()
        description = response.xpath("//span[contains(text(),'Overview')]/following::div[@class='product-description']/text()").get()
        logo = response.xpath("//h3[contains(text(),'Features')]/following-sibling::div/div/ul/li/img/@src").get()
        what_is_include = response.xpath("//h3[contains(text(),'Included')]/parent::div/descendant ::ul/li//text()").getall()        
        energyrating = response.xpath("//span[contains(text(),'Opens a New Window')]/parent::a/text()").get()
        energyrating_link = response.xpath("//span[contains(text(),'Opens a New Window')]/parent::a/@href").get()

        soup = BeautifulSoup(response.text,'html.parser')
        feacture = soup.find('div',{'class':'pdp-utils-product-info'}).text


        content = response.xpath("//script[contains(@id,'shop-specifications-')]/text()").get()
        
        xx = json.loads(content)
        values = []
        dict1= {}
        dict2 ={}
        
        for spec in xx["specifications"]["categories"]:
            try:
                b = spec.get("displayName")
              
                a = spec.get("specifications")
                values = None
                mydict={}
                for i in a:
                    keys = i.get("displayName")
                    if i.get("value"):
                        values = i.get("value")                                            
                        mydict[keys] = values
                dict1[b] = mydict
                
            except:
                values= None  

        reviewscontent =response.xpath("//script[contains(@id,'user-generated-content-ratings-and-reviews')]/text()").get()
        ccc =json.loads(reviewscontent)
        
       
        try :
            stats =ccc["app"]["stats"]
            dict2["average_overall_rating"] = stats.get("averageOverallRating")

        except:
            average_overall_rating = None      

        try :

            dict2["total_review_count"] = ccc["app"]["stats"]["totalReviewCount"]
        except :
            total_review_count = None
        empty2 =[]
        empty=[]
        dict3={}
        for x in ccc["app"]["reviews"]["topics"]:
            try :
                dict2["author"] = x.get("author")
            except:
                author = None

            try :
                dict2["title"] = x.get("title","")
            except:
                title = None

            try:
                dict2["text"] = x.get("text","")
            except :
                text = None
            
            try :
                dict2["time"] = x.get("submissionTime",'')
            except:
                time  =  None 
            
            try :
                dict2["rating"] = x.get("rating")
                
            except:
                rating = None
            empty2.append(dict2)
            


        que_ans_content = response.xpath("//script[contains(@id,'user-generated-content-question-distillation')]/text()").get()
        www =json.loads(que_ans_content) 
        

        for xx in www["app"]["questions"]["results"]:
            try :
                
                dict3["que"] =xx.get("questionTitle")
                
            except:
                que = None 
        
            try :
                dict3["subtime"] = xx.get("submissionTime")
                
            except :
                subtime = None

            try :
                dict3["user_nickname"] = xx.get("userNickname")
                
            except:
                user_nickname = None 
            
            try :
                anw = xx.get("answersForQuestion")                
                dict3["ans"] = anw[0].get("answerText").replace("\n"," ")
                
               
            except :
                aws = None
            empty.append(dict3)
       
        
            
               
        yield{
            "name":name,
            "model":model,
            "SKU" : SKU,
            "rating_reviews_details":ratings_reviews_details,
            "rating":rating,
            "reviews": reviews,
            "price" :price,
            "all_images": all_images,
            "discription" : description,
            "logo" :logo,
            "feacture" : feacture,
            "what_is_include" : what_is_include,
            "energyrating" : energyrating,
            "energyrating_link": energyrating_link,
            "specifications" : dict1,
            "Reviews" :empty2,
            "que_ans" : empty,}
        
            
            
     




        
