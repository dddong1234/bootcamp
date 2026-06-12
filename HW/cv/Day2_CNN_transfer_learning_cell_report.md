   # Day2_CNN_전이학습.ipynb 셀별 해설 보고서

대상 파일: `Day2_CNN_전이학습.ipynb`  
분석 기준: 노트북에 저장되어 있는 셀 코드, 마크다운, 실행 출력값 기준  
전체 셀 수: 71개  
구성: 코드 셀 30개, 마크다운 셀 41개

---

## 0. 노트북 전체 목적

이 노트북의 핵심 서사는 다음과 같습니다.

> **데이터가 많으면 Simple CNN도 잘 된다 → 데이터를 200장으로 줄이면 무너진다 → 같은 200장이어도 전이학습을 쓰면 성능이 회복된다.**

실험은 3막 구조입니다.

| 구간 | 데이터 | 모델 | 초기값 | 핵심 질문 |
|---|---:|---|---|---|
| 1막 | 전체 27,558장 | 직접 만든 Simple CNN | scratch | 데이터가 충분하면 CNN이 직접 특징을 배울 수 있는가? |
| 2막 | 클래스당 200장, 총 400장 | 같은 Simple CNN | scratch | 데이터만 줄였을 때 성능이 무너지는가? |
| 3막 | 같은 400장 | ResNet18 | ImageNet 사전학습 | 전이학습이 작은 데이터 문제를 보완하는가? |

최종 결론은 다음 수치로 정리됩니다.

| 실험 | Best/평가 성능 | 해석 |
|---|---:|---|
| 1막 전체 데이터 Simple CNN | val acc 약 0.9604 | 데이터가 충분하면 scratch CNN도 잘 학습 |
| 2막 200장 Simple CNN | val acc 약 0.7250 | 데이터 부족으로 성능 하락, 과적합 갭 증가 |
| 3막 전략 A ResNet18 classifier only | val acc 약 0.9125 | 같은 200장이지만 사전학습으로 크게 회복 |
| Resume fine-tuning | val acc 약 0.9375 | A에서 저장한 best 모델을 이어서 미세조정해 개선 |
| 전략 B Full fine-tuning | val acc 약 0.9375 | 처음부터 전체를 풀면 빠르게 수렴하지만 과적합 위험 |
| 전략 C Gradual unfreezing | val acc 약 0.9500 | 단계적 미세조정이 가장 안정적이고 최고 성능 |
| 전략 D ResNet scratch | val acc 약 0.9250 | 구조가 좋아도 사전학습 없이 작은 데이터는 불안정 |

---

## 1. 중요한 재현성/코드 주의사항

### 1-1. Cell 1은 fresh kernel에서 오류 가능성이 큽니다

Cell 1에서 아래 코드가 나옵니다.

```python
CV_DIR = PROJECT_ROOT / "HW" / "cv"
```

그런데 `PROJECT_ROOT`는 Cell 5에서 정의됩니다.

```python
PROJECT_ROOT = Path('/mnt/c/Users/sdh08/PycharmProjects/PythonProject1')
```

저장된 실행결과에서는 Cell 1이 성공했지만, 이는 이전 커널 상태에 `PROJECT_ROOT`가 이미 있었기 때문일 가능성이 큽니다. 노트북을 처음부터 다시 실행하면 `NameError: name 'PROJECT_ROOT' is not defined`가 날 수 있습니다.

권장 수정:

```python
PROJECT_ROOT = Path('/mnt/c/Users/sdh08/PycharmProjects/PythonProject1')
CV_DIR = PROJECT_ROOT / "HW" / "cv"
CKPT_DIR = CV_DIR / "checkpoints"
```

즉, `PROJECT_ROOT` 정의를 Cell 1 맨 위로 올리는 것이 안전합니다.

### 1-2. checkpoint 경로 표현이 불필요하게 복잡합니다

여러 셀에서 다음 형태가 반복됩니다.

```python
str(CKPT_DIR / str(CKPT_DIR / 'best_A.pth'))
```

현재 WSL 절대경로에서는 우연히 동작할 수 있지만, 의도가 불명확합니다. 아래처럼 쓰는 것이 맞습니다.

```python
str(CKPT_DIR / 'best_A.pth')
```

모든 `best_act1.pth`, `best_act2.pth`, `best_A.pth`, `best_resume.pth`, `best_B.pth`, `best_C.pth`, `best_D.pth` 경로도 같은 방식으로 단순화하는 것이 좋습니다.

### 1-3. 결과 해석 마크다운 일부가 실제 출력과 불일치합니다

노트북에는 이전 실행 기준으로 작성된 해석이 일부 남아 있습니다.

대표 예시:

- Cell 40 마크다운은 2막 recall을 `감염 0.61 / 정상 0.83`처럼 설명하지만, 실제 저장된 출력은 `감염 0.7105 / 정상 0.7381`입니다.
- Cell 55 마크다운은 resume이 `val_acc 0.95`까지 올랐다고 말하지만, 실제 Cell 54와 Cell 56 기준 resume best는 `0.9375`입니다.
- Cell 65 출력에서는 전략 A의 학습 가능 파라미터가 `4,721,666`으로 나오지만, 전략 A 정의 직후 Cell 43의 실제 학습 가능 파라미터는 `1,026`입니다. 이는 Cell 51 Grad-CAM에서 `layer4[-1]`의 `requires_grad=True`를 바꾼 상태가 뒤 셀까지 남았기 때문입니다.

따라서 최종 제출용이라면 **마크다운 해석을 실제 출력값에 맞게 수정**하는 것이 필요합니다.

---

# 2. 셀별 상세 해설

## Cell 1 — 환경 준비

### 코드 목적

```python
# [0] 환경 준비 — 로컬/캐글 겸용 + 안전한 device 선택
```

이 셀은 실험 환경을 고정하고, GPU/CPU 장치를 안전하게 선택하며, 한글 폰트와 checkpoint 폴더를 준비합니다.

### 주요 동작

- `SEED = 42`로 난수 고정
- `random`, `numpy`, `torch` seed 설정
- CUDA 사용 가능 여부 확인
- CUDA가 가능하면 `device='cuda'`, 아니면 `cpu`
- Matplotlib 한글 폰트 설정
- `CKPT_DIR` 생성
- DataLoader 옵션 설정

### 왜 이 메서드를 쓰는가?

`set_seed()`를 쓰는 이유는 학습 결과의 변동성을 줄이기 위해서입니다. 딥러닝은 가중치 초기화, 데이터 셔플, GPU 연산 등에서 랜덤성이 들어갑니다. seed를 고정하면 같은 조건에서 비슷한 결과를 재현하기 쉽습니다.

`torch.backends.cudnn.deterministic=True`와 `benchmark=False`는 재현성을 더 높이는 설정입니다. 다만 속도는 조금 느려질 수 있습니다.

`get_safe_device()`는 단순히 `torch.cuda.is_available()`만 믿지 않고, 실제로 CUDA tensor를 만들었다가 CPU로 옮겨보며 GPU가 정상 동작하는지 확인합니다.

### 저장된 실행결과

```text
font: NanumGothic
device: cuda
NUM_WORKERS: 0, PIN_MEMORY: True
```

해석하면 GPU가 사용 가능했고, CUDA 기준으로 `pin_memory=True`가 설정되었습니다.

### 주의

앞에서 말했듯이 이 셀은 `PROJECT_ROOT`를 쓰지만, 현재 셀 안에서 정의하지 않습니다. fresh kernel 재실행 시 오류 가능성이 있습니다.

---

## Cell 2 — 노트북 전체 설명 마크다운

### 마크다운 목적

노트북의 실험 구조를 설명합니다. 1막, 2막, 3막을 통해 전이학습의 효과를 보여주겠다는 안내입니다.

### 핵심 설명

- 1막: 전체 데이터 + Simple CNN + scratch
- 2막: 클래스당 200장 + Simple CNN + scratch
- 3막: 클래스당 200장 + ResNet18 + ImageNet 사전학습

### 왜 이런 구성이 좋은가?

변수를 하나씩만 바꿉니다.

1막에서 2막은 **데이터 양만 변경**합니다.  
2막에서 3막은 **모델 초기값/구조만 변경**합니다.

이렇게 해야 성능 변화의 원인을 명확히 해석할 수 있습니다.

---

## Cell 3 — 빈 마크다운 셀

내용이 없습니다. 삭제해도 됩니다.

---

## Cell 4 — 데이터 경로 찾는 법 마크다운

### 마크다운 목적

말라리아 데이터셋이 로컬 `data/` 폴더 아래 어디에 있는지 찾는 기준을 설명합니다.

### 핵심 내용

데이터셋 후보 경로:

