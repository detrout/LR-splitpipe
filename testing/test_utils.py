from unittest import TestCase


from LR_splitpipe.utils import (
    get_bc_round_set,
    load_barcodes,
    load_barcodes_set,
)


class TestUtils(TestCase):
    def test_get_bc_round_set(self):
        test_data = [
            ("WT", "v1", [['bc1', 'v2'], ['bc2', 'v1'], ['bc3', 'v1']]),
            ("WT", "v2", [['bc1', 'n96_v4'], ['bc2', 'v1'], ['bc3', 'v1']]),
            ("WT_mini", "v2", [['bc1', 'n24_v4'], ['bc2', 'v1'], ['bc3', 'v1']])
        ]
        for kit, chemistry, expected in test_data:
            result = get_bc_round_set(kit, chemistry)
            self.assertEqual(result, expected)

    def test_load_barcodes(self):
        barcodes = load_barcodes("WT", "v2")
        self.assertIsInstance(barcodes, dict)
        self.assertEqual(len(barcodes), 3)
        self.assertEqual(list(barcodes.keys()), ["bc1", "bc2", "bc3"])
        self.assertEqual(len(barcodes["bc1"]), 4)
        self.assertEqual(len(barcodes["bc1"][0]["CATTCCTA"]), 1)
        self.assertEqual(len(barcodes["bc1"][1]["CATTCCTA"]), 0)
        self.assertEqual(len(barcodes["bc1"][2]["CATTCCTA"]), 1)
        self.assertEqual(len(barcodes["bc1"][3]["CATTCCTA"]), 14)

    def test_load_barcodes_set(self):
        barcodes_set = load_barcodes_set("WT_mega", "v1")
        self.assertIsInstance(barcodes_set, dict)
        self.assertEqual(len(barcodes_set), 3)
        self.assertEqual(list(barcodes_set.keys()), ["bc1", "bc2", "bc3"])

        self.assertEqual(len(barcodes_set["bc1"]), 192)
        self.assertEqual(len(barcodes_set["bc2"]), 96)
        self.assertEqual(len(barcodes_set["bc3"]), 96)
