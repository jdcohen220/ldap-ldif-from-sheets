import os
from datetime import datetime
from read import Users
from ldif import LDIF


class Model:

    def __init__(self):
        self.ldif_snippets = {}
        self.users = Users()

    def _generate_ldif_snippets(self):
        for group in self.users.group_roster:
            tmp = LDIF('ldif_template.ldif', group)
            tmp.add_users(self.users.group_roster[group])
            self.ldif_snippets[group] = tmp

    def publish_ldif(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        target_path = './ldif/{date}'.format(date=current_date)
        try:
            os.makedirs(target_path)
        except FileExistsError:
            pass
        for k, v in self.ldif_snippets.items():
            with open('{path}/{group}.ldif'.format(path=target_path,
                                                   group=k), 'w') as f:
                f.write(v.template)


if __name__ == '__main__':
    model = Model()
    model._generate_ldif_snippets()
    model.publish_ldif()

