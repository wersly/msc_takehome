from etl import db_setup
from routes import app
import os


if __name__ == '__main__':

    db_setup(app.config.get("DB_FILE"))
    app.run()
