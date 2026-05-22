"""
10. Cockcroft-Gault Creatinine Clearance 계산 정답
"""

age = int(input("나이: "))
weight = float(input("체중(kg): "))
sex = input("성별(M/F): ")
creatinine = float(input("혈청 Creatinine(mg/dL): "))

if sex == "F":
    sex_factor = 0.85
else:
    sex_factor = 1

crcl = ((140 - age) * weight * sex_factor) / (72 * creatinine)

if crcl < 30:
    interpretation = "CrCl 감소: 신기능 저하 가능"
elif crcl < 60:
    interpretation = "CrCl 경도 감소 가능"
else:
    interpretation = "CrCl 보존 범위"

print(f"Creatinine Clearance: {crcl:.1f} mL/min")
print(f"해석: {interpretation}")