```text
data/cell-images-for-detecting-malaria.zip
data/malaria-cell-images/cell_images/Parasitized
data/malaria-cell-images/cell_images/Uninfected
data/malaria-cell-images/cell_images/cell_images/...
```

캐글 데이터셋은 압축 해제 후 폴더가 중첩되는 경우가 많기 때문에 후보 경로를 여러 개 검사합니다.

---

## Cell 5 — 데이터 경로 자동 탐색

### 코드 목적

로컬 프로젝트의 `data/` 폴더에서 말라리아 이미지 데이터셋의 실제 위치를 찾아 `base_path`로 저장합니다.

### 주요 코드

```python
PROJECT_ROOT = Path('/mnt/c/Users/sdh08/PycharmProjects/PythonProject1')
DATA_ROOT = PROJECT_ROOT / 'data'
```

프로젝트 루트와 데이터 루트를 지정합니다.

```python
def ensure_local_dataset():
    ...
```

zip 파일이 있으면 압축을 풀고, 이미 압축이 풀려 있으면 그대로 사용합니다.

```python
def is_clean_dataset_dir(path):
    return list_visible_dirs(path) == ['Parasitized', 'Uninfected']
```

실제 데이터 폴더인지 확인합니다. 올바른 폴더라면 하위 폴더가 정확히 `Parasitized`, `Uninfected` 두 개여야 합니다.

### 왜 이 메서드를 쓰는가?

하드코딩된 경로 하나만 쓰면 폴더 구조가 조금만 달라도 실패합니다. 후보 경로를 순서대로 검사하면 로컬/캐글/압축해제 구조 차이에 더 강해집니다.

### 저장된 실행결과

```text
base_path: /mnt/c/Users/sdh08/PycharmProjects/PythonProject1/data/malaria-cell-images/cell_images/cell_images
dirs: ['Parasitized', 'Uninfected']
```

데이터 경로가 정상적으로 찾아졌습니다.

---

## Cell 6 — 데이터 경로와 클래스 균형 확인 마크다운

### 마크다운 목적

학습 전 데이터 구조와 클래스 균형을 반드시 확인해야 한다는 설명입니다.

### 핵심 설명

말라리아 데이터셋은:

```text
Parasitized: 13,779장
Uninfected: 13,779장
```

으로 1:1 균형입니다.

### 왜 중요한가?

결핵 X-ray처럼 클래스 불균형이 크면 accuracy가 왜곡될 수 있습니다. 반면 이 데이터셋은 균형 데이터라 accuracy도 어느 정도 의미가 있습니다. 그래도 의료 문제이므로 recall과 confusion matrix는 함께 봐야 합니다.

---

## Cell 7 — 클래스별 이미지 개수 확인

### 코드 목적

`base_path`가 실제 데이터 폴더인지 확인하고, 각 클래스 이미지 수를 계산합니다.

### 주요 코드

```python
os.path.isdir(base_path)
os.listdir(base_path)
```

경로 존재 여부와 하위 폴더를 확인합니다.

```python
files = [f for f in os.listdir(cls_dir) if f.lower().endswith('.png')]
```

PNG 이미지 파일만 세어 클래스별 개수를 출력합니다.

### 저장된 실행결과

```text
경로 존재: True
하위 폴더: ['Parasitized', 'Uninfected']
Parasitized: 13779
Uninfected: 13779
```

### 결과 해석

두 클래스가 정확히 13,779장씩 있습니다. 이 데이터셋은 클래스 불균형 실험보다는 전이학습 전략 비교에 적합합니다.

---

## Cell 8 — 샘플 100장 격자 마크다운

### 마크다운 목적

학습 전에 이미지를 직접 눈으로 확인하자는 설명입니다.

### 왜 필요한가?

이미지 분류에서는 모델이 진짜 신호가 아니라 가짜 단서를 배울 수 있습니다. 예를 들어 한 클래스에만 특정 테두리, 마커, 밝기 차이, 워터마크가 있으면 모델은 병변이 아니라 그 단서를 보고 맞힐 수 있습니다.

이 셀은 감염/정상 이미지를 100장씩 격자로 펼쳐 데이터가 깨끗한지 확인하도록 안내합니다.

---

## Cell 9 — 샘플 이미지 100장 시각화

### 코드 목적

감염 이미지 100장, 정상 이미지 100장을 격자로 시각화하고, 원본 이미지 크기 분포도 확인합니다.

### 주요 코드

```python
para_paths = sorted(glob.glob(os.path.join(base_path, 'Parasitized', '*.png')))[:100]
uninf_paths = sorted(glob.glob(os.path.join(base_path, 'Uninfected', '*.png')))[:100]
```

각 클래스에서 앞 100장 경로를 가져옵니다.

```python
sizes = [Image.open(p).size for p in paths[:30]]
```

앞 30장의 원본 크기를 확인합니다.

```python
img = np.array(Image.open(p).convert('RGB').resize((cell, cell)))
```

격자에 넣기 위해 모든 이미지를 64×64로 resize합니다.

### 왜 `resize`를 쓰는가?

CNN은 batch 단위로 이미지를 처리하므로 같은 batch 안의 이미지 크기가 같아야 합니다. 원본 세포 이미지는 크기가 제각각이므로 학습 전 크기 통일이 필요합니다.

### 저장된 실행결과

```text
원본 이미지 크기 확인 (W x H):
  Parasitized : W 121~169, H 97~208
  Uninfected  : W 100~181, H 109~193
→ 세포 이미지는 원본 크기가 제각각입니다. 그래서 학습 전 Resize로 통일합니다.
```

그리고 100장 격자 이미지 2개가 출력됩니다.

### 시각화 해석

이 시각화는 모델 학습 전 데이터 검수입니다. 감염 세포에는 보라색 기생충 반점이 있고, 정상 세포에는 없어야 합니다. 또한 한쪽 클래스에만 이상한 테두리나 출처 단서가 보이면 안 됩니다.

---

## Cell 10 — 1막 전체 데이터 Simple CNN 설명 마크다운

### 마크다운 목적

첫 번째 실험의 의미를 설명합니다.

### 핵심 메시지

> 데이터가 충분하면, 사전학습 없이도 Simple CNN이 잘 배울 수 있다.

전체 데이터 27,558장을 사용하여 scratch CNN의 기준선을 만듭니다. 이 기준선이 있어야 2막에서 데이터 부족 효과를 비교할 수 있습니다.

---

## Cell 11 — 1막 DataLoader 제목 마크다운

다음 코드 셀이 전체 데이터셋을 `ImageFolder`, `random_split`, `DataLoader`로 준비한다는 제목 역할입니다.

---

## Cell 12 — 전체 데이터 DataLoader 생성

### 코드 목적

전체 말라리아 데이터셋을 PyTorch 학습용 Dataset/DataLoader로 변환합니다.

### 주요 코드

```python
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])
```

이미지를 64×64로 통일하고 tensor로 변환합니다.

```python
full_dataset = datasets.ImageFolder(base_path, transform=transform)
```

폴더 구조를 기반으로 자동 라벨링합니다.

`ImageFolder`는 하위 폴더 이름을 클래스명으로 보고, 알파벳순으로 라벨을 부여합니다.

```text
Parasitized → 0
Uninfected → 1
```

```python
random_split(full_dataset, [n_train, n_val],
             generator=torch.Generator().manual_seed(42))
```

전체 데이터의 80%를 train, 20%를 val로 분할합니다.

### 왜 `DataLoader`를 쓰는가?

딥러닝 학습에서는 데이터를 batch 단위로 공급해야 합니다. `DataLoader`는 batch 생성, shuffle, 병렬 로딩, GPU 전송 최적화를 담당합니다.

### 저장된 실행결과

```text
클래스: ['Parasitized', 'Uninfected']
전체 장수: 27558
Train: 22,047 | Val: 5,511
```

### 결과 해석

전체 데이터가 정상적으로 로딩되었고, 검증셋도 5,511장으로 충분히 큽니다. 따라서 1막 평가는 비교적 안정적입니다.

---

## Cell 13 — Simple CNN 정의 제목 마크다운

다음 코드에서 직접 만든 CNN 구조를 정의한다는 제목입니다.

---

## Cell 14 — SimpleCNN 모델 정의

### 코드 목적

말라리아 세포 이미지를 2개 클래스로 분류하는 작은 CNN을 직접 정의합니다.

### 모델 구조

```python
self.features = nn.Sequential(
    nn.Conv2d(3, 32, 3, padding=1),  nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(64, 128, 3, padding=1),nn.ReLU(), nn.MaxPool2d(2),
)
```

입력은 RGB 이미지이므로 채널 수가 3입니다.

흐름:

```text
64×64×3
→ Conv 32채널 + Pool → 32×32×32
→ Conv 64채널 + Pool → 16×16×64
→ Conv 128채널 + Pool → 8×8×128
```

