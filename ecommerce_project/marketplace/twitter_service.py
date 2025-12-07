# Twitter integration for auto-tweeting new stores and products

import json
from requests_oauthlib import OAuth1Session
from django.conf import settings


class TwitterService:
    _instance = None
    
    CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
    CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')
    ACCESS_TOKEN = getattr(settings, 'TWITTER_ACCESS_TOKEN', '')
    ACCESS_TOKEN_SECRET = getattr(settings, 'TWITTER_ACCESS_TOKEN_SECRET', '')
    
    def __new__(cls):
        if cls._instance is None:
            print('Initializing Twitter service...')
            cls._instance = super(TwitterService, cls).__new__(cls)
            cls._instance.oauth = None
            cls._instance._setup_oauth()
        return cls._instance
    
    def _setup_oauth(self):
        if not all([self.CONSUMER_KEY, self.CONSUMER_SECRET, 
                   self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET]):
            print("Warning: Twitter credentials not configured. Tweets will not be sent.")
            return
        
        self.oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=self.ACCESS_TOKEN,
            resource_owner_secret=self.ACCESS_TOKEN_SECRET,
        )
        print("Twitter authentication complete.")
    
    def tweet_new_store(self, store):
        if not self.oauth:
            return False
        
        try:
            tweet_text = f"🏪 New Store: {store.name}\n"
            if store.description:
                desc = store.description[:180]
                if len(store.description) > 180:
                    desc += "..."
                tweet_text += f"{desc}\n"
            tweet_text += f"#eCommerce #NewStore"
            
            response = self.oauth.post(
                "https://api.twitter.com/1.1/statuses/update.json",
                data={"status": tweet_text},
            )
            
            if response.status_code == 200:
                print(f"Tweeted about store: {store.name}")
                return True
            else:
                print(f"Tweet failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error tweeting about store {store.name}: {e}")
            return False
    
    def tweet_new_product(self, product):
        if not self.oauth:
            return False
        
        try:
            tweet_text = f"🆕 New Product!\n"
            tweet_text += f"🏪 {product.store.name}\n"
            tweet_text += f"📦 {product.name}\n"
            
            if product.description:
                desc = product.description[:120]
                if len(product.description) > 120:
                    desc += "..."
                tweet_text += f"{desc}\n"
            
            tweet_text += f"💰 R{product.price}\n"
            tweet_text += f"#eCommerce #NewProduct"
            
            response = self.oauth.post(
                "https://api.twitter.com/1.1/statuses/update.json",
                data={"status": tweet_text},
            )
            
            if response.status_code == 200:
                print(f"Tweeted about product: {product.name}")
                return True
            else:
                print(f"Tweet failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error tweeting about product {product.name}: {e}")
            return False


twitter_service = TwitterService()
