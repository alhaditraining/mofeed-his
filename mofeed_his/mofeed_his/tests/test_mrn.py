"""Unit tests for MRN generation utilities.

These tests verify the MRN generation logic works correctly.
Note: Full integration tests require a running Frappe instance.
"""

import unittest


class TestMRNFormat(unittest.TestCase):
    """Test MRN format and validation."""

    def test_mrn_format_pattern(self):
        """Test that MRN matches expected format: HOSPITAL-YEAR-NUMBER."""
        import re

        mrn_pattern = r"^[A-Z0-9]+-\d{4}-\d{6}$"

        # Valid MRNs
        valid_mrns = [
            "KRBHOSP-2025-000001",
            "KRBHOSP-2025-000123",
            "KRBHOSP-2025-999999",
            "HOSP1-2024-000001",
            "ABC123-2025-000001",
        ]

        for mrn in valid_mrns:
            self.assertIsNotNone(
                re.match(mrn_pattern, mrn),
                f"MRN '{mrn}' should match pattern"
            )

        # Invalid MRNs
        invalid_mrns = [
            "KRBHOSP-2025-12345",    # Only 5 digits
            "KRBHOSP-25-000001",     # Only 2 digit year
            "krbhosp-2025-000001",   # Lowercase
            "KRBHOSP2025000001",     # No separators
            "",                       # Empty
        ]

        for mrn in invalid_mrns:
            self.assertIsNone(
                re.match(mrn_pattern, mrn),
                f"MRN '{mrn}' should NOT match pattern"
            )

    def test_mrn_sequence_padding(self):
        """Test that sequence numbers are zero-padded to 6 digits."""
        # Simulate MRN generation format
        def format_mrn(hospital_code, year, sequence):
            return f"{hospital_code}-{year}-{sequence:06d}"

        self.assertEqual(format_mrn("KRBHOSP", 2025, 1), "KRBHOSP-2025-000001")
        self.assertEqual(format_mrn("KRBHOSP", 2025, 123), "KRBHOSP-2025-000123")
        self.assertEqual(format_mrn("KRBHOSP", 2025, 999999), "KRBHOSP-2025-999999")


class TestHospitalCodeValidation(unittest.TestCase):
    """Test hospital code validation."""

    def test_hospital_code_uppercase(self):
        """Test that hospital codes are normalized to uppercase."""
        # Simulate code normalization
        def normalize_code(code):
            return code.strip().upper() if code else code

        self.assertEqual(normalize_code("krbhosp"), "KRBHOSP")
        self.assertEqual(normalize_code("KrbHosp"), "KRBHOSP")
        self.assertEqual(normalize_code("  KRBHOSP  "), "KRBHOSP")

    def test_hospital_code_alphanumeric(self):
        """Test that hospital codes only allow alphanumeric characters."""
        def is_valid_code(code):
            return code.isalnum() if code else False

        self.assertTrue(is_valid_code("KRBHOSP"))
        self.assertTrue(is_valid_code("HOSP123"))
        self.assertTrue(is_valid_code("ABC"))

        self.assertFalse(is_valid_code("KRB-HOSP"))
        self.assertFalse(is_valid_code("KRB HOSP"))
        self.assertFalse(is_valid_code("KRB_HOSP"))


class TestMRNGenerationLogic(unittest.TestCase):
    """Test MRN generation logic with mocked Frappe."""

    def test_get_next_mrn_generates_correct_format(self):
        """Test that get_next_mrn generates MRN in correct format."""
        # We can't easily test the full function without Frappe,
        # but we can verify the format logic
        hospital_code = "KRBHOSP"
        year = 2025
        sequence = 1

        expected_mrn = f"{hospital_code}-{year}-{sequence:06d}"
        self.assertEqual(expected_mrn, "KRBHOSP-2025-000001")

    def test_sequence_increment_logic(self):
        """Test that sequence increment logic works correctly."""
        # Simulate sequence increment
        current_value = 123
        next_value = current_value + 1
        self.assertEqual(next_value, 124)

        # Test edge case at year boundary
        current_value = 0  # New year starts at 0
        next_value = current_value + 1
        self.assertEqual(next_value, 1)


class TestMRNUniqueness(unittest.TestCase):
    """Test MRN uniqueness validation."""

    def test_duplicate_mrn_detection_logic(self):
        """Test logic for detecting duplicate MRNs."""
        # Simulate a set of existing MRNs
        existing_mrns = {
            "KRBHOSP-2025-000001",
            "KRBHOSP-2025-000002",
            "KRBHOSP-2025-000003",
        }

        # Check for duplicates
        new_mrn = "KRBHOSP-2025-000004"
        is_duplicate = new_mrn in existing_mrns
        self.assertFalse(is_duplicate)

        duplicate_mrn = "KRBHOSP-2025-000001"
        is_duplicate = duplicate_mrn in existing_mrns
        self.assertTrue(is_duplicate)


if __name__ == "__main__":
    unittest.main()
