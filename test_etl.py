import unittest
import etl
import pandas as pd
import sqlite3
import os


class TestExpandNameFn(unittest.TestCase):
    """
    Tests the etl.expand_name_fn against the following name cases:
    - first last
    - first middle last
    - first
    - last, first
    - last, first middle
    - last, f. middle
    - last, first m.

    These are the styles of naming that we get in `names.txt`
    """

    def _apply_fn(self, test_dict):

        t = pd.DataFrame([test_dict])
        t = t.apply(etl.expand_name_fn, axis=1, name_col="Name")
        return t[["first_name", "middle_name", "last_name"]].to_dict("records")


    def test_first_last(self):

        first_last = {
            "Name": "Pepe LePew",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(first_last)

        expected_first_last = [{
            "first_name": "Pepe",
            "middle_name": None,
            "last_name": "LePew"
        }]

        self.assertEqual(t, expected_first_last)


    def test_first_middle_last(self):

        first_middle_last = {
            "Name": "Daffy Sheldon Duck",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(first_middle_last)

        expected_first_middle_last = [{
            "first_name": "Daffy",
            "middle_name": "Sheldon",
            "last_name": "Duck"
        }]

        self.assertEqual(t, expected_first_middle_last)


    def test_first(self):

        first = {
            "Name": "Bender",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(first)

        expected_first = [{
            "first_name": "Bender",
            "middle_name": None,
            "last_name": None
        }]

        self.assertEqual(t, expected_first)


    def test_last_first(self):

        last_first = {
            "Name": "Simpson, Lisa",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(last_first)

        expected_last_first = [{
            "first_name": "Lisa",
            "middle_name": None,
            "last_name": "Simpson"
        }]

        self.assertEqual(t, expected_last_first)


    def test_last_first_middle(self):

        last_first_middle = {
            "Name": "Burns, Charles Montgomery",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(last_first_middle)

        expected_last_first_middle = [{
            "first_name": "Charles",
            "middle_name": "Montgomery",
            "last_name": "Burns"
        }]

        self.assertEqual(t, expected_last_first_middle)


    def test_last_f_middle(self):

        last_f_middle = {
            "Name": "Skinner, W. Seymour",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(last_f_middle)

        expected_last_f_middle = [{
            "first_name": "W.",
            "middle_name": "Seymour",
            "last_name": "Skinner"
        }]

        self.assertEqual(t, expected_last_f_middle)


    def test_last_first_m(self):

        last_first_m = {
            "Name": "Simpson, Homer J.",
            "first_name": None,
            "middle_name": None,
            "last_name": None
        }

        t = self._apply_fn(last_first_m)

        expected_last_first_m = [{
            "first_name": "Homer",
            "middle_name": "J.",
            "last_name": "Simpson"
        }]

        self.assertEqual(t, expected_last_first_m)


class ReportsIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # run the whole etl process
        etl.db_setup(os.environ.get("DB_FILE", "orchestra.db"))


    def setUp(self):

        self.conn = sqlite3.connect(os.environ.get("DB_FILE", "orchestra.db"))
        self.cursor = self.conn.cursor()


    def tearDown(self):

        self.cursor.close()
        self.conn.close()


    def _get_data(self, query):

        return pd.read_sql(query, self.conn).to_dict("records")


    def test_report_1(self):
        """
        1. A report showing the name, instrument, and section for all musicians.
        """

        report = self._get_data("select * from all_musicians;")
        expected_report = [
            # {"first_name": "", "middle_name": "", "last_name": "", "instrument": "", "section": ""}
            {"first_name": "pepe", "middle_name": None, "last_name": "lepew", "instrument": None, "section": None},
            {"first_name": "charlie", "middle_name": None, "last_name": "brown", "instrument": None, "section": None},
            {"first_name": "bender", "middle_name": None, "last_name": None, "instrument": "french horn", "section": "brass"},
            {"first_name": "goofy", "middle_name": None, "last_name": None, "instrument": None, "section": None},
            {"first_name": "ned", "middle_name": None, "last_name": "flanders", "instrument": "clarinet", "section": "woodwinds"},
            {"first_name": "charles", "middle_name": "montgomery", "last_name": "burns", "instrument": None, "section": None},
            {"first_name": "marvin", "middle_name": None, "last_name": "martian", "instrument": "flute", "section": "woodwinds"},
            {"first_name": "spongebob", "middle_name": None, "last_name": "squarepants", "instrument": None, "section": None},
            {"first_name": "shaggy", "middle_name": None, "last_name": "rogers", "instrument": "harmonica", "section": "other"},
            {"first_name": "felix", "middle_name": None, "last_name": "cat", "instrument": None, "section": None},
            {"first_name": "yogi", "middle_name": None, "last_name": "bear", "instrument": "banjo", "section": "strings"},
            {"first_name": "bart", "middle_name": None, "last_name": "simpson", "instrument": "bass", "section": "strings"},
            {"first_name": "daffy", "middle_name": "sheldon", "last_name": "duck", "instrument": "piano", "section": "percussion"},
            {"first_name": "stewie", "middle_name": None, "last_name": "griffin", "instrument": None, "section": None},
            {"first_name": "w.", "middle_name": "seymour", "last_name": "skinner", "instrument": "trombone", "section": "brass"},
            {"first_name": "mighty", "middle_name": None, "last_name": "mouse", "instrument": None, "section": None},
            {"first_name": "fat", "middle_name": None, "last_name": "albert", "instrument": "accordian", "section": "other"},
            {"first_name": "lisa", "middle_name": None, "last_name": "simpson", "instrument": "saxophone", "section": "woodwinds"},
            # betty boop appears twice
            {"first_name": "betty", "middle_name": None, "last_name": "boop", "instrument": "piano", "section": "percussion"},
            {"first_name": "betty", "middle_name": None, "last_name": "boop", "instrument": "singer", "section": "other"},
            {"first_name": "fred", "middle_name": None, "last_name": "flintstone", "instrument": "singer", "section": "other"},
            {"first_name": "mickey", "middle_name": None, "last_name": "mouse", "instrument": "whistle", "section": "other"},
            # snoopy appears twice
            {"first_name": "snoopy", "middle_name": None, "last_name": None, "instrument": "bass", "section": "strings"},
            {"first_name": "snoopy", "middle_name": None, "last_name": None, "instrument": "tuba", "section": "brass"},
            {"first_name": "eric", "middle_name": None, "last_name": "cartman", "instrument": None, "section": None},
            {"first_name": "bugs", "middle_name": None, "last_name": "bunny", "instrument": "singer", "section": "other"},
            # homer appears twice
            {"first_name": "homer", "middle_name": "j.", "last_name": "simpson", "instrument": "piano", "section": "percussion"},
            {"first_name": "homer", "middle_name": "j.", "last_name": "simpson", "instrument": "singer", "section": "other"}
        ]

        self.assertEqual(report, expected_report)


    def test_report_2(self):
        """
        2. A report showing the instruments that don't yet have musicians (i.e. no one plays the trumpet), and their sections, sorted by section, alphabetically in ascending order.
        """

        report = self._get_data("select * from instruments_without_musicians;")
        expected_report = [
            # {"instrument": "", "section": ""}
            {"instrument": "trumpet", "section": "brass"},
            {"instrument": "violin", "section": "strings"},
            {"instrument": "viola", "section": "strings"},
            {"instrument": "cello", "section": "strings"},
            {"instrument": "oboe", "section": "woodwinds"},
            {"instrument": "bassoon", "section": "woodwinds"}
        ]

        self.assertEqual(report, expected_report)


    def test_report_3(self):
        """
        A report showing any musicians that play two or more instruments, their instrument, and section.
        """

        report = self._get_data("select * from multi_instrumentalists;")
        expected_report = [
            {"first_name": "betty", "middle_name": None, "last_name": "boop", "instrument": "piano", "section": "percussion"},
            {"first_name": "betty", "middle_name": None, "last_name": "boop", "instrument": "singer", "section": "other"},
            {"first_name": "snoopy", "middle_name": None, "last_name": None, "instrument": "bass", "section": "strings"},
            {"first_name": "snoopy", "middle_name": None, "last_name": None, "instrument": "tuba", "section": "brass"},
            {"first_name": "homer", "middle_name": "j.", "last_name": "simpson", "instrument": "piano", "section": "percussion"},
            {"first_name": "homer", "middle_name": "j.", "last_name": "simpson", "instrument": "singer", "section": "other"}
        ]

        self.assertEqual(report, expected_report)


    def test_report_4(self):
        """
        A report showing any instruments that are played by multiple musicians, as well as the musician names and sections.
        """

        report = self._get_data("select * from multiple_players;")
        expected_report = [
            # {"instrument": "", "section": "", "first_name": "", "middle_name": "", "last_name": ""}
            {"instrument": "bass", "section": "strings", "first_name": "bart", "middle_name": None, "last_name": "simpson"},
            {"instrument": "bass", "section": "strings", "first_name": "snoopy", "middle_name": None, "last_name": None},
            {"instrument": "piano", "section": "percussion", "first_name": "daffy", "middle_name": "sheldon", "last_name": "duck"},
            {"instrument": "piano", "section": "percussion", "first_name": "betty", "middle_name": None, "last_name": "boop"},
            {"instrument": "piano", "section": "percussion", "first_name": "homer", "middle_name": "j.", "last_name": "simpson"},
            {"instrument": "singer", "section": "other", "first_name": "betty", "middle_name": None, "last_name": "boop"},
            {"instrument": "singer", "section": "other", "first_name": "fred", "middle_name": None, "last_name": "flintstone"},
            {"instrument": "singer", "section": "other", "first_name": "bugs", "middle_name": None, "last_name": "bunny"},
            {"instrument": "singer", "section": "other", "first_name": "homer", "middle_name": "j.", "last_name": "simpson"}
        ]

        self.assertEqual(report, expected_report)


if __name__ == '__main__':

    unittest.main()
