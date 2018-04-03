import scrapy

class Data(scrapy.Item):
    cookie = scrapy.Field()

class Login(scrapy.Spider):
    name = 'siakad.poltektedc.ac.id'
    start_urls = ['http://siakad.poltektedc.ac.id/politeknik/mahasiswa.php']

    custom_settings = {
#        'ITEM_PIPELINES' : {'app.MyPipeline': 1}
    }

    def parse(self, response):
        yield {
            #'cookie': str(response.headers.getlist('Set-Cookie')) + str(response["meta"]["id"]),
            'cookie': str(response.meta)
        }
        return scrapy.FormRequest.from_response(
            response,
            formcss='form',
            #formdata={'username': response.meta["id"], 'passwd': response.meta["pass"]},
        #    callback=self.extract
        )



