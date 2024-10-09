from typing import List
from dataclasses import dataclass

@dataclass
class MultiplicationParams:
    numbers: List[int]

class MultiplicationTool:
    """Multiplies a list of numbers."""

    def multiply(self, parameters: MultiplicationParams) -> int:
        """
        Returns the product of a list of numbers.

        Args:
            parameters (MultiplicationParams): The numbers to multiply.

        Returns:
            int: The product of the numbers.
        """
        product = 1
        for number in parameters.numbers:
            product *= number
        return product
