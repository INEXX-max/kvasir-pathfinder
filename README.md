# 🔬 kvasir-pathfinder

> ⚠️ Work in Progress — actively improving.

**🔗 Live Notebook on Kaggle:** [kvasir-pathfinder](https://www.kaggle.com/code/inexxcsgo/kvasir-pathfinder)

---

Endoscopy exams generate thousands of images. Doctors have to go through all of them manually — and things get missed. This project is my attempt to build something that helps with that: a model that looks at gastrointestinal images and classifies what it sees, automatically.

I built this after reading the published work of Prof. Pekka Toivanen and Dr. Keijo Haataja from UEF on WCE and GI image analysis. Their research made it clear how much room there is for deep learning to make a real difference in this space, and I wanted to try building a version of that pipeline myself.

---

## Results

| Metric | Score |
|--------|-------|
| Test Accuracy | **89%** |
| Macro ROC-AUC (OvR) | **0.9668** |
| Weighted F1 | **0.88** |

Standout class results:
- `retroflex-stomach` — Precision 1.00, Recall 1.00
- `cecum` — AUC 1.000
- `polyps` — AUC 0.996, Recall 0.99
- `pylorus` — AUC 1.000

Weaker classes (`barretts`, `ulcerative-colitis-grade-0-1`) had very few samples — class imbalance is the main issue, not the model architecture.

---

## Why HyperKvasir?

HyperKvasir is one of the largest publicly available GI endoscopy datasets — 10,662 images across 23 classes, ranging from normal findings to polyps and other abnormalities. It's what the UEF research group works with, so it made sense to start here.

---

## What the Model Does

The backbone is EfficientNet-B3, pretrained on ImageNet and fine-tuned for this task. Lower layers are frozen, only the top blocks and classification head are trained.

**Training setup:**
- Optimizer: AdamW
- Scheduler: CosineAnnealingLR
- Loss: CrossEntropyLoss + Label Smoothing (0.1)
- Early Stopping: patience 6
- Image size: 300×300 | Batch size: 32

Data split: 70% train / 15% val / 15% test (stratified). Classes with fewer than 10 samples removed before training.

---

## What Gets Generated

**Data exploration:**
- `class_distribution.png` — bar chart + pie chart of images per class
- `sample_images.png` — 2×4 grid of example endoscopy images per class

**Training:**
- `training_curves.png` — loss and accuracy across epochs for train and val

**Evaluation:**
- `confusion_matrix.png` — full prediction heatmap on test set
- `roc_curves.png` — ROC-AUC curves for the top 6 classes

**Explainability:**
- `gradcam.png` — Grad-CAM heatmaps from the last conv block, showing which pixels the model focused on. For medical AI, this matters — accuracy alone isn't enough if the model is looking at the wrong parts of the image.

---

## Running It

Runs on Kaggle or Google Colab with a T4 GPU.

**On Kaggle:**
1. Add HyperKvasir via **Add Data**
2. Set accelerator to **GPU T4 x2**
3. Run All

```bash
pip install timm grad-cam
```

---

## References

- Habe, Haataja, Toivanen. RT-DETR for Wireless Capsule Endoscopy. *Frontiers in AI*, 2025.
- Habe, Haataja, Toivanen. Benchmarking Object Detection in WCE. *IEEE Access*, 2024.
- Habe, Haataja, Toivanen. Deep Learning Review for GI Classification. *F1000Research*, 2024.
- [HyperKvasir Dataset](https://www.kaggle.com/datasets/melidsa/hyperkvasir)
- [EfficientNet — Tan & Le, ICML 2019](https://arxiv.org/abs/1905.11946)
- [Grad-CAM — Selvaraju et al., ICCV 2017](https://arxiv.org/abs/1610.02391)

---

## About

**Muhammed Inanc**
Computer Programming, Inonu University — Turkey
Founder, [INEXX Interactive](https://inexxinteractive.com)
