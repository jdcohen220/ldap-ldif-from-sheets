from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from ldap_config import LdapConfig


SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1aHthF6_5d-VRRyKst5ygD8S13-xc-K_AEM4Fq20MGHg'


def get_row_from_sheet(sheetname, range):
    """
    Uses the Google Sheets API to return a row of data from the spreadsheet
    :return: a single row of data as a dictionary result object
    """
    store = file.Storage('src/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('src/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    range_string= '{sheet}!{range}'.format(sheet=sheetname, range=range)
    return service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=range_string).execute()


def _parse_memberships(row):
    """
    Grab the membership indicators from a single result row
    :param row:
    :return: a list of strings, x's indicate group membership.
    """
    return row['values'][0][:-1]


def _parse_ldap_distinguished_name(result):
    return result['values'][0][-1]


def match_groups(result_row, groups_list):
    zipped = dict(zip(groups_list, result_row))
    return [x for x, y in zipped.items() if y != '']


if __name__ == '__main__':
    result_row = get_row_from_sheet('Qlik Sense Users', 'D397:X397')
    groups = LdapConfig().groups
    print(match_groups(result_row, groups))


