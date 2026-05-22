"""
06. 산소포화도 우선순위 판단 정답
"""

spo2 = int(input("산소포화도 SpO2(%): "))
dyspnea = input("호흡곤란이 있나요? (y/n): ")

if spo2 < 90 or dyspnea == "y":
    priority = "응급: 즉시 보고 및 산소 공급 준비"
elif spo2 < 94:
    priority = "주의: 재측정하고 증상 확인"
elif spo2 < 96:
    priority = "관찰: 정상 범위에 가까움"
else:
    priority = "정상 범위"

print(f"SpO2: {spo2}%")
print(f"호흡곤란: {dyspnea}")
print(f"판정: {priority}")
