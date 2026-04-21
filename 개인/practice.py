clinic_info = {
    "operating_hours": (9, 18),    # 클리닉 운영시간: 9시-18시
    "lunch_break": (12, 13),       # 점심시간: 12시-13시
}

# 예약 현황 리스트 (전역 변수)
appointments = []  # 딕셔너리 리스트: [{"time": 10, "patient": 김환자}, ...]


# 상태 키워드
AVAILABLE = "AVAILABLE"           # 예약 가능
LUNCH_TIME = "LUNCH_TIME"         # 점심시간
OUT_OF_HOURS = "OUT_OF_HOURS"     # 운영시간 외
ALREADY_BOOKED = "ALREADY_BOOKED"
START_TIME , END_TIME = clinic_info["operating_hours"]
LUNCH_START, LUNCH_END = clinic_info["lunch_break"]

def get_booked_time():
    return {appointment.get("time") for appointment in appointments}

def check_appointment_availability(time):
    booked_time = get_booked_time()
    status = AVAILABLE
    if not START_TIME <= time < END_TIME:
        status = OUT_OF_HOURS
        return False, status
    if LUNCH_START <= time <= LUNCH_END:
        status = LUNCH_TIME
        return False, status
    if time in booked_time:
        status = ALREADY_BOOKED
        return False, status
    return True, status


def add_appointment(patient_name, time):
    is_available, status = check_appointment_availability(time)
    appointment_str = ""
    match status:
        case "AVAILABLE" :
            appointment_str = "예약 완료"
        case "LUNCH_TIME" :
            appointment_str = "점심시간 (예약 불가)"
        case "OUT_OF_HOURS" :
            appointment_str = "운영시간 외 (예약 불가)"
        case "ALREADY_BOOKED" :
            appointment_str = "이미 예약된 시간입니다"

    if is_available:
        appointments.append({"patient_name": patient_name, "time": time})
    return f"{patient_name} - {time}시: {appointment_str}"

def show_appointments():
    if not appointments:
        print("예약된 환자가 없습니다.")
        return
    for appointment in sorted(appointments, key=lambda x : x["time"]):
        print(f"{appointment['time']}시: {appointment['patient_name']}")




test_requests = [
    ("김환자", 10),    # 정상 예약
    ("이환자", 10),    # 중복 시간
    ("박환자", 12),    # 점심시간
    ("정환자", 20),    # 운영시간 외
    ("최환자", 14)     # 정상 예약
]

print("=== 예약 처리 결과 ===")
for patient_name, time in test_requests:
    result = add_appointment(patient_name, time)
    print(result)

print("\n=== 현재 예약 현황 ===")
show_appointments()
