import os
import io
import pickle as pk
from abc import ABCMeta, abstractmethod
from .twitter_account import TwitterAccountProxy
import random 
import json
import threading
from datetime import datetime
from aws_s3_resource.s3_bucket_error import NumberRandomCharsException, NumberCharsBucketNameException
from aws_s3_resource.s3_bucket import S3Bucket
from aws_s3_resource.s3_object import S3Object
import time



class TwitterBot:
    def __init__(self,  bot_crediential_file,
        strategy_time_interval_range, action_time_interval_range,
        strategy_class, strategy_params,bucket_name):
    
        self.bot_account = TwitterAccountProxy(bot_crediential_file)
        self.strategy_time_interval = random.randint(*strategy_time_interval_range)
        self.action_time_interval = random.randint(*action_time_interval_range)
        self.strategy_class = strategy_class
        self.strategy_params = strategy_params
        self.bucket_name= bucket_name
        
    
    def go(self):
        strategy = self.strategy_class(**self.strategy_params)
        try:
            actions = strategy.start()
            for action in actions:
                # Do action
                self.bot_account.do(action)
                time.sleep(self.action_time_interval * 60)

        except Exception as e:
            bucket_name = self.bucket_name
            object_key = 'errors.pkl'
            errors = list()
            if S3Object.is_available(bucket_name, object_key):
                logg_bytes = S3Object.download(bucket_name, object_key)
                with io.BytesIO(logg_bytes) as f:
                    errors = pk.load(f)

            errors.append({'time': str(datetime.now()), 'error_message': str(e)})

            data_bytes = pk.dumps(errors)

            file_dict = {
                    'file_name': object_key,
                    'file_bytes': data_bytes
                }

            S3Object.upload(bucket_name, file_dict, with_random_prefix=False)

        threading.Timer(self.strategy_time_interval * 3600 , self.go).start()

        