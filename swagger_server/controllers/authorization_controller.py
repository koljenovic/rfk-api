from typing import List
from connexion.exceptions import OAuthProblem
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
''.join([secrets.choice(string.ascii_letters + string.digits) for _ in range(50)])
"""
def check_ReadKey(api_key, required_scopes):
    if api_key == 'ggbTbze1HH9V5WHdctgcA8PKvnE1htlxWyczGHOgQHYHEpO13X':
        return {'uid': 200}

    raise OAuthProblem('Invalid ReadKey supplied.')

def check_WriteKey(api_key, required_scopes):
    if api_key == '1L7g6eq0LXil2xzoEv7CnwvglwWEu9PNgA2vgulNhAZR5HD1MM':
        return {'uid': 100}

    raise OAuthProblem('Invalid WriteKey supplied.')

