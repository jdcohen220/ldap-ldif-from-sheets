"""
Generate LDIF for new users based on groups
"""

class LDIF:

    def __init__(self, template_path, group):
        self.template_path = template_path
        self.template = self._read_template().format(group=group)


    def _read_template(self):
        with open(self.template_path, 'r') as f:
            template = f.read()
        return template

    def add_users(self, users):
        for user in users:
            user_line = 'uniquemember:        {user_string}'.format(
                user_string=user)
            self.template = '{template}\n{user}'.format(
                template=self.template,
                user=user_line)