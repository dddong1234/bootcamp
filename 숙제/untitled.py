patients = [
    {"name": "김환자", "age": 65, "systolic": 145},
    {"name": "이환자", "age": 45, "systolic": 125},
    {"name": "박환자", "age": 32, "systolic": 115},
    {"name": "최환자", "age": 28, "systolic": 135},
    {"name": "정환자", "age": 70, "systolic": 190}
]

htn_class = [
    "정상",
    "고혈압 전단계",
    "1기 고혈압",
    "2기 고혈압"
]

htn_action = {
    "정상": "정기 검진",
    "고혈압 전단계": "생활습관 개선",
    "1기 고혈압": "약물 치료 필요",
    "2기 고혈압": "즉시 치료 필요"
}

htn_list = {cls: [] for cls in htn_class}

def classify_htn(systolic):
    if systolic < 120: return 0
    if systolic < 140: return 1
    if systolic < 160: return 2
    return 3

def classify_emergency(patient):
    systolic = patient["systolic"]
    return systolic >= 180


print("=== 개별 환자 혈압 분류 ===")
htn_count:int = 0
em_count:int = 0
for patient in patients:
    if patient["systolic"] >= 140:
        htn_count += 1
    if patient["systolic"] >= 180:
        em_count += 1
    code = classify_htn(patient["systolic"])
    label = htn_class[code]
    htn_list[label].append(patient)
    name = patient["name"]
    age = patient["age"]
    systolic = patient["systolic"]
    print(f"{name}({age}세): {systolic} mmHg - {label} ({htn_action[label]})")

print("\n")
print("=== 응급 처치 대상 ===")
for patient in patients:
    if classify_emergency(patient):
        name = patient["name"]
        systolic = patient["systolic"]
        print(f'🚨 응급 : {name}({systolic} mmHg) - 즉시 치료 필요')
        break

print("\n")

print("=== 혈압 등급별 통계 ===")
total_patents = len(patients)
for stage, patients_by_stage in htn_list.items():
    print(f"{stage}: {len(patients_by_stage)}명 ({(len(patients_by_stage)/total_patents):.1%})")

print("\n")

print("=== 전체 현황 요약 ===")
print(f"총 환자수: {len(patients)}명")
systolics = [patient["systolic"] for patient in patients]
print(f"평균 혈압: {sum(systolics)/total_patents:.1f} mmHg")
print(f"고혈압 환자: {htn_count}명 ({htn_count/total_patents:.1%})")
print(f"응급 처치 대상: {em_count}명")