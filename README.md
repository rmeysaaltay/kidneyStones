# 🩺 Ultrason Görüntülerinde Böbrek Bulgularının Tespiti

Bu çalışma, böbrek ultrason görüntülerindeki kist, taş ve tümör gibi patolojik bulguları nesne tespiti yaklaşımıyla yakalamak ve bunu pratik bir web arayüzü üzerinden hızlıca test edebilmek amacıyla geliştirildi.

Eğitilen model, görüntü üzerinde lezyonların yerini tespit edip sınırlayıcı kutularla (bounding box) işaretlerken, arayüz tarafında da sonuçlar temiz bir özet tablo olarak sunulmaktadır.

---

## 📸 Arayüzden Görüntüler

Sistem, yüklenen ultrason görüntüsünü analiz ederek bulunan lezyonu, konumunu ve tespit güvenini sade bir raporla ekrana basar.

| Analiz Öncesi | Analiz Sonucu |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/781d9276-1b1d-42d2-8304-c35f74400c35" width="450" alt="Analiz Öncesi" /> | <img src="https://github.com/user-attachments/assets/147ea7f1-f6a1-4606-8784-1f592fa32b51" width="450" alt="Analiz Sonucu" /> |

---

## 🎯 Model Performansı ve Metrikler

Eğitim sürecinde elde edilen metrikler, modelin tespit hassasiyetinin genel olarak yüksek bir seviyeye ulaştığını gösteriyor:

- **mAP@50:** %96.7
- **Precision (Kesinlik):** %94.7
- **Recall (Duyarlılık):** %95.6
- **Genel F1-Skoru:** 0.9517

### Sınıf Bazlı Sonuçlar

| Sınıf | Precision | Recall | mAP@50 | F1-Skoru |
| :--- | :---: | :---: | :---: | :---: |
| **Kist (cysts)** | 0.998 | 1.000 | 0.995 | 0.999 |
| **Normal Doku** | 0.926 | 1.000 | 0.995 | 0.962 |
| **Taş (stones)** | 0.940 | 0.941 | 0.968 | 0.940 |
| **Tümör (tumors)** | 0.925 | 0.882 | 0.910 | 0.903 |

<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c856de0c-d878-49e8-8a78-03c590dc3238" width="700" alt="Metrik Tablosu" />
</p>

---

## 🔬 Eğitim Süreci ve Değerlendirme

### Kayıp (Loss) ve Öğrenme Grafikleri
50 epoch süresince eğitim ve doğrulama kayıpları istikrarlı bir şekilde düşerken; precision, recall ve mAP değerleri ilk 20 epoch civarında dengeli bir plato seviyesine oturmuştur.

<p align="center">
  <img src="https://github.com/user-attachments/assets/de1e7001-4aa0-4cbe-8c0f-3dfef04845d6" width="750" alt="Eğitim Grafikleri" />
</p>

### Karmaşıklık Matrisi (Confusion Matrix) ve Eşik Değeri Seçimi
Modelin lezyonları kendi aralarında ayırt etme başarısı oldukça yüksektir. Ancak karmaşıklık matrisi detaylı incelendiğinde, ultrason dokusunun doğası gereği arka planın (background) bazı durumlarda yanlışlıkla kist veya taş olarak algılanabildiği görülmektedir.

<p align="center">
  <img src="https://github.com/user-attachments/assets/28f4d0bd-ce29-4831-8006-5e63215b78d9" width="500" alt="Karmaşıklık Matrisi" />
</p>

⚠️ Sorumluluk Reddi
Bu proje akademik araştırma ve geliştirme amaçlı hazırlanmıştır. Elde edilen çıkarımlar tıbbi tanı veya teşhis niteliği taşımaz; klinik kararlarda doğrudan kullanılamaz.
