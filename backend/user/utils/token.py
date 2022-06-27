import secrets

def Token():
    return secrets.token_urlsafe(16)