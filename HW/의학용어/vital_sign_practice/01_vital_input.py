"""
01. 활력징후 입력 연습

목표:
- input()으로 값을 입력받기
- int(), float()으로 숫자 변환하기
- f-string으로 보기 좋게 출력하기

실습:
- ____ 부분을 알맞은 코드로 채우세요.
"""

print("활력징후 입력 연습")
print("-" * 30)

name = input("환자 이름: ")
temperature = float(input("체온(섭씨): "))
pulse = int(input("맥박(회/분): "))
respiration = int(input("호흡수(회/분): "))
bp = input("혈압: ").split("/")
systolic_bp = int(bp[0])
diastolic_bp = int(bp[1])
spo2 = float(input("산소포화도(%): "))

print()
print("입력한 활력징후")
print("-" * 30)
print(f"이름: {name}")
print(f"체온: {temperature} C")
print(f"맥박: {pulse} 회/분")
print(f"호흡수: {respiration} 회/분")
print(f"혈압: {systolic_bp}/{diastolic_bp} mmHg")
print(f"산소포화도: {spo2}%")
