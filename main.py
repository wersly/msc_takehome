from etl import db_setup
from routes import app
import os

# QUESTIONS
# - can file paths be hardcoded? or should they be passed in from the env or designated in a config file?
# - any HTML/CSS fanciness required? Or are HTML tables good enough?
# - All Musicians Report: What to do when a musician is listed multiple times (because they play more than one instrument)
#    - should I leave it as is? Or should the musicians' instruments and sections be STRING_AGG'ed?
# - All Musicians Report: what to do with people who are not assigned instruments/sections? Should they be surfaced?
# - Multi-Instrumentalists Report: same as above. Should instruments and sections be string-agged by name?
# - Multiple Players Report: reverse of the above - should names be aggregated?
# TODO: integration tests for your queries


if __name__ == '__main__':

    db_setup(app.config.get("DB_FILE"))
    app.run()