분류기:

```python
nn.Flatten()
nn.Linear(128 * 8 * 8, 128)
nn.ReLU()
nn.Dropout(0.3)
nn.Linear(128, num_classes)
```

`Flatten`으로 feature map을 벡터로 펼치고, fully connected layer로 2개 class logit을 출력합니다.

### 왜 이 구조를 쓰는가?

- `Conv2d`: 지역적인 이미지 특징 추출
- `ReLU`: 비선형성 추가
- `MaxPool2d`: 공간 크기 축소, 중요한 반응 유지
- `Dropout(0.3)`: 과적합 완화
- 마지막 `Linear(..., 2)`: 감염/정상 2클래스 분류

### 저장된 실행결과

```text
Simple CNN 파라미터 수: 1142210
```

### 결과 해석

직접 만든 작은 CNN이지만 파라미터가 약 114만 개입니다. 전체 데이터 27,558장에서는 학습 가능하지만, 2막의 400장에서는 이 파라미터 수가 과적합을 만들 수 있습니다.

---

## Cell 15 — 공통 학습 함수 설명 마크다운

학습/평가 함수를 따로 정의해 여러 실험에서 재사용하겠다는 설명입니다.

---

## Cell 16 — 공통 학습/평가 함수 정의

### 코드 목적

모델 학습, 평가, best checkpoint 저장, confusion matrix 출력을 위한 공통 함수를 정의합니다.

### 주요 함수

#### `count_trainable_params(model)`

```python
return sum(p.numel() for p in model.parameters() if p.requires_grad)
```

학습 가능한 파라미터 수만 셉니다. 전이학습에서 freeze/unfreeze 상태를 확인할 때 중요합니다.

#### `count_all_params(model)`

전체 파라미터 수를 셉니다.

#### `safe_load_state_dict(model, ckpt_path)`

저장된 `state_dict`를 불러와 모델에 적용합니다. PyTorch에서는 보통 모델 객체 전체보다 가중치 딕셔너리만 저장하는 것이 일반적입니다.

#### `train_model(...)`

핵심 학습 루프입니다.

주요 설정:

```python
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)
```

- `CrossEntropyLoss`: 다중분류/이진 다중클래스 logit 학습에 적합
- `Adam`: 학습률을 파라미터별로 적응적으로 조절
- `filter(lambda p: p.requires_grad, ...)`: freeze된 파라미터는 optimizer에서 제외

학습 중에는:

```python
model.train()
loss.backward()
optimizer.step()
```

검증 중에는:

```python
model.eval()
with torch.no_grad():
```

를 사용합니다.

`model.train()`은 Dropout/BatchNorm을 학습 모드로 두고, `model.eval()`은 평가 모드로 둡니다. `torch.no_grad()`는 평가 시 gradient 계산을 끄므로 메모리와 시간이 절약됩니다.

#### `evaluate_model(...)`

best checkpoint를 불러와 예측을 수행하고, accuracy, class recall, FN count, confusion matrix, classification report를 반환합니다.

#### `plot_confusion(...)`

Seaborn heatmap으로 confusion matrix를 그립니다.

### 왜 best 모델 저장을 하는가?

마지막 epoch 모델이 항상 최고는 아닙니다. 학습 후반에 과적합이 생기면 validation 성능이 떨어질 수 있습니다. 그래서 `val_acc`가 최고일 때의 가중치를 저장해두고 평가에 사용합니다.

---

## Cell 17 — 1막 전체 데이터 학습

### 코드 목적

SimpleCNN을 전체 데이터로 scratch부터 학습합니다.

### 주요 파라미터

```python
epochs=8
lr=1e-3  # train_model 기본값
batch_size=64  # Cell 12 DataLoader
optimizer=Adam
loss=CrossEntropyLoss
```

### 저장된 실행결과

```text
[1막-전체] epoch 1/8  train_acc=0.8274  val_acc=0.9463
[1막-전체] epoch 2/8  train_acc=0.9516  val_acc=0.9594
...
[1막-전체] epoch 6/8  train_acc=0.9612  val_acc=0.9604
...
best 모델 저장됨: best_act1.pth (val_acc=0.9604, epoch=6)
```

### 결과 해석

처음부터 학습한 Simple CNN이 전체 데이터에서는 validation accuracy 0.9604까지 올라갔습니다. 데이터가 충분하면 작은 CNN도 말라리아 세포의 주요 특징을 학습할 수 있음을 보여줍니다.

---

## Cell 18 — 1막 평가 설명 마크다운

### 마크다운 목적

1막 모델을 정확도 곡선, 손실 곡선, 혼동행렬, recall로 평가하겠다는 설명입니다.

### 왜 confusion matrix와 recall을 보는가?

전체 accuracy가 높아도 의료 문제에서는 감염자를 정상으로 놓치는 FN이 위험합니다. 그래서 클래스별 recall을 확인해야 합니다.

---

## Cell 19 — 1막 평가: 학습 곡선, 혼동행렬, classification report

### 코드 목적

1막 모델의 과적합 여부와 클래스별 성능을 평가합니다.

### 시각화 1: 정확도/손실 곡선

```python
ax[0].plot(hist_act1['train_acc'])
ax[0].plot(hist_act1['val_acc'])
ax[1].plot(hist_act1['train_loss'])
ax[1].plot(hist_act1['val_loss'])
```

Train과 validation 곡선이 크게 벌어지면 과적합입니다.

### 시각화 2: 혼동행렬

```python
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
```

실제 클래스와 예측 클래스를 2×2 표로 보여줍니다.

### 저장된 실행결과

```text
최종 Train Acc: 0.9664
최종 Val   Acc: 0.9590
과적합 갭 (train - val): +0.0074
→ 갭이 작음: 과적합 심하지 않음
```

Classification report:

```text
Parasitized recall: 0.95
Uninfected recall : 0.97
accuracy          : 0.96
support           : 5511
```

### 결과 해석

train/val gap이 0.0074로 매우 작습니다. 과적합이 심하지 않고 일반화가 잘 됩니다. 클래스별 recall도 0.95와 0.97로 균형이 좋습니다.

---

## Cell 20 — 1막 결과 해석 마크다운

### 마크다운 목적

1막 결과를 자연어로 해석합니다.

### 핵심 해석

- 전체 정확도 약 96%
- 과적합 거의 없음
- 클래스별 recall 균형
- 데이터가 충분하면 scratch Simple CNN도 잘 동작

### 주의

마크다운에는 감염 2,693명 중 2,568명을 맞히고 125명을 놓쳤다고 되어 있습니다. 이 값은 Cell 23의 FN 125장과도 일치합니다.

---

## Cell 21 — 틀린 샘플 분석 설명 마크다운

### 목적

숫자만 보는 것이 아니라 실제 오답 이미지를 확인하자는 설명입니다.

특히 중요하게 보는 오류는:

```text
False Negative = 실제 감염인데 정상으로 예측
```

의료 관점에서는 감염자를 놓치는 것이 가장 위험합니다.

---

## Cell 22 — 틀린 샘플 보기 제목 마크다운

다음 코드가 오답 샘플을 수집하고 시각화한다는 제목입니다.

---

## Cell 23 — 틀린 샘플 수집 및 시각화

### 코드 목적

1막 best 모델이 틀린 validation 이미지만 모아 False Negative와 False Positive로 분리하고, 각각 10장씩 보여줍니다.

### 주요 코드

```python
wrong_FN = []
wrong_FP = []
```

- `wrong_FN`: 실제 감염(0)인데 정상(1)으로 예측
- `wrong_FP`: 실제 정상(1)인데 감염(0)으로 예측

```python
for img, label in val_full:
    pred = model_act1(img.unsqueeze(0).to(device)).argmax(1).item()
```

이미지 한 장씩 예측합니다.

### 왜 `unsqueeze(0)`를 쓰는가?

모델은 batch 차원이 있는 입력을 기대합니다.

```text
단일 이미지: (C, H, W)
모델 입력:   (N, C, H, W)
```

그래서 `unsqueeze(0)`로 batch 차원을 추가합니다.

### 저장된 실행결과

```text
False Negative (감염 놓침): 125장
False Positive (정상 오판): 93장
```

그리고 FN 10장, FP 10장 이미지가 출력됩니다.

### 결과 해석

전체 성능은 높지만 여전히 감염을 놓친 샘플이 125장 있습니다. 실제 의료 문제라면 이 FN을 줄이는 방향으로 threshold 조정, 모델 개선, 더 높은 해상도 입력 등을 고려할 수 있습니다.

---

## Cell 24 — 오답 이미지 해석 마크다운

### 마크다운 핵심

