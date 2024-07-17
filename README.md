# hamming-simulator

Bu Python uygulaması, Hamming kodu oluşturma, belleğe yazma, bellekten okuma, hata enjekte etme ve hatalı verileri düzeltme işlemlerini simüle eder. Hamming kodu, veri iletilirken oluşabilecek tek bitlik hataları tespit edip düzeltebilen bir hata düzeltme kodlama tekniğidir.

## Özellikler

- Veri girişi için kullanıcı dostu arayüz.
- Oluşturulan Hamming kodunun gösterilmesi.
- Hamming kodunun belleğe yazılması ve bellekten okunması.
- Belirli bir adres ve bit pozisyonuna hata enjekte edilmesi.
- Enjekte edilen hatanın tespit edilip düzeltilmesi.

## Nasıl Kullanılır

1. **Veri Girişi**: Uygulama başlatıldığında, "Veri (4, 8, 16 bit) boşluksuz" bir form görüntülenir. Buraya oluşturmak istediğiniz veriyi girin.

2. **Hamming Kodu Oluşturma**: "Hamming Kodu Oluştur" butonuna tıklayarak girdiğiniz veri için Hamming kodunu oluşturun. Oluşturulan kod, ekranda gösterilir.

3. **Belleğe Yazma**: "Belleğe Yaz" butonu ile oluşturulan Hamming kodunu belirli bir adrese belleğe yazın.

4. **Bellekten Okuma**: "Bellekten Oku" butonu ile belirli bir adresten Hamming kodunu okuyun. Eğer hata tespit edilirse, düzeltilmiş kod ekranda gösterilir.

5. **Hata Enjekte Etme**: "Hata Enjekte Et" butonu ile belirli bir adreste ve bit pozisyonunda hata enjekte edin. Enjekte edilen hatalı kod ve düzeltilmiş kod ekranda gösterilir.

## Kurulum

1. Depoyu yerel makinenize klonlayın:

    ```bash
    git clone https://github.com/Adileakklc/hamming-simulator.git
    cd hamming-simulator
    ```

2. Uygulamayı başlatın:

    ```bash
    python hamming_simulator.py
    ```

## Gereksinimler

- Python 3.x
- tkinter (Python'un standart kütüphanesi)
