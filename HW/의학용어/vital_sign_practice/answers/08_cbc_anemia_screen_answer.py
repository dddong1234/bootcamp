"""
08. CBC로 빈혈과 MCV 해석하기 정답
"""

sex = input("성별(M/F): ")
hemoglobin = float(input("Hemoglobin(g/dL): "))
mcv = float(input("MCV(fL): "))

if sex == "M":
    anemia_cutoff = 13.5
else:
    anemia_cutoff = 12.0

if hemoglobin < anemia_cutoff:
    anemia_result = "빈혈 가능"
else:
    anemia_result = "Hb 정상 범위"

if mcv < 80:
    mcv_result = "소구성 경향"
elif mcv > 100:
    mcv_result = "대구성 경향"
else:
    mcv_result = "정구성 범위"

print(f"Hb: {hemoglobin} g/dL")
print(f"MCV: {mcv} fL")
print(f"빈혈 판정: {anemia_result}")
print(f"MCV 해석: {mcv_result}")