FN은 기생충 점이 작거나 희미한 경우가 많고, FP는 염색 얼룩이나 보라색 잔여물을 기생충으로 착각한 경우가 많다고 해석합니다.

### 중요한 관점

Simple CNN이 색 기반 규칙에 많이 의존했을 가능성을 제기합니다.

```text
보라색이 너무 작으면 놓침
기생충이 아닌 보라색 얼룩에는 속음
```

이후 피처맵/Grad-CAM으로 이 해석을 확인합니다.

---

## Cell 25 — 피처맵 시각화 설명 마크다운

### 목적

CNN 내부 Conv layer가 어떤 특징을 잡는지 보기 위해 forward hook을 사용하겠다는 설명입니다.

### 핵심 개념

- 얕은 층: 색, 가장자리, 명암
- 깊은 층: 복잡한 모양, 질감, 기생충 패턴
- MaxPool을 거치며 feature map의 공간 크기는 줄고 채널 수는 증가

---

## Cell 26 — 감염 샘플의 Conv feature map 시각화

### 코드 목적

감염 샘플 한 장을 모델에 통과시키고, 각 Conv 층의 출력 feature map을 시각화합니다.

### 주요 코드

```python
for layer in model_act1.features:
    if isinstance(layer, torch.nn.Conv2d):
        handles.append(layer.register_forward_hook(hook))
```

Conv 층마다 forward hook을 겁니다. 모델이 forward할 때 각 Conv 층의 출력이 `activations`에 저장됩니다.

### 왜 forward hook을 쓰는가?

모델 구조를 뜯어고치지 않고도 중간 layer 출력을 가져올 수 있기 때문입니다. XAI나 feature map 분석에서 자주 쓰는 방법입니다.

### 저장된 실행결과

- 원본 감염 세포 이미지 1개
- Conv 1 feature map 8채널
- Conv 2 feature map 8채널
- Conv 3 feature map 8채널
- 출력 문장:

```text
얕은 층 → 가장자리·색 같은 단순 특징
깊은 층 → 기생충 반점 같은 복잡하고 추상적인 패턴
층이 깊어질수록 해상도(크기)는 작아지고 채널 수는 늘어난다.
```

### 시각화 해석

Conv 1은 비교적 원본에 가까운 색/엣지 반응, Conv 2~3은 더 추상적인 반응을 보여야 합니다. 만약 깊은 층에서 기생충 위치가 잘 살아남지 않으면 FN이 늘 수 있습니다.

---

## Cell 27 — 오답 피처맵 시각화 제목 마크다운

오답 샘플에 대해 같은 feature map 분석을 적용하겠다는 제목입니다.

---

## Cell 28 — FN/FP 오답 샘플의 feature map 시각화

### 코드 목적

False Negative 1장, False Positive 1장을 골라 Conv 층별 feature map을 시각화합니다.

### 주요 코드

```python
def show_featuremaps(sample_img, sample_label, sample_pred, case_name):
```

오답 이미지 하나를 넣으면 원본과 각 Conv 층의 feature map을 출력합니다.

### 저장된 실행결과

- FN 원본 이미지와 Conv 1~3 feature map 출력
- FP 원본 이미지와 Conv 1~3 feature map 출력
- 출력 문장:

```text
→ 깊은 층(Conv 3)에서 기생충 위치에 반응이 뜨는가?
→ 깊은 층이 보라색 얼룩 위치에 강하게 반응하는가?
```

### 결과 해석

이 셀은 "왜 틀렸는가"를 시각적으로 검토하는 단계입니다. FN은 기생충 점에 깊은 층 반응이 약한지, FP는 얼룩에 깊은 층 반응이 강한지 확인하는 목적입니다.

---

## Cell 29 — Grad-CAM 설명 마크다운

### 목적

Feature map과 Grad-CAM의 차이를 설명합니다.

- Feature map: 각 Conv 층이 어떤 특징을 뽑았는가
- Grad-CAM: 최종 예측에 어느 위치가 결정적으로 기여했는가

### 핵심

틀린 샘플에 Grad-CAM을 적용하면 모델이 잘못 본 위치를 알 수 있습니다.

---

## Cell 30 — Simple CNN Grad-CAM

### 코드 목적

1막 Simple CNN의 마지막 Conv 층에 hook을 걸고 Grad-CAM heatmap을 만듭니다.

### 주요 코드

```python
target_layer = conv_layers[-1]
```

Simple CNN의 마지막 Conv 층을 Grad-CAM 대상 layer로 선택합니다.

```python
out[0, target_class].backward()
```

관심 class score에 대해 역전파를 수행합니다.

```python
w = g.mean(dim=(1, 2))
cam = F.relu((w[:, None, None] * f).sum(0))
```

Grad-CAM의 핵심 계산입니다. gradient를 spatial 평균내어 채널별 중요도 weight로 만들고, feature map과 가중합합니다.

### 왜 마지막 Conv 층을 쓰는가?

마지막 Conv 층은 위치 정보와 고수준 특징을 둘 다 어느 정도 갖고 있습니다. 너무 얕은 층은 단순 색/엣지만 보고, 너무 뒤의 FC layer는 공간 위치 정보가 사라집니다.

### 저장된 실행결과

3개의 Grad-CAM 그림이 출력됩니다.

- False Negative
- False Positive
- 맞힌 감염 세포

### 시각화 해석

- FN: 기생충 위치 대신 윤곽/엉뚱한 곳에 heatmap이 뜨면 모델이 핵심 신호를 놓친 것입니다.
- FP: 정상 이미지의 얼룩에 heatmap이 뜨면 얼룩을 기생충으로 착각한 것입니다.
- 맞힌 감염: heatmap이 기생충 위치에 뜨면 모델이 올바른 단서를 본 것입니다.

---

## Cell 31 — Grad-CAM 결과 해석 마크다운

### 핵심 해석

- FN에서는 기생충이 작거나 흐려서 최종 판단에 충분히 반영되지 못함
- FP에서는 보라색 얼룩이나 세포 경계가 감염 단서처럼 작동함
- 맞힌 감염 세포에서는 기생충 위치에 heatmap이 잘 뜸

### 의미

Simple CNN은 어느 정도 올바른 신호를 보지만, 작은 기생충과 얼룩을 정교하게 구분하는 데 한계가 있습니다.

---

## Cell 32 — 2막 전체 설명 마크다운

### 목적

데이터만 클래스당 200장으로 줄여 같은 Simple CNN을 다시 학습하는 실험을 설명합니다.

### 핵심

1막과 비교해 바꾸는 것은 오직 데이터 양입니다.

```text
전체 27,558장 → 총 400장
```

이렇게 변수 통제를 해야 성능 하락의 원인을 데이터 부족으로 해석할 수 있습니다.

---

## Cell 33 — 2막 데이터 축소 제목 마크다운

다음 코드가 클래스당 200장 샘플링을 수행한다는 제목입니다.

---

## Cell 34 — 클래스당 200장 데이터셋 생성

### 코드 목적

전체 데이터에서 감염 200장, 정상 200장만 뽑아 작은 데이터셋을 만듭니다.

### 주요 코드

```python
targets = np.array(full_dataset.targets)
N_PER_CLASS = 200
```

클래스별 index를 뽑기 위해 전체 라벨 배열을 가져옵니다.

```python
rng = np.random.default_rng(42)
chosen = rng.choice(cls_idx, N_PER_CLASS, replace=False)
```

각 클래스에서 중복 없이 200장씩 샘플링합니다.

```python
small_dataset = Subset(full_dataset, small_idx)
```

PyTorch `Subset`으로 원본 dataset의 일부만 사용하는 dataset을 만듭니다.

### 왜 `Subset`을 쓰는가?

이미지를 복사하지 않고, 원본 dataset에서 선택된 index만 참조할 수 있어서 효율적입니다.

### 저장된 실행결과

```text
축소 데이터 — 클래스당 200장, 총 400장
Train: 320 | Val: 80
```

### 결과 해석

검증셋이 80장뿐입니다. 이후 0.0125 accuracy 차이는 이미지 1장 차이에 해당합니다. 따라서 작은 val set에서 1~2장 차이로 큰 결론을 내리면 안 됩니다.

---

## Cell 35 — 2막 학습 설명 마크다운

같은 Simple CNN을 200장 데이터로 scratch부터 다시 학습한다는 설명입니다.

---

## Cell 36 — 2막 Simple CNN 학습

### 코드 목적

1막과 같은 SimpleCNN을 작은 데이터셋으로 학습하여 성능이 무너지는지 확인합니다.

### 주요 파라미터

```python
epochs=15
lr=1e-3  # 기본값
train size=320
val size=80
```

### 저장된 실행결과

