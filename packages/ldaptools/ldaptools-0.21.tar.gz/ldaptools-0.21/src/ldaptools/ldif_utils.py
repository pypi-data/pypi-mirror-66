import ldap
import ldif
from ldap.dn import dn2str

from ldaptools.utils import idict, str2dn, str2bytes_entry, bytes2str_entry


class AddError(Exception):
    pass


class ListLDIFParser(ldif.LDIFParser):
    def __init__(self, *args, **kwargs):
        self.entries = []
        ldif.LDIFParser.__init__(self, *args, **kwargs)

    def handle(self, dn, entry):
        dn = str2dn(dn)
        dn = [[(part[0].lower(),) + part[1:] for part in rdn] for rdn in dn]
        dn = dn2str(dn)
        self.entries.append((dn, bytes2str_entry(entry)))

    def add(self, conn):
        for dn, entry in self.entries:
            try:
                conn.add_s(dn, ldap.modlist.addModlist(str2bytes_entry(entry)))
            except Exception as e:
                raise AddError('error when adding %s' % dn, e)

    def __iter__(self):
        for dn, attributes in self.entries:
            yield dn, idict(attributes)
