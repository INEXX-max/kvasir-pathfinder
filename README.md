# kvasir-pathfinder — Gastrointestinal Disease Detection via Transfer Learning

## Project Overview

Endoscopy exams generate thousands of images, and clinicians must review them manually, which is time-consuming and error-prone.  
This project investigates whether a deep learning model can automatically classify gastrointestinal (GI) endoscopy images and highlight clinically relevant findings, using the HyperKvasir dataset.

---

## Why HyperKvasir?

HyperKvasir is one of the largest publicly available GI endoscopy datasets:

- 10,662 images  
- 23 classes (normal findings, polyps, inflammatory conditions, etc.)

Because it is widely used by leading research groups in GI and wireless capsule endoscopy (WCE), it provides a solid and comparable baseline for this work.

You can view and run the full pipeline here:  
**Live Kaggle Notebook:** [kvasir-pathfinder](https://www.kaggle.com/code/inexxcsgo/kvasir-pathfinder)

---

## Connection to UEF’s Research

This project is inspired by the WCE and GI image analysis research led by Prof. Pekka Toivanen, Dr. Keijo Haataja, and Dr. Tsedeke Temesgen Habe at the University of Eastern Finland (UEF).

Their work focuses on real-time, deployment-oriented pipelines for detecting and localizing findings in WCE videos (for example, RT-DETR–based object detection).  
My model is a frame-level classifier on the HyperKvasir dataset and is designed as an initial step toward such pipelines, with the following objectives:

- Use a lightweight backbone (EfficientNet-B3) for frame-level GI classification.  
- Address class imbalance and evaluate with clinically meaningful metrics (macro ROC-AUC, F1-score, confusion matrix).  
- Apply Grad-CAM to verify that the model relies on relevant anatomical regions rather than artifacts.

In a future extension, this classifier could serve as a pre-filter in a WCE pipeline: first flagging potentially abnormal frames, then passing them to more computationally expensive detection models for lesion localization.

---

## Model Architecture and Training

Backbone: EfficientNet-B3 (pretrained on ImageNet, fine-tuned on HyperKvasir)

- Lower layers: frozen  
- Upper blocks and a custom classification head: trainable

Training setup:

- Optimizer: AdamW  
- Scheduler: CosineAnnealingLR  
- Loss: CrossEntropyLoss with label smoothing (0.1)  
- Early stopping: patience of 6 epochs  
- Image size: 224 × 224  
- Batch size: 32  

Data split (stratified):

- 75% train  
- 12.5% validation  
- 12.5% test  

Classes with fewer than 10 samples were excluded prior to training to avoid extreme imbalance.

---

## Results

| Metric              | Score   |
|---------------------|---------|
| Test accuracy       | 89%     |
| Macro ROC-AUC (OvR) | 0.9668  |
| Weighted F1-score   | 0.88    |

Selected class-level performance:

- `retroflex-stomach`: precision 1.00, recall 1.00  
- `cecum`: AUC 1.000  
- `polyps`: AUC 0.996, recall 0.99  
- `pylorus`: AUC 1.000  

Weaker classes such as Barrett’s esophagus and ulcerative-colitis-grade-0-1 have very few samples; here the main limitation is class imbalance rather than the model architecture.

---

## Class Imbalance and Clinical Risk

The poorest performing classes are those with very few samples. This is not only a statistical issue but also a clinical one:

- Under-represented classes tend to have lower recall, increasing the risk of false negatives.  
- In a clinical setting, false negatives are often more problematic than false positives, especially for pre-cancerous or inflammatory conditions.

Current handling:

- Excluding classes with fewer than 10 samples  
- Using stratified train/validation/test splits  

Planned next steps:

- Introduce class-weighted loss functions for minority classes.  
- Explore data-level augmentation for rare classes (oversampling, Mixup/CutMix).  
- Report per-class recall and false negative counts for clinically important categories (such as polyps and Barrett’s esophagus), rather than relying only on global metrics.

The objective is not only high overall accuracy but also error patterns that are clinically interpretable and acceptable.

---

## Explainability (XAI) and Generated Artifacts

High accuracy alone is not sufficient in medical AI; the model must focus on clinically relevant structures.

The pipeline produces the following artifacts:

- `class_distribution.png` – distribution of images per class  
- `training_curves.png` – training and validation loss and accuracy over epochs  
- `confusion_matrix.png` – test-set prediction heatmap  
- `roc_curves.png` – ROC-AUC curves for the top six classes  
- `gradcam.png` – Grad-CAM heatmaps from the final convolutional block  

Qualitative analysis:

- Polyps: verify that Grad-CAM highlights the polyp surface and surrounding mucosa, not specular highlights or tools.  
- Normal findings: check that attention is more diffuse and does not consistently focus on borders or artifacts.  
- Rare conditions: inspect whether the model is capturing meaningful patterns or simply overfitting to noise.

This qualitative inspection step is important before considering any model as clinically trustworthy.

---

## Running the Code

Kaggle:

- Open the notebook:  
  https://www.kaggle.com/code/inexxcsgo/kvasir-pathfinder  
- Attach the HyperKvasir dataset.  
- Enable a T4 GPU.  
- Run all cells.

Local or Google Colab:

```bash
# Install dependencies
pip install timm grad-cam scikit-learn

# Ensure the HyperKvasir dataset is available,
# then run the notebook cells sequentially.
```

---

## References

- Habe, Haataja, Toivanen. RT-DETR for Wireless Capsule Endoscopy. Frontiers in AI, 2025.  
- Habe, Haataja, Toivanen. Benchmarking Object Detection in WCE. IEEE Access, 2024.  
- Habe, Haataja, Toivanen. Deep Learning Review for GI Classification. F1000Research, 2024.  
- HyperKvasir dataset.  
- Tan and Le. EfficientNet. ICML, 2019.  
- Selvaraju et al. Grad-CAM. ICCV, 2017.  

---

## Author

Muhammed Inanc  
Student / Researcher, Inonu University — Turkey  
Founder, INEXX Interactive 
