from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from LRsplitpipe.demultiplex import main, get_args

testing = Path(__file__).parent


class TestDemultiplexMain(TestCase):
    def test_running_score_linkers_t1(self):
        fq = testing / "fq1.fastq"
        with TemporaryDirectory("lrsplit") as tmpdir:
            prefix = Path(tmpdir) / "score_linkers_tq"
            main(["score_linkers", "-k", "WT", "-f", str(fq), "-o", str(prefix)])

    def test_running_score_linkers_t2(self):
        fq = testing / "fq1.fastq"
        with TemporaryDirectory("lrsplit") as tmpdir:
            prefix = Path(tmpdir) / "score_linkers_t2"
            main(
                [
                    "score_linkers",
                    "-t",
                    "2",
                    "-k",
                    "WT",
                    "-f",
                    str(fq),
                    "-o",
                    str(prefix),
                ]
            )

    def test_running_all_t1(self):
        fq = testing / "fq1.fastq"
        with TemporaryDirectory("lrsplit") as tmpdir:
            prefix = Path(tmpdir) / "all_t1"
            main(["all", "-k", "WT", "-f", str(fq), "-o", str(prefix)])

    def test_running_all_t2(self):
        fq = testing / "fq1.fastq"
        with TemporaryDirectory("lrsplit") as tmpdir:
            prefix = Path(tmpdir) / "all_t2"
            main(["all", "-t", "2", "-k", "WT", "-f", str(fq), "-o", str(prefix)])

    def test_parse_args(self):
        args = get_args(
            [
                "score_linkers",
                "-t",
                "2",
                "-k",
                "WT",
                "-f",
                "name.fastq.gz",
                "-o",
                "target/name",
            ]
        )
        self.assertEqual(args.mode, "score_linkers")
        self.assertEqual(args.threads, "2")
        self.assertEqual(args.kit, "WT")

    def test_version(self):
        from LRsplitpipe import _version

        self.assertEqual(len(_version.version_tuple), 4)
