# Copyright © 2020 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module xxx provides xxx."""

import json
import urllib.request

from jose import jwt

AUTH0_KEYS = []
AUTH0_DOMAIN = 'thermalcloudservices-dev-ci.auth0.com'
AUTH0_CLIENT_ID = 'J2HDSG7KFuAoaj54phD6cPbaGb14CQat'


def init():
    '''Initializes auth0 authentication.'''

    global AUTH0_KEYS  # pylint: disable=global-statement
    jsonurl = urllib.request.urlopen('https://' + AUTH0_DOMAIN +
                                     '/.well-known/jwks.json')
    auth0_jwks = json.loads(jsonurl.read())
    AUTH0_KEYS = [{
        'kty': key['kty'],
        'kid': key['kid'],
        'use': key['use'],
        'n': key['n'],
        'e': key['e']
    } for key in auth0_jwks["keys"]]
