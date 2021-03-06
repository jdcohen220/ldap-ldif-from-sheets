from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from ldap_config import LdapConfig

# Constants
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1aHthF6_5d-VRRyKst5ygD8S13-xc-K_AEM4Fq20MGHg'
TABLE_RANGE = 'D2:Z1000'

def get_row_from_sheet(sheetname, range):
    """
    Uses the Google Sheets API to return a row of data from the spreadsheet
    :return: a single row of data as a dictionary result object
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    range_string= '{sheet}!{range}'.format(sheet=sheetname, range=range)
    return service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=range_string).execute()


def _parse_memberships(row):
    return row['values'][0][:-1]


def _parse_ldap_distinguished_name(result):
    return result['values'][0][-1]


def match_groups(result_row, groups_list):
    """
    Matches membership denoted by an X to the corresponding group.
    :param result_row: A single user row
    :param groups_list: The list of LDAP groups
    :return: a list of groups filtered to those a user is a member of.
    """
    zipped = dict(zip(groups_list, result_row))
    return [x for x, y in zipped.items() if y != '']


def _get_entire_spreadsheet(sheetname):
    return get_row_from_sheet(sheetname, TABLE_RANGE)

def _get_new_users(entire_sheet_values):
    new_user_rows  = []
    for row in entire_sheet_values:
        if row[21] == '':
            new_user_rows.append(row)
    return new_user_rows


class Users:
    def __init__(self):
        # result_row = get_row_from_sheet('Qlik Sense Users', 'D397:X397')
        self._groups_list = LdapConfig().groups
        entire_sheet = _get_entire_spreadsheet('Qlik Sense Users')
        self._raw_data = _get_new_users(entire_sheet['values'])
        self._user_table = self._generate_user_table()
        self.group_roster = self._generate_group_roster()

    def _generate_user_table(self):
        return {row[20]: match_groups(row, self._groups_list)
                for row in self._raw_data}

    def _generate_group_roster(self):
        group_roster = {}
        group_roster_filtered = {}
        for group in self._groups_list:
            group_roster[group] = [k for k, v in self._user_table.items()
                                   if group in v]
            group_roster_filtered = {k: v for k, v in group_roster.items()
                                     if v}
        return group_roster_filtered


if __name__ == '__main__':
    users = Users()
    print(users.group_roster)


