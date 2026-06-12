# CXR-DET — 흉부 X-ray 이상 탐지 모델 개선

**프로젝트**: Chest X-ray Abnormality Detection
**데이터셋**: VinBigData Chest X-ray (512px)
**베이스라인 노트북**: `Day3_baseline_v2.ipynb` (YOLOv8n / imgsz=512 / epoch=3 / 단일 클래스 `abnormality`)
**담당**: (assignee)
**스프린트**: Day 3

---

## 시작 전 (필수 선행)

1. 베이스라인 노트북을 **위에서부터 끝까지** 한 번 실행한다.
2. 특히 **3. EDA**와 **5. 변환 검증**을 눈으로 확인한다. 아래 티켓들은 EDA에서 관찰한 사실에 근거한다.
3. baseline의 4개 지표(mAP50, mAP50-95, Precision, Recall)를 결과표 기준값으로 먼저 기록한다.

## 작업 공통 규칙

- 변수는 한 번에 하나만 변경한다. 동시 변경 시 원인 분리 불가.
- 변경은 노트북 **1번 설정 셀에서만** 한다. 코드 본문은 건드리지 않는다.
- 실험마다 `EXP_NAME` 고유값 지정. `runs_cxr/` 덮어쓰기 금지.
- 비교 대상은 항상 baseline. baseline을 먼저 1회 실행하여 기준값 확보 후 착수.
- 각 티켓 완료 시 하단 `리포트` 양식 작성. 미작성 시 미완료로 간주.

> 설정 셀에서 실험에 쓰는 변수: `IMG_SIZE`, `BATCH`, `EPOCHS`, `MODEL_PT`, `INCLUDE_NO_FINDING`, `SINGLE_CLASS`, `EXP_NAME`

---

## CXR-DET-001 — 소형 병변 미탐지

| | |
|---|---|
| Priority | High |
| Type | Improvement |
| Status | Open |

**Description**
검수 피드백상 결절·석회화 등 소형 소견의 누락 빈도가 높음. 현재 입력 해상도에서 소형 객체 손실 가능성 의심됨.

**근거 (EDA)**
노트북 3-4(박스 크기 분포)에서 작은 병변의 비중을 확인했을 것. 그 수치를 이 티켓의 출발점으로 인용한다.

**Task**
입력 해상도가 소형 병변 탐지에 미치는 영향을 검증하고 개선 여부를 수치로 입증한다. (어떤 설정 변수를 어떻게 바꿀지는 담당자가 결정)

**Constraints**
- 해상도 상향 시 배치 크기 조정 필요할 수 있음 (GPU 메모리).
- 학습 시간 증가분 측정 필수.

**Acceptance Criteria**
- [ ] baseline 대비 Recall 변화 수치 제시
- [ ] 학습 시간 변화 기록
- [ ] 비용 대비 채택 가치 판단 (1줄)

---

## CXR-DET-002 — mAP 목표 미달

| | |
|---|---|
| Priority | High |
| Type | Improvement |
| Status | Open |

**Description**
현재 mAP가 데모 가능 수준 미달. 모델 용량 확대를 통한 개선 여지 확인 필요. 단, 추론 속도/학습 비용 트레이드오프 동반.

**Task**
모델 용량 변경이 성능에 미치는 영향과 그에 따른 비용 증가를 측정한다.

**Acceptance Criteria**
- [ ] baseline 대비 mAP50 / mAP50-95 변화 제시
- [ ] 학습 시간(또는 epoch당 시간) 변화 기록
- [ ] 성능 향상이 비용 증가를 정당화하는지 판단

---

## CXR-DET-003 — 학습 수렴 여부 미확인

| | |
|---|---|
| Priority | Medium |
| Type | Investigation |
| Status | Open |

**Description**
baseline은 epoch 3에서 종료됨. 미수렴 상태로 추정. 무한정 학습은 비용 낭비이므로 중단 시점을 데이터로 판단해야 함.

**Task**
학습량 증가에 따른 성능 추이를 관찰하고 수렴/정체 지점을 식별한다.

**Acceptance Criteria**
- [ ] `results.png` loss 곡선 하강/정체 여부 판단
- [ ] 성능 정체 시작 epoch 추정
- [ ] 추가 학습 가치 판단
- [ ] loss 곡선 캡처 첨부

---

## CXR-DET-004 — 정상 클래스 편향

| | |
|---|---|
| Priority | Medium |
| Type | Investigation |
| Status | Open |

**Description**
'No finding'(정상) 이미지 비중이 과다. "이상 없음" 예측만으로 손실이 낮아지는 구조 → 병변 누락 방향 편향 우려.

**근거 (EDA)**
노트북 3-1(정상 vs 이상 비중)에서 정상 이미지 비율을 확인했을 것. 그 수치를 인용한다.

