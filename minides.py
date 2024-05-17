from utils import *
import random

EXPANSION_LIST = [[8, 1, 2, 3, 4, 5], [4, 5, 6, 7, 8, 1]]

PERMUTATION_LIST = [[2, 8, 4, 7], [6, 5, 3, 1]]

PERMUTED_CHOICE_LIST = [[8, 7, 1, 4, 10, 5], [3, 9, 2, 12, 6, 11]]

sbox1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
]

sbox2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
]


def generate_16_bit_message():
    # Générer un nombre aléatoire entre 0 et 65535 (inclus), qui est la plage des nombres de 16 bits
    number = random.randint(0, 65535)
    # Convertir ce nombre en une chaîne binaire de 16 bits
    message = format(number, "016b")
    return message


def permutation(message: int, list_to_rearrange):
    # EXPANSION_LIST

    l1, l2 = [], []
    for index in list_to_rearrange[0]:
        l1 += message[index - 1]
    for index in list_to_rearrange[1]:
        l2 += message[index - 1]

    result = l1 + l2
    return "".join(result)


def sbox_switch(xor_result, sbox):
    first_bit = xor_result[0]
    last_bit = xor_result[-1]

    row_index = int(first_bit + last_bit, 2)

    middle_bits = xor_result[1:-2]

    column_index = int(middle_bits, 2)

    value = sbox[row_index][column_index]

    # convert to bits
    return format(value, "b").zfill(4)


def minides_encrypt(message, key):
    # Split en 2
    message_left, message_right = message[:8], message[8:]

    for i in range(16):
        # Expansion step
        expansion_result = permutation(message_right, EXPANSION_LIST)
        # XOR on Expansion result + Key
        xor_result = xor(expansion_result, key)
        # Split
        l1, l2 = xor_result[:6], xor_result[6:]
        # S-box step
        sbox_result = sbox_switch(l1, sbox1) + sbox_switch(l2, sbox2)
        # Permutation Step
        permutation_result = permutation(sbox_result, PERMUTATION_LIST)
        round_result = xor(message_left, permutation_result)
        # Reassign values to vars
        message_left = message_right
        message_right = round_result
        # shift left
        nth_shift = 1 if i in (0, 1, 8, 15) else 2
        message_left = shift_left(message_left, nth_shifts=nth_shift)
        message_right = shift_left(message_right, nth_shifts=nth_shift)
        # permute keys
        key = permutation(key, PERMUTED_CHOICE_LIST)

    print(message_left, message_right, key)
    return message_left, message_right, key


# Exemple d'utilisation
# message = generate_16_bit_message()
message = "0110010011100101".zfill(16)
print("Message de 16 bits:", message)
key = "101011110010".zfill(12)
minides_encrypt(message=message, key=key)