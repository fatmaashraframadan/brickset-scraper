import scrapy


class BrickSetScraper(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']
    user_agent = "Chrome/22.0.1207.1"
    pages = 1

    def parse(self, response):

        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h1 ::text'
            IMG_SELECTOR = 'img ::attr(src)'
            PIECES_SELECTOR = '//*[@id="body"]/div[2]/div/div/section/article[3]/div[2]/div[4]/dl/dt[1]' #'.//dl[dt/text() = "Pieces"]//dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]//dd[2]/a/text()'

            yield{
                'name' : brickset.css(NAME_SELECTOR).extract_first(),
                'IMG' : brickset.css(IMG_SELECTOR).extract_first(),
                'pieces' : brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs' : brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        self.pages = self.pages +1

        if next_page and self.pages < 5:
            print("##################################################### NEW PAGE #####################################################")
            yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
            )
