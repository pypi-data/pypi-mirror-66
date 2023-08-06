from .activity_identifier import ActivityIdentifier
from .resources import available_activities
import pickle as pk
import os


class SaveToFolder:

    """
        This class have tow main functions :
        1- initialize the storing medium (local folder) in case that it does not exist
        2- save the activity:
         - call the activity identifier to determine the activity name
         - save it on its correct file
    """

    def  __init__(self, events_folder ):
        self.events_folder = events_folder

    @staticmethod
    def initialize_local_storing_medium(events_folder = None):
        if not os.path.exists(events_folder):
            os.mkdir(events_folder)
            for activity in available_activities:
                loggs = list()
                with open(os.path.join(events_folder, f'{activity}.pkl'), 'wb') as f:
                    pk.dump(loggs, f)

    def save_activity(self,response):
        identified_activity = ActivityIdentifier().identify_activities(response=response)

        with open(os.path.join(self.events_folder, f'{identified_activity}.pkl'), 'rb') as f:
            events = pk.load(f)

        events.append(response)

        with open(os.path.join(self.events_folder, f'{identified_activity}.pkl'), 'wb') as f:
            pk.dump(events, f)

        return f'successful {identified_activity}'
