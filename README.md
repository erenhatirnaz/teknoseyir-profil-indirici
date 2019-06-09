# TeknoSeyir Profil İndirici
> [TeknoSeyir](https://teknoseyir.com)'de paylaştığınız içerikleri
> indirmenize yarayan betik.

**Sürüm: 0.1.0 - Beta**

**İndirilen içerikler:**
* Takipçi ve takip edilenler listesi
* Profil resmi
* Durumlar (+ yorumlar, cevaplar ve resimler)
* Blog Yazıları (+ yorumlar, cevaplar ve resimler)
* İncelemeler (+ yorumlar, cevaplar ve resimler)
* Resim dosyaları

## Motivasyon
Gün içerisinde en çok vakit geçirdiğim, videolarıyla satın alma kararı verdiğim
ve bağımsızlığına güvendiğim tek platforma bir şekilde katkı sağlamış olmak bu
proje için ana motivasyonum. Bunun yanında, üyelere, hesaplarını silmek
isterlerse ya da günün birinde TeknoSeyir kapanacak olursa, paylaşımlarının
yedeklerini alabilmeleri için bir imkan sağlamak istedim.

## Gereksinimler
* Python 3 ve/veya üzeri
* BeautifulSoup4 (`sudo apt install python3-bs4` ya da `pip install -r
  gereksinimler.txt` komutları ile yüklenebilir)

Sisteminizin gereksinimleri karşılayıp karşılamadığını kontrol etmek için:
* `python --version` komutunu çalıştırarak Python sürümünüzü öğrenebilirsiniz.
  Bazı GNU/Linux dağıtımlarında Python 2 ve Python 3 sürümleri aynı anda
  bulunabiliyor ve genelde `python`, `pip` komutları Python 2 sürümünü işaret
  eder. Böyle bir durumda onların yerine `python3` ve `pip3` komutlarını
  kullanın. Dökümanın devamındaki komutları da bu bilgiye göre
  değiştirebilirsiniz.
* `pip freeze | grep -i beautifulsoup4` komutu çıktı veriyorsa ilgili kütüphane
  sisteminizde yüklü demektir.

**NOT:** Bu betiği bir GNU/Linux dağıtımı üzerinde kodladığım için sadece bu
sistem üzerinde deneme imkanım oldu. Windows ya da Mac için bir deneme
yapamadım. İşletim sistemine özel komutlar kullanmadığım için büyük ihtimal
gereksinimleri karşılayan her sistemde çalışacaktır fakat çalışmadığı durumlarda
[Hata Raporlama başlığına bakınız](#hata-raporlama).

## Kurulum
Depoyu indirmek için:

* ZIP arşivi olarak indirmek için:
```sh
$ wget https://github.com/erenhatirnaz/teknoseyir-profil-indirici/archive/master.zip
$ unzip master.zip -d teknoseyir-profil-indirici
```
* `git` kullanarak indirmek için:
```sh
$ git clone https://github.com/erenhatirnaz/teknoseyir-profil-indirici.git
```

Daha sonra kurulumu tamamlamak için:
```sh
$ cd teknoseyir-profil-indirici
$ pip install -r gereksinimler.txt
```

## Kullanım
Kurulum aşamaları sorunsuz bir şekilde tamamlandıysa `python
teknoseyir-profil-indirici.py` komutunu çalıştırdınızda şöyle
bir çıktı alıyor olmanız gerek:

```txt
     _____    _               ____             _
    |_   _|__| | ___ __   ___/ ___|  ___ _   _(_)_ __
      | |/ _ \ |/ / '_ \ / _ \___ \ / _ \ | | | | '__|
      | |  __/   <| | | | (_) |__) |  __/ |_| | | |
      |_|\___|_|\_\_| |_|\___/____/ \___|\__, |_|_|
                               _         |___/
  ____             __ _ _     (_)           _ _      _      _
 |  _ \ _ __ ___  / _(_) |   |_ _|_ __   __| (_)_ __(_) ___(_)
 | |_) | '__/ _ \| |_| | |    | || '_ \ / _` | | '__| |/ __| |
 |  __/| | | (_) |  _| | |    | || | | | (_| | | |  | | (__| |
 |_|   |_|  \___/|_| |_|_|   |___|_| |_|\__,_|_|_|  |_|\___|_|
                    Sürüm: 0.1.0 - Beta
        Eren Hatırnaz (teknoseyir.com/u/erenhatirnaz)
                        ---*---
 Bu betik GNU Genel Kamu Lisansı v3 ile lisanslanmıştır ve
 bir özgür yazılımdır. Bazı koşullar altında yeniden dağıtmak
 serbesttir. Lisans detayları için LICENSE dosyasına bakınız.
                        ---*---

> Kullanıcı Adın:
```
kullanıcı adınızı yazıp, `[ENTER]` tuşuna basarak paylaşımlarınızı indirmeye
başlayabilirsiniz. İndirme işlemini iptal etmek için `CTRL+C` tuşlarına
basabilirsiniz. Profil indirme işleminiz bittiğinde indirilen içerik sayılarını
gösteren bir çıktı almanız gerekiyor. İndirilen tüm içerikleriniz betik dosyası
ile aynı klasör içerisinde olacaktır.

## Bilinen Sorunlar
* Yetki gerektiği için kendi durumlarınız dışındaki durumlara yaptığınız
  yorumları getiremiyor.
* WordPress yapısı nedeniyle durumlarda paylaşılan bağlantıların önizleme
  görüntüleri de (thumbnail) resimler klasörüne indiriliyor. Maalesef ayırt
  etmenin bir yolunu bulamadım.
* Nedenini anlamadığım bir şekilde bazı kullanıcıların bilgilerini getiremiyorum.
  Yorumlarda bazı kullanıcı adlarını göremezseniz nedeni büyük ihtimal budur.
* Profil resminiz animasyonlu bir GIF dosyası ise ana dizindeki
  `profil-resmi.jpg` dosyası gerçek profil resminiz olmayabilir. Gerçek profil
  resminiz `resimler` klasörü içerisine indirilecek. Bu sorunun sebebi
  Wordpress'in Gravatar sisteminin GIF uzantısını desteklememesi ve TeknoSeyir'de
  bunun farklı bir şekilde çözülmüş olması.
* Blog yazılarındaki resimleri HTML içerisinden işleyip `İçerik:` kısmında yazı
  içerisinde göstermek kod karmaşıklığını arttıracağı için resim linklerini
  `Resimler:` kısmında, yazıdaki sırasına göre alt alta yazdırmayı tercih ettim.
* Yetki gerektiği için engellenenler listesini getiremiyorum.
* Yazdığınız ürün incelemelerinde ürüne verdiğiniz puanı getiremiyorum.

## Hata Raporlama
Betiğin çalışması sırasında, kodlardan kaynaklı olduğunu düşündüğünüz bir hata
alırsanız bunu, betik çıktısı ile birlikte [Github üzerinden issue
açarak](https://github.com/erenhatirnaz/teknoseyir-profil-indirici/issues/new) ya
da [e-posta adresim üzerinden bana yazarak](mailto:erenhatirnaz@hotmail.com.tr)
iletilirsiniz.

## Lisans
> teknoseyir-profil-indirici

> Copyright (C) 2019 Eren Hatırnaz <erenhatirnaz@hotmail.com.tr> [GPG: 0x8e64942a]

Bu program özgür yazılımdır: Özgür Yazılım Vakfı tarafından yayımlanan GNU
Genel Kamu Lisansı’nın sürüm 3 ya da (isteğinize bağlı olarak) daha sonraki
sürümlerinin hükümleri altında yeniden dağıtabilir ve/veya değiştirebilirsiniz.

Bu program, yararlı olması umuduyla dağıtılmış olup, programın BİR TEMİNATI
YOKTUR; TİCARETİNİN YAPILABİLİRLİĞİNE VE ÖZEL BİR AMAÇ İÇİN UYGUNLUĞUNA dair
bir teminat da vermez. Ayrıntılar için GNU Genel Kamu Lisansı’na göz atınız.

Bu programla birlikte GNU Genel Kamu Lisansı’nın bir kopyasını elde etmiş
olmanız gerekir. Eğer elinize ulaşmadıysa <http://www.gnu.org/licenses/>
adresine bakınız.
