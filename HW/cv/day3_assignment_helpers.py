import json
import math
import os
import shutil
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Optional

import pandas as pd
from IPython.display import Markdown, display
from sklearn.model_selection import train_test_split
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSIGNMENT_WORK_ROOT = PROJECT_ROOT / "HW" / "cv" / "day3_assignment_artifacts"
ASSIGNMENT_WORK_ROOT.mkdir(parents=True, exist_ok=True)

DEFAULT_CLASSES = [
    "Aortic enlargement",
    "Atelectasis",
    "Calcification",
    "Cardiomegaly",
    "Consolidation",
    "ILD",
    "Infiltration",
    "Lung Opacity",
    "Nodule/Mass",
    "Other lesion",
    "Pleural effusion",
    "Pleural thickening",
    "Pneumothorax",
    "Pulmonary fibrosis",
]


@dataclass
class ExperimentConfig:
    exp_name: str
    changed_variable: str
    hypothesis: str
    img_size: int = 512
    epochs: int = 3
    batch: int = 16
    workers: int = 8
    device: Optional[str] = None
    model_pt: str = "yolov8n.pt"
    include_no_finding: bool = False
    single_class: bool = True
    seed: int = 42
    val_size: float = 0.2


PRESET_EXPERIMENTS = {
    "baseline": ExperimentConfig(
        exp_name="baseline_local",
        changed_variable="없음 (기준 실행)",
        hypothesis="기준값 확보용 실행이다. 이후 모든 티켓 실험은 이 결과와 비교한다.",
    ),
    "ticket001": ExperimentConfig(
        exp_name="ticket001_imgsz768",
        changed_variable="IMG_SIZE",
        hypothesis="입력 해상도를 높이면 작은 병변의 정보 손실이 줄어 Recall이 개선될 가능성이 있다.",
        img_size=768,
    ),
    "ticket002": ExperimentConfig(
        exp_name="ticket002_yolov8s",
        changed_variable="MODEL_PT",
        hypothesis="모델 용량을 키우면 표현력이 늘어나 mAP50과 mAP50-95가 개선될 가능성이 있다.",
        model_pt="yolov8s.pt",
    ),
    "ticket003": ExperimentConfig(
        exp_name="ticket003_epoch10",
        changed_variable="EPOCHS",
        hypothesis="epoch 3은 미수렴일 가능성이 높아서 학습을 더 길게 하면 성능이 추가로 오를 수 있다.",
        epochs=10,
    ),
    "ticket004": ExperimentConfig(
        exp_name="ticket004_include_no_finding",
        changed_variable="INCLUDE_NO_FINDING",
        hypothesis="정상 이미지를 학습에 포함하면 배경 오탐이 줄어 Precision이 오르지만 Recall은 흔들릴 수 있다.",
        include_no_finding=True,
    ),
    "ticket005": ExperimentConfig(
        exp_name="ticket005_multiclass",
        changed_variable="SINGLE_CLASS",
        hypothesis="14개 다중 클래스로 확장하면 클래스별 AP 격차와 희귀 클래스의 약점이 드러날 것이다.",
        single_class=False,
    ),
}


def clone_config(key: str, **updates) -> ExperimentConfig:
    return replace(PRESET_EXPERIMENTS[key], **updates)


def candidate_dataset_roots():
    roots = []
    env_root = os.environ.get("VINBIGDATA_ROOT")
    if env_root:
        roots.append(Path(env_root))
    roots.extend(
        [
            Path("/data/vinbigdata-512-image-dataset/vinbigdata"),
            Path("/data/vinbigdata/vinbigdata"),
            PROJECT_ROOT / "data" / "vinbigdata-512-image-dataset" / "vinbigdata",
            PROJECT_ROOT / "data" / "vinbigdata",
        ]
    )
    return roots


def resolve_dataset_root() -> Path:
    for root in candidate_dataset_roots():
        if (root / "train.csv").exists() and (root / "train").exists():
            return root
    searched = "\n".join(f"- {path}" for path in candidate_dataset_roots())
    raise FileNotFoundError(
        "VinBigData 데이터 경로를 찾지 못했습니다. 아래 후보 중 한 곳에 train.csv와 train/ 폴더를 두세요.\n"
        + searched
    )


def load_vinbig_df(dataset_root: Optional[Path] = None):
    dataset_root = Path(dataset_root) if dataset_root else resolve_dataset_root()
    df = pd.read_csv(dataset_root / "train.csv")
    return dataset_root, df


