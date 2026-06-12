"""
08. CBC로 빈혈과 MCV 해석하기

참고:
- Clinical-Analysis/Medcalc의 CBC reference ranges를 참고했습니다.
- Hb 참고치 예시: 남성 13.5-17.5 g/dL, 여성 12.0-16.0 g/dL
- MCV 참고치 예시: 80-100 fL

목표:
- 성별에 따라 Hb 기준을 다르게 적용하기
- MCV로 microcytic/normocytic/macrocytic 방향을 나누기

실습:
- ____ 또는 ??? 부분을 알맞은 기준 또는 판정으로 채우세요.

주의:
- 교육용 단순화 예시입니다.
- 실제 빈혈 평가는 출혈, 철분, ferritin, B12/folate, 만성질환 등을 함께 봅니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

sex = input("성별(M/F): ")
hemoglobin = float(input("Hemoglobin(g/dL): "))
mcv = float(input("MCV(fL): "))

if sex == "M":
    anemia_cutoff = ???
else:
    anemia_cutoff = ____

if hemoglobin < ???:
    anemia_result = "빈혈 가능"
else:
    anemia_result = "Hb 정상 범위"

if mcv < ???:
    mcv_result = "소구성 경향"
elif ____:
    mcv_result = "대구성 경향"
else:
    mcv_result = "정구성 범위"

print(f"Hb: {hemoglobin} g/dL")
print(f"MCV: {mcv} fL")
print(f"빈혈 판정: {anemia_result}")
print(f"MCV 해석: {mcv_result}")
