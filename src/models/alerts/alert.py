import datetime
from src.common.database import Database
from src.models.items.item import Item
import smtplib
import pytz
from email.message import EmailMessage
import os

__author__ = 'victor cheng'

import uuid
import requests
import src.models.alerts.constants as AlertConstants

class Alert():
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.active = active
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        time_now = utc_now.astimezone(pytz.timezone("America/Chicago"))
        self.last_checked = time_now if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        
    # define the string representation
    def __repr__(self):
        return "<Alert for {} on item {} with price limit{}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):

        email = EmailMessage()
        email['Subject'] = '[Pricing Service] Price Limit Reached!'
        email['From'] = 'pricing.alert.service@gmail.com'
        email['To'] = self.user_email
        content = 'The price for your item: {} has reached your price limit: {}. To nagvigate to your item, please click this URL: {}'.format(
            self.item.name, self.price_limit, self.item.url
        )
        email.set_content(content)
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('pricing.alert.service@gmail.com', os.environ.get('EMAIL_PW'))
        s.send_message(email)
        s.quit()


    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        time_now = utc_now.astimezone(pytz.timezone("America/Chicago"))
        last_updated_limit = time_now - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit},
                                                       "active": True
                                                       })]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):

        self.item.load_price()
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        time_now = utc_now.astimezone(pytz.timezone("America/Chicago"))
        self.last_checked = time_now
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {"_id": self._id})

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_email":user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))