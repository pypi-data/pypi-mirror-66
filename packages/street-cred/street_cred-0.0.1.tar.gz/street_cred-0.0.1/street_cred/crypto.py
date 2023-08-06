import os

from cryptography.fernet import Fernet, MultiFernet

_fernet = None  # type: Optional[FernetProtocol]


def get_fernet():
    """Get fernet encrypter."""
    global _fernet

    if _fernet:
        return _fernet

    fernet_key = os.getenv('FERNET_KEY')
    if fernet_key:
        _fernet = MultiFernet([
            Fernet(fernet_part.encode('utf-8'))
            for fernet_part in fernet_key.split(',')
        ])
    return _fernet
