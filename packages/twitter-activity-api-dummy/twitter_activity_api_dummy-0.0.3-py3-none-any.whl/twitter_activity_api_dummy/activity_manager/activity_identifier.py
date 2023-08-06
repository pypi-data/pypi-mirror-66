from aws_s3_resource.s3_bucket import S3Bucket
from aws_s3_resource.s3_object import S3Object
import pickle as pk
import time
import os
import io

class ActivityIdentifier:
    """ The main purpose of this class is to extract the activity name"""
    basic_activities = ['tweet_delete_events', 'direct_message_mark_read_events',
                    'direct_message_indicate_typing_events']

    type_based_activities = ['follow_events','mute_events','block_events']

    # Conditons to determine who did the event
    by_to_conditions = {
        'by_if_equal': lambda id1, id2: 'by' if id1 == id2 else 'to',
        'to_if_equal': lambda id1, id2: 'to' if id1 == id2 else 'by'
    }

    @classmethod
    def identify_activities(cls, response):
        # Get activities list
        keys_list = response.keys()

        # Get activity name
        activity_name = ActivityIdentifier.get_activity_name(keys_list)

        if activity_name in cls.basic_activities:
            activity = activity_name

        else:
            # If activity depends on type
            if activity_name in cls.type_based_activities:

                # Get activity type
                activity_type = response[f'{activity_name}'][0]['type']

                # Test if the event done by user or to user
                if activity_type == 'follow':
                    follow_to = response['follow_events'][0]['target']['id']
                    user_id = response['for_user_id']
                    res = cls.by_to_conditions['to_if_equal'](user_id, follow_to)
                    activity = f'follow_{res}_user_events'

                # If event is unfollow, mute, unmute, block, or unblock
                else:
                    activity = f'{activity_type}_by_user_events'

            elif activity_name == 'direct_message_events':
                message_by = response["direct_message_events"][0]['message_create']['sender_id']
                user_id = response['for_user_id']
                res = cls.by_to_conditions['by_if_equal'](message_by, user_id)
                activity = f'message_{res}_user_events'

            elif activity_name == 'favorite_events':
                favorite_by = response['favorite_events'][0]['user']['id_str']
                user_id = response['for_user_id']
                res = cls.by_to_conditions['by_if_equal'](favorite_by, user_id)
                activity = f'favorite_{res}_user_events'

            elif activity_name == 'tweet_create_events':
                # Tweet create events maybe tweet (by user), re-tweet(to user,by user) , reply(to user,by user),mention (to user)
                if response['tweet_create_events'][0]['in_reply_to_status_id'] is None:
                   # Recognize the activity is it re-tweet or tweet by user ?
                   # If false it is tweet event
                    if "retweeted_status" in response['tweet_create_events'][0].keys():
                        retweeted_by = response['tweet_create_events'][0]['user']['id_str']
                        user_id = response['for_user_id']

                        res = cls.by_to_conditions['by_if_equal'](retweeted_by, user_id)
                        activity = f'retweet_{res}_user_events'

                    else:
                        activity = activity_name

                else:

                    if response['tweet_create_events'][0]['in_reply_to_user_id_str'] == response['for_user_id']:
                        activity = 'reply_to_user_events'

                    else:
                        if response['tweet_create_events'][0]['user']['id_str'] == response['for_user_id']:
                            activity = 'reply_by_user_events'
                        else:
                            activity = 'mention_to_user_events'

        return activity

    @staticmethod
    def get_activity_name(keys_list):
        for k in keys_list:
            if 'event' in k:
                return k