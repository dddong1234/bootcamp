"""
04. 여러 번 측정한 활력징후 평균 구하기 정답
"""

pulses = []

print("맥박을 3번 입력해 평균을 구합니다.")

for count in range(1, 4):
    pulse = int(input(f"{count}번째 맥박(회/분): "))
    pulses.append(pulse)

average_pulse = sum(pulses) / len(pulses)

print()
print(f"입력값: {pulses}")
print(f"평균 맥박: {average_pulse:.1f} 회/분")

if average_pulse < 60:
    print("평균 맥박이 낮은 편입니다.")
elif average_pulse <= 100:
    print("평균 맥박이 일반적인 범위입니다.")
else:
    print("평균 맥박이 높은 편입니다.")