저장된 stream output은 중간에서 잘려 있지만, 이후 Cell 38~39 결과에 따르면 최종 val accuracy는 0.7250입니다.

대표 출력:

```text
[2막-200장] epoch 1/15  train_acc=0.5437  val_acc=0.5250
...
[2막-200장] epoch 13/15 train_acc=0.7688  val_acc=0.7000
...
2막 최종 val_acc: 0.7250
```

### 결과 해석

전체 데이터에서는 0.96이던 모델이, 400장에서는 약 0.725까지 떨어졌습니다. 같은 모델과 학습 방식이므로 성능 하락의 주된 원인은 데이터 부족입니다.

---

## Cell 37 — 1막 vs 2막 비교 제목 마크다운

데이터 양 차이에 따른 성능 차이를 비교하는 시각화 제목입니다.

---

## Cell 38 — 1막 vs 2막 validation accuracy 곡선 비교

### 코드 목적

전체 데이터 학습 곡선과 200장 학습 곡선을 한 그래프에 겹쳐 보여줍니다.

### 시각화 설명

```python
plt.plot(hist_act1['val_acc'], label='1막: 전체 데이터')
plt.plot(hist_act2['val_acc'], label='2막: 200장')
```

1막은 초반부터 높은 validation accuracy에 도달하고 안정적이어야 합니다. 2막은 낮고 불안정합니다.

### 저장된 실행결과

```text
1막(전체)  최종 val_acc: 0.9590
2막(200장) 최종 val_acc: 0.7250

→ 같은 모델, 같은 방식인데 데이터만 줄였더니 성능이 떨어졌다.
```

### 결과 해석

데이터가 충분할 때와 부족할 때의 차이가 명확합니다. 이 결과가 3막 전이학습의 필요성을 보여주는 근거가 됩니다.

---

## Cell 39 — 2막 평가: 과적합 곡선과 혼동행렬

### 코드 목적

2막 모델의 train/val 곡선, loss 곡선, confusion matrix, classification report를 확인합니다.

### 저장된 실행결과

```text
최종 Train Acc: 0.8031
최종 Val   Acc: 0.7250
과적합 갭 (train - val): +0.0781
※ 1막 갭은 +0.0074
→ 갭이 큼: 과적합. 400장을 외웠지만 일반화는 안 됨.
```

Classification report:

| class | precision | recall | f1-score | support |
|---|---:|---:|---:|---:|
| Parasitized | 0.7105 | 0.7105 | 0.7105 | 38 |
| Uninfected | 0.7381 | 0.7381 | 0.7381 | 42 |
| accuracy | 0.7250 | 0.7250 | 0.7250 | 80 |

### 결과 해석

2막은 1막보다 train/val gap이 훨씬 큽니다. 검증셋 정확도도 크게 낮아졌습니다. 다만 저장된 실제 출력 기준으로는 감염/정상 recall이 0.7105/0.7381로 둘 다 낮은 편이며, 마크다운 Cell 40의 0.61/0.83 설명과는 다릅니다.

---

## Cell 40 — 2막 결과 해석 마크다운

### 내용

데이터 부족으로 정확도 하락, 과적합, 감염 recall 하락을 설명합니다.

### 수정 필요

이 셀의 수치 일부는 실제 저장된 출력과 다릅니다.

실제 출력 기준:

```text
감염 recall: 0.7105
정상 recall: 0.7381
accuracy: 0.7250
gap: 0.0781
```

따라서 제출용이라면 이 수치에 맞게 마크다운을 고쳐야 합니다.

권장 수정 문장:

> 1막은 감염/정상 recall이 0.9536/0.9670으로 높고 균형적이었지만, 2막은 0.7105/0.7381로 둘 다 크게 낮아졌습니다. 데이터가 400장으로 줄면서 모델이 충분한 일반 패턴을 배우지 못했고, train-val gap도 0.0781로 커져 과적합이 나타났습니다.

---

## Cell 41 — 3막 전이학습 설명 마크다운

### 목적

2막과 같은 200장 데이터를 사용하되, 이번에는 ImageNet 사전학습 ResNet18을 사용한다는 설명입니다.

### 핵심

데이터 양은 유지하고 초기값만 바꿉니다.

```text
2막: 200장 + Simple CNN scratch
3막: 200장 + ResNet18 pretrained
```

---

## Cell 42 — 전략 A 제목 마크다운

전략 A는 ResNet18 사전학습 모델의 backbone을 freeze하고 fc만 교체/학습하는 방식입니다.

---

## Cell 43 — 전략 A 모델 생성: ResNet18 pretrained + fc 교체

### 코드 목적

ImageNet으로 사전학습된 ResNet18을 불러오고, 마지막 classification head만 말라리아 2클래스용으로 교체합니다.

### 주요 코드

```python
weights_enum = models.ResNet18_Weights.IMAGENET1K_V1
model_A = models.resnet18(weights=weights_enum)
```

ImageNet 사전학습 가중치를 불러옵니다.

```python
for p in model_A.parameters():
    p.requires_grad = False
```

backbone을 freeze합니다.

```python
model_A.fc = nn.Linear(model_A.fc.in_features, 2)
```

기존 1000클래스 ImageNet 분류기를 2클래스 분류기로 교체합니다.

### 왜 fc만 학습하는가?

작은 데이터에서는 전체 모델을 처음부터 많이 바꾸면 과적합이나 catastrophic forgetting이 생길 수 있습니다. 이미 학습된 일반 이미지 특징은 유지하고, 마지막 분류기만 말라리아 데이터에 맞게 학습하는 것이 안전합니다.

### 저장된 실행결과

```text
전체 파라미터:     11,177,538
학습 가능 파라미터: 1,026  (fc만)
```

### 결과 해석

전략 A는 전체 1,117만 파라미터 중 마지막 fc의 1,026개만 학습합니다. 작은 데이터에 적합한 안전한 전이학습 방식입니다.

---

## Cell 44 — 전략 A 학습 설명 마크다운

전략 A를 200장 데이터로 학습하고 best 모델을 저장한다는 설명입니다.

---

## Cell 45 — ResNet용 transform과 전략 A 학습

### 코드 목적

ResNet18 입력 형식에 맞게 transform을 바꾸고, 2막과 동일한 400장 index로 전략 A 모델을 학습합니다.

### 주요 코드

```python
transforms.Resize((224, 224))
transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
```

ResNet18은 ImageNet 사전학습 모델이므로 ImageNet 입력 전처리와 맞춰야 합니다.

### 왜 Normalize를 쓰는가?

사전학습 당시 ImageNet 데이터가 이 평균/표준편차로 정규화되었습니다. 입력 분포를 맞춰야 사전학습 feature extractor가 제대로 작동합니다.

### 공정 비교

```python
small_resnet = Subset(dataset_resnet, small_idx)
```

2막에서 뽑은 같은 이미지 index를 사용합니다. 데이터가 달라지지 않아야 Simple CNN과 전이학습을 공정하게 비교할 수 있습니다.

### 주요 파라미터

```python
epochs=10
lr=1e-3
학습 대상: fc only
train=320, val=80
```

### 저장된 실행결과

```text
[3막-전이A] epoch 1/10  train_acc=0.6000  val_acc=0.5750
...
[3막-전이A] epoch 6/10  train_acc=0.8938  val_acc=0.9125
...
best 모델 저장됨: best_A.pth (val_acc=0.9125, epoch=6)

3막(전이학습 A) 최종 val_acc: 0.9125
```

### 결과 해석

같은 400장 데이터인데 Simple CNN scratch는 0.7250, ResNet18 전이학습 A는 0.9125입니다. 이 차이가 전이학습의 효과입니다.

---

## Cell 46 — 전략 A 혼동행렬 설명 마크다운

전체 accuracy만 보지 말고 감염을 놓치는지 확인하자는 설명입니다.

---

## Cell 47 — 전략 A 평가

### 코드 목적

전략 A best checkpoint를 불러와 confusion matrix와 classification report를 출력합니다.

### 저장된 실행결과

| class | precision | recall | f1-score | support |
|---|---:|---:|---:|---:|
| Parasitized | 0.8974 | 0.9211 | 0.9091 | 38 |
| Uninfected | 0.9268 | 0.9048 | 0.9157 | 42 |
| accuracy | 0.9125 | 0.9125 | 0.9125 | 80 |

### 결과 해석

2막의 0.7250에서 0.9125로 크게 회복했습니다. 감염 recall도 0.9211로 좋아졌습니다. 의료적으로 중요한 FN이 줄어든 것이 핵심입니다.

---

## Cell 48 — 1/2/3막 종합 비교 제목 마크다운

1막, 2막, 3막을 한눈에 비교하는 그래프를 그리겠다는 제목입니다.

---

## Cell 49 — 세 실험 best accuracy와 학습 곡선 비교

