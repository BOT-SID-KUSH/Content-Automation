from typing import List

# Initialize base64 encoding/decoding arrays
b64_to_i = {}
i_to_b64 = {}

num_base = ord('0')
lower_case_base = ord('a') 
upper_case_base = ord('A')

# Initialize digit mappings (0-9)
for i in range(10):
    b64_to_i[num_base + i] = i
    i_to_b64[i] = chr(num_base + i)

# Initialize letter mappings (a-z, A-Z)
for i in range(26):
    b64_to_i[lower_case_base + i] = i + 10
    i_to_b64[i + 10] = chr(lower_case_base + i)
    b64_to_i[upper_case_base + i] = i + 36
    i_to_b64[i + 36] = chr(upper_case_base + i)

# Add special characters
b64_to_i[ord('-')] = 62
i_to_b64[62] = '-'
b64_to_i[ord('_')] = 63
i_to_b64[63] = '_'

def count_set_bits(n: int) -> int:
    """
    Counts the number of set bits (1s) in the binary representation of an integer.

    :param n: The integer to count set bits in.
    :return: The number of set bits.
    """
    count = 0
    while n > 0:
        count += n & 1  # Add 1 if the least significant bit is set
        n >>= 1         # Right shift n by 1 bit
    return count

def pop_count(v: int) -> int:
    """
    Efficiently counts the number of 1 bits (population count) in an integer using bit manipulation.
    
    This is an implementation of the Hamming Weight algorithm that uses parallel bit counting:
    1. First groups bits into pairs and counts 1s in each pair
    2. Then groups into nibbles (4 bits) and sums the counts
    3. Finally multiplies and shifts to sum all the nibbles
    
    For example:
    v = 14 (binary 1110)
    Step 1: Groups bits into pairs -> (01,11,00)
    Step 2: Groups into nibbles -> (0011)
    Step 3: Returns 3 (number of 1 bits)
    
    Args:
        v: Integer to count bits in
        
    Returns:
        Number of 1 bits in the integer
    """
  

    v = v - ((v >> 1) & 0x55555555)  # Count pairs of bits
    v = (v & 0x33333333) + ((v >> 2) & 0x33333333)  # Count nibbles
    return (((v + (v >> 4)) & 0xf0f0f0f) * 0x1010101) >> 24  # Sum all nibbles

BitArray = List[int]

__all__ = [
    'BitArray',
    'zero',
    'from_string', 
    'is_zero',
    'clamp',
    'set_bit',
    'to_string',
    'bit_length',
    'bit_count',
    'and_bits',
    'in_place_and',
    'active_bits'
]

def zero() -> BitArray:
    return [0]

def from_string(input_str: str, base: int) -> BitArray:
    if base == 32:
        input_str = input_str.lower()
    
    bits_per_char = 5 if base == 32 else 6
    chars_per_num = 6 if base == 32 else 5

    nums = []
    used_ints = 0

    for i in range(len(input_str)):
        index = len(input_str) - i - 1
        x = b64_to_i[ord(input_str[index])]
        mod = i % chars_per_num
        if mod == 0:
            nums.append(x)
            used_ints += 1
        else:
            nums[used_ints - 1] |= x << (mod * bits_per_char)
    return nums

def is_zero(ba: BitArray) -> bool:
    return len(ba) == 0 or (len(ba) == 1 and ba[0] == 0)

def clamp(ba: BitArray) -> None:
    while len(ba) > 1 and ba[-1] == 0:
        ba.pop()

def set_bit(ba: BitArray, index: int) -> None:
    num_index = index // 30
    rem = index % 30
    while len(ba) < num_index + 1:
        ba.append(0)
    ba[num_index] |= 1 << rem

def unset_bit(ba: BitArray, index: int) -> None:
    num_index = index // 30
    rem = index % 30
    if num_index < len(ba):
        ba[num_index] &= ~(1 << rem)
        clamp(ba)


def to_string(ba: BitArray, base: int) -> str:
    bits_per_char = 5 if base == 32 else 6
    chars_per_num = 6 if base == 32 else 5
    mask = (1 << bits_per_char) - 1
    s = ''
    
    for i in range(len(ba)-1, -1, -1):
        for j in range(chars_per_num-1, -1, -1):
            char = i_to_b64[(ba[i] >> (j * bits_per_char)) & mask]
            if s or char != '0':
                s += char
    return s or '0'

def bit_length(ba: BitArray) -> int:
    if not ba:
        return 0
    return 30 * (len(ba) - 1) + (32 - ba[-1].bit_length())

def bit_count(ba: BitArray) -> int:
    return sum(count_set_bits(bit) for bit in ba if bit)

def and_bits(ba: BitArray, other: BitArray) -> BitArray:
    nums = []
    used_ints = min(len(ba), len(other))
    
    for i in range(used_ints):
        nums.append(ba[i] & other[i])
        
    clamp(nums)
    return nums

def in_place_and(ba: BitArray, other: BitArray) -> None:
    for i in range(len(ba)):
        if i < len(other):
            ba[i] &= other[i]
        else:
            ba[i] = 0
    clamp(ba)

def active_bits(ba: BitArray) -> list[int]:
    ret = []
    for i in range(len(ba)-1, -1, -1):
        num = ba[i]
        while num != 0:
            t = num.bit_length() - 1
            num ^= 1 << t
            ret.append(i * 30 + t)
    return ret
