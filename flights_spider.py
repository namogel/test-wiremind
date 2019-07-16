import scrapy
from scrapy.http import Request
from random import choice
from datetime import datetime


USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15',
]
VERIFICATION_TOKEN = 'BkcahKOfyCxQ-4ZxaIeJiNKHJGVDGdkT8a6LaBPY07Sn04FiMV7NzfNm47xIjPR_qDwwxEIZJNawX5aOwYAlLxawD6nfVXkNOAMzYxOBYrw1'


def parse_date(date):
    return datetime.strptime(date, '%Y-%m-%d')


class QuotesSpider(scrapy.Spider):
    name = 'transavia_flights'

    def __init__(self, *args, start, end, distil_cookies, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_date = parse_date(start)
        self.end_date = parse_date(end)
        self.distil_cookies = distil_cookies

    def start_requests(self):
        query_params = {
            '__RequestVerificationToken': VERIFICATION_TOKEN,
            'routeSelection.DepartureStation': 'ORY',
            'routeSelection.ArrivalStation': 'AMS',
            'dateSelection.OutboundDate.Day': self.end_date.day,
            'dateSelection.OutboundDate.Month': self.end_date.month,
            'dateSelection.OutboundDate.Year': self.end_date.year,
            'dateSelection.IsReturnFlight': True,
            'dateSelection.InboundDate.Day': self.start_date.day,
            'dateSelection.InboundDate.Month': self.start_date.month,
            'dateSelection.InboundDate.Year': self.start_date.year,
            'selectPassengersCount.AdultCount': 1,
            'selectPassengersCount.ChildCount': 0,
            'selectPassengersCount.InfantCount': 0,
            'flyingBlueSearch.FlyingBlueSearch': False,
        }
        url = '{}?{}'.format(
            'https://www.transavia.com/fr-FR/reservez-un-vol/vols/rechercher/',
            '&'.join('{}={}'.format(key, value) for key, value in query_params.items())
        )
        headers = {
            'connection': 'close',
            'accept-encoding': 'gzip',
            'accept': '*/*',
            'user-agent': choice(USER_AGENTS)
        }

        yield Request(url, headers=headers, cookies=self.distil_cookies)

    def parse(self, response):
        prices = response.css('ol.days .day-with-availability').get()
        print(prices)