def assignment_eda_snapshot(dataset_root: Optional[Path] = None) -> dict:
    dataset_root, df = load_vinbig_df(dataset_root)
    abnormal = df[df["class_name"] != "No finding"].copy()
    abnormal = abnormal.dropna(subset=["x_min", "y_min", "x_max", "y_max"])

    image_level = df.groupby("image_id")["class_name"].apply(
        lambda s: "No finding" if (s == "No finding").all() else "Abnormality"
    )
    image_mix = image_level.value_counts()

    abnormal["box_area_ratio"] = (
        (abnormal["x_max"] - abnormal["x_min"])
        * (abnormal["y_max"] - abnormal["y_min"])
    ) / (abnormal["width"] * abnormal["height"])
    class_counts = abnormal["class_name"].value_counts()

    return {
        "dataset_root": str(dataset_root),
        "num_images": int(df["image_id"].nunique()),
        "normal_images": int(image_mix.get("No finding", 0)),
        "abnormal_images": int(image_mix.get("Abnormality", 0)),
        "normal_ratio": float(image_mix.get("No finding", 0) / len(image_level)),
        "abnormal_ratio": float(image_mix.get("Abnormality", 0) / len(image_level)),
        "small_box_ratio_lt_1pct": float((abnormal["box_area_ratio"] < 0.01).mean()),
        "largest_class": class_counts.index[0],
        "largest_class_count": int(class_counts.iloc[0]),
        "smallest_class": class_counts.index[-1],
        "smallest_class_count": int(class_counts.iloc[-1]),
    }


def print_assignment_eda(dataset_root: Optional[Path] = None):
    snapshot = assignment_eda_snapshot(dataset_root)
    text = (
        "### EDA 근거 요약\n\n"
        f"- 데이터 경로: `{snapshot['dataset_root']}`\n"
        f"- 전체 이미지 수: `{snapshot['num_images']:,}`\n"
        f"- 정상 이미지: `{snapshot['normal_images']:,}` ({snapshot['normal_ratio']:.1%})\n"
        f"- 이상 이미지: `{snapshot['abnormal_images']:,}` ({snapshot['abnormal_ratio']:.1%})\n"
        f"- 박스 면적 비율 1% 미만의 소형 병변 비율: `{snapshot['small_box_ratio_lt_1pct']:.1%}`\n"
        f"- 최다 클래스: `{snapshot['largest_class']}` ({snapshot['largest_class_count']:,})\n"
        f"- 최저 클래스: `{snapshot['smallest_class']}` ({snapshot['smallest_class_count']:,})"
    )
    display(Markdown(text))
    return snapshot


def make_yolo_label_from_row(row):
    w_img, h_img = row["width"], row["height"]
    x_center = ((row["x_min"] + row["x_max"]) / 2) / w_img
    y_center = ((row["y_min"] + row["y_max"]) / 2) / h_img
    box_w = (row["x_max"] - row["x_min"]) / w_img
    box_h = (row["y_max"] - row["y_min"]) / h_img
    return (
        f"{int(row['yolo_class'])} "
        f"{x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}"
    )


def build_labels(df: pd.DataFrame, include_no_finding: bool, single_class: bool):
    df_bbox = df[df["class_name"] != "No finding"].copy()
    df_bbox = df_bbox.dropna(subset=["x_min", "y_min", "x_max", "y_max"])
    df_bbox["yolo_class"] = 0 if single_class else df_bbox["class_id"].astype(int)
    df_bbox["yolo_line"] = df_bbox.apply(make_yolo_label_from_row, axis=1)

    labels = df_bbox.groupby("image_id")["yolo_line"].apply(lambda x: "\n".join(x))
    if include_no_finding:
        labels = labels.reindex(
            pd.Index(df["image_id"].unique(), name="image_id"), fill_value=""
        )
    return labels, ["abnormality"] if single_class else DEFAULT_CLASSES


