"""
  ALL available actions that could be taken by a user, this list will be used while  naming pickle
  files
"""

available_activities = ['tweet_delete_events',
                    'direct_message_mark_read_events',
                    'direct_message_indicate_typing_events',
                    'retweet_to_user_events',
                    'retweet_by_user_events',
                    'tweet_create_events',
                    'reply_to_user_events',
                    'reply_by_user_events',
                    'mention_to_user_events',
                    'message_to_user_events',
                    'message_by_user_events',
                    'follow_to_user_events',
                    'follow_by_user_events',
                    'unfollow_by_user_events',
                    'block_by_user_events',
                    'unblock_by_user_events',
                    'mute_by_user_events',
                    'unmute_by_user_events',
                    'favorite_to_user_events',
                    'favorite_by_user_events']