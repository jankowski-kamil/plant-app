from django.core.exceptions import ValidationError


class PasswordValidator:
    def __init__(
        self,
        min_length=8,
        number_of_capitals=1,
        number_of_lowercase=1,
        number_of_numbers=1,
        symbols="[~!@#$%^&*()_+{}\":;'[]",
        number_of_symbols=2,
    ):
        self.min_length = min_length
        self.number_of_capitals = number_of_capitals
        self.number_of_lowercase = number_of_lowercase
        self.numbers = number_of_numbers
        self.symbols = symbols
        self.number_of_symbols = number_of_symbols

    def validate(self, password, user=None):
        capitals = [char for char in password if char.isupper()]
        lower = [char for char in password if char.islower()]
        numbers = [char for char in password if char.isnumeric()]
        symbols = [char for char in password if char in self.symbols]
        if len(password) < self.min_length:
            raise ValidationError(
                f"Your password is too short. Min length is {self.min_length}",
            )
        if len(capitals) < self.number_of_capitals:
            raise ValidationError(
                f"Your password is too short. Number of capitals is {self.number_of_capitals}",
            )
        if len(lower) < self.number_of_lowercase:
            raise ValidationError(
                f"Your password is too short. Number of lowercase is {self.number_of_lowercase}",
            )
        if len(numbers) < self.numbers:
            raise ValidationError(
                f"Your password is too short. Number of numbers is {self.numbers}",
            )
        if len(symbols) < self.number_of_symbols:
            raise ValidationError(
                f"Your password is too short. Number of symbols is {self.number_of_symbols}",
            )
