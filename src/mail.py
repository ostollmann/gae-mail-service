from email.utils import parseaddr
from string import *

class EmailAddress(object):
    
    rfc822_specials = '()<>@,;:\\"[]'

    def __init__(self, address, real_name=''):
        if EmailAddress.is_valid(address):
            self.address = address
        else:
            raise ValueError('invalid email address')

        self.real_name = real_name
    
    def __repr__(self):
        if not self.real_name:
            return self.address
        else:
            return '%s <%s>' % (self.real_name, self.address)

    @staticmethod
    def from_string(address_str):
        parsed = parseaddr(address_str)
        return EmailAddress(parsed[1], parsed[0])

    # Email validation taken from:
    # http://www.secureprogramming.com/?action=view&feature=recipes&recipeid=1
    @staticmethod
    def is_valid(addr):
        # First we validate the name portion (name@domain)
        c = 0
        while c < len(addr):
            if addr[c] == '"' and (not c or addr[c - 1] == '.' or addr[c - 1] == '"'):
                c = c + 1
                while c < len(addr):
                    if addr[c] == '"': break
                    if addr[c] == '\\' and addr[c + 1] == ' ':
                        c = c + 2
                        continue
                    if ord(addr[c]) < 32 or ord(addr[c]) >= 127: return False
                    c = c + 1
                else: return False
                if addr[c] == '@': break
                if addr[c] != '.': return False
                c = c + 1
                continue
            if addr[c] == '@': break
            if ord(addr[c]) <= 32 or ord(addr[c]) >= 127: return False
            if addr[c] in EmailAddress.rfc822_specials: return False
            c = c + 1
        if not c or addr[c - 1] == '.': return False

        # Next we validate the domain portion (name@domain)
        domain = c = c + 1
        if domain >= len(addr): return False
        count = 0
        while c < len(addr):
            if addr[c] == '.':
                if c == domain or addr[c - 1] == '.': return False
                count = count + 1
            if ord(addr[c]) <= 32 or ord(addr[c]) >= 127: return False
            if addr[c] in EmailAddress.rfc822_specials: return False
            c = c + 1

        return count >= 1    

