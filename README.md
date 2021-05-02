## Friday: Female Replacement Intelligent Digital Assistant Youth

<small>_Optimized for python 3.8+_</small>

This project is aimed on creating a telegram personal assistant for replying
 messages and automating daily tasks by using specific ```commands```.

------------------------------

### Project's Structure

```bash
.
└── friday
    ├── data
    │   └── a.png
    ├── docs
    │   └── CREDITS
    ├── src
    │   ├── cnn
    │   │   ├── CNN.model
    │   │   │   └── saved_model.pb
    │   │   ├── data
    │   │   │   ├── non-wawaweewa
    │   │   │   └── wawaweewa
    │   │   ├── __init__.py
    │   │   ├── helpers.py
    │   │   ├── vega_fitting.py
    │   │   └── vega_preditcting.py
    │   ├── settings
    │   │   └── settings.json
    │   ├── __init__.py
    │   ├── settings.json
    │   └── telegram_replier.py
    ├── tests
    │   └── unittests
    │   └── __init__.py
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```
----------------

#### Directory description

- __data:__ The data dir. Group of non-script support files.
- __docs:__ The documentation dir.
- __src:__ The scripts & source code dir.
- __tests:__ The unittests dir.

----------------

## Usage Notes

Section aimed on clarifying some running issues.

### Running

For running it, at the `~/src` directory just run:

```shell script
python telegram_replier.py
``` 

or, if importing it as a module, just run:
````python
from friday import message_handler

if __name__ == '__main__':
    message_handler('args', 'kwargs')
````

### Settings

- ``telegram_settings.json``:
````json
{
  "token": "541233:A12JASBN12JASIJDW12321KN"
}
````

- `gcp_settings.json`
````json
{
  "type": "service_account",
  "project_id": "sdnasjdn923",
  "private_key_id": "2193undasidhuh1287ebdu2he2e",
  "private_key": "-----BEGIN PRIVATE KEY-----\n",
  "client_email": "wawaweewa@wawaweewa-545459.iam.gserviceaccount.com",
  "client_id": "65649498411548484",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/"
}
````

- `maps_settings.json`
````json
{
  "api_key": "AIzaSyDx2RCq2og6zp5aYbnProvMjCWletM03B0"
}
````

- `ps_settings.json`
````json
{
  "consumer": {
    "consumer_key": "n2133n21j3nj12ndnasjnd",
    "consumer_secret": "3u21h3unbdsajndsajnd821n2jndcawsdwd21e12"
  },
  "application": {
    "key": "knduh12873bd217ge721db217eg271d217ge81db218",
    "secret": "d12b217gd821gdu2b128ge8gdu9128dy"
  }
}
````

- `punch_a_clock.json`
````json
{
  "cpf": "64454554845",
  "token": "948484545488454554"
}
````

---------------
