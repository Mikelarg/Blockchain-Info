import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib
from blockchain import blockexplorer

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def generate_keys():
    private_key = generate_private_key()
    public_key = private_key_to_public_key(private_key)
    address = key_to_addr(private_key)
    return private_key, public_key, address


def generate_private_key():
    return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string()


def key_to_addr(s):
    return pub_key_to_addr(private_key_to_public_key(s))


def pub_key_to_addr(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(s.decode('hex')).digest())
    return base58_check_encode(0, ripemd160.digest())


def private_key_to_public_key(s):
    sk = ecdsa.SigningKey.from_string(s, curve=ecdsa.SECP256k1)
    return ('\04' + sk.verifying_key.to_string()).encode('hex')


def private_key_to_wif(key_hex):
    return base58_check_encode(0x80, key_hex.decode('hex'))


def base58_check_encode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leading_zeros = count_leading_chars(result, '\0')
    return '1' * leading_zeros + base58encode(base256decode(result))


def count_leading_chars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count


def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result


def base58encode(n):
    result = ''
    while n > 0:
        result = B58[n % 58] + result
        n /= 58
    return result
