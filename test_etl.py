import unittest
import etl
import pandas as pd


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


if __name__ == '__main__':

    unittest.main()
