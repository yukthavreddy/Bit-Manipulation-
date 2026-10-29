def float_to_fixed_8bit(val: float) -> int:
    scaled = int(round(val * 16))
    return scaled & 0xFF

def to_binary_str(val: int) -> str:
    b_str = f"{val & 0xFF:08b}"
    return f"{b_str[:4]}.{b_str[4:]}"

def fixed_to_signed_decimal(val: int) -> float:
    val = val & 0xFF
    if val >= 128:
        val = val - 256
    return val / 16.0

def add_8bit(a_val: int, b_val: int):
    a_bin = a_val & 0xFF
    b_bin = b_val & 0xFF
    carry = 0
    carry_into_msb = 0
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
        "res_bin_raw": result_bin,
        "carry_out": carry_out_msb,
        "overflow": overflow,
    }

def sub_fixed_8bit(a_float: float, b_float: float):
    a_scaled = float_to_fixed_8bit(a_float)
    b_scaled = float_to_fixed_8bit(b_float)
    
    b_neg_scaled = (~b_scaled + 1) & 0xFF
    
    addition_result = add_8bit(a_scaled, b_neg_scaled)
    res_bin = addition_result["res_bin_raw"]
    
    return {
        "op_a_bin": to_binary_str(a_scaled),
        "op_b_bin": to_binary_str(b_scaled),
        "op_b_neg_bin": to_binary_str(b_neg_scaled),
        "res_bin": to_binary_str(res_bin),
        "res_dec": fixed_to_signed_decimal(res_bin),
        "expected_dec": a_float - b_float,
        "carry_out": addition_result["res_bin_raw"],
        "overflow": addition_result["overflow"],
    }

def display_verification(label: str, a: float, b: float):
    res = sub_fixed_8bit(a, b)

    print(f"=== Expression {label}: ({a}) - ({b}) ===")
    print(f"  Operand A (Binary):     {res['op_a_bin']} ({a})")
    print(f"  Operand B (Binary):     {res['op_b_bin']} ({b})")
    print(f"  Operand -B (2's Comp):  {res['op_b_neg_bin']} (-{b})")
    print(f"  Result Binary:          {res['res_bin']}")
    print(f"  Result Decimal:         {res['res_dec']}")
    print(f"  Expected Decimal:       {res['expected_dec']}")
    print(f"  Overflow:               {'YES (Arithmetic Overflow)' if res['overflow'] else 'NO'}")
    print()

display_verification("(a)", 1.5, 0.25)