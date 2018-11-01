import unittest
from read import match_groups, _get_entire_spreadsheet

class LogicTests(unittest.TestCase):

    def setUp(self):

        self.sample_input_row = ['', 'x', '', '', '', 'x', '', 'x', '', '', '', 'x', '', '', '', '', '', '', '', '']

        self.groups = ['QLIKSENSE_MARKETING_USERS',
        'QLIKSENSE_MARKETING_LOGINS',
        'QLIKSENSE_MARKETING_ADMINS',
        'QLIKSENSE_MARKETING_DEV',
        'QLIKSENSE_MARKETING_ALL_STREAMS',
        'QLIKVIEW_MKTG_GEO_ALL',
        'QLIKVIEW_GEO_APAC',
        'QLIKVIEW_GEO_EMEA',
        'QLIKVIEW_GEO_LATAM',
        'QLIKVIEW_GEO_NACOMM',
        'QLIKVIEW_GEO_NAPS',
        'QLIKSENSE_ABM',
        'QLIKSENSE_GEO_APAC_DEV',
        'QLIKSENSE_GEO_APAC_DEV_STREAM',
        'QLIKSENSE_GEO_EMEA_DEV',
        'QLIKSENSE_GEO_EMEA_DEV_STREAM',
        'QLIKSENSE_GEO_LATAM_DEV',
        'QLIKSENSE_GEO_LATAM_DEV_STREAM',
        'QLIKSENSE_GEO_NA_DEV',
        'QLIKSENSE_GEO_NA_DEV_STREAM']

    def test_match_groups(self):
        matched_groups = match_groups(self.sample_input_row, self.groups)
        expected = ['QLIKSENSE_MARKETING_LOGINS',
                    'QLIKVIEW_MKTG_GEO_ALL',
                    'QLIKVIEW_GEO_EMEA',
                    'QLIKSENSE_ABM']
        self.assertEqual(sorted(expected), sorted(matched_groups))



