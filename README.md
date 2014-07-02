# International Bass Station Flask App 
[![Build Status][build-status-badge]] [build-status]

## Contributing

To get a local copy of the app up and running, first checkout the source;

`git clone https://github.com/beats-to/intbass.git`

Add some music files locally

`mkdir intbass/local/Music && cp ~/*.mp3 intbass/local/Music/`

Install a python virtual environment and the required modules;

```
virtualenv-2.7 intbass
source intbass/bin/activate
pip install -r intbass/requirements-dev.txt
```

Create the initial database

```
python intbass/db_create.py
```

Run the local instance

```
python intbass/run.py
```

Enjoy http://localhost:5000
