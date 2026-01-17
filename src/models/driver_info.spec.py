"""Tests for Driver model lic_color_hex computed field"""
import pytest
from models.driver_info import Driver


class TestDriverLicColorHex:
    """Test the lic_color_hex computed field"""

    def test_lic_color_hex_with_integer_hex_value(self):
        """Test conversion of integer hex value to hex string"""
        driver = Driver(LicColor=0x0153db)
        assert driver.lic_color_hex == "#0153db"

    def test_lic_color_hex_with_decimal_integer(self):
        """Test conversion of decimal integer to hex string"""
        driver = Driver(LicColor=87003)  # 87003 decimal = 0x0153db hex
        assert driver.lic_color_hex == "#0153db"

    def test_lic_color_hex_with_string_hex(self):
        """Test conversion of string hex value to hex string"""
        driver = Driver(LicColor="0x0153db")
        assert driver.lic_color_hex == "#0153db"

    def test_lic_color_hex_with_invalid_string(self):
        """Test handling of invalid string value"""
        driver = Driver(LicColor="0xundefined")
        assert driver.lic_color_hex == "#000000"

    def test_lic_color_hex_with_non_hex_string(self):
        """Test handling of non-hex string"""
        driver = Driver(LicColor="invalid")
        assert driver.lic_color_hex == "#000000"

    def test_lic_color_hex_with_zero(self):
        """Test conversion of zero to hex string"""
        driver = Driver(LicColor=0)
        assert driver.lic_color_hex == "#000000"

    def test_lic_color_hex_with_default_value(self):
        """Test default value conversion"""
        driver = Driver()
        assert driver.lic_color_hex == "#000000"

    def test_lic_color_hex_included_in_dict(self):
        """Test that lic_color_hex is included in to_dict() output"""
        driver = Driver(LicColor=0x0153db, UserName="Test Driver")
        driver_dict = driver.to_dict()
        
        assert "lic_color_hex" in driver_dict
        assert driver_dict["lic_color_hex"] == "#0153db"
        assert driver_dict["LicColor"] == 0x0153db

    def test_lic_color_hex_included_in_json(self):
        """Test that lic_color_hex is included in to_json() output"""
        driver = Driver(LicColor=0x0153db, UserName="Test Driver")
        driver_json = driver.to_json()
        
        assert '"lic_color_hex":"#0153db"' in driver_json
        assert '"LicColor":87003' in driver_json

    def test_lic_color_hex_with_various_colors(self):
        """Test conversion of various color values"""
        test_cases = [
            (0xFF0000, "#ff0000"),  # Red
            (0x00FF00, "#00ff00"),  # Green
            (0x0000FF, "#0000ff"),  # Blue
            (0xFFFFFF, "#ffffff"),  # White
            (0x123456, "#123456"),  # Random color
        ]
        
        for color_int, expected_hex in test_cases:
            driver = Driver(LicColor=color_int)
            assert driver.lic_color_hex == expected_hex

    def test_lic_color_hex_padding(self):
        """Test that hex values are properly zero-padded to 6 characters"""
        driver = Driver(LicColor=0x000001)  # Should be #000001, not #1
        assert driver.lic_color_hex == "#000001"
        assert len(driver.lic_color_hex) == 7  # # + 6 hex digits

