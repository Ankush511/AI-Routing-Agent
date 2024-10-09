from dataclasses import dataclass

@dataclass
class VowelCountParams:
    text: str

class VowelCounter:
    """Counts the number of vowels in a string."""

    def count_vowels(self, parameters: VowelCountParams) -> int:
        """
        Returns the number of vowels in the input text.

        Args:
            parameters (VowelCountParams): The text to analyze.

        Returns:
            int: The count of vowels.
        """
        vowels = 'aeiouAEIOU'
        return sum(1 for char in parameters.text if char in vowels)
