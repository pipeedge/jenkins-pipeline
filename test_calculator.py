"""
Unit tests for Calculator application
Comprehensive test suite for Jenkins pipeline demo.
"""

import pytest
import logging
from calculator import Calculator


class TestCalculator:
    """Test class for Calculator operations."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        assert self.calc.add(5, 3) == 8
        assert self.calc.add(10, 20) == 30
        assert self.calc.add(0, 5) == 5
    
    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        assert self.calc.add(-5, 3) == -2
        assert self.calc.add(-10, -20) == -30
        assert self.calc.add(5, -3) == 2
    
    def test_add_floats(self):
        """Test addition with floating point numbers."""
        assert self.calc.add(2.5, 3.7) == pytest.approx(6.2)
        assert self.calc.add(-1.5, 2.5) == pytest.approx(1.0)
    
    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers."""
        assert self.calc.subtract(10, 3) == 7
        assert self.calc.subtract(20, 5) == 15
        assert self.calc.subtract(5, 5) == 0
    
    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        assert self.calc.subtract(-5, 3) == -8
        assert self.calc.subtract(5, -3) == 8
        assert self.calc.subtract(-10, -5) == -5
    
    def test_subtract_floats(self):
        """Test subtraction with floating point numbers."""
        assert self.calc.subtract(5.5, 2.3) == pytest.approx(3.2)
        assert self.calc.subtract(-1.5, 2.5) == pytest.approx(-4.0)
    
    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers."""
        assert self.calc.multiply(5, 3) == 15
        assert self.calc.multiply(10, 4) == 40
        assert self.calc.multiply(1, 7) == 7
    
    def test_multiply_with_zero(self):
        """Test multiplication with zero."""
        assert self.calc.multiply(5, 0) == 0
        assert self.calc.multiply(0, 10) == 0
        assert self.calc.multiply(0, 0) == 0
    
    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        assert self.calc.multiply(-5, 3) == -15
        assert self.calc.multiply(-4, -2) == 8
        assert self.calc.multiply(6, -3) == -18
    
    def test_multiply_floats(self):
        """Test multiplication with floating point numbers."""
        assert self.calc.multiply(2.5, 4) == pytest.approx(10.0)
        assert self.calc.multiply(-1.5, 2.0) == pytest.approx(-3.0)
    
    def test_divide_positive_numbers(self):
        """Test division of positive numbers."""
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(15, 3) == 5
        assert self.calc.divide(7, 2) == 3.5
    
    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        assert self.calc.divide(-10, 2) == -5
        assert self.calc.divide(10, -2) == -5
        assert self.calc.divide(-10, -2) == 5
    
    def test_divide_floats(self):
        """Test division with floating point numbers."""
        assert self.calc.divide(7.5, 2.5) == pytest.approx(3.0)
        assert self.calc.divide(-6.0, 3.0) == pytest.approx(-2.0)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)
        
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(-5, 0)
    
    def test_power_positive_numbers(self):
        """Test power calculation with positive numbers."""
        assert self.calc.power(2, 3) == 8
        assert self.calc.power(5, 2) == 25
        assert self.calc.power(10, 0) == 1
    
    def test_power_negative_base(self):
        """Test power calculation with negative base."""
        assert self.calc.power(-2, 3) == -8
        assert self.calc.power(-3, 2) == 9
        assert self.calc.power(-5, 0) == 1
    
    def test_power_negative_exponent(self):
        """Test power calculation with negative exponent."""
        assert self.calc.power(2, -2) == pytest.approx(0.25)
        assert self.calc.power(4, -1) == pytest.approx(0.25)
        assert self.calc.power(10, -3) == pytest.approx(0.001)
    
    def test_power_floats(self):
        """Test power calculation with floating point numbers."""
        assert self.calc.power(2.5, 2) == pytest.approx(6.25)
        assert self.calc.power(4, 0.5) == pytest.approx(2.0)
    
    def test_square_root_positive_numbers(self):
        """Test square root of positive numbers."""
        assert self.calc.square_root(4) == pytest.approx(2.0)
        assert self.calc.square_root(9) == pytest.approx(3.0)
        assert self.calc.square_root(25) == pytest.approx(5.0)
        assert self.calc.square_root(0) == pytest.approx(0.0)
    
    def test_square_root_floats(self):
        """Test square root of floating point numbers."""
        assert self.calc.square_root(6.25) == pytest.approx(2.5)
        assert self.calc.square_root(2.25) == pytest.approx(1.5)
    
    def test_square_root_negative_number(self):
        """Test square root of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.square_root(-4)
        
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.square_root(-1)


class TestCalculatorIntegration:
    """Integration tests for Calculator operations."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def test_complex_calculation(self):
        """Test complex calculation combining multiple operations."""
        # (5 + 3) * 2 = 16
        result1 = self.calc.add(5, 3)
        result2 = self.calc.multiply(result1, 2)
        assert result2 == 16
    
    def test_calculation_chain(self):
        """Test chain of calculations."""
        # Start with 10, add 5, subtract 3, multiply by 2, divide by 4
        result = 10
        result = self.calc.add(result, 5)      # 15
        result = self.calc.subtract(result, 3)  # 12
        result = self.calc.multiply(result, 2)  # 24
        result = self.calc.divide(result, 4)    # 6
        assert result == 6
    
    def test_power_and_square_root(self):
        """Test power and square root operations together."""
        # Calculate 3^2 then take square root
        power_result = self.calc.power(3, 2)  # 9
        sqrt_result = self.calc.square_root(power_result)  # 3
        assert sqrt_result == pytest.approx(3.0)


# Pytest fixtures and configuration
@pytest.fixture
def calculator():
    """Fixture to provide a Calculator instance."""
    return Calculator()


def test_calculator_logging(calculator, caplog):
    """Test that calculator operations are properly logged."""
    with caplog.at_level(logging.INFO):
        calculator.add(5, 3)
    
    assert "Addition: 5 + 3 = 8" in caplog.text


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"]) 