**Task**
정상 이미지 비중이 편향에 미치는 영향을 검증하고, 데이터 구성 변경이 Recall에 주는 효과를 확인한다.
(관련 설정 변수: `INCLUDE_NO_FINDING`)

**Constraints**
- 데이터 구성 변경 시 Precision/Recall이 상반되게 움직일 수 있음. 양쪽 모두 측정.

**Acceptance Criteria**
- [ ] 변경 전/후 Precision, Recall 비교
- [ ] 부작용(있을 경우) 서술
- [ ] 프로덕션 채택 여부 판단

---

## CXR-DET-005 — 다중 클래스 확장 (Stretch)

| | |
|---|---|
| Priority | Low |
| Type | Feature |
| Status | Open |

**Description**
현재 전 병변을 `abnormality` 단일 클래스로 처리. 제품 가치 제고를 위해 14개 소견 분류로 확장 필요. 클래스 증가 시 불균형 노출 및 희귀 소견 저성능 예상.

**근거 (EDA)**
노트북 3-2(클래스별 분포)에서 최다/최소 클래스의 개수 격차를 확인했을 것. AP가 낮게 나올 클래스를 미리 예측해보고, 실제 결과와 비교한다.

**Task**
14개 다중 클래스로 확장하여 클래스별 성능 격차를 측정하고 문제 클래스를 식별한다.
(관련 설정 변수: `SINGLE_CLASS = False` — 노트북이 자동으로 nc=14, names 14종으로 data.yaml을 생성함)

**Acceptance Criteria**
- [ ] 클래스별 AP 제시
- [ ] 저성능 클래스 식별 및 원인 추정 (데이터 개수 연계)
- [ ] 후속 개선 방향 제안
- [ ] 클래스별 AP 표 첨부

---

## 리포트 양식 (티켓별 작성)

```
### [CXR-DET-00X] Report

EXP_NAME:
Changed variable:
Hypothesis:

Result:
| Metric     | baseline | this exp | delta |
|------------|----------|----------|-------|
| mAP50      |          |          |       |
| mAP50-95   |          |          |       |
| Precision  |          |          |       |
| Recall     |          |          |       |
| Train time |          |          |       |

Observation:
Hypothesis verified (Y/N):
Decision:
```

---

## 작성 예시 (baseline 기준 — 이 수준으로 작성)

> 아래는 baseline을 1회 실행한 뒤 작성한 예시입니다. 수치는 예시값이며, 본인 실행 결과로 대체합니다.
> 핵심은 표의 숫자만 채우는 것이 아니라 `Hypothesis` / `Observation` / `Decision`을 **문장으로** 남기는 것입니다.

### [CXR-DET-000] Report (baseline)

EXP_NAME: `baseline`
Changed variable: 없음 (기준 실행)
Hypothesis: 기준값 확보용 실행이므로 가설 없음. 이후 모든 실험은 이 수치와 비교한다.

Result:
| Metric     | baseline | this exp | delta |
|------------|----------|----------|-------|
| mAP50      | 0.182    | 0.182    | ref   |
| mAP50-95   | 0.071    | 0.071    | ref   |
| Precision  | 0.241    | 0.241    | ref   |
| Recall     | 0.198    | 0.198    | ref   |
| Train time | 2m 10s   | 2m 10s   | ref   |

Observation: epoch 3에서 종료되어 `results.png`의 box/cls/dfl loss가 모두 우하향 중이며 평탄화 구간이 전혀 없음 → 명백한 미수렴 상태. 추론 시 conf=0.25에서 배경에 거짓양성 박스가 다수 잡힘. Recall이 0.2 미만으로, 실제 병변의 80%가량을 놓치고 있음.
Hypothesis verified (Y/N): N/A (기준 실행)
Decision: 이 수치를 baseline으로 고정. loss가 아직 내려가는 중이므로 epoch 증가(CXR-DET-003)가 효과를 낼 가능성이 높음. 우선순위 High인 001/002부터 착수.

---

## 결과 종합

| Ticket | mAP50 | mAP50-95 | Precision | Recall | Train time | Adopt? | Key finding |
|--------|-------|----------|-----------|--------|-----------|--------|-------------|
| baseline   | | | | | | ref | imgsz=512, yolov8n, ep=3 |
| CXR-DET-001 | | | | | | | |
| CXR-DET-002 | | | | | | | |
| CXR-DET-003 | | | | | | | |
| CXR-DET-004 | | | | | | | |
| CXR-DET-005 | | | | | | | |

---

## Wrap-up (제출 필수)

1. 효과가 가장 컸던 변경과 그 이유
2. 비용 대비 효과가 가장 낮았던 변경
3. 추가 시도할 다음 작업 (위 5개 외)
4. 프로덕션 투입 시 현재 최대 리스크
