__author__ = 'Tim MacDonald'
# Copyright 2019 Timothy MacDonald
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

# This is the built-in CredentialsDB class for sumologictoolbox. It has the following specifications:
#
# 1. argon2 for main password hashing
# 2. AES 256 (GCM) for encrypt/decrypt of credentials
# 3. PBKDF2HMAC using SHA3_512 to create encryption/decryption hashes (500,000 iterations using a 64 byte random salt)
# 4. salts are generated randomly per set of credentials every time they are saved/updated in the database
#
# FAQ:
#
# Q: I see a flaw in this class. Can I send feedback?
# A: Please do! I have done my utmost to do this in the most secure fashion possible but any constructive feedback is
#    welcomed! Please read the rest of the FAQ first though before sending feedback.
#    You can send feedback to: tmacdonald@sumologic.com
#
# Q: What is Argon2? I've never heard of it!
# A: At the time of writing argon2 was the recommended password hashing algoritm by the password hashing competition
#    https://password-hashing.net/
#
# Q: I have my own keystore, can I use that instead?
# A: Yes! I have attempted to write sumologictoolbox in such a way that you can implement your own version of this class
#    that calls or implements a different keystore. To this end I have done the following:
#
#    1. Sumologictoolbox will pass a username as well as a password if one is set in the sumologictoolbox ini file
#    2. You can turn off the "create cred database" button in sumologictoolbox with the appropriate setting in the
#       sumologictoolbox ini file. This will leave only the load button to be used in connecting to the external
#       credential store
#    3. Sumologictoolbox will only activate the "create preset", 'update preset', and 'delete preset' buttons if the
#       "add_cred", "update_cred", and "delete_cred" methods exist in this class. This means you can implement a
#       read-only version of this class that authenticates against an external credential store. I've added comments
#       to each method marking them as "required", "optional", and "internal". You only need to implement the
#       "required" methods for a read-only keystore.
#
# Q: Why are you storing the salt in the open? Doesn't that make it worthless?
# A: The salt is stored in "plain" text with the encrypted data as they must be used for decryption. This is an accepted
#    practice. For more information on why that is the case I suggest the following reading:
#    https://crackstation.net/hashing-security.htm
#
# Q: Can I turn all of this off? I don't want my users using your/any credential store.
# A: Yes! You can turn it off in the Sumotoolbox ini file.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary
import argon2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import sys

