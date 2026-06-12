"""
04. 여러 번 측정한 활력징후 평균 구하기

목표:
- 리스트(list)에 숫자 저장하기
- for 반복문 사용하기
- sum(), len()으로 평균 계산하기

실습:
- ____ 또는 ??? 부분을 알맞은 코드/기준값으로 채우세요.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""

pulses = ____

print("맥박을 3번 입력해 평균을 구합니다.")

for count in range(____, ____):
    pulse = ____(input(f"{count}번째 맥박(회/분): "))
    pulses.____(pulse)

average_pulse = ____(pulses) / ____(pulses)

print()
print(f"입력값: {pulses}")
print(f"평균 맥박: {average_pulse:.1f} 회/분")

if average_pulse < ???:
    print("평균 맥박이 낮은 편입니다.")
elif average_pulse <= ???:
    print("평균 맥박이 일반적인 범위입니다.")
else:
    print("평균 맥박이 높은 편입니다.")
