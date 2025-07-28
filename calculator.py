"""
Calculator Application
A simple calculator with basic arithmetic operations for Jenkins pipeline demo.
"""

import logging
from typing import Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Calculator:
    """A simple calculator class with basic arithmetic operations."""
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Add two numbers."""
        result = a + b
        logger.info(f"Addition: {a} + {b} = {result}")
        return result
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Subtract two numbers."""
        result = a - b
        logger.info(f"Subtraction: {a} - {b} = {result}")
        return result
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Multiply two numbers."""
        result = a * b
        logger.info(f"Multiplication: {a} * {b} = {result}")
        return result
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Divide two numbers."""
        if b == 0:
            logger.error("Division by zero attempted")
            raise ValueError("Cannot divide by zero")
        result = a / b
        logger.info(f"Division: {a} / {b} = {result}")
        return result
    
    def power(self, base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """Calculate power of a number."""
        result = base ** exponent
        logger.info(f"Power: {base} ^ {exponent} = {result}")
        return result
    
    def square_root(self, number: Union[int, float]) -> float:
        """Calculate square root of a number."""
        if number < 0:
            logger.error("Square root of negative number attempted")
            raise ValueError("Cannot calculate square root of negative number")
        result = number ** 0.5
        logger.info(f"Square root: √{number} = {result}")
        return result


def main():
    """Main function to demonstrate calculator usage."""
    calc = Calculator()
    
    print("Calculator Demo")
    print("===============")
    
    # Demonstrate basic operations
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"√25 = {calc.square_root(25)}")


if __name__ == "__main__":
    main() 