class CredentialsDB:

    # We're gonna be using SQLAlchemy's ability to declare database tables as python objects
    # both database classes will inherit from this class
    Base = declarative_base()

    class SumoCredentials(Base):

        __tablename__ = 'sumocredentials'
        id = Column(Integer, primary_key=True)
        name = Column(String(1024), nullable=False, unique=True)
        # the following are all "LargeBinary" type because the encryption cipher returns byte objects, not strings
        # and it's way easier to store them as such rather than converting them back into strings for storage
        sumoregion = Column(LargeBinary, nullable=False)
        accesskeyid = Column(LargeBinary, nullable=False)
        accesskey = Column(LargeBinary, nullable=False)
        salt = Column(LargeBinary, nullable=False)
        nonce = Column(LargeBinary, nullable=False)

        def __repr__(self):
            return f"SumoCredentials('{self.name}')"

    class MainPassword(Base):
        __tablename__ = 'mainpassword'
        id = Column(Integer, primary_key=True)
        hashed_password = Column(String(1024), nullable=False)

    # passing create_new=True will create a new db file, otherwise the object is initialized and the password is
    # tested. An Exception is raised if the password doesn't match.
    # required method - sumologictoolbox needs this to function properly (Duh!)
    def __init__(self, password, username=None, create_new=False):

        # number of iterations that PBKDF2HMAC uses to create the hash used for access key encrypt/decrypt
        # 500,000 seems to be a decent number that exceeds most recommendations but doesn't impact usability too much
        # the larger the better though, so if you don't mind waiting a bit longer for each encrypt/decrypt call
        # by all means increase it.
        self.iterations = 500000
        # we'll be encoding/decoding strings later so lets get the default encoding for the python interpreter
        # it's probably utf-8 but no harm in checking.
        self.system_encoding = sys.getdefaultencoding()
        self.engine = create_engine('sqlite:///credentials.db')
        if create_new:
            self.Base.metadata.create_all(self.engine)

        self.Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        if create_new:
            hash = self.__hash_password(password)
            new_entry = self.MainPassword(hashed_password=hash)
            self.session.add(new_entry)
            self.session.commit()

        result = self.session.query(self.MainPassword).one()
        if self.__validate_password(password, result.hashed_password):
            self.password = password.encode(self.system_encoding)
        else:
            raise Exception('Bad Password')

    # internal method
    def __hash_password(self, password):
        ph = argon2.PasswordHasher()
        hashed_password = ph.hash(password)
        return hashed_password

    # internal method
    def __validate_password(self, password, hash):
        ph = argon2.PasswordHasher()
        return ph.verify(hash, password)

    # all method params should be strings
    # internal method
    def __encrypt(self, name, sumoregion, accesskeyid, accesskey):
        # generate a salt for hash creation, which we pass back to be stored alongside the encrypted data
        # it'll be needed for decryption later
        salt = os.urandom(64)
        # generate a hash from that salt. self.iterations is set in __init__
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        # here's our encryption key
        key = kdf.derive(self.password)
        print(sys.getsizeof(key))
        # we also need to generate a random initialization vector
        nonce = os.urandom(12)
        cipher = AESGCM(key)
        # the cipher requires bytes, not strings, so we're doing some encoding here
        encrypted_sumoregion = cipher.encrypt(nonce, base64.urlsafe_b64encode(sumoregion.encode(self.system_encoding)), None)
        encrypted_accesskeyid = cipher.encrypt(nonce, base64.urlsafe_b64encode(accesskeyid.encode(self.system_encoding)), None)
        encrypted_accesskey = cipher.encrypt(nonce, base64.urlsafe_b64encode(accesskey.encode(self.system_encoding)), None)

        # we return byte objects, not strings
        data = {'name': name,
                'encrypted_sumoregion': encrypted_sumoregion,
                'encrypted_accesskeyid': encrypted_accesskeyid,
                'encrypted_accesskey': encrypted_accesskey,
                'salt': salt,
                'nonce': nonce
                }
        return data

    # all method params should be byte objects except for name, which should be a string
    # internal method
    def __decrypt(self, salt, nonce, name, encrypted_sumoregion, encrypted_accesskeyid, encrypted_accesskey):
        # generate a hash from the salt we were sent to be used in decryption
        # self.iterations is set in __init__
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        # here's our encryption key
        key = kdf.derive(self.password)
        cipher = AESGCM(key)
        # these are returned as byte objects
        sumoregion = cipher.decrypt(nonce, encrypted_sumoregion, None)
        accesskeyid = cipher.decrypt(nonce, encrypted_accesskeyid, None)
        accesskey = cipher.decrypt(nonce, encrypted_accesskey, None)
        # This method should always return strings, so we have to decode the results from the cypher
        data = {'name': name,
                'sumoregion': base64.urlsafe_b64decode(sumoregion).decode(self.system_encoding),
                'accesskeyid': base64.urlsafe_b64decode(accesskeyid).decode(self.system_encoding),
                'accesskey': base64.urlsafe_b64decode(accesskey).decode(self.system_encoding)
                }
        return data

    # write new credentials to the credential store
    # optional method - if this doesn't exist sumologictoolbox will disable the UI buttons associated with
    # adding creds to the cred store
    def add_creds(self, name, sumoregion, accesskeyid, accesskey):
        # encrpt that data
        encrypted_dict = self.__encrypt(name, sumoregion, accesskeyid, accesskey)
        # write to database
        new_cred_entry = self.SumoCredentials(name=encrypted_dict['name'],
                                              sumoregion=encrypted_dict['encrypted_sumoregion'],
                                              accesskeyid=encrypted_dict['encrypted_accesskeyid'],
                                              accesskey=encrypted_dict['encrypted_accesskey'],
                                              salt=encrypted_dict['salt'],
                                              nonce=encrypted_dict['nonce'])
        self.session.add(new_cred_entry)
        # don't forget to commit the write!
        self.session.commit()

    # retrieve unencrypted credentials from the credential store
    # required method - sumologictoolbox needs this to function properly
    def get_creds(self, name):
        # read them from the store
        encrypted_creds = self.session.query(self.SumoCredentials).filter(self.SumoCredentials.name == name).one()
        # decrypt them
        creds = self.__decrypt(encrypted_creds.salt,
                               encrypted_creds.nonce,
                               name,
                               encrypted_creds.sumoregion,
                               encrypted_creds.accesskeyid,
                               encrypted_creds.accesskey
                               )
        return creds

    # return a list of names (identifiers) that can be used to retrieve credentials later
    # required method - sumologictoolbox needs this to function properly
    def list_names(self):
        creds = self.session.query(self.SumoCredentials).all()
        names = []
        for cred in creds:
            names.append(cred.name)
        return names

    # check if a name (identifier) already exists in the credential store
    # required method- sumologictoolbox needs this to function properly
    def name_exists(self, name):
        results = self.session.query(self.SumoCredentials).filter(self.SumoCredentials.name == name).all()
        if results:
            return True
        else:
            return False

    # optional method - if this doesn't exist sumologictoolbox will disable the UI buttons associated with
    # deleting creds from the cred store
    def delete_creds(self, name):
        status = self.session.query(self.SumoCredentials).filter(self.SumoCredentials.name == name).delete()
        if status:
            self.session.commit()
        return status

    # optional method - if this doesn't exist sumologictoolbox will disable the UI buttons associated with
    # writing updated creds to the cred store
    def update_creds(self, name, sumoregion, accesskeyid, accesskey):
        encrypted_dict = self.__encrypt(name, sumoregion, accesskeyid, accesskey)
        update_dict = {
            self.SumoCredentials.sumoregion: encrypted_dict['encrypted_sumoregion'],
            self.SumoCredentials.accesskeyid: encrypted_dict['encrypted_accesskeyid'],
            self.SumoCredentials.accesskey: encrypted_dict['encrypted_accesskey'],
            self.SumoCredentials.salt: encrypted_dict['salt'],
            self.SumoCredentials.nonce: encrypted_dict['nonce']
        }
        status = self.session.query(self.SumoCredentials).filter(self.SumoCredentials.name == name).update(
            update_dict,
            synchronize_session = 'fetch'
        )
        print(status)
        if status:
            self.session.commit()
        return status


