"""
01. 활력징후 입력 연습 정답
"""

print("활력징후 입력 연습")
print("-" * 30)

name = input("환자 이름: ")
temperature = float(input("체온(섭씨): "))
pulse = int(input("맥박(회/분): "))
respiration = int(input("호흡수(회/분): "))
systolic_bp = int(input("수축기 혈압(mmHg): "))
diastolic_bp = int(input("이완기 혈압(mmHg): "))
spo2 = int(input("산소포화도(%): "))

print()
print("입력한 활력징후")
print("-" * 30)
print(f"이름: {name}")
print(f"체온: {temperature} C")
print(f"맥박: {pulse} 회/분")
print(f"호흡수: {respiration} 회/분")
print(f"혈압: {systolic_bp}/{diastolic_bp} mmHg")
print(f"산소포화도: {spo2}%")
