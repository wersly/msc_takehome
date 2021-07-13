import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import re
from routes import app
import os


def create_db_file(db_file):

    db_file_path = Path(db_file)

    # if db already exists, make a backup of the former db and create a new one
    if db_file_path.exists():

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        db_file_path.rename("{}.{}.bak".format(db_file, now))

    db_file_path.touch()


def get_db_connection(db_file):

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor


def run_sql_script(conn, cursor, sql_file):

    with open(sql_file, 'r') as f:
        sql = f.read()

    cursor.executescript(sql)
    conn.commit()

    return conn, cursor


def expand_name_fn(df, name_col=None):

    first_last = re.compile("^\w+ \w+$")  # eg "George Washington"
    first_middle_last = re.compile("^\w+ [\w.]+ \w+$")  # eg "John Quincy Adams" OR "John Q. Adams"
    first_only = re.compile("^\w+$")  # assumes a single, non-abbreviated name as the first name; eg "Prince"
    last_first = re.compile("^\w+, [\w.]+$")  # eg "Obama, Barack". Would also accept "Obama, B.", though this doesn't occur in our input set
    last_first_middle = re.compile("^\w+, [\w.]+ [\w.]+$")  # eg "Bush, George W.", or "Bush, G. Walker", or even "Bush, G. W."

    if re.match(first_last, df[name_col]):
        f, l = [x.strip() for x in df[name_col].split(" ")]
        # return (f, l, None)
        # return (f, None, l)
        df["first_name"], df["last_name"] = [f, l]

    elif re.match(first_middle_last, df[name_col]):
        f, m, l = [x.strip() for x in df[name_col].split(" ")]
        # return (f, m, l)
        df["first_name"], df["middle_name"], df["last_name"] = [f, m, l]

    elif re.match(first_only, df[name_col]):
        f = df[name_col].strip()
        # return (f, None, None)
        df["first_name"] = f

    elif re.match(last_first, df[name_col]):
        l, f = [x.strip() for x in df[name_col].split(",")]
        # return (f, l, None)
        # return (f, None, l)
        df["first_name"], df["last_name"] = [f, l]

    elif re.match(last_first_middle, df[name_col]):
        l, x = [x.strip() for x in df[name_col].split(",")]
        f, m = [y.strip() for y in x.split(" ")]
        # return (f, m, l)
        df["first_name"], df["middle_name"], df["last_name"] = [f, m, l]

    return df


def pre_process_df(df):

    for column in df:

        # lowercase all string columns
        # NOTE: pandas classifies string columns as being "object" columns - but many other types can be objects as well! For instance, pandas will classify lists and dictionaries as objects too. To add insult to injury, attempting to use the .str accessor and str methods on these types won't throw any noticeable Exception - it will just return NaN!
        # for now, I'm going to leave this be, since I know that I'll always be operating on string data within the columns that I'm reading. However, if I was writing this to be a more general fn that was to be applied to unknown or variable data, I would need to think harder about this, and how to better distinguish "true" string data from other objects in the dataframe
        if df[column].dtype == "object":
            df[column] = df[column].str.lower()

    return df


def load_df(conn, cursor, df, sql):

    records = df.to_records(index=False)

    cursor.executemany(sql, records)
    conn.commit()

    return conn, cursor


def db_setup(db_file):

    # initialize db
    create_db_file(db_file)
    conn, cursor = get_db_connection(db_file)
    conn, cursor = run_sql_script(conn, cursor, "sql/create_schema_sqlite.sql")

    # instruments ETL
    instruments_df = pre_process_df(pd.read_csv("instruments.csv", delimiter=",", index_col=False))
    conn, cursor = load_df(conn,
                           cursor,
                           instruments_df,
                           "INSERT INTO instruments(instrument, section) VALUES (?, ?)")

    # names ETL
    names_df = pre_process_df(pd.read_csv("names.txt", delimiter="\t", index_col=False, names=["Name"]))
    names_df["first_name"], names_df["middle_name"], names_df["last_name"] = [None, None, None]
    names_df = names_df.apply(expand_name_fn, axis=1, name_col="Name")
    conn, cursor = load_df(conn,
                           cursor,
                           names_df[["first_name", "middle_name", "last_name"]],
                           "INSERT INTO names(first_name, middle_name, last_name) VALUES (?, ?, ?)")

    # assignments_by_name ETL
    assignments_df = pre_process_df(pd.read_csv("name_instrument.csv", delimiter=",", index_col=False))
    assignments_df["first_name"], assignments_df["middle_name"], assignments_df["last_name"] = [None, None, None]
    assignments_df = assignments_df.apply(expand_name_fn, axis=1, name_col="Name")
    conn, cursor = load_df(conn,
                           cursor,
                           assignments_df[["Instrument", "first_name", "middle_name", "last_name"]],
                           "INSERT INTO assignments_by_name(instrument, first_name, middle_name, last_name) VALUES (?, ?, ?, ?)")

    # create db relationships between assignments_by_name entries and names/instruments tables
    assignments_sql = [
        """
        INSERT INTO assignments (player_id, instrument_id)
        WITH normalized_assignments as (
        SELECT
        instrument,
        CASE
	    WHEN first_name LIKE ? THEN middle_name
	    WHEN first_name LIKE ? THEN middle_name
	    ELSE first_name
        END AS nick_name,
        COALESCE (last_name, 'UNDEFINED') AS last_name
        FROM assignments_by_name
        )
        -- handle assignments where n.first_name / n.last_name is used
        SELECT n.id, i.id
        FROM normalized_assignments a
        INNER JOIN names n, instruments i
        ON n.first_name = a.nick_name
        AND COALESCE(n.last_name, 'UNDEFINED') = a.last_name
        AND i.instrument = a.instrument
        UNION ALL
        -- handle assignments where n.middle_name / n.last_name is used
        SELECT n.id, i.id
        FROM normalized_assignments a
        INNER JOIN names n, instruments i
        ON n.middle_name = a.nick_name
        AND COALESCE(n.last_name, 'UNDEFINED') = a.last_name
        AND i.instrument = a.instrument;
        """,
        ["_.", "_"]
    ]

    cursor.execute(*assignments_sql)
    conn.commit()

    # close out
    cursor.close()
    conn.close()


if __name__ == '__main__':

    db_setup(os.environ.get("DB_FILE", "orchestra.db"))
