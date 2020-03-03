import subprocess

__author__ = 'Marios Keir'
__date__ = '03-03-2020'


class UserFile:
    def __init__(self):
        self._output = subprocess.check_output(['cat', '/etc/passwd'])
        self._output = str(self._output)[2:-2]
        self._output = self._output.split('\\n')
        self.num_of_users = len(self._output)
        self.users_names = self._clean_user_names()

    def _clean_user_names(self):
        users = set()
        for name in self._output:
            name = name.split(':')[0]
            users.add(name)
        return users

    def get_users(self):
        """returns the number of users avaliale in a linux system"""
        return self.users_names


if __name__ == '__main__':
    user_file = UserFile()
    for name in user_file.get_users():
        print(name)