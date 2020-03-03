import subprocess

__author__ = 'Marios Keri'


class Ipv4:
    def __init__(self):
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

        for i in self._dirty:
            self._clean.append(str(i).replace(' ', ','))

        self._clean.remove(self._clean[0])
        self._clean.remove(self._clean[-1])

        for i in self._clean:
            e = i.split(',')
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

    def get_internal_ip(self):
        return(self.internal_ips)

    def get_external_ip(self):
        ips = set()
        for i in self.connected_to:
            ips.add(i.split(':')[0])
        return ips

    def get_connection_type(self):
        return(self.connection_type)

    def get_connections(self):
        return(self.connections)


class Nslookup:
    def __init__(self, ip):
        try:
            self._output = subprocess.check_output(['nslookup', f'{ip.strip()}'])
        except subprocess.CalledProcessError:
            assert ValueError

        self._output = str(self._output)
        self._output = self._output[1: ]
        self._output = self._output.replace('\\t', '')
        self._output = self._output.split('\\n')
        self._organized = {}

        for x in self._output:
            if len(x.split(':')) == 2:
                k, v = x.split(':')
                self._organized[k] = v

    def get_name(self):
        return self._organized['Name']

    def get_server(self):
        return self._organized['Server']

    def get_address(self):
        return self._organized['Address']


if __name__ == '__main__':
    my_connections = Ipv4()
    connected = my_connections.get_external_ip()

    for ip in connected:
        try:
            ns = Nslookup(ip)
            print(ns.get_address(), '  ', ns.get_name())
        except Exception:
            pass


