import subprocess

__author__ = 'Marios Keri'


class Ipv4:
    """Ipv4 object that works on the output of 'lsof -i 4'"""
    def __init__(self):
        """cleans the output returned by 'lsof -i 4'"""
        try:
            self._output = subprocess.check_output(['lsof', '-i', '4'])
        except Exception:
            assert Exception

        self._dirty = self._output.split(b'\n')
        self._clean = []
        self.connections = set()
        self.connected_to = set()
        self.connection_type = set()
        self.internal_ips = set()
        self.commands = set()

        for i in self._dirty:
            self._clean.append(str(i).replace(' ', ','))

        self._clean.remove(self._clean[0])
        self._clean.remove(self._clean[-1])

        for i in self._clean:
            e = i.split(',')
            self.commands.add(e[0][1: ])
            if len(e[-3:]) == 3:
                self.connections.add(e[-3:-1][1])
                self.connection_type.add(e[-3:-1][0])

        self._extract_external_ip()

    def _extract_external_ip(self):
        for con in self.connections:
            if '->' in con:
                internal = con.split('->')[0]
                external = con.split('->')[1]
                self.internal_ips.add(internal)
                self.connected_to.add(external)

    def get_internal_ip(self) -> set:
        """return internal ip where the device is connected"""
        return self.internal_ips

    def get_external_ip(self) -> set:
        """returns the external ip connected to the device"""
        ips = set()
        for i in self.connected_to:
            ips.add(i.split(':')[0])
        return ips

    def get_connection_type(self) -> set:
        """returns the type of connection"""
        return self.connection_type

    def get_connections(self) -> set:
        """returns the internet connections of a linux device"""
        return self.connections

    def get_users(self) -> set:
        """returns names of the command connected to internet"""
        return self.commands


class Nslookup:
    """Look up a given ip address"""
    def __init__(self, ip):
        try:
            self._output = subprocess.check_output(['nslookup', f'{ip.strip()}'])
        except subprocess.CalledProcessError:
            assert ValueError

        self._output = str(self._output)
        self._output = self._output[1: ]
        self._output = self._output.replace('\\t', '')
        self._output = self._output.split('\\n')
        self.organized = {}

        for x in self._output:
            if len(x.split(':')) == 2:
                k, v = x.split(':')
                self.organized[k] = v

    def get_name(self) -> str:
        """ip translated in name"""
        return self.organized['Name']

    def get_server(self) -> str:
        return self.organized['Server']

    def get_address(self) -> str:
        """return ipv4 address"""
        return self.organized['Address']

# TEST
if __name__ == '__main__':

    my_connections = Ipv4()
    connected = my_connections.get_external_ip()
    users = my_connections.get_users()

    # prints out where your linux machine is coneccted
    print('CONNECTED TO ')
    for ip in connected:
        try:
            ns = Nslookup(ip)
            print(ns.get_address(), '  ', ns.get_name())
        except Exception:
            pass

    # prints out which commands are coneccted to internet
    print()
    print('# USERS')
    for command in my_connections.get_users():
        print(command)