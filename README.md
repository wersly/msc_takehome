# One-time Setup
```
# create a virtual env for this project
python -m venv $(pwd)
```

# Work On This Project
```
# activate virtual env
source bin/activate

# install requirements
pip install -r requirements.txt
```

# Run the App
```
python msc_takehome/main.py
```

# Run the Tests
```
python -m unittest discover
```

# Packaging
```
# pip freeze, excluding locally developed packages
pip freeze --exclude-editable > requirements.txt

# create package
python setup.py sdist

# check package contents
tar --list -f dist/msc_takehome-1.0.0.tar.gz

# register package for local use and development
python setup.py develop
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
