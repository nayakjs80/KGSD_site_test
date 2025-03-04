import re

def is_valid_ssn(ssn):
    """
    한국 주민등록번호 유효성 검사 함수
    :param ssn: 주민등록번호 (형식: 123456-1234567)
    :return: 유효하면 True, 그렇지 않으면 False
    """
    if not re.match(r'^\d{6}-\d{7}$', ssn):
        return False

    digits = [int(d) for d in ssn.replace('-', '')]
    if len(digits) != 13:
        return False

    weights = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    checksum = sum(w * d for w, d in zip(weights, digits[:-1])) % 11
    check_digit = (11 - checksum) % 10

    return check_digit == digits[-1]

# # 예제 사용
# ssn = "123456-1234567"
# if is_valid_ssn(ssn):
#     print("유효한 주민등록번호입니다.")
# else:
#     print("유효하지 않은 주민등록번호입니다.")