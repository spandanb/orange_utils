"""
Interface for interacting with keys on local system 
such as creating keys, checking fingerprint.
"""
from os import chmod
from os.path import expanduser, isfile
from Crypto.PublicKey import RSA
import hashlib
import base64
import pdb
from utils import create_and_raise

#See: 
#http://stackoverflow.com/questions/2466401
#https://gist.github.com/jtriley/7270594
#http://stackoverflow.com/questions/6682815

def hash_to_fingerprint(seq):
    """returns seq with a colon after every 2 chars
    """
    chunks = (seq[pos:pos + 2] for pos in xrange(0, len(seq), 2))
    return ":".join(chunks)

def check_and_create_privkey(location="~/.ssh/"):
    """
    Creates private key file at `location`
    if one does not exist.
    Supports path with variable expansion
    """
    location = expanduser(location)
    privkey_path= "{}id_rsa".format(location)
    pubkey_path = "{}id_rsa.pub".format(location)

    #file exists, return
    if isfile(privkey_path): return

    key = RSA.generate(2048)
    with open(privkey_path, 'w') as content_file:
        chmod(privkey_path, 0600)
        content_file.write(key.exportKey('PEM'))
    pubkey = key.publickey()
    with open(pubkey_path, 'w') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))

def get_pubkey(location="~/.ssh/id_rsa.pub", strip_hostname=False):
    """
    Gets the contents of the pubkey
    Arguments:-
        location:- location of pub key
    """
    location = expanduser(location)
    with open(location, 'r') as content_file:
        pubkey = content_file.read()
    
    if strip_hostname:
        pubkey = " ".join(pubkey.split(" ")[:2])

    return pubkey

def get_pubkey_fingerprint(hashtype, privkey_path="~/.ssh/id_rsa", pubkey_path="~/.ssh/id_rsa.pub"):
    """
    Gets the fingerprint of the pubkey
    Arguments:-
        hashtype:- [savi | aws] 
        privkey_path:- location of private key
        pubkey_path:- location of public key
    """
    #TODO: why are the following 2 different; both are md5 hashes
    #might be because of hostname
    if hashtype == "aws":
        privkey = RSA.importKey(open(expanduser(privkey_path)))
        pubkey = privkey.publickey()
        md5digest = hashlib.md5(pubkey.exportKey('DER')).hexdigest()

    elif hashtype == "savi":
        with open(expanduser(pubkey_path)) as pubkey_file:
            pubkey = pubkey_file.read()
            pubkey = base64.b64decode(pubkey.split()[1])
            #pubkey = base64.b64decode(pubkey.strip().split()[1].encode('ascii'))
            md5digest = hashlib.md5(pubkey).hexdigest()
    else:
        create_and_raise("InvalidHashTypeException", "hashtype must be 'savi' or 'aws'")
        
    return hash_to_fingerprint(md5digest)



if __name__ == "__main__":
    #check_and_create_privkey()
    pub = get_pubkey()
    print get_pubkey_fingerprint("savi")
    print get_pubkey_fingerprint("aws")


