'''
Copyright (C) 2013 Rasmus Eneman <rasmus@eneman.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from string import Template

from django.forms import Form, ChoiceField, IPAddressField, RadioSelect
from django.utils.translation import ugettext as _


def read():
    file = open('/etc/network/interfaces', 'r').readlines()

    ip = ''
    dns = ''
    netmask = ''
    gateway = ''

    if 'iface eth0 inet dhcp\n' in file:
        type = 'dhcp'
    else:
        type = 'static'
        for line in file:
            if line.startswith('address'):
                ip = line.split(' ')[1]
            elif line.startswith('dns-nameservers'):
                dns = line.split(' ')[1]
            elif line.startswith('netmask'):
                netmask = line.split(' ')[1]
            elif line.startswith('gateway'):
                gateway = line.split(' ')[1]

    return type, ip, dns, netmask, gateway


def set_dhcp():
    dynamic = 'auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n'
    file = open('/etc/network/interfaces', 'w')
    file.write(dynamic)
    file.close()


def set_static(ip, dns, netmask, gateway):
    parts = ip.split('.')
    network = '%s.%s.%s.0' % (parts[0], parts[1], parts[2])

    tpl = Template('''auto lo
    iface lo inet loopback

    auto eth0
    iface eth0 inet static
    address $ip
    network $network
    dns-nameservers $dns
    netmask $netmask
    gateway $gateway
    ''')
    static = tpl.safe_substitute(ip=ip, network=network, dns=dns, netmask=netmask, gateway=gateway)

    file = open('/etc/network/interfaces', 'w')
    file.write(static)
    file.close()


class NetworkForm(Form):
    choices = [
        ('dhcp', _('DHCP')),
        ('static', _('Static')),
    ]
    type = ChoiceField(choices=choices, widget=RadioSelect)
    ip = IPAddressField()
    dns = IPAddressField()
    netmask = IPAddressField()
    gateway = IPAddressField()

    def __init__(self, *args, **kwargs):
        super(NetworkForm, self).__init__(*args, **kwargs)
        type, ip, dns, netmask, gateway = read()
        self.fields['type'].initial = type

    def save(self):
        if self.cleaned_data['type'] == 'static':
            set_static(
                self.cleaned_data['ip'],
                self.cleaned_data['dns'],
                self.cleaned_data['netmask'],
                self.cleaned_data['gateway'],
            )
        else:
            set_dhcp()