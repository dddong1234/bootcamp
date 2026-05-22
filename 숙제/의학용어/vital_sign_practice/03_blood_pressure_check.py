"""
03. 혈압 판정 연습

목표:
- 여러 값을 입력받기
- and / or 조건 사용하기
- 조건 순서가 결과에 영향을 줄 수 있음을 이해하기

실습:
- ____ 또는 ??? 부분을 알맞은 코드/기준값으로 채우세요.

주의:
- 아래 기준은 수업용 단순 예시입니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

systolic = ____(input("수축기 혈압을 입력하세요(mmHg): "))
diastolic = ____(input("이완기 혈압을 입력하세요(mmHg): "))

if systolic >= ??? or diastolic >= ???:
    message = "매우 높은 혈압: 즉시 보고 필요"
elif systolic >= ??? or diastolic >= ???:
    message = "높은 혈압"
elif systolic < ??? or diastolic < ???:
    message = "낮은 혈압 가능성"
else:
    message = ____

print(f"혈압 {systolic}/{diastolic} mmHg")
print(message)