### 코드 목적

1막, 2막, 3막의 최고 validation accuracy를 막대그래프로 보여주고, validation accuracy 곡선을 한 그래프에 겹칩니다.

### 시각화

- 왼쪽: 세 실험의 best val accuracy bar chart
- 오른쪽: epoch별 val accuracy curve

### 저장된 실행결과

```text
서사 요약:
  1막(전체)     : 0.960  — 데이터 많으니 잘 됨
  2막(200장)    : 0.725  — 데이터 줄이니 무너짐
  3막(전이학습) : 0.912  — 같은 200장인데 회복!
```

### 결과 해석

노트북의 핵심 메시지를 가장 잘 보여주는 셀입니다. 데이터가 줄어들면 성능이 무너지지만, 사전학습 모델을 사용하면 상당 부분 회복됩니다.

---

## Cell 50 — ResNet Grad-CAM 설명 마크다운

### 목적

전략 A ResNet18이 실제로 세포 안 기생충을 보고 판단하는지 Grad-CAM으로 확인합니다.

### 핵심

좋은 모델이라면 heatmap이 세포 배경이나 테두리가 아니라 기생충 반점 위에 떠야 합니다.

---

## Cell 51 — 전략 A ResNet18 Grad-CAM

### 코드 목적

전략 A 모델의 `layer4[-1]`에 hook을 걸어 Grad-CAM을 생성합니다.

### 주요 코드

```python
target_layer = model_A.layer4[-1]
```

ResNet18의 마지막 residual block을 Grad-CAM 대상 layer로 선택합니다.

```python
mean = torch.tensor([0.485, 0.456, 0.406]).view(3,1,1)
std  = torch.tensor([0.229, 0.224, 0.225]).view(3,1,1)
```

Normalize된 이미지를 다시 시각화하기 위해 denormalize에 사용합니다.

```python
show = (img * std + mean).clamp(0,1)
```

정규화된 tensor를 사람이 볼 수 있는 RGB 범위로 복원합니다.

### 왜 ResNet은 `layer4[-1]`을 쓰는가?

ResNet18의 `layer4`는 가장 깊은 convolution block입니다. 고수준 semantic feature를 갖고 있으면서 아직 공간 정보가 남아 있어 Grad-CAM에 적합합니다.

### 저장된 실행결과

- PyTorch backward hook warning 1개
- Grad-CAM figure 1개 출력

```text
UserWarning: Full backward hook is firing ...
```

### warning 해석

이 warning은 backward hook 사용 방식 때문에 뜬 것으로, Grad-CAM 시각화 자체가 반드시 실패했다는 뜻은 아닙니다. 다만 최신 PyTorch에서는 hook 동작 방식이 바뀔 수 있으므로 주의하라는 경고입니다.

### 주의

이 셀에서 다음 코드가 있습니다.

```python
for p in target_layer.parameters():
    p.requires_grad = True
```

Grad-CAM을 위해 gradient를 얻으려는 의도지만, 이 변경이 이후 셀의 파라미터 카운트에 영향을 줍니다. 그래서 Cell 65에서 전략 A의 학습 가능 파라미터가 1,026이 아니라 4,721,666으로 나오는 부작용이 생겼습니다.

Grad-CAM 후에는 원래대로 되돌리거나, 파라미터 수를 Cell 43에서 저장한 `params_A_trainable` 값으로 사용해야 합니다.

---

## Cell 52 — 실무 패턴 resume → fine-tune 설명 마크다운

### 목적

best 모델을 저장해두고, 그 가중치를 다시 불러와 이어서 미세조정하는 실무 패턴을 설명합니다.

### 핵심 개념

1. `load_state_dict`로 best 가중치 불러오기
2. `requires_grad=True`로 전체 backbone 풀기
3. 작은 learning rate `1e-5`로 전체 미세조정
4. 좋은 모델 위에서 안전하게 성능을 더 다듬기

### 왜 작은 lr을 쓰는가?

이미 잘 학습된 사전학습 가중치를 큰 learning rate로 업데이트하면 기존 지식이 망가질 수 있습니다. 따라서 전체 fine-tuning은 작은 lr로 조심스럽게 진행합니다.

---

## Cell 53 — resume fine-tune 제목 마크다운

전략 A best 모델을 불러와 전체 미세조정을 진행한다는 제목입니다.

---

## Cell 54 — 전략 A best 모델에서 이어서 전체 미세조정

### 코드 목적

전략 A의 best checkpoint를 불러온 뒤, 모든 파라미터를 unfreeze하고 작은 lr로 추가 학습합니다.

### 주요 코드

```python
model_resume = models.resnet18(weights=weights_enum)
model_resume.fc = nn.Linear(model_resume.fc.in_features, 2)
model_resume = safe_load_state_dict(model_resume, ...)
```

동일한 구조의 모델을 만든 뒤 `best_A.pth` 가중치를 불러옵니다.

```python
for p in model_resume.parameters():
    p.requires_grad = True
```

전체 모델을 학습 가능하게 바꿉니다.

```python
epochs=8
lr=1e-5
```

작은 learning rate로 미세조정합니다.

### 저장된 실행결과

```text
이제 학습 가능 파라미터: 11,177,538  (전체)

[resume-미세조정] epoch 1/8  train_acc=0.8500  val_acc=0.9125
...
[resume-미세조정] epoch 4/8  train_acc=0.9719  val_acc=0.9375
...
best 모델 저장됨: best_resume.pth (val_acc=0.9375, epoch=4)

A 단독 best       : 0.9125
A 불러와 이어학습 후: 0.9375
```

### 결과 해석

전략 A의 0.9125에서 resume fine-tuning 후 0.9375로 올랐습니다. 단, train accuracy가 후반에 1.0000까지 올라가므로 과적합 징후도 있습니다. best checkpoint를 저장했기 때문에 epoch 4의 좋은 시점을 사용할 수 있습니다.

---

## Cell 55 — resume 결과 해석 마크다운

### 수정 필요

이 셀은 실제 출력과 일부 다릅니다.

실제 출력 기준:

```text
전략 A 단독 best: 0.9125
resume 후 best: 0.9375
```

마크다운에는 0.95까지 올랐다는 표현이 있는데, 현재 저장된 실행결과 기준으로는 0.9375입니다.

권장 해석:

> 전략 A에서 fc만 학습했을 때 best val acc는 0.9125였고, 이를 불러와 전체 backbone을 작은 lr=1e-5로 미세조정하자 best val acc가 0.9375까지 올랐습니다. 다만 후반부 train accuracy가 1.0에 도달하고 train-val gap이 커지므로 과적합이 시작됩니다.

---

## Cell 56 — resume 모델 혼동행렬 평가

### 코드 목적

`best_resume.pth`를 불러와 confusion matrix와 classification report를 확인합니다.

### 저장된 실행결과

| class | precision | recall | f1-score | support |
|---|---:|---:|---:|---:|
| Parasitized | 0.9459 | 0.9211 | 0.9333 | 38 |
| Uninfected | 0.9302 | 0.9524 | 0.9412 | 42 |
| accuracy | 0.9375 | 0.9375 | 0.9375 | 80 |

### 결과 해석

전략 A보다 accuracy가 0.9125 → 0.9375로 올랐습니다. 감염 recall은 0.9211로 유지되고, 정상 recall은 0.9048 → 0.9524로 올랐습니다. 즉 전체 성능은 개선되었지만, 감염 놓침 수 자체는 크게 줄지 않았습니다.

---

## Cell 57 — resume 혼동행렬 해석 마크다운

### 수정 필요

마크다운은 일부 수치를 과장하거나 이전 실행 결과를 반영합니다. 실제 출력 기준으로는 resume이 0.9375이고, 감염 recall은 전략 A와 같은 0.9211입니다.

더 정확한 해석:

> resume fine-tuning은 전체 accuracy를 높였지만, 감염 recall은 전략 A와 동일한 0.9211입니다. 개선은 주로 정상 클래스 recall 상승에서 나왔습니다. validation set이 80장뿐이므로, 1~2개 예측 차이로 수치가 크게 흔들릴 수 있습니다.

---

## Cell 58 — 전략 B 설명 마크다운

### 전략 B

사전학습 ResNet18을 불러오지만 처음부터 전체 파라미터를 학습합니다.

```text
pretrained ResNet18 + full fine-tuning
```

---

## Cell 59 — 전략 B Full Fine-tuning

### 코드 목적

ImageNet 사전학습 ResNet18의 모든 파라미터를 처음부터 학습 가능하게 두고 10 epoch 학습합니다.

### 주요 파라미터

```python
weights=IMAGENET1K_V1
requires_grad=True for all params
epochs=10
lr=1e-4
trainable params=11,177,538
```

