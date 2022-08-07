import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from csv import writer
from pprint import pprint


def funct():
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '1bxdwMoqJ2xYycESOtmwiTFqg6Rvxhw8gBr2P0wMYY30'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:C10000',
        majorDimension='ROWS'
    ).execute()
    with open("clients_and_emails.csv") as f:
        s = sum(1 for line in f)
    l = len(values['values'][1:])
    if os.stat("clients_and_emails.csv").st_size == 0:
        df = pd.DataFrame(values['values'])
        df.drop(0, inplace=True, axis=0)
        false_column = [False] * len(df[0])
        df[3] = false_column
        df.to_csv('clients_and_emails.csv', header=False, index=False)
        print(df)
    elif len(values['values'][1:]) > s:
        new_df = (values['values'][s + 1:])
        with open('clients_and_emails.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            for i in new_df:
                i.append('False')
                writer_object.writerow(i)

