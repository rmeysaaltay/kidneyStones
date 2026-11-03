import os
from google.colab import drive

drive.mount('/content/drive')
!pip install -q ultralytics
import os

!rm -rf /content/kidney /content/kidney.zip /content/None
!cp "/content/drive/MyDrive/kidney.v2i.yolov8.zip" /content/kidney.zip
!unzip -q /content/kidney.zip -d /content/kidney

LOCAL = None
for root, dirs, _ in os.walk("/content/kidney"):
    if "train" in dirs and "valid" in dirs and "test" in dirs:
        LOCAL = root
        break

print("Veri seti yolu:", LOCAL)
for k in ("train/images", "train/labels", "valid/images", "test/images", "test/labels"):
    print(f"{k:15s} -> {len(os.listdir(os.path.join(LOCAL, k)))} dosya")
import os
import glob

!rm -rf /content/valid_labels_tmp /content/valid_labels.zip
!cp "/content/drive/MyDrive/valid_labels.zip" /content/valid_labels.zip
!unzip -q /content/valid_labels.zip -d /content/valid_labels_tmp

src = None
for root, dirs, files_ in os.walk("/content/valid_labels_tmp"):
    if any(f.endswith(".txt") for f in files_):
        src = root
        break
print("Etiket kaynağı:", src)

dst = f"{LOCAL}/valid/labels"
os.makedirs(dst, exist_ok=True)
!cp "{src}"/*.txt "{dst}"/

for split in ("train", "valid", "test"):
    imgs = {os.path.splitext(f)[0] for f in os.listdir(f"{LOCAL}/{split}/images")}
    lbls = {os.path.splitext(f)[0] for f in os.listdir(f"{LOCAL}/{split}/labels")}
    print(f"{split:6s} görsel: {len(imgs)} | etiket: {len(lbls)} | "
          f"etiketsiz görsel: {len(imgs - lbls)} | görselsiz etiket: {len(lbls - imgs)}")


import os
import yaml

DRIVE_RUNS = "/content/drive/MyDrive/kidney.v2i.yolov8/runs"
os.makedirs(DRIVE_RUNS, exist_ok=True)

cfg = {
    "path": LOCAL,
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": 4,
    "names": {0: "cysts", 1: "normal", 2: "stones", 3: "tumors"},
}
YAML_PATH = f"{LOCAL}/data_local.yaml"
with open(YAML_PATH, "w") as f:
    yaml.dump(cfg, f, sort_keys=False)

print(open(YAML_PATH).read())
from ultralytics import YOLO

model = YOLO("yolov8s.pt")
model.train(
    data=YAML_PATH,
    epochs=100,
    imgsz=640,
    batch=16,
    patience=20,
    cache="ram",          
    workers=2,
    project=DRIVE_RUNS,
    name="kidney_v2",
    exist_ok=True,
    seed=42,
) import os
import pandas as pd
from IPython.display import display
from ultralytics import YOLO

best_path = f"{DRIVE_RUNS}/kidney_v2/weights/best.pt"
model = YOLO(best_path)

metrics = model.val(
    data=YAML_PATH,
    split="test",
    imgsz=640,
    plots=True,
    project=DRIVE_RUNS,
    name="kidney_v2_test",
    exist_ok=True,
)

print(f"\nmAP@50     : {metrics.box.map50:.4f}")
print(f"mAP@50-95  : {metrics.box.map:.4f}")
print(f"Precision  : {metrics.box.mp:.4f}")
print(f"Recall     : {metrics.box.mr:.4f}")
f1 = 2 * metrics.box.mp * metrics.box.mr / (metrics.box.mp + metrics.box.mr + 1e-9)
print(f"F1         : {f1:.4f}")

rows = []
for i, c in enumerate(metrics.box.ap_class_index):
    p, r, ap50, ap = metrics.box.class_result(i)
    rows.append({
        "Sınıf": model.names[c],
        "Precision": p,
        "Recall": r,
        "mAP50": ap50,
        "mAP50-95": ap,
        "F1": 2 * p * r / (p + r + 1e-9),
    })

df = pd.DataFrame(rows).round(4)
display(df)
df.to_csv(f"{DRIVE_RUNS}/kidney_v2_test/class_metrics.csv", index=False)
import os
from IPython.display import display, Image

test_dir = f"{DRIVE_RUNS}/kidney_v2_test"
train_dir = f"{DRIVE_RUNS}/kidney_v2"

for p in [f"{test_dir}/confusion_matrix_normalized.png",
          f"{test_dir}/PR_curve.png",
          f"{train_dir}/results.png"]:
    if os.path.exists(p):
        display(Image(p, width=700))
    else:
        print("Bulunamadı:", p)
from google.colab import files

files.download(f"{DRIVE_RUNS}/kidney_v2/weights/best.pt")


