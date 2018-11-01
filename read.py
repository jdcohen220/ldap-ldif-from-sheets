from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '1aHthF6_5d-VRRyKst5ygD8S13-xc-K_AEM4Fq20MGHg'
    RANGE_NAME = 'Qlik Sense Users!D397:X397'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()

    data = list(result.values())
    print(data[1])


if __name__ == '__main__':
    main()