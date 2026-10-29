def to_twos_comp_8bit(val: int) -> int:
    return val & 0xFF
def to_binary_str(val: int) -> str:
    return f"{to_twos_comp_8bit(val):08b}"
def to_signed_decimal(val: int) -> int:
    val = val & 0xFF
    return val - 256 if val >= 128 else val
def add_8bit(a_dec: int, b_dec: int):
    a_bin = to_twos_comp_8bit(a_dec)
    b_bin = to_twos_comp_8bit(b_dec)
    carry = 0
    carry_into_msb = 0
    carry_out_msb = 0
    result_bits = []
    for i in range(8):
        bit_a = (a_bin >> i) & 1
        bit_b = (b_bin >> i) & 1
        if i == 7:
            carry_into_msb = carry
        s = bit_a ^ bit_b ^ carry
        carry = (bit_a & bit_b) | (carry & (bit_a ^ bit_b))
        result_bits.append(str(s))
    carry_out_msb = carry
    result_bin = int("".join(reversed(result_bits)), 2)
    overflow = bool(carry_into_msb ^ carry_out_msb)
    return {
        "op_a_bin": to_binary_str(a_bin),
        "op_b_bin": to_binary_str(b_bin),
        "res_bin": to_binary_str(result_bin),
        "res_dec": to_signed_decimal(result_bin),
        "expected_dec": a_dec + b_dec,
        "carry_out": carry_out_msb,
        "overflow": overflow,
    }
def sub_8bit(a_dec: int, b_dec: int):
    return add_8bit(a_dec, -b_dec)
def display_verification(label: str, a: int, b: int, is_subtraction: bool = False):
    symbol = "-" if is_subtraction else "+"
    res = sub_8bit(a, b) if is_subtraction else add_8bit(a, b)

    print(f"=== Expression {label}: ({a:+d}) {symbol} ({b:+d}) ===")
    print(f"  Operand A:  {res['op_a_bin']} ({a:+d})")
    print(f"  Operand B:  {res['op_b_bin']} ({b:+d})")
    print(f"  Carry-Out:  {res['carry_out']}")
    print(f"  Result Bin: {res['res_bin']}")
    print(f"  Result Dec: {res['res_dec']}")
    print(f"  Overflow:   {'YES (Arithmetic Overflow)' if res['overflow'] else 'NO'}")
    print()
display_verification("(a)", 20, 15)
display_verification("(b)", -20, -15)