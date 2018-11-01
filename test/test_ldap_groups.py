import unittest
from ldap_config import LdapConfig
class TestLdapGroups(unittest.TestCase):

    def testLdapGroups(self):
        groups = LdapConfig()
        self.assertEqual(20, len(groups.groups))