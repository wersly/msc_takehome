Note, this project was developed in `Python 3.9.5`. If you are having any issues running this code, please try working within a venv based on `Python 3.9.5`.

# One-time Setup
```
# create a virtual env for this project
python -m venv $(pwd)
```

# Install / Work On This Project
```
# activate virtual env
source bin/activate

# install requirements
pip install -r requirements.txt

# locally install the package
python setup.py develop
```

# Run the App
```
python msc_takehome/main.py
```

# Run the Tests
```
python -m unittest discover
```

# Additional / Useful Packaging Commands
```
# pip freeze, excluding locally developed packages
pip freeze --exclude-editable > requirements.txt

# create a source distribution
python setup.py sdist

# check dist contents
tar --list -f dist/msc_takehome-1.0.0.tar.gz
```

# Instructions
Using any Python web framework (Django, Flask, etc.), and a SQLite database (a file), create a web
application using the three attached files (names.txt, instruments.csv, and name_instrument.csv),
please write code that:

1. Parses and loads the Names into one table, and the Instruments into another table. Note, when commas exist in the
names.txt file, they separate "last, first".  Otherwise, it's "first last".
2. Parses and loads the name_instrument.csv file, and create database-level associations between the Instruments,
and the characters playing those instruments.

Then, using your framework, please create a "homepage" that is a list of links to the following
html reports.

1. A report showing the name, instrument, and section for all musicians.
2. A report showing the instruments that don't yet have musicians (i.e. no one plays the trumpet), and their sections, sorted by section, alphabetically in ascending order.
3. A report showing any musicians that play two or more instruments, their instrument, and section.
4. A report showing any instruments that are played by multiple musicians, as well as the musician names and sections.
