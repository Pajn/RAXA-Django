import subprocess
import urllib
import xml.etree.ElementTree as ET
from RAXA.settings import UPDATE_URL

class Update():

    def __init__(self, version, patch):
        if isinstance('version', str):
            version = version.split('.')
            version = (
                int(version[0]),
                int(version[1]),
                int(version[2])
                )

        self.version = version
        self.patch = patch

    def apply(self):
        patch = urllib.urlopen(self.patch).read()

        f = open('update.patch', 'w')
        f.write(patch)
        f.close()

        p = subprocess.Popen('patch -p1 < update.patch ', shell = True)
        p.wait()
        print p.stdout
        print p.stderr

        if p.returncode == 0:
            import update
            return update.run()
        else:
            return False

def version():
    from version import __version_info__

    return __version_info__

def write_version(version):
    return '.'.join(map(str, version))

def check():
    xml = urllib.urlopen(UPDATE_URL).read()
    updates = ET.fromstring(xml)

    latest_update = None

    for update in updates.findall('update'):
        required_version = update.find('required_version').text
        required_version = required_version.split('.')
        required_version = (
            int(required_version[0]),
            int(required_version[1]),
            int(required_version[2])
            )

        if version() >= required_version:
            latest_update = update
            break

    if latest_update is not None:
        update = Update(
            latest_update.find('version').text,
            latest_update.find('patch_url').text,
        )
        return True, update

    else:
        return False, None