## Friday - Personal Assistant

Optimized for python 3.6

This project is aimed on creating personal assistants for replying messages 
about specifics issues.

------------------------------


### Project's Structure ###

```bash
.
├── data
│   └── dataset.xlsx
├── dependencies
│   └── chromedriver
├── src
│   ├── __init__.py
│   ├── crawler.py
│   └── lang_processing.py
├── src
├── .gitignore
├── README.md
└── requirements.txt
```
----------------

### Modules ###

- __crawler:__ Class responsible for accessing internet.
- __lang_processing:__ Class responsible for processing natural language.

----------------

### Python requirements ###

In your python environment, run the following command:

`pip install requests bs4`

or access the root directory _(~/requirements.txt)_ and run the following command:

`pip install -r requirements.txt`

----------------

### Usage Notes ###

For running the script on terminal/cmd, access the project directory _(./src)_ and run the following command:

`python __init__.py`

_obs: you must be inside the scr directory._

----------------