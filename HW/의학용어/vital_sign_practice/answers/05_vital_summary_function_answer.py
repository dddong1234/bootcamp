"""
05. 활력징후 요약 함수 만들기 정답
"""


def count_warning_signs(vital):
    warning_count = 0

    if vital["temperature"] >= 38.0:
        warning_count += 1

    if vital["pulse"] < 60 or vital["pulse"] > 100:
        warning_count += 1

    if vital["respiration"] < 12 or vital["respiration"] > 20:
        warning_count += 1

    if vital["systolic_bp"] < 90 or vital["systolic_bp"] >= 140:
        warning_count += 1

    if vital["spo2"] < 95:
        warning_count += 1

    return warning_count


def print_vital_summary(vital):
    print()
    print("활력징후 요약")
    print("-" * 30)
    print(f"환자 이름: {vital['name']}")
    print(f"체온: {vital['temperature']} C")
    print(f"맥박: {vital['pulse']} 회/분")
    print(f"호흡수: {vital['respiration']} 회/분")
    print(f"혈압: {vital['systolic_bp']}/{vital['diastolic_bp']} mmHg")
    print(f"산소포화도: {vital['spo2']}%")

    warning_count = count_warning_signs(vital)
    print(f"주의 항목 개수: {warning_count}")

    if warning_count == 0:
        print("특별한 주의 항목이 없습니다.")
    elif warning_count <= 2:
        print("주의 깊게 관찰하고 필요 시 보고하세요.")
    else:
        print("여러 항목이 범위를 벗어났습니다. 빠른 보고가 필요합니다.")


patient_vital = {
    "name": input("환자 이름: "),
    "temperature": float(input("체온(C): ")),
    "pulse": int(input("맥박(회/분): ")),
    "respiration": int(input("호흡수(회/분): ")),
    "systolic_bp": int(input("수축기 혈압(mmHg): ")),
    "diastolic_bp": int(input("이완기 혈압(mmHg): ")),
    "spo2": int(input("산소포화도(%): ")),
}

print_vital_summary(patient_vital)
