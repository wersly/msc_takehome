from flask import Flask, render_template, g
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
app.config.from_object("config.Config")

reports = [
    {
        "view": "all_musicians",
        "name": "Name, instrument, and section for all musicians"
    },
    {
        "view": "instruments_without_musicians",
        "name": "Instruments that don't yet have musicians (i.e. no one plays the trumpet), and their sections"
    },
    {
        "view": "multi_instrumentalists",
        "name": "Any musicians that play two or more instruments, their instrument, and section"
    },
    {
        "view": "multiple_players",
        "name": "Any instruments that are played by multiple musicians, as well as the musician names and sections"
    }
]


def get_db(db_file):

    db = getattr(g, "_database", None)

    if db is None:
        conn = g._database = sqlite3.connect(db_file)

    return conn


def process_report_df(df):

    # re-upper case strings
    for column in df:

        if df[column].dtype == "object":
            df[column] = df[column].str.title()

    # convert `None` to empty string
    df = df.fillna(value="")

    return df


@app.route("/")
def index():

    return render_template("index.html", reports=reports)


@app.teardown_appcontext
def close_connection(exception):

    db = getattr(g, "_database", None)

    if db is not None:
        db.close()

    return None


# TODO: how fancy does the output table need to be?
# - Should a header tag (eg h1) be applied to better name the table?
@app.route("/report/<view_name>")
def report(view_name):

    conn = get_db(app.config.get("DB_FILE"))
    query = "select * from {view_name}".format(view_name=view_name)
    df = process_report_df(pd.read_sql(query, conn))
    return df.to_html(index=False)
