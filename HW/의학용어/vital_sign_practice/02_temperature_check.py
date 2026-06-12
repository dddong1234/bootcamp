"""
02. 체온 판정 연습

목표:
- if / elif / else 조건문 사용하기
- 숫자 범위에 따라 메시지 출력하기

실습:
- ____ 또는 ??? 부분을 알맞은 코드/기준값으로 채우세요.

주의:
- 아래 기준은 파이썬 조건문 실습용 예시입니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

temperature = float(input("체온을 입력하세요(C): "))

if temperature < 36.0:
    result = "저체온 가능성"
elif temperature < 37.5:
    result = "정상 범위"
elif temperature < 38.0:
    result = "미열"
else:
    result = "고열"

print(f"체온 {temperature} C: {result}")
