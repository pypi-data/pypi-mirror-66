from aws_s3_resource.s3_bucket import S3Bucket
from aws_s3_resource.s3_object import S3Object
from .activity_identifier import ActivityIdentifier
from .resources import available_activities
import pickle as pk
import os
import io
import time

class SaveToS3:
    """
            This class have to main functions :
            1- initialize the storing medium (s3 bucket) in case that it does not exist
            2- save the activity:
             - call the activity identifier to determine the activity name
             - save it on its correct file
    """

    def  __init__(self, bucket_name):
        self.bucket_name = bucket_name

    @staticmethod
    def initialize_s3_storing_medium(bucket_name = None):
        if not S3Bucket.is_available(bucket_name):

            # Create a Bucket
            S3Bucket.create(bucket_name)
            for activity in available_activities:
                loggs = list()

                # Save empty list to each action log
                file_dict = {
                            'file_name': f'{activity}.pkl',
                            'file_bytes': pk.dumps(loggs) }

                S3Object.upload(bucket_name, file_dict, with_random_prefix=False)

    def save_activity(self,response):

        identified_activity = ActivityIdentifier().identify_activities(response= response)
        object_key  = f'{identified_activity}.pkl'
        logg_bytes = S3Object.download(self.bucket_name, object_key)

        with io.BytesIO(logg_bytes) as f:
            loggs = pk.load(f)

        saved_event = {f'{identified_activity}' : response}

        # Add current action to log
        saved_event['timestamp'] = int(time.time())
        loggs.append(saved_event)

        data_bytes = pk.dumps(loggs)

        file_dict = {
            'file_name': object_key,
            'file_bytes': data_bytes
        }

        S3Object.upload(self.bucket_name, file_dict, with_random_prefix=False)
        return f'successful {identified_activity}'

