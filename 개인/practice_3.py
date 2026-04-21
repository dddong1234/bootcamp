test_patients = [
    ("P001", "김환자", "감기"),
    ("P002", "이환자", "두통"),
    ("", "박환자", "복통"),      # 오류 케이스: 빈 ID
    ("P003", "", "발열"),        # 오류 케이스: 빈 이름
    ("P004", "최환자", "고혈압")
]

test_lookups = ["P001", "P002", "P999"]

def save_patient(patient_id, name, diagnosis):
    try:
        if not patient_id or not name:
            raise ValueError("환자 ID와 이름은 필수입니다")

        with open(f"{patient_id}.txt", "w", encoding = 'utf-8') as patients_file:
            patients_file.write(f"환자명: {name}\n진단: {diagnosis}\n")
            print(f"✅ {name} 환자 저장 완료")
    except ValueError as e:
        print(f"❌ 오류: {e}")
    except OSError as e:
        print(f"❌ 파일 처리 오류: {e}")




def load_patient(patient_id):
    try:
        with open(patient_id, "r", encoding = 'utf-8') as patients_file:
            print(f"✅ {patient_id} 환자 조회 완료")
            return patients_file.read()
    except FileNotFoundError:
        print(f"❌ 환자 {patient_id}를 찾을 수 없습니다.")

print("=== 환자 등록 테스트 ===")
for patient_id, name, diagnosis in test_patients:
    save_patient(patient_id, name, diagnosis)

# 2. 환자 조회 테스트
print("\n=== 환자 조회 테스트 ===")
for patient_id in test_lookups:
    content = load_patient(patient_id)
    if content:
        print(content)