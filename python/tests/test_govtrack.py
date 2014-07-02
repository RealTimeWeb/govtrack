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

        keys = ['district', 'end_date', 'leadership_title', 'name',
                'start_date', 'state', 'title', 'website']

        reps = govtrack.get_representatives({"party": "Democrat"})
        self.assertTrue(isinstance(reps, list))

        for rep_dict in reps:
            self.assertTrue(isinstance(rep_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(rep_dict)
            self.assertEqual(8, len(intersection))

        senators = govtrack.get_senators({"party": "Democrat"})
        self.assertTrue(isinstance(reps, list))

        for sen_dict in senators:
            self.assertTrue(isinstance(rep_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(rep_dict)
            self.assertEqual(8, len(intersection))

    def test_method_offline(self):
        govtrack.disconnect("../src/govtrack_cache.json")


        keys = ['district', 'end_date', 'leadership_title', 'name',
                'start_date', 'state', 'title', 'website']

        reps = govtrack.get_representatives({"party": "Democrat"})
        self.assertTrue(isinstance(reps, list))

        for rep_dict in reps:
            self.assertTrue(isinstance(rep_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(rep_dict)
            self.assertEqual(8, len(intersection))

        senators = govtrack.get_senators({"party": "Democrat"})
        self.assertTrue(isinstance(reps, list))

        for sen_dict in senators:
            self.assertTrue(isinstance(rep_dict, dict))
            # Assert all of the keys are in item
            intersection = set(keys).intersection(rep_dict)
            self.assertEqual(8, len(intersection))
