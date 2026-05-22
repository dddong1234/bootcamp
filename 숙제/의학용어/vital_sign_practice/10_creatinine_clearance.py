"""
10. Cockcroft-Gault Creatinine Clearance 계산

참고:
- Clinical-Analysis/Medcalc의 Creatinine_Clearance.py 계산 구조를 참고했습니다.

개념:
- CrCl = ((140 - 나이) * 체중 * 성별 보정계수) / (72 * 혈청 Cr)
- 여성 보정계수 예시: 0.85

목표:
- 신장 기능을 추정하는 계산식을 이해하기
- 나이, 체중, 성별, creatinine이 결과에 미치는 영향을 보기

실습:
- ____ 또는 ??? 부분을 알맞은 값 또는 계산식으로 채우세요.

주의:
- 교육용 단순화 예시입니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

age = int(input("나이: "))
weight = float(input("체중(kg): "))
sex = input("성별(M/F): ")
creatinine = float(input("혈청 Creatinine(mg/dL): "))

if sex == "F":
    sex_factor = ???
else:
    sex_factor = ____

crcl = ((??? - age) * weight * sex_factor) / (??? * creatinine)

if crcl < ???:
    interpretation = "CrCl 감소: 신기능 저하 가능"
elif crcl < ???:
    interpretation = "CrCl 경도 감소 가능"
else:
    interpretation = "CrCl 보존 범위"

print(f"Creatinine Clearance: {crcl:.1f} mL/min")
print(f"해석: {interpretation}")
