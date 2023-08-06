"""
Contains the methods to decipher the equation cipher method.
"""
import base64
import sys
from time_handler import TimeConverter
sys.path.append('..')


class Decrypter(object):
    """
    Class to decrypt the equation cipher encryption.
    Note: This decryption can not be done complete decryption but partial
    decryption can be done and string passed can be verified at some stage of
    encryption.
    """

    def __init__(self):
        self.coverter = TimeConverter()

    def decrypt(self, hash_str: bytes) -> str:
        """
        Function to decrypt the passed the hash
        :param hash_str: the hash which needs to be decrypted

        :return: decrypted data
        """
        decrypted_hash = base64.b64decode(hash_str).decode('utf-8')
        equation = decrypted_hash.split("=")[0]
        epoch = float(decrypted_hash.split("=")[1])
        data = self.break_and_check(equation, epoch)
        return data

    def break_and_check(self, equation: str, epoch: float) -> str:
        date_obj = self.coverter.epoch_to_datetime(epoch)

        addition_factor = date_obj.day + date_obj.month + date_obj.year

        mult_factor = date_obj.hour + date_obj.minute + date_obj.second

        terms = equation.split("-")
        all_terms = []

        for term in terms:
            if "+" in term:
                all_terms.extend(term.split("+"))
            else:
                all_terms.append(term)
        data = ""

        for term in all_terms:
            data += self.break_the_term(term, addition_factor,
                                        mult_factor)

        return data

    def break_the_term(self, term: str, addition_factor: int,
                       mult_factor: int) -> str:
        char = ''
        if term.isdigit():
            value = int(int(term) / mult_factor)
            value -= addition_factor
            char = chr(value)

        elif 'Y' in term:
            value = int(term.split("^")[1])
            value = value - mult_factor
            value = int(value / addition_factor)
            char = chr(value)

        elif 'x' in term:
            mult = int(term.split('x^')[0])
            pow_val = int(term.split('x^')[1])

            mult = int(mult / mult_factor)
            pow_val = pow_val - mult_factor

            mult = mult - addition_factor
            pow_val = pow_val - addition_factor

            if pow_val == 1:
                char = chr(78 + (mult - 1))

            elif pow_val == 2:
                if mult in (range(1, 4)):
                    adding = 78
                else:
                    adding = 65
                char = chr((adding + (mult - 1)))

            elif pow_val == 3:
                char = chr(72 + (mult - 1))

        elif 'X' in term:
            mult = int(term.split('X^')[0])
            pow_val = int(term.split('X^')[1])

            mult = int(mult / mult_factor)
            pow_val = pow_val - mult_factor

            mult = mult - addition_factor
            pow_val = pow_val - addition_factor

            if pow_val == 1:
                char = chr(104 + (mult - 1))

            elif pow_val == 2:
                if mult in (range(1, 10)):
                    adding = 114
                    char = chr((adding + (mult - 1)))
                else:
                    adding = 97
                    char = chr(adding)

            elif pow_val == 3:
                char = chr(98 + (mult - 1))

        return char
