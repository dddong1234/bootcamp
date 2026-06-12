"""
06. 산소포화도 우선순위 판단

참고:
- Clinical-Analysis/Medcalc의 oxygen saturation, vital sign 참고치 구조를 참고했습니다.

목표:
- 산소포화도(SpO2)를 보고 우선순위를 나누기
- 호흡곤란 여부를 함께 고려하기

실습:
- ____ 또는 ??? 부분을 알맞은 의학 기준 또는 값으로 채우세요.

주의:
- 교육용 단순화 예시입니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

spo2 = int(input("산소포화도 SpO2(%): "))
dyspnea = input("호흡곤란이 있나요? (y/n): ")

if spo2 < ??? or dyspnea == "???":
    priority = "응급: 즉시 보고 및 산소 공급 준비"
elif spo2 < ???:
    priority = "주의: 재측정하고 증상 확인"
elif spo2 < ???:
    priority = "관찰: 정상 범위에 가까움"
else:
    priority = "정상 범위"

print(f"SpO2: {spo2}%")
print(f"호흡곤란: {dyspnea}")
print(f"판정: {priority}")
