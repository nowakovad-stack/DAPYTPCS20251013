'''
This module provides tools for de/encryption of text
'''
import os
import logging
import hashlib
from cryptography.fernet import Fernet

log = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

APPKEY = "cczhfNja6UHUQ6O9Ied5QxS7fhQCSJevB1L6SMg4dzQ="
''' Master "default" key for encryption/decryption operations '''

#========== Fernet symetrical encryption ==============
def encrypt_message(message,key = APPKEY):
    '''
    Encrypt message using Fernet library 
    
    Parameters
    ----------
    message: str
        plain text input
    key: str
        Base64 encoded key (default `APPKEY`)

    Returns
    -------
    str:
        Base64 encoded result of encryption

    Raises
    ------
    Error
        in case of any failure in encryption process
    '''
    try:
        f = Fernet(key)
        message_encoded = message.encode("utf-8")
        encrypted = f.encrypt(message_encoded)
        return encrypted.decode('ascii')
    except:
        log.warning("Unable to encrypt message")#,exc_info=log.isEnabledFor(logging.DEBUG))
        raise


def decrypt_message(message,key = APPKEY):
    '''
    Decrypt message using Fernet library
    
    This method doesn't raise any error => in case of any error original string is returned.
    It enables transparent processing of plain text inputs 
    
    Parameters
    ----------
    message: str
        Base64 encoded encrypted message
    key: str
        Base64 encoded key (default `APPKEY`)

    Returns
    -------
    str:
        result of decryption

    '''
    try:
        f = Fernet(key)
        message_encoded = message.encode("ascii")
        decrypted = f.decrypt(message_encoded)
        return decrypted.decode('utf-8')
    except:
        log.warning("Unable to decrypt message; considering it plain text")#,exc_info=log.isEnabledFor(logging.DEBUG))
        return message


def blake(text):
    ''' generate 'blake2' hash from argument '''
    return hashlib.blake2s(bytes(text,'utf-8')).hexdigest()
    


#################################################################
##  Ochrana před přímým spuštěním souboru
if __name__ == "__main__":
    print(f"!!! Module {os.path.basename(__file__)} is not built for direct execution !!!")
    print("... but in this case one exception: you can update your master security key into this file :-)")
    print("APPKEY =",Fernet.generate_key().decode('ascii'))

