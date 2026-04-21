import numpy as np

patients_data = np.array([
    [80, 45.0, 250, 490, 780],   # 환자1: [나이, BMI, 수축기혈압, 혈당수치, 콜레스테롤]
    [75, 38.0, 200, 220, 300],   # 환자2: [나이, BMI, 수축기혈압, 혈당수치, 콜레스테롤]
    [35, 23.0, 115, 90, 180],   # 환자3: [나이, BMI, 수축기혈압, 혈당수치, 콜레스테롤]
    [60, 30.0, 160, 140, 250],   # 환자4: [나이, BMI, 수축기혈압, 혈당수치, 콜레스테롤]
    [40, 25.0, 120, 100, 200]    # 환자5: [나이, BMI, 수축기혈압, 혈당수치, 콜레스테롤]
])
stages = ["낮음", "보통", "높음", "매우높음"]
clinical_recommendation = ["정기검진 유지", "생활습관 개선", "전문의 상담", "즉시 치료"]


def calculate_risk(patients_data):
    risk_weights = np.array([0.05, 0.08, 0.02, 0.03, 0.01])
    risks = np.dot(patients_data, risk_weights)
    return risks

def get_risk_strings(risks):
    str_list = []
    for index, risk in enumerate(risks):
        str_list.append(f"환자{index+1}: {risk:.1f}점")
    return str_list

def print_risk_strings(str_list):
    for string in str_list:
        print(string)

def get_stage_index_list(risks):
    risk_stage = {
        "낮음": [],
        "보통": [],
        "높음": [],
        "매우 높음": []
    }
    index_list = []

    for risk in risks:
        if risk < 15:
            stage = "낮음"
            index = 0
        elif 15 <= risk < 25:
            stage = "보통"
            index = 1
        elif 25 <= risk < 35:
            stage = "높음"
            index = 2
        else:
            stage = "매우 높음"
            index = 3
        risk_stage[stage].append(risk) # 만약 patient 객체가 있다면 risk 대신 patient객체를 넣고싶음
                                       #현재는 쓰이지 않는 dict이지만 미래 확장성을 생각한다면 만들어도 좋을듯
        index_list.append(index)
    return index_list, risk_stage

def print_patients_summary(index_list,str_list):
        for i, risk_str in enumerate(str_list):
            stage = stages[index_list[i]]
            recommendation = clinical_recommendation[index_list[i]]
            print(f"{risk_str} ({stage}) → {recommendation}")

def get_max_min_index(risks):
    max_risk_index = np.argmax(risks)
    min_risk_index = np.argmin(risks)
    return max_risk_index, min_risk_index

def print_max_min_patient(risks):
    max_risk_index, min_risk_index = get_max_min_index(risks)
    print(f"가장 위험한 환자: 환자{max_risk_index+1} ({risks[max_risk_index]:.1f}점)")
    print(f"가장 안전한 환자: 환자{min_risk_index + 1} ({risks[min_risk_index]:.1f}점)")



risks = calculate_risk(patients_data)
index_list, risk_stage = get_stage_index_list(risks)
str_list= get_risk_strings(risks)

print("=== 환자 위험도 통합 평가 시스템 ===\n")
print("=== 1단계: 전체 환자 위험도 계산 ===")
print_risk_strings(str_list)
print("\n=== 2단계: 위험도 등급 분류 ===")
print_patients_summary(index_list,str_list)
print("\n=== 3단계: 최고/최저 위험 환자 ===")
print_max_min_patient(risks)




