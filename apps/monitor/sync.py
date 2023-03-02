import shutil
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


from exel import Excel
from board import Board
from timing import Timing
from constants import Constants


class Sync:
    public_file_is_up_to_date = True
    drive_file_is_up_to_date = True
    cloud_credentials = None

    @staticmethod
    def update_drive_files():
        if Sync.drive_file_is_up_to_date:
            return

        if not Timing.check_if_need_to_try_to_update_drive():
            return

        Sync.cloud_authenticate()

        Timing.fix_drive_try_to_update()
        cloud_folder_mime_type = 'application/vnd.google-apps.folder'
        try:
            service = build('drive', 'v3', credentials=Sync.cloud_credentials)

            query = f"name='data.xlsx'"
            response = service.files().list(q=query).execute()
            for file in response['files']:
                service.files().delete(fileId=file['id']).execute()

            query = f"name='{Constants.CLOUD_DATA_DIR}' and mimeType='{cloud_folder_mime_type}'"
            response = service.files().list(q=query, spaces='drive').execute()

            if not response['files']:
                folder_metadata = {
                    'name': Constants.CLOUD_DATA_DIR,
                    'mimeType': cloud_folder_mime_type
                }
                folder = service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = folder.get('id')
            else:
                folder_id = response['files'][0]['id']

            for file_name in os.listdir(Constants.CASH_DIR):
                folder_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(f'{Constants.CASH_DIR}/{file_name}')
                service.files().create(body=folder_metadata,
                                       media_body=media,
                                       fields='id').execute()
            Sync.drive_file_is_up_to_date = True
        except:
            pass

    @staticmethod
    def cloud_authenticate():
        try:
            scopes = ['https://www.googleapis.com/auth/drive']

            if os.path.exists(Constants.CLOUD_TOKEN_PATH):
                Sync.cloud_credentials =\
                    Credentials.from_authorized_user_file(Constants.CLOUD_TOKEN_PATH, scopes)

            if not Sync.cloud_credentials or not Sync.cloud_credentials.valid:
                if Sync.cloud_credentials and\
                        Sync.cloud_credentials.expired and\
                        Sync.cloud_credentials.refresh_token:
                    Sync.cloud_credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        Constants.CLOUD_CREDENTIALS_PATH, scopes)
                    Sync.cloud_credentials = flow.run_local_server(port=0)

                with open(Constants.CLOUD_TOKEN_PATH, 'w') as token:
                    token.write(Sync.cloud_credentials.to_json())
        except Exception as _ex:
            print(f'Error: {_ex}')

    @staticmethod
    def save_measurements_to_storage():
        connected_sensors = Board.get_all_connected_sensors()
        Excel.open(Constants.CASH_FILE_PATH)
        Excel.add_measurements(connected_sensors)
        Excel.save(Constants.CASH_FILE_PATH)
        Sync.public_file_is_up_to_date = False
        Sync.drive_file_is_up_to_date = False

    @staticmethod
    def update_public_data_files():
        if Sync.public_file_is_up_to_date:
            return

        try:
            shutil.copyfile(Constants.CASH_FILE_PATH,
                            Constants.PUBLIC_FILE_PATH)
            Sync.public_file_is_up_to_date = True
        except (OSError, shutil.SameFileError):
            return
