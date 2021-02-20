## Friday - Personal Assistant

<small>_Optimized for python 3.6+_</small>

This project is aimed on creating a telegram personal assistant for replying
 messages and automating daily tasks by using specific ```/commands```.

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
from telegram_replier import message_handler

if __name__ == '__main__':
    message_handler('args', 'kwargs')
````

### JSON structure

````json
{
  "token": "A12JASBN12JASIJDW12321KN"
}
````

_obs: in order to run this application you must have a json file at 
`~/src/settings.json`. This json must follow the structure above._

---------------
