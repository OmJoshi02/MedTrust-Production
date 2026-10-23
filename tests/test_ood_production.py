import sys
import unittest
from pathlib import Path
from PIL import Image

PROD_DIR = Path(__file__).resolve().parent.parent
if str(PROD_DIR) not in sys.path:
    sys.path.insert(0, str(PROD_DIR))

from backend.engine import MedTrustBackendEngine, verify_artifacts


class TestProductionOODCandidate1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = MedTrustBackendEngine()
        cls.d2_path = PROD_DIR / "test_images" / "d2.jpg"
        cls.mri_path = PROD_DIR / "test_images" / "mri.jpg"
        cls.disease_path = PROD_DIR / "test_images" / "disease.png"

    def test_artifact_integrity_verification(self):
        rep = verify_artifacts(PROD_DIR, enforce_hashes=True)
        self.assertTrue(rep.get("ready"), f"Artifacts not ready: {rep.get('failures')}")
        self.assertTrue(rep.get("critical_present"), "Critical artifacts missing")
        self.assertEqual(len(rep.get("failures", [])), 0)

    def test_candidate1_thresholds_applied(self):
        self.assertTrue(self.d2_path.exists(), "test_images/d2.jpg missing")
        img = Image.open(self.d2_path)
        res = self.engine.analyze_full(img, query_filename="d2.jpg")

        self.assertFalse(res.get("is_ood"), "d2.jpg should be accepted under Candidate 1 thresholds")
        self.assertEqual(res.get("status"), "ANALYZED")
        self.assertIsNotNone(res.get("prediction"), "Predictions should be generated for ID images")

        ood = res.get("ood", {})
        self.assertEqual(ood.get("status"), "ID")
        self.assertEqual(ood.get("trust_decision"), "PREDICTION CAN BE CONSIDERED")

        methods = ood.get("method_results", {})
        self.assertAlmostEqual(methods["mahalanobis"]["threshold"], 975.531329, places=3)
        self.assertAlmostEqual(methods["msp"]["threshold"], 0.737333, places=3)
        self.assertAlmostEqual(methods["energy"]["threshold"], -0.071788, places=3)

    def test_non_chest_ood_gating(self):
        self.assertTrue(self.mri_path.exists(), "test_images/mri.jpg missing")
        img = Image.open(self.mri_path)
        res = self.engine.analyze_full(img, query_filename="mri.jpg")

        self.assertTrue(res.get("is_ood"), "MRI must be flagged as OOD")
        self.assertEqual(res.get("status"), "REJECTED_OOD")
        self.assertIsNone(res.get("prediction"), "Predictions must be suppressed for OOD input")


if __name__ == "__main__":
    unittest.main()

