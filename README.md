## Why does this exist?
[EchoMobile](echomobile.org) provide a great communications platform, but not much in terms of programmatic access. There is [an API](https://www.echomobile.org/docs) but that needs a lot of raw requests to get to working (it's a pain to say the least), so I decided to build this!!


## Pre-requisites
- An [EchoMobile](echomobile.org) account, enterprise or otherwise
- Python 3.6 or higher
- See how to get the user credentials [here](https://www.echomobile.org/docs/authentication)

## Installation
```pip install pyforecho```

## Usage
```python
from pyforecho import EchoMobile
if __name__ == "__main__":
	echo = EchoMobile(acc_id = 12345, eid = 6789, e_passw = "pass")
	echo.test_connection()
	client = echo.clients.lookup(phone = "254718953619")
	for a_client in echo.clients.get_all(since = 1604188800, group_name = "MYGROUP"):
		print(a_client)
```

The more detailed documentation - https://pyforecho.readthedocs.io/en/latest/

## Changelog
### 0.0.5 7th Dec 2020
*Fixed*
- api.clients.create() to include the client's name in the payload

### 0.0.4 7th Dec 2020
*Fixed*
- Exception Handling. Instead of throwing exceptions, bools are returned instead

### 0.0.3 7th Dec 2020
*Added*
- Survey triggering
- Utility to check if client is available for survey
- Updating client custom field
- Custom Exceptions

### 0.0.2 7th Dec 2020
*Added*
- Sending bulk messages

### 0.0.1 23rd Nov 2020
*Released*
- Bare bones version with only the ability to create, lookup and get all contacts