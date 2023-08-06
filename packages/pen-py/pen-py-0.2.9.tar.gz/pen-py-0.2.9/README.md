# Penbox Python

**v0.2.7 available**:

```console
pip install pen-py
```

```python
from penpy import DicPlus, Store
```

## Included:

**DicPlus** : A advanced Ordered Dictionnary using . for referecing.

- class DicPlus()
- Includes a following functions:
  - format()
  - mapping()
  - overwrite()
  - clean_json()
  - from_json()
  - pprint()
  - search() : using jmespath syntax : http://jmespath.org/

**Dates** : A light version of dates handling:

- absolute_date() : from ISO-like to datetime
- relative_date() : from timedelta-like string to datetime
- str_to_timedelta() : from timedelta-like string to timedelta
- TimeFrame object : from a simple timeframe json (see below), can check if a date is included, get the closest date within timeframe for a given date or the next available date within timeframe

```python

timeframe = TimeFrame{
    "mon:fri": "8:11-14:15",
    "sat": "10:11"
})

print(timeframe.get_closest(datetime.now()))
print(timeframe.get_next(datetime.now()))

```

**Secure** : A full version that helps to manage authentication, authorization, signature and signature verification

```python

from .secure import *

secure = Secure(
    service="https://notif.pnbx.cc",  # Notify here your service
    keySet=[
        {
            "issuer": "https://notif.pnbx.cc",
            "keys": {
                "kty": "RSA",
                "e": "",
                "use": "sig",
                "alg": "RS256",
                "n": "" },
        },
        {"issuer": "https://penbox.eu.auth0.com/"}
    ],
    auth_makers=[
        {
            "name": "core",
            "type": "auth0",
            "config": {
                "client_id": "",
                "client_secret": "",
                "domain": "penbox.eu.auth0.com",
                "audience": "https://core.penbox.io",
            },
        }
    ],
    auth_checkers=[
        {
            "name": "root",
            "audience": "https://core.penbox.io",
            "issuers": ["https://penbox.eu.auth0.com/"], # just reference issuers from the keySet
        }
    ],
    sign_makers=[
        {
            "name": "root",
            "issuer": "https://notif.pnbx.cc",
            "private_key": {
                "p": "",
                "kty": "RSA",
                "q": "",
                "d": "",
                "e": "AQAB",
                "...": "...",
            },
            "public_key": {
                "kty": "RSA",
                "e": "",
                "use": "sig",
                "alg": "RS256",
                "n": ""
                },
        }
    ],
    sign_checkers=[
        {
            "name": "root",
            "audience": "https://notif.pnbx.cc",
            "issuers": ["https://notif.pnbx.cc"], # just reference issuers from the keySet
        }
    ],
)

```

```python
# anywhere in the code:

from app import secure

# create bearer headers : authenticate to service (token is automatically refreshed if required only):
headers = secure.auth_headers()

# create signature headers with signed body included:
headers = secure.signed_headers(body, "https://notif.pnbx.cc")

# verify signature against issuers (MUST BE IN KEYSET):
@app.route("/test_authorized")
@secure.auth_check("flows:read requests:read")
def test_auth_check():
    return "All right baby"


@app.route("/test_signed")
@secure.sign_check(json_dec=True)
def test_sign_check():
    return "All right baby"

```

**Store** : A light version of ORM using Google Cloud Datastore:

- class Store()
  WARNING : to use the datastore, please make sure you reference your google cloud credentials & project json in the env, or provide the filename and project name in argument:

```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pnbx-rd-xxxxxxxx.json"
# OR
mystore = Store('type', credentials="pnbx-rd-xxxxxxxx.json", project = "myproject")
```

- [ ] Please request the json file of r&d account for testing
