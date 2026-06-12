"""
07. Shock Index 계산

개념:
- Shock Index = 맥박수 / 수축기 혈압
- 출혈, 패혈증, 탈수 등에서 순환 불안정을 의심할 때 참고할 수 있습니다.

목표:
- 활력징후 2개로 shock index를 계산하기
- 계산값에 따라 위험도를 분류하기

실습:
- ____ 또는 ??? 부분을 알맞은 계산식 또는 기준으로 채우세요.

주의:
- 교육용 단순화 예시입니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

pulse = int(input("맥박(회/분): "))
systolic_bp = int(input("수축기 혈압(mmHg): "))

shock_index = pulse / ???

if shock_index >= ???:
    risk = "높음: 순환 불안정 가능성"
elif shock_index >= ???:
    risk = "경계: 추적 관찰 필요"
else:
    risk = "낮음"

print(f"Shock Index: {shock_index:.2f}")
print(f"위험도: {risk}")
