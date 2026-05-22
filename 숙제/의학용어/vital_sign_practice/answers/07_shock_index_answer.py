"""
07. Shock Index 계산 정답
"""

pulse = int(input("맥박(회/분): "))
systolic_bp = int(input("수축기 혈압(mmHg): "))

shock_index = pulse / systolic_bp

if shock_index >= 1.0:
    risk = "높음: 순환 불안정 가능성"
elif shock_index >= 0.7:
    risk = "경계: 추적 관찰 필요"
else:
    risk = "낮음"

print(f"Shock Index: {shock_index:.2f}")
print(f"위험도: {risk}")
