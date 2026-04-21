class MedicalStaff:
    def __init__(self,name:str,department:str):
        self.name = name
        self.department = department
        self.status = "근무중"

    def change_status(self,new_status):
        self.status = new_status

    def get_info(self):
        return f"{self.name}({self.department}) - {self.status}"

class Nurse(MedicalStaff):
    def __init__(self,name:str,department:str):
        super().__init__(name,department)
        self.patients = []

    def assign_patient(self,patient_name:str):
        if self.status != "근무중":
            return f"{self.name} {self.status}, 환자 배정 불가"
        if patient_name in self.patients:
            return f"{patient_name}은(는) {self.name}가 이미 담당 중인 환자입니다."
        self.patients.append(patient_name)
        return f"{self.name}에게 {patient_name} 배정 완료"

class Doctor(MedicalStaff):
    def __init__(self,name:str,department:str,specialty:str):
        super().__init__(name,department)
        self.specialty = specialty

    def treat_patient(self,patient_name:str,diagnosis:str):
        if self.status != "근무중":
            return f"{self.name} {self.status}. 진료 불가"
        return f"{self.name}가 {patient_name}을(를) {diagnosis}로 진료했습니다"

nurse = Nurse("김간호사", "내과")
doctor = Doctor("이의사", "외과", "정형외과")

# 환자 배정
print("=== 환자 배정 결과 ===")
print(nurse.assign_patient("환자A"))
print(nurse.assign_patient("환자B"))

# 의사 상태 변경
doctor.change_status("휴무중")
print("이의사는 현재 휴무중이므로 환자 배정 불가")

# 현재 상황 출력
print("\n=== 의료진 현황 ===")
print(nurse.get_info())
print(doctor.get_info())

# 의사 근무 복귀 후 진료
doctor.change_status("근무중")
print("\n=== 진료 결과 ===")
print(doctor.treat_patient("환자D", "무릎 관절염"))