import requests
from bs4 import BeautifulSoup
import re
from src.common.database import Database
import src.models.items.constants as ItemConstants
import uuid
from src.models.stores.store import Store

class Item():
    def __init__(self, name, url, store_id, price=None, _id=None):
        self.name = name
        self.url = url
        self.store_id = store_id
        store = Store.get_by_id(store_id)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL{}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.get_text().strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "store_id": self.store_id
        }
    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))