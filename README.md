# 🩺 Ultrason Görüntülerinde Böbrek Bulgularının Tespiti

Bu çalışma, böbrek ultrason görüntülerindeki kist, taş ve tümör gibi patolojik bulguları nesne tespiti yaklaşımıyla yakalamak ve bunu pratik bir web arayüzü üzerinden hızlıca test edebilmek amacıyla geliştirildi.

Eğitilen model, görüntü üzerinde lezyonların yerini tespit edip sınırlayıcı kutularla (bounding box) işaretlerken, arayüz tarafında da sonuçlar temiz bir özet tablo olarak sunulmaktadır.

---

## 📸 Arayüzden Görüntüler

Sistem, yüklenen ultrason görüntüsünü analiz ederek bulunan lezyonu, konumunu ve tespit güvenini sade bir raporla ekrana basar.

| Analiz Öncesi | Analiz Sonucu |
| :---: | :---: |
| <img src=<img width="1600" height="901" alt="WhatsApp Image 2026-11-03 at 13 43 18" src="https://github.com/user-attachments/assets/781d9276-1b1d-42d2-8304-c35f74400c35" />
 width="450" /> | <img src=<img width="1600" height="914" alt="WhatsApp Image 2026-11-03 at 13 44 01" src="https://github.com/user-attachments/assets/147ea7f1-f6a1-4606-8784-1f592fa32b51" />
 width="450" /> |



---

## 🎯 Model Performansı ve Metrikler

Eğitim sürecinde elde edilen metrikler, modelin tespit hassasiyetinin genel olarak yüksek bir seviyeye ulaştığını gösteriyor:

* **mAP@50:** %96.7
* **Precision (Kesinlik):** %94.7
* **Recall (Duyarlılık):** %95.6
* **Genel F1-Skoru:** 0.9517

### Sınıf Bazlı Sonuçlar

| Sınıf | Precision | Recall | mAP@50 | F1-Skoru |
| :--- | :---: | :---: | :---: | :---: |
| **Kist (cysts)** | 0.998 | 1.000 | 0.995 | 0.999 |
| **Normal Doku** | 0.926 | 1.000 | 0.995 | 0.962 |
| **Taş (stones)** | 0.940 | 0.941 | 0.968 | 0.940 |
| **Tümör (tumors)** | 0.925 | 0.882 | 0.910 | 0.903 |

<br>

<p align="center">
  <img src=<img width="715" height="357" alt="WhatsApp Image 2026-11-03 at 13 17 49" src="https://github.com/user-attachments/assets/c856de0c-d878-49e8-8a78-03c590dc3238" />
 width="750" alt="Metrik Tablosu" />
</p>

---

## 🔬 Eğitim Süreci ve Değerlendirme

### Kayıp (Loss) ve Öğrenme Grafikleri
50 epoch süresince eğitim ve doğrulama kayıpları istikrarlı bir şekilde düşerken; precision, recall ve mAP değerleri ilk 20 epoch civarında dengeli bir plato seviyesine oturmuştur.

<p align="center">
  <img src=<img width="715" height="357" alt="WhatsApp Image 2026-11-03 at 13 17 49" src="https://github.com/user-attachments/assets/de1e7001-4aa0-4cbe-8c0f-3dfef04845d6" />
 />
width="800" alt="Eğitim Grafikleri" />
</p>

### Karmaşıklık Matrisi (Confusion Matrix) ve Eşik Değeri Seçimi
Modelin lezyonları kendi aralarında ayırt etme başarısı oldukça yüksektir. Ancak karmaşıklık matrisi detaylı incelendiğinde, ultrason dokusunun doğası gereği arka planın (background) bazı durumlarda yanlışlıkla kist veya taş olarak algılanabildiği görülmektedir.

<p align="center">
  <img src=<img width="716" height="536" alt="WhatsApp Image 2026-11-03 at 13 17 36" src="https://github.com/user-attachments/assets/28f4d0bd-ce29-4831-8006-5e63215b78d9" />
 width="500" alt="Karmaşıklık Matrisi" />
</p>

Bu durum göz önünde bulundurularak, arayüz tarafındaki güven eşiği (confidence threshold) varsayılan `0.25` yerine **`0.40`** bandına çekilmiştir. Böylece arka plan parazitleri filtrelenirken gerçek bulguların kaçırılmaması hedeflenmiştir.

---

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel ortamınızda ayağa kaldırmak için:

### 1. Depoyu Klonlayın
```bash
git clone [https://github.com/kullanici-adiniz/proje-adiniz.git](https://github.com/kullanici-adiniz/proje-adiniz.git)
cd proje-adiniz
