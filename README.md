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
	client = echo.clients.get_client(phone = "254718953619")
	for a_client in echo.clients.get_all(since = 1604188800, group_name = "MYGROUP"):
		print(a_client)
```

The more detailed documentation - 