전략 A보다 learning rate를 낮춥니다. 전체 모델을 업데이트하기 때문입니다.

### 저장된 실행결과

```text
전략 B 학습 가능 파라미터: 11,177,538
[전략B-FullFT] epoch 1/10  train_acc=0.8187  val_acc=0.8750
[전략B-FullFT] epoch 2/10  train_acc=0.9875  val_acc=0.9375
...
best 모델 저장됨: best_B.pth (val_acc=0.9375, epoch=2)
```

Classification report:

| class | precision | recall | f1-score | support |
|---|---:|---:|---:|---:|
| Parasitized | 0.9714 | 0.8947 | 0.9315 | 38 |
| Uninfected | 0.9111 | 0.9762 | 0.9425 | 42 |
| accuracy | 0.9375 | 0.9375 | 0.9375 | 80 |

### 결과 해석

전략 B는 매우 빠르게 수렴하지만, epoch 3부터 train accuracy가 1.0으로 올라가 과적합 가능성이 큽니다. 감염 recall은 0.8947로 전략 A보다 낮습니다. 의료 관점에서는 감염 놓침이 늘어날 수 있으므로 accuracy만 보고 선택하면 위험합니다.

---

## Cell 60 — 전략 C 설명 마크다운

### 전략 C

Gradual Unfreezing입니다.

1. fc만 먼저 학습해 분류기를 안정화
2. best stage1을 불러와 전체를 unfreeze
3. 작은 lr로 전체 미세조정

---

## Cell 61 — 전략 C Gradual Unfreezing

### 코드 목적

전략 A와 full fine-tuning의 중간 방식으로, 단계적 미세조정을 구현합니다.

### Stage 1

```python
for p in model_C.parameters():
    p.requires_grad = False
model_C.fc = nn.Linear(..., 2)
epochs=5
lr=1e-3
```

fc만 학습합니다.

저장된 결과:

```text
best_C_stage1.pth (val_acc=0.9125, epoch=4)
```

### Stage 2

```python
model_C = safe_load_state_dict(model_C, 'best_C_stage1.pth')
for p in model_C.parameters():
    p.requires_grad = True
epochs=8
lr=1e-5
```

전체를 작은 lr로 미세조정합니다.

저장된 출력은 stream이 잘렸지만, classification report 기준 최종 best는 0.9500입니다.

Classification report:

| class | precision | recall | f1-score | support |
|---|---:|---:|---:|---:|
| Parasitized | 0.9722 | 0.9211 | 0.9459 | 38 |
| Uninfected | 0.9318 | 0.9762 | 0.9535 | 42 |
| accuracy | 0.9500 | 0.9500 | 0.9500 | 80 |

### 결과 해석

전략 C가 네 전략 중 best val accuracy 0.9500으로 가장 높습니다. 감염 recall 0.9211과 정상 recall 0.9762를 동시에 확보하여 균형도 좋습니다.

### 왜 C가 좋은가?

fc가 랜덤 초기값인 상태에서 전체 backbone을 바로 크게 흔들지 않습니다. 먼저 fc를 안정화한 다음, 전체 모델을 작은 lr로 미세조정하므로 사전학습 feature를 덜 망가뜨립니다.

---

## Cell 62 — 전략 D 설명 마크다운

### 전략 D

ResNet18 구조는 사용하지만, ImageNet 사전학습 없이 `weights=None`으로 200장 데이터만으로 학습합니다.

---

## Cell 63 — 전략 D ResNet18 from scratch

### 코드 목적

ResNet18 구조 자체의 효과와 사전학습 가중치의 효과를 분리해서 보기 위한 실험입니다.

### 주요 파라미터

```python
weights=None
requires_grad=True
epochs=10
lr=1e-3
trainable params=11,177,538
```

### 저장된 실행결과

```text
[전략D-Scratch] epoch 1/10  train_acc=0.5000  val_acc=0.4750
...
[전략D-Scratch] epoch 8/10  train_acc=0.9094  val_acc=0.9250
...
[전략D-Scratch] epoch 10/10 train_acc=0.9594  val_acc=0.5375
best_D.pth (val_acc=0.9250, epoch=8)
```

Classification report:

| class | precision | recall | f1-score | support |
|---|---:|---:|---:|---:|
| Parasitized | 0.9444 | 0.8947 | 0.9189 | 38 |
| Uninfected | 0.9091 | 0.9524 | 0.9302 | 42 |
| accuracy | 0.9250 | 0.9250 | 0.9250 | 80 |

### 결과 해석

ResNet18 구조가 강력해서 0.9250까지 올라가긴 하지만, 학습 곡선이 매우 불안정합니다. 특히 마지막 epoch에서 val accuracy가 0.5375로 급락합니다. 작은 데이터에서 큰 모델을 scratch로 학습하는 것이 위험하다는 증거입니다.

---

## Cell 64 — 3막 종합 비교 제목 마크다운

전략 A/B/C/D를 종합 비교한다는 제목입니다.

---

## Cell 65 — 종합 비교 표와 그래프

### 코드 목적

1막/2막 결과와 3막 전략 A/B/C/D 결과를 표와 그래프로 정리합니다.

### 주요 출력 1 — 1막 vs 2막

| 실험 | 데이터 | 전체 정확도 | 감염 recall | 정상 recall | 과적합 갭 |
|---|---|---:|---:|---:|---:|
| 1막 | 전체 | 0.9604 | 0.9536 | 0.9670 | 0.0074 |
| 2막 | 200장 | 0.7250 | 0.7105 | 0.7381 | 0.0781 |

### 주요 출력 2 — 전략 A/B/C/D

저장된 출력 기준:

| 전략 | 학습 가능 파라미터 | Best Val Acc | 감염 recall | 정상 recall | 수렴 시작 epoch |
|---|---:|---:|---:|---:|---:|
| A. Classifier only | 4,721,666 | 0.9125 | 0.9211 | 0.9048 | 6 |
| B. Full fine-tuning | 11,177,538 | 0.9375 | 0.8947 | 0.9762 | 2 |
| C. Gradual unfreezing | 11,177,538 | 0.9500 | 0.9211 | 0.9762 | 8 |
| D. ResNet scratch | 11,177,538 | 0.9250 | 0.8947 | 0.9524 | 8 |

### 주의: 전략 A 파라미터 수

전략 A의 실제 학습 가능 파라미터는 Cell 43 직후 기준 `1,026`이 맞습니다. Cell 65 출력의 `4,721,666`은 Cell 51 Grad-CAM에서 ResNet `layer4[-1]`를 `requires_grad=True`로 바꾼 부작용입니다.

### 주요 출력 3 — resume 효과

| 모델 | Best Val Acc | 감염 recall | 감염 놓침(FN) |
|---|---:|---:|---:|
| 전략 A fc만 | 0.9125 | 0.9211 | 3 |
| A → 전체 미세조정 resume | 0.9375 | 0.9211 | 3 |

### 결과 해석

가장 좋은 전략은 C입니다. 다만 validation set이 80장으로 작기 때문에 0.9375와 0.9500 차이는 1장 정도 차이에 해당할 수 있습니다. 그래도 방향성은 명확합니다. 작은 데이터에서는 사전학습 + 단계적 미세조정이 가장 안정적입니다.

---

## Cell 66 — 결과표 마크다운

### 목적

Cell 65의 결과를 제출용 표로 정리합니다.

### 수정 필요

이 셀의 전략 A 학습 가능 파라미터는 `1,026`으로 되어 있고, 이는 개념상 맞습니다. 하지만 Cell 65 출력과 불일치합니다. Cell 65의 출력값을 고치려면 Grad-CAM 이후 변경된 `requires_grad` 상태를 되돌리거나, 저장해둔 `params_A_trainable` 값을 사용해야 합니다.

권장 코드:

```python
summary_strategies = pd.DataFrame([
    {
        '전략': 'A. Classifier only',
        '학습 가능 파라미터': params_A_trainable,  # Cell 43에서 저장된 1,026
        ...
    }
])
```

---

## Cell 67 — 전체 분석 마크다운

### 내용 요약

이 셀은 결과를 다음 관점으로 종합 해석합니다.

1. 데이터 이해
2. 데이터 양의 효과
3. 전이학습 원리
4. 전략 비교
5. XAI 관점
6. 실무적 결론

### 좋은 점

단순히 성능 숫자만 쓰지 않고, 왜 전이학습이 작은 데이터에서 도움이 되는지 설명합니다.

### 수정하면 좋은 점

2막 recall, resume 성능 등 일부 수치를 실제 출력 기준으로 다시 맞추는 것이 좋습니다.

---

## Cell 68 — 핵심 결론 마크다운

### 내용

최종 결론을 bullet로 정리합니다.

핵심은 다음입니다.

