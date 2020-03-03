import subprocess

__author__ = 'Marios Keri'


class Ipv4:
    def __init__(self):
        self._output = subprocess.check_output(['lsof', '-i', '4'])
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
        return(self.connected_to)

    def get_connection_type(self):
        return(self.connection_type)

    def get_connections(self):
        return(self.connections)


if __name__ == '__main__':
    ip = Ipv4()
    print('Type of connections           ', ip.get_connection_type())
    print('Internal->External connections', ip.get_connections())
    print('External ip                   ', ip.get_external_ip())
    print('Internal ip                   ', ip.get_internal_ip())
