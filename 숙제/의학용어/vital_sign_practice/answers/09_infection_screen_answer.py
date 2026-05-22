"""
09. 감염 의심 환자 SIRS 기준 세기 정답
"""

temperature = float(input("체온(C): "))
pulse = int(input("맥박(회/분): "))
respiration = int(input("호흡수(회/분): "))
wbc = int(input("WBC(/uL): "))

sirs_count = 0

if temperature > 38 or temperature < 36:
    sirs_count += 1

if pulse > 90:
    sirs_count += 1

if respiration > 20:
    sirs_count += 1

if wbc > 12000 or wbc < 4000:
    sirs_count += 1

if sirs_count >= 2:
    result = "SIRS 기준 2개 이상: 감염 여부와 전신 상태 평가 필요"
else:
    result = "SIRS 기준 2개 미만"

print(f"SIRS 기준 개수: {sirs_count}")
print(result)
