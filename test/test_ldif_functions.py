import unittest
from ldif import LDIF

class TestLdif(unittest.TestCase):

    def setUp(self):
        self.LDIF = LDIF(template_path='../src/ldif_template.ldif', group='TEST GROUP')
        self.expected_template = \
'''dn: cn=TEST GROUP,ou=servicegroups,dc=redhat,dc=com
changetype: modify
add: uniquemember'''
        self.expected_add = \
'''dn: cn=TEST GROUP,ou=servicegroups,dc=redhat,dc=com
changetype: modify
add: uniquemember
uniquemember:        test1
uniquemember:        test2'''


    def test_ldif(self):
        self.assertEqual(self.LDIF.template, self.expected_template)

    def test_add_users(self):
        users = ['test1', 'test2']
        self.LDIF.add_users(users)
        self.assertEqual(self.LDIF.template, self.expected_add)


