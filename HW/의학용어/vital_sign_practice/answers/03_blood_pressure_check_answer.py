"""
03. 혈압 판정 연습 정답
"""

systolic = int(input("수축기 혈압을 입력하세요(mmHg): "))
diastolic = int(input("이완기 혈압을 입력하세요(mmHg): "))

if systolic >= 180 or diastolic >= 120:
    message = "매우 높은 혈압: 즉시 보고 필요"
elif systolic >= 140 or diastolic >= 90:
    message = "높은 혈압"
elif systolic < 90 or diastolic < 60:
    message = "낮은 혈압 가능성"
else:
    message = "일반적인 범위"

print(f"혈압 {systolic}/{diastolic} mmHg")
print(message)
