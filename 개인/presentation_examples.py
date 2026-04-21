import time

def benchmark_list_growth():
    sizes = [10_000, 100_000, 1_000_000, 5_000_000]

    for n in sizes:
        numbers = list(range(n))

        # 인덱스 접근
        start = time.time()
        _ = numbers[n // 2]
        index_time = time.time() - start

        # 값 찾기
        start = time.time()
        _ = (n - 1) in numbers
        search_time = time.time() - start

        print(
            f"{n:>10,}개 | "
            f"index: {index_time:.20f}s | "
            f"search: {search_time:.20f}s |"
        )

benchmark_list_growth()

'''








'''


















#relationship 1:N (1)
patients = [
    {"id": 1, "name": "김철수"},
    {"id": 2, "name": "이영희"},
]

prescriptions = [
    {"prescription_id": 1, "patient_id": 1, "medication": "타이레놀"},
    {"prescription_id": 2, "patient_id": 1, "medication": "항생제"},
]

#relationship 1:N (2)
doctors = [
    {"id": 1, "name": "김의사"},
    {"id": 2, "name": "박의사"},
]

patients = [
    {"id": 1, "name": "김철수", "doctor_id": 1},
    {"id": 2, "name": "이영희", "doctor_id": 1},
    {"id": 3, "name": "박민수", "doctor_id": 2},
]
'''
1:N과 N:1은 같은 관계를 보는 방향만 다른 것
'''


#relationship 1:0
patients = [
    {"id": 1, "name": "김철수"},
    {"id": 2, "name": "이영희"},
]

appointments = [
    {"id": 1, "patient_id": 1, "time": "09:00"},
]


#relationship 1:1
patients = [
    {"id": 1, "name": "김철수"},
    {"id": 2, "name": "이영희"},
]

patient_profiles = [
    {
        "id": 1,
        "patient_id": 1,
        "address": "서울",
        "phone": "010-1234-5678"
    },
    {
        "id": 2,
        "patient_id": 2,
        "address": "부산",
        "phone": "010-9999-8888"
    },
]