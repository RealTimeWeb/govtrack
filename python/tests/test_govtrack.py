import unittest

import sys

sys.path.append("../src")

try:
    import govtrack
except ImportError:
    from python.src import govtrack


class TestGovTrack(unittest.TestCase):
    # @unittest.skip("demonstrating skipping")
    def test_method_online(self):
        govtrack.connect()
        govtrack._start_editing()

        keys = ['district', 'end_date', 'leadership_title', 'name',
                'start_date', 'state', 'title', 'website']

        reps = govtrack.get_representatives("Democrat")
        self.assertTrue(isinstance(reps, list))

        for rep_dict in reps:
            self.assertTrue(isinstance(rep_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(rep_dict)
            self.assertEqual(8, len(intersection))

        senators = govtrack.get_senators("Democrat")
        self.assertTrue(isinstance(senators, list))

        for sen_dict in senators:
            self.assertTrue(isinstance(sen_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(sen_dict)
            self.assertEqual(8, len(intersection))

        keys = ['is_alive', 'is_current', 'title', 'number',
                'description', 'congress_session', 'introduced_date']

        bills = govtrack.get_bills_by_keyword("healthcare")
        self.assertTrue(isinstance(bills, list))

        for bill in bills:
            self.assertTrue(isinstance(bill, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(bill)
            self.assertEqual(7, len(intersection))

        govtrack._save_cache("../src/govtrack_cache.json")

    def test_method_offline(self):
        govtrack.disconnect("../src/govtrack_cache.json")


        keys = ['district', 'end_date', 'leadership_title', 'name',
                'start_date', 'state', 'title', 'website']

        reps = govtrack.get_representatives("Democrat")
        self.assertTrue(isinstance(reps, list))

        for rep_dict in reps:
            self.assertTrue(isinstance(rep_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(rep_dict)
            self.assertEqual(8, len(intersection))

        senators = govtrack.get_senators("Democrat")
        self.assertTrue(isinstance(senators, list))

        for sen_dict in senators:
            self.assertTrue(isinstance(sen_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(sen_dict)
            self.assertEqual(8, len(intersection))

        keys = ['is_alive', 'is_current', 'title', 'number',
                'description', 'congress_session', 'introduced_date']

        bills = govtrack.get_bills_by_keyword("healthcare")
        self.assertTrue(isinstance(bills, list))

        for bill in bills:
            self.assertTrue(isinstance(bill, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(bill)
            self.assertEqual(7, len(intersection))