- 전체 데이터에서는 Simple CNN도 0.9604 정확도로 잘 작동
- 200장으로 줄이면 0.7250까지 하락
- 같은 200장이어도 전이학습 전략들은 0.9125~0.9500까지 회복
- 가장 좋은 전략은 Gradual Unfreezing(C)

### 해석

노트북의 최종 메시지로 적절합니다. 단, 검증셋 80장이라는 한계를 함께 써주면 더 좋습니다.

권장 추가 문장:

> 단, 2막·3막 검증셋은 80장이므로 1~2개 샘플 차이로 accuracy가 크게 변할 수 있다. 따라서 전략 간 미세한 차이보다 전체 경향, 즉 전이학습이 scratch보다 안정적이라는 점에 초점을 둔다.

---

## Cell 69 — 빈 마크다운 셀

내용 없음. 삭제 가능.

---

## Cell 70 — 빈 코드 셀

내용 없음. 삭제 가능.

---

## Cell 71 — 빈 코드 셀

내용 없음. 삭제 가능.

---

# 3. 모델 파라미터 정리

## SimpleCNN

```python
Conv2d(3, 32, kernel_size=3, padding=1)
Conv2d(32, 64, kernel_size=3, padding=1)
Conv2d(64, 128, kernel_size=3, padding=1)
MaxPool2d(2) after each conv block
Linear(128*8*8, 128)
Dropout(0.3)
Linear(128, 2)
```

총 파라미터 수:

```text
1,142,210
```

입력 이미지:

```text
64×64 RGB
```

학습:

```text
optimizer: Adam
loss: CrossEntropyLoss
lr: 1e-3
```

## ResNet18 전략 A

```python
weights = ResNet18_Weights.IMAGENET1K_V1
backbone frozen
fc = Linear(512, 2)
```

전체 파라미터:

```text
11,177,538
```

학습 가능 파라미터:

```text
1,026
```

학습:

```text
lr=1e-3
epochs=10
```

## Resume Fine-tuning

```text
시작점: best_A.pth
학습 범위: 전체 파라미터
lr=1e-5
epochs=8
```

## 전략 B Full Fine-tuning

```text
시작점: ImageNet pretrained ResNet18
학습 범위: 전체 파라미터
lr=1e-4
epochs=10
```

## 전략 C Gradual Unfreezing

```text
Stage 1: fc만 학습, lr=1e-3, epochs=5
Stage 2: 전체 unfreeze, lr=1e-5, epochs=8
```

## 전략 D ResNet Scratch

```text
weights=None
학습 범위: 전체 파라미터
lr=1e-3
epochs=10
```

---

# 4. 시각화 부분 설명

## 4-1. 100장 격자

목적: 데이터가 깨끗한지 확인합니다.

볼 것:

- 감염 세포에 실제 기생충 반점이 보이는가
- 정상 세포에는 반점이 없는가
- 클래스별로만 나타나는 인공 단서가 있는가

## 4-2. Train/Val Accuracy/Loss 곡선

목적: 과적합 여부 확인

해석법:

```text
train acc 상승 + val acc 정체/하락 = 과적합
train loss 하락 + val loss 상승 = 과적합
train/val gap 작음 = 일반화 양호
```

1막은 gap 0.0074로 안정적입니다.  
2막은 gap 0.0781로 커져 과적합이 나타납니다.

## 4-3. Confusion Matrix

목적: 어떤 클래스를 틀리는지 확인합니다.

말라리아에서는 특히 다음 칸이 중요합니다.

```text
실제 Parasitized, 예측 Uninfected = False Negative
```

감염자를 정상으로 놓치는 것이므로 의료적으로 위험합니다.

## 4-4. Feature Map

목적: Conv layer가 내부에서 어떤 반응을 만드는지 확인합니다.

얕은 층은 색/엣지, 깊은 층은 더 복잡한 질감/형태를 봅니다.

## 4-5. Grad-CAM

목적: 최종 판단에 영향을 준 이미지 위치를 heatmap으로 확인합니다.

좋은 결과:

```text
감염 예측 시 기생충 위치에 heatmap이 뜸
```

나쁜 결과:

```text
기생충이 아닌 얼룩, 테두리, 배경에 heatmap이 뜸
```

---

# 5. 제출용으로 넣기 좋은 예시 코드와 결과

## 5-1. 전이학습 전략 A 핵심 코드

```python
from torchvision import models
import torch.nn as nn

weights_enum = models.ResNet18_Weights.IMAGENET1K_V1

model_A = models.resnet18(weights=weights_enum)

# backbone freeze
for p in model_A.parameters():
    p.requires_grad = False

# 2-class classifier로 교체
model_A.fc = nn.Linear(model_A.fc.in_features, 2)

print("전체 파라미터:", count_all_params(model_A))
print("학습 가능 파라미터:", count_trainable_params(model_A))
```

예상 결과:

```text
전체 파라미터: 11,177,538
학습 가능 파라미터: 1,026
```

해석:

> ImageNet에서 학습된 feature extractor는 그대로 두고, 마지막 분류층만 말라리아 2클래스에 맞게 학습한다.

## 5-2. ResNet 전처리 코드

```python
transform_resnet = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    ),
])
```

해석:

> 사전학습 ResNet18은 ImageNet 정규화 기준으로 학습되었기 때문에 입력도 같은 평균/표준편차로 맞춰준다.

## 5-3. Gradual Unfreezing 핵심 코드

```python
# Stage 1: fc만 학습
model_C = models.resnet18(weights=weights_enum)
for p in model_C.parameters():
    p.requires_grad = False
model_C.fc = nn.Linear(model_C.fc.in_features, 2)

model_C, hist_C_stage1 = train_model(
    model_C, train_loader_r, val_loader_r,
    epochs=5, lr=1e-3,
    tag='전략C-stage1',
    save_path=str(CKPT_DIR / 'best_C_stage1.pth')
)

# Stage 2: 전체 unfreeze 후 작은 lr
model_C = safe_load_state_dict(model_C, str(CKPT_DIR / 'best_C_stage1.pth'))
for p in model_C.parameters():
    p.requires_grad = True

model_C, hist_C_stage2 = train_model(
    model_C, train_loader_r, val_loader_r,
    epochs=8, lr=1e-5,
    tag='전략C-stage2',
    save_path=str(CKPT_DIR / 'best_C.pth')
)
```

저장된 결과:

```text
전략 C Best Val Acc: 0.9500
Parasitized recall: 0.9211
Uninfected recall: 0.9762
```

해석:

> 먼저 fc만 안정화하고, 이후 backbone을 작은 lr로 풀어 사전학습 특징을 크게 망가뜨리지 않으면서 말라리아 데이터에 맞게 조정했다.

## 5-4. 결과 비교 예시 문장

제출용 문장 예시:

> 전체 데이터 27,558장에서는 scratch Simple CNN도 0.9604의 검증 정확도를 기록했다. 그러나 같은 구조를 클래스당 200장으로 제한하자 검증 정확도는 0.7250으로 하락했고, train-val gap도 0.0074에서 0.0781로 증가했다. 이는 데이터 부족이 일반화 성능 저하와 과적합을 유발했음을 보여준다. 반면 같은 400장 데이터에서 ImageNet 사전학습 ResNet18을 사용한 전략 A는 0.9125까지 회복되었고, gradual unfreezing 전략 C는 0.9500으로 가장 높은 성능을 보였다. 따라서 작은 데이터셋에서는 사전학습 가중치와 단계적 미세조정이 scratch 학습보다 안정적이다.

---

# 6. 최종 평가

이 노트북은 실험 설계가 좋습니다. 특히 좋은 점은 다음입니다.

1. 변수 통제가 명확합니다.
   - 1막 → 2막: 데이터 양만 변경
   - 2막 → 3막: 사전학습 여부/모델 전략 변경

2. 단순 accuracy로 끝내지 않고 confusion matrix와 recall을 확인합니다.

3. Grad-CAM과 feature map으로 모델이 무엇을 보는지 설명하려고 합니다.

4. 전략 A/B/C/D를 비교해 전이학습 방식의 차이를 보여줍니다.

보완하면 좋은 점은 다음입니다.

1. fresh kernel에서 실행되도록 `PROJECT_ROOT` 정의 위치를 수정해야 합니다.
2. checkpoint 경로 코드를 단순화해야 합니다.
3. 일부 마크다운 해석 수치를 현재 실행결과에 맞게 업데이트해야 합니다.
4. Grad-CAM에서 바꾼 `requires_grad=True`가 뒤 셀의 파라미터 카운트에 영향을 주지 않도록 관리해야 합니다.
5. 2막/3막 검증셋이 80장뿐이라는 한계를 최종 결론에 명시해야 합니다.

