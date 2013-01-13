from django.forms import Form, ChoiceField, IPAddressField, RadioSelect
from django.utils.translation import ugettext as _
from string import Template

def read():
    file = open('/etc/network/interfaces', 'r').readlines()

    ip = ''
    dns = ''
    netmask = ''
    gateway = ''

    if 'iface eth0 inet dhcp' in file:
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
    choices=[
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