import unittest
import datetime

import racetrack.lineups.week as week


class NflWeekFinderTest(unittest.TestCase):
    def day(self, test):
        return week.NflWeekFinder(test).get_nfl_sunday()

    def test_sunday(self):
        sunday = datetime.date(2015, 10, 25)
        self.assertEqual(sunday, self.day(sunday))

    def test_thursday(self):
        thursday = datetime.date(2015, 11, 5)
        self.assertEqual(datetime.date(2015, 11, 8), self.day(thursday))

    def test_monday(self):
        monday = datetime.date(2015, 11, 9)
        self.assertEqual(datetime.date(2015, 11, 15), self.day(monday))
