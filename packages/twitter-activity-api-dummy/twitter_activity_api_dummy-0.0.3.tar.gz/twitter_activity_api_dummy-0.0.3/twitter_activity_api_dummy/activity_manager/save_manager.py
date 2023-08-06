from .save_to_s3 import SaveToS3
from .save_to_folder import SaveToFolder
import os


class SaveManager:
    """ This class works on :
         1- determine the storing medium and call the setup function depends on that at the first of running the app.
        2- call the correct save function to process and save the activity

    """


    def __init__(self, storing_medium='local', events_folder=os.getcwd(), bucket_name=None):

        self.storing_medium = storing_medium

        if self.storing_medium == 'local':
            self.events_folder = events_folder
            SaveToFolder.initialize_local_storing_medium(events_folder=events_folder)
            self.save_medium = SaveToFolder(self.events_folder)

        elif self.storing_medium == 's3':
            self.bucket_name = bucket_name
            SaveToS3.initialize_s3_storing_medium(bucket_name=bucket_name)
            self.save_medium = SaveToS3(self.bucket_name)






