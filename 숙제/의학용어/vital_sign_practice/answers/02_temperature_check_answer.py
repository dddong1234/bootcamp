"""
02. 체온 판정 연습 정답
"""

temperature = float(input("체온을 입력하세요(C): "))

if temperature < 35.0:
    result = "저체온 가능성"
elif temperature < 37.5:
    result = "정상 범위"
elif temperature < 38.0:
    result = "미열"
else:
    result = "발열"

print(f"체온 {temperature} C: {result}")
