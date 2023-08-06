try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from ldaptools.ldif_utils import ListLDIFParser


def test_ldifparser():
    parser = ListLDIFParser(StringIO('''dn: o=orga
objectClass: organization
jpegPhoto:: E+o9UYDeUDNblBzchRD/1+2HMdI=

'''))
    parser.parse()
    assert len(list(parser)) == 1
    assert list(parser)[0][0] == 'o=orga'
    assert list(parser)[0][1]['objectClass'] == ['organization']
    assert list(parser)[0][1]['jpegPhoto']
