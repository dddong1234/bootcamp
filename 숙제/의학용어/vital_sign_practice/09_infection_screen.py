"""
09. 감염 의심 환자 SIRS 기준 세기

개념:
- SIRS 예시 기준:
  체온 > 38 또는 < 36
  맥박 > 90
  호흡수 > 20
  WBC > 12000 또는 < 4000

목표:
- 여러 임상 지표를 한 번에 평가하기
- 기준을 몇 개 만족하는지 세어보기

실습:
- ____ 또는 ??? 부분을 알맞은 기준 또는 증가값으로 채우세요.

주의:
- 교육용 단순화 예시입니다.
- SIRS만으로 감염이나 패혈증을 진단하지 않습니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

temperature = float(input("체온(C): "))
pulse = int(input("맥박(회/분): "))
respiration = int(input("호흡수(회/분): "))
wbc = int(input("WBC(/uL): "))

sirs_count = 0

if temperature > ??? or temperature < ???:
    sirs_count += ____

if pulse > ???:
    sirs_count += ____

if respiration > ???:
    sirs_count += ____

if wbc > ??? or wbc < ???:
    sirs_count += ____

if sirs_count >= ???:
    result = "SIRS 기준 2개 이상: 감염 여부와 전신 상태 평가 필요"
else:
    result = "SIRS 기준 2개 미만"

print(f"SIRS 기준 개수: {sirs_count}")
print(result)
