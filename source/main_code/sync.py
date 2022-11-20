import shutil
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from exel import Excel
from board import Board
import constant


class Sync:
    public_file_is_up_to_date = True
    cloud_credentials = None

    @staticmethod
    def cloud_authenticate():
        scopes = ['https://www.googleapis.com/auth/drive']

        if os.path.exists(constant.CLOUD_TOKEN_PATH):
            Sync.cloud_credentials =\
                Credentials.from_authorized_user_file(constant.CLOUD_TOKEN_PATH, scopes)

        if not Sync.cloud_credentials or not Sync.cloud_credentials.valid:
            if Sync.cloud_credentials and\
                    Sync.cloud_credentials.expired and\
                    Sync.cloud_credentials.refresh_token:
                Sync.cloud_credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    constant.CLOUD_CREDENTIALS_PATH, scopes)
                Sync.cloud_credentials = flow.run_local_server(port=0)

            with open(constant.CLOUD_TOKEN_PATH, 'w') as token:
                token.write(Sync.cloud_credentials.to_json())

    @staticmethod
    def upload_files_in_dir_to_cloud(dir_path):
        cloud_folder_mime_type = 'application/vnd.google-apps.folder'
        try:
            service = build('drive', 'v3', credentials=Sync.cloud_credentials)

            query = f"name='{constant.CLOUD_DATA_DIR}' and mimeType='{cloud_folder_mime_type}'"
            response = service.files().list(q=query, spaces='drive').execute()

            if not response['files']:
                folder_metadata = {
                    'name': constant.CLOUD_DATA_DIR,
                    'mimeType': cloud_folder_mime_type
                }
                folder = service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = folder.get('id')
            else:
                folder_id = response['files'][0]['id']

            for file_name in os.listdir(dir_path):
                folder_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(f'{dir_path}/{file_name}')
                service.files().create(body=folder_metadata,
                                       media_body=media,
                                       fields='id').execute()
                print(f'Backed up file {file_name}')
        except HttpError as e:
            print(f'Error: {e}')

    @staticmethod
    def save_measurements_to_storage():
        connected_sensors = Board.get_all_connected_sensors()
        Excel.open(constant.WORKING_FILE_PATH)
        Excel.add_measurements(connected_sensors)
        Excel.save(constant.WORKING_FILE_PATH)
        Sync.public_file_is_up_to_date = False

    @staticmethod
    def update_public_data_file():
        if Sync.public_file_is_up_to_date:
            return

        try:
            shutil.copyfile(constant.WORKING_FILE_PATH, constant.PUBLIC_FILE_PATH)
            Sync.public_file_is_up_to_date = True
        except:
            return
