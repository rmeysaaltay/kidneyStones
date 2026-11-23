
# 🩺 Böbrek Ultrason Görüntülerinde Patoloji Tespiti (YOLOv8)

Böbrek ultrason (US) görüntüleri üzerinde **kist (`cysts`)**, **böbrek taşı (`stones`)**, **tümör (`tumors`)** ve **normal doku (`normal`)** sınıflarını gerçek zamanlı olarak tespit eden derin öğrenme ve Gradio arayüzlü karar destek sistemidir[cite: 14].

Bu repo hem temel **YOLOv8s** tespit modelini hem de veri artırma (augmentation) kullanılmadan yürütülen **klinik ön işleme (CLAHE, Median, Bilateral)** ve **sınıf dengesizliği (Class Weighting, Focal Loss)** ablasyon deneylerini içerir[cite: 12, 13, 14].

---

## 📂 Proje Yapısı

- `kidney_stones.py`: YOLOv8s tabanlı temel model eğitimi ve test değerlendirme betiği[cite: 14].
- `kidney_experiments.ipynb`: Veri artırma kapalı (`NO_AUG`) koşullarda ön işleme ve kayıp fonksiyonu (loss) ablasyon deneyleri[cite: 12, 13].
- `interface`: Gradio tabanlı etkileşimli web arayüzü[cite: 14].
- `kidneybest.pt`: Eğitilmiş model ağırlık dosyası[cite: 14].
- `all_results.csv` & `comparison.png`: Deneylerin karşılaştırmalı test metrikleri ve görselleştirmeleri.

---

## 🧪 Deneysel Sonuçlar (Ablasyon Çalışması)

Tüm ablasyon deneyleri **YOLOv8n** mimarisi üzerinde, aynı hiperparametreler (`epochs=30`, `imgsz=640`, `batch=16`, `seed=42`) ve **online/offline augmentation kapalı** olarak 66 görüntülük bağımsız test setinde değerlendirilmiştir[cite: 13].

### Genel Performans Karşılaştırması

| Deney Grubu | Yöntem | mAP@50 | mAP@50-95 | Precision (P) | Recall (R) | Süre (ms) | FPS |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline** | `yolov8n_ham` (İşlemsiz) | %95.18 | %55.17 | %87.20 | %94.76 | 10.20 ms | 98.1 |
| **Ön İşleme** | `yolov8n_clahe` | %95.82 | %54.54 | %93.83 | **%96.74** | 10.80 ms | 92.6 |
| **Ön İşleme** | `yolov8n_median` | **%97.79** | **%56.87** | **%98.24** | %91.34 | 11.03 ms | 90.7 |
| **Ön İşleme** | `yolov8n_bilateral` | %97.10 | %55.24 | %91.27 | %93.31 | 10.47 ms | 95.5 |
| **Sınıf Dengesizliği** | `yolov8n_classweight` | %96.99 | %53.07 | %98.19 | %94.16 | 10.44 ms | 95.8 |
| **Sınıf Dengesizliği** | `yolov8n_focal` | %91.11 | %54.14 | %73.09 | %89.64 | 13.35 ms | 74.9 |

### Sınıf Bazlı AP@50 / Recall Dağılımı

| Yöntem | Cysts (AP50 / R) | Normal (AP50 / R) | Stones (AP50 / R) | Tumors (AP50 / R) |
| :--- | :---: | :---: | :---: | :---: |
| **Ham (Baseline)** | %99.5 / %100.0 | %99.5 / %92.1 | %90.1 / %94.1 | %91.6 / %92.9 |
| **CLAHE** | %99.5 / %100.0 | %99.5 / **%100.0** | %88.1 / %94.1 | %96.1 / %92.9 |
| **Median Filtre** | %99.5 / %100.0 | %99.5 / %78.4 | **%94.5** / %94.1 | **%97.7** / %92.9 |
| **Bilateral Filtre** | %99.5 / %100.0 | %99.5 / %93.4 | **%94.5** / %94.1 | %94.9 / %85.7 |
| **Class Weighting** | %98.7 / %96.6 | %99.5 / **%100.0** | **%94.5** / %94.1 | %95.2 / %86.0 |
| **Focal Loss** | %96.3 / %100.0 | %85.4 / %83.3 | %92.1 / %82.4 | %90.7 / %92.9 |

### Öne Çıkan Bulgular
- **Speckle Gürültü Giderimi:** Ultrason görüntülerindeki beneklenme gürültüsünü bastıran **Median Filtre (`5x5`)**, mAP@50 değerini `%95.18`'den **`%97.79`** seviyesine ve Precision değerini **`%98.24`** seviyesine taşıyarak en yüksek genel tespiti sağladı.
- **Azınlık Sınıf Dengesi:** Veri çoğaltma yapılmadan uygulanan **Ters Frekans Ağırlıklı BCE (Class Weighting)** yöntemi, veri setindeki en az örnekli sınıf olan `normal` dokuda Recall oranını `%92.1`'den **`%100.0`** seviyesine çıkardı.

---
## 📸 Arayüzden Görüntüler

Sistem, yüklenen ultrason görüntüsünü analiz ederek bulunan lezyonu, konumunu ve tespit güvenini sade bir raporla ekrana basar.

| Analiz Öncesi | Analiz Sonucu |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/781d9276-1b1d-42d2-8304-c35f74400c35" width="450" alt="Analiz Öncesi" /> | <img src="https://github.com/user-attachments/assets/147ea7f1-f6a1-4606-8784-1f592fa32b51" width="450" alt="Analiz Sonucu" /> |


⚠️ Sorumluluk Reddi
Bu proje akademik araştırma ve geliştirme amaçlı hazırlanmıştır. Elde edilen çıkarımlar tıbbi tanı veya teşhis niteliği taşımaz; klinik kararlarda doğrudan kullanılamaz.
