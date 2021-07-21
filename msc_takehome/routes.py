from flask import Flask, render_template, g
import pandas as pd
import sqlite3


app = Flask(__name__)
app.config.from_object("config.Config")


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

    # convert database col names to human friendly
    df = df.rename(
        mapper=lambda col: col.replace("_", " ").title(),
        axis="columns"
    )

    return df


@app.teardown_appcontext
def close_connection(exception):

    db = getattr(g, "_database", None)

    if db is not None:
        db.close()

    return None


@app.route("/")
def index():

    return render_template("index.html", reports=app.config.get("REPORTS"))


@app.route("/report/<view_name>")
def report(view_name):

    conn = get_db(app.config.get("DB_FILE"))
    query = "select * from {view_name}".format(view_name=view_name)
    df = process_report_df(pd.read_sql(query, conn))
    name = list(filter(lambda x: x["view"] == view_name, app.config.get("REPORTS")))[0]["name"]

    return render_template(
        "report.html",
        content=df.to_html(index=False),
        name=name
    )
