import os
from newsapi import NewsApiClient

api = NewsApiClient(api_key="b01f1c03cbb44b31a1ad0fb98c6eb155")

api.get_top_headlines()