def prepare_dataset(cfg: ExperimentConfig, dataset_root: Optional[Path] = None) -> dict:
    dataset_root, df = load_vinbig_df(dataset_root)
    labels, class_names = build_labels(df, cfg.include_no_finding, cfg.single_class)
    image_ids = labels.index.tolist()
    train_ids, val_ids = train_test_split(
        image_ids, test_size=cfg.val_size, random_state=cfg.seed
    )

    work_dir = ASSIGNMENT_WORK_ROOT / cfg.exp_name / "dataset"
    run_dir = ASSIGNMENT_WORK_ROOT / cfg.exp_name / "runs"
    shutil.rmtree(work_dir, ignore_errors=True)
    shutil.rmtree(run_dir, ignore_errors=True)

    for split, ids in [("train", train_ids), ("val", val_ids)]:
        (work_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (work_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
        for img_id in ids:
            src = dataset_root / "train" / f"{img_id}.png"
            dst = work_dir / "images" / split / f"{img_id}.png"
            if not src.exists():
                raise FileNotFoundError(f"이미지를 찾지 못했습니다: {src}")
            shutil.copy2(src, dst)
            (work_dir / "labels" / split / f"{img_id}.txt").write_text(labels[img_id])

    yaml_content = (
        f"path: {work_dir.resolve()}\n"
        "train: images/train\n"
        "val: images/val\n\n"
        f"nc: {len(class_names)}\n"
        f"names: {json.dumps(class_names, ensure_ascii=False)}\n"
    )
    yaml_path = work_dir / "data.yaml"
    yaml_path.write_text(yaml_content)

    return {
        "dataset_root": dataset_root,
        "yaml_path": yaml_path,
        "work_dir": work_dir,
        "run_dir": run_dir,
        "class_names": class_names,
        "train_images": len(train_ids),
        "val_images": len(val_ids),
    }


def run_assignment_experiment(
    cfg: ExperimentConfig, dataset_root: Optional[Path] = None
) -> dict:
    bundle = prepare_dataset(cfg, dataset_root)
    model = YOLO(cfg.model_pt)

    started = time.perf_counter()
    model.train(
        data=str(bundle["yaml_path"]),
        epochs=cfg.epochs,
        imgsz=cfg.img_size,
        batch=cfg.batch,
        workers=cfg.workers,
        device=cfg.device,
        project=str(bundle["run_dir"]),
        name=cfg.exp_name,
        exist_ok=True,
        seed=cfg.seed,
    )
    elapsed = time.perf_counter() - started

    out_dir = bundle["run_dir"] / cfg.exp_name
    best_model = YOLO(str(out_dir / "weights" / "best.pt"))
    metrics = best_model.val(data=str(bundle["yaml_path"]))

    result = {
        "config": asdict(cfg),
        "dataset_root": str(bundle["dataset_root"]),
        "yaml_path": str(bundle["yaml_path"]),
        "run_dir": str(out_dir),
        "train_images": bundle["train_images"],
        "val_images": bundle["val_images"],
        "mAP50": float(metrics.box.map50),
        "mAP50_95": float(metrics.box.map),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "train_time_sec": elapsed,
        "results_png": str(out_dir / "results.png"),
        "confusion_matrix_png": str(out_dir / "confusion_matrix_normalized.png"),
        "box_pr_png": str(out_dir / "BoxPR_curve.png"),
        "box_f1_png": str(out_dir / "BoxF1_curve.png"),
    }

    cls_maps = getattr(metrics.box, "maps", None)
    if cls_maps is not None and len(cls_maps):
        result["class_ap50_95"] = {
            class_name: float(ap)
            for class_name, ap in zip(bundle["class_names"], cls_maps)
        }
    else:
        result["class_ap50_95"] = None

    result_path = out_dir / "assignment_result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"저장 완료: {result_path}")
    return result


def _fmt_metric(value: Optional[float], digits: int = 4) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value:.{digits}f}"


def _fmt_seconds(sec: Optional[float]) -> str:
    if sec is None:
        return "-"
    return f"{int(sec // 60)}m {int(sec % 60):02d}s"


def display_experiment_report(
    result: dict,
    baseline: Optional[dict] = None,
    ticket_id: str = "TICKET-XXX",
    observation: str = "",
    decision: str = "",
    hypothesis_verified: str = "",
):
    base = baseline or result
    train_delta = (
        "ref"
        if baseline is None
        else f"{result['train_time_sec'] - base['train_time_sec']:+.1f} sec"
    )
    delta = lambda key: "ref" if baseline is None else f"{result[key] - base[key]:+.4f}"

    table = "\n".join(
        [
            "| Metric | baseline | this exp | delta |",
            "|---|---:|---:|---:|",
            f"| mAP50 | {_fmt_metric(base['mAP50'])} | {_fmt_metric(result['mAP50'])} | {delta('mAP50')} |",
            f"| mAP50-95 | {_fmt_metric(base['mAP50_95'])} | {_fmt_metric(result['mAP50_95'])} | {delta('mAP50_95')} |",
            f"| Precision | {_fmt_metric(base['precision'])} | {_fmt_metric(result['precision'])} | {delta('precision')} |",
            f"| Recall | {_fmt_metric(base['recall'])} | {_fmt_metric(result['recall'])} | {delta('recall')} |",
            f"| Train time | {_fmt_seconds(base['train_time_sec'])} | {_fmt_seconds(result['train_time_sec'])} | {train_delta} |",
        ]
    )

    text = (
        f"### [{ticket_id}] Report\n\n"
        f"EXP_NAME: `{result['config']['exp_name']}`\n"
        f"Changed variable: `{result['config']['changed_variable']}`\n"
        f"Hypothesis: {result['config']['hypothesis']}\n\n"
        f"Result:\n{table}\n\n"
        f"Observation: {observation or '직접 실행 후 curves / 예측 샘플을 보고 작성'}\n"
        f"Hypothesis verified (Y/N): {hypothesis_verified or '실행 후 작성'}\n"
        f"Decision: {decision or '실행 후 작성'}"
    )
    display(Markdown(text))

    if result.get("class_ap50_95"):
        ap_df = pd.DataFrame(
            sorted(result["class_ap50_95"].items(), key=lambda item: item[1]),
            columns=["class_name", "AP50-95"],
        )
        display(ap_df)
        return ap_df
    return None


def build_final_summary(results_by_ticket: dict) -> pd.DataFrame:
    rows = []
    for ticket, result in results_by_ticket.items():
        rows.append(
            {
                "Ticket": ticket,
                "EXP_NAME": result["config"]["exp_name"],
                "Changed variable": result["config"]["changed_variable"],
                "mAP50": result["mAP50"],
                "mAP50-95": result["mAP50_95"],
                "Precision": result["precision"],
                "Recall": result["recall"],
                "Train time": _fmt_seconds(result["train_time_sec"]),
            }
        )
    return pd.DataFrame(rows)
