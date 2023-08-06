import csv
from pathlib import Path
from typing import Dict, List


class Fenton:
    lms_rows = None

    @classmethod
    def _get_lms_rows(cls) -> List[Dict]:
        """Gets the LMS rows from the fentonlms.csv file and returns them.

        This should only be called from `get_lms` and only once per instantiation of
        class Fenton. I'm not sure if this is the best way to initialize this class
        variable (`lms_rows`).

        Returns:
            List[Dict] -- LMS rows in a dict, one row per gestational_age_in_days
        """
        rows = []
        lms_file_path = Path(__file__).resolve().parents[0] / "fentonlms.csv"

        with open(lms_file_path, "r") as lms_file:
            for row in csv.DictReader(lms_file):
                row["gestational_age_in_days"] = int(row["gestational_age_in_days"])
                row["l"] = float(row["l"])
                row["m"] = float(row["m"])
                row["s"] = float(row["s"])
                rows.append(row)
        print("getting lms rows")

        return rows

    @classmethod
    def get_lms(
        cls, metric: str, sex: str, gestational_age_in_days: int
    ) -> (float, float, float):
        """returns the LMS parameters from Fenton tables.

        Fenton TR and Kim JH, BMC Pediatrics 2013, 13:59
        http://www.ncbi.nlm.nih.gov/pubmed/23601190

        Arguments:
            metric {str} -- Metric to calculate z-score for. Must be `weight`, `length`,
                or `hc` (head circumference). Units must be in grams for weight, or cm
                for length or hc.
            sex {str} -- Patient sex. Must be `f` or `m`.
            gestational_age_in_days {int} -- Patient gestational age. Ie, to calculate
                z-scores for a baby born at 24 weeks 0d on dol 5:
                gestational_age_in_days = 24 * 7 + 5 = 173

        Returns:
            float -- l parameter
            float -- m parameter (mean)
            float -- s parameter
        """
        if cls.lms_rows is None:
            cls.lms_rows = cls._get_lms_rows()

        for row in cls.lms_rows:
            if (
                row["metric"] == metric
                and row["sex"] == sex
                and row["gestational_age_in_days"] == gestational_age_in_days
            ):
                return row["l"], row["m"], row["s"]

        raise ValueError(
            f"get_fenton_lms failed to find for `{ metric }`, `{ sex }`, "
            f"`{ gestational_age_in_days }`"
        )

    @classmethod
    def calc_zscore(
        cls, metric: str, sex: str, gestational_age_in_days: int, measure: float
    ) -> float:
        """calculates a z-score using Fenton tables and the LMS methodology.

        Fenton TR and Kim JH, BMC Pediatrics 2013, 13:59
        http://www.ncbi.nlm.nih.gov/pubmed/23601190

        Arguments:
            metric {str} -- Metric to calculate z-score for. Must be `weight`, `length`,
                or `hc` (head circumference). Units must be in grams for weight, or cm
                for length or hc.
            sex {str} -- Patient sex. Must be `f` or `m`.
            gestational_age_in_days {int} -- Patient gestational age. Ie, to calculate
                z-scores for a baby born at 24 weeks 0d on dol 5:
                gestational_age_in_days = 24 * 7 + 5 = 173
            measure {float} -- the patient's value of the meausurement for which the
                z-score shall be calculated.

        Returns:
            float -- z-score for the given inputs
        """

        # get_fenton_lms will raise a value error if any parameters are bad
        l, m, s = cls.get_lms(metric.lower(), sex.lower(), int(gestational_age_in_days))

        return ((measure / m) ** l - 1) / (l * s)
