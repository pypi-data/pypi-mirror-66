# Sage Pay lib

> **Note:** This library still refers to netcash. I'll update all references to NetCash in the future

A simple library for interacting with Sage Pay SOAP services

## Installation

```
pip install python-netcash
```

## Usage

The preferred way to interact with the repo is using docker.

### Quick commands:

**Run the tests**

> Warning: These are integration tests and will hit the netcash endpoints

```bash
docker-compose up
```

- See: `tests.py` for example code

You must provide the following environment variables in `env.dev` (you can copy `env.example` and put your values in):

NETCASH_MERCHANT_ACCOUNT=...
NETCASH_SOFTWARE_VENDOR_KEY=...

You customer will provide:

NETCASH_SERVICE_ID=...
NETCASH_SERVICE_KEY=...

## Integration requirements

In order to integrate with Netcash, you will be required to implement the following functionality:

**Tip:** You can get an interactive shell with:

```
docker-compose run --rm netcash ipython
```

### Setup the client

```python
# get environment variables into constants:
from netcash.client import Netcash
import os

NETCASH_MERCHANT_ACCOUNT = os.environ.get("NETCASH_MERCHANT_ACCOUNT")
NETCASH_SOFTWARE_VENDOR_KEY = os.environ.get("NETCASH_SOFTWARE_VENDOR_KEY")

service_id = ...
service_key = ...

netcash = Netcash(NETCASH_MERCHANT_ACCOUNT, NETCASH_SOFTWARE_VENDOR_KEY)
```

### Validate service key

```python
# returns a boolean True if valid account. Otherwise False
netcash.validate_service_key(service_id, service_key)
```

### Request and retrieve merchant statement

```python
# request a statement:

# this is just for readability:
from datetime import date, timedelta

from_date = date.today() - timedelta(days=7) # get the last week's worth of transactions

polling_id = netcash.request_merchant_statement(
    from_date=from_date, service_key=service_key,
)
res = netcash.retrieve_merchant_statement(
    polling_id, service_key=service_key, as_csv_reader=True
)
for row in res.rows:
    print(row)

>> ['2020-04-14', 'OBL', '0', 'Opening Balance', '0.0000', '+', '0', '', '', '']
>> ['2020-04-14', 'CBL', '0', 'Closing Balance', '0.0000', '+', '0']
```

## Paynow

Creating a form to initiate a PayNow request:

```html
<form method="POST"
    action="https://paynow.netcash.co.za/site/paynow.aspx" target="_top">
  <input type="hidden" name="M1" value="..">  <!--- YOUR PAY NOW SERVICE KEY GOES IN HERE --->
  <input type="hidden" name="M2" value="..">  <!--- SOFTWARE VENDOR KEY GOES IN HERE --->
  <input type="hidden" name="P2" value="">  <!--- TRANSACTION_ID --->
  <input type="hidden" name="P3" value="">  <!--- TRANSACTION DESCRIPTION --->
  <input type="hidden" name="P4" value="">  <!--- TRANSACTION AMOUNT --->

  <!--- ARBITARY FIELDS FOR STORING ANY INFORMATION YOU MIGHT NEED (E.G.: REFERENCES ETC) --->
  <input type="hidden" name="M4" value="">
  <input type="hidden" name="M5" value="">
  <input type="hidden" name="M6" value="">

  <input type="hidden" name="M9" value=""> <!--- CARDHOLDER EMAIL --->
  <input type="hidden" name="M11" value=""> <!--- CARDHOLDER MOBILE NUMBER --->

  <input type="hidden" name="Budget" value="Y">  <!--- REQUIRED, MUST BE Y --->
</form>
```

* Documentation on all the fields can be found [here](https://api.netcash.co.za/integration/Inbound%20Payments/paynow_gateway#post-to-the-pay-now-page)
* [Logos and press kit](https://netcash.co.za/logo-download-centre/)

## Contributing

This library is pretty simple. To add support for a new web method do:

1. Add a payload to `sagepay/payloads.py`
2. Add a method to wrap request in `sagepay/client.py`
