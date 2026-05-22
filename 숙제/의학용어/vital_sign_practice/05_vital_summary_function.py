"""
05. 활력징후 요약 함수 만들기

목표:
- 딕셔너리(dict)로 환자 정보 저장하기
- 함수를 만들어 코드 정리하기
- 간단한 위험 신호 개수 세기

실습:
- ____ 또는 ??? 부분을 알맞은 코드/기준값으로 채우세요.

주의:
- 이 파일은 프로그래밍 실습용입니다.
- https://www.mdcalc.com/
- 위 사이트에서 체온과 관련된 reference range를 참고하여 기준값을 채워보세요.
"""


def ____(vital):
    warning_count = 0

    if vital["temperature"] >= ???:
        warning_count += ____

    if vital["pulse"] < ??? or vital["pulse"] > ???:
        warning_count += ____

    if vital["respiration"] < ??? or vital["respiration"] > ???:
        warning_count += ____

    if vital["systolic_bp"] < ??? or vital["systolic_bp"] >= ???:
        warning_count += ____

    if vital["spo2"] < ???:
        warning_count += ____

    return ____


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

    warning_count = ____(vital)
    print(f"주의 항목 개수: {warning_count}")

    if warning_count == 0:
        print("특별한 주의 항목이 없습니다.")
    elif warning_count <= 2:
        print("주의 깊게 관찰하고 필요 시 보고하세요.")
    else:
        print("여러 항목이 범위를 벗어났습니다. 빠른 보고가 필요합니다.")


patient_vital = {
    "name": input("환자 이름: "),
    "temperature": ____(input("체온(C): ")),
    "pulse": ____(input("맥박(회/분): ")),
    "respiration": ____(input("호흡수(회/분): ")),
    "systolic_bp": ____(input("수축기 혈압(mmHg): ")),
    "diastolic_bp": ____(input("이완기 혈압(mmHg): ")),
    "spo2": ____(input("산소포화도(%): ")),
}

print_vital_summary(patient_vital)
