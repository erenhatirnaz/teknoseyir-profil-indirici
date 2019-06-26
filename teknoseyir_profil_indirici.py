# -*- coding: utf-8 -*-

# teknoseyir-profil-indirici
# Copyright (C) 2019 Eren Hatırnaz <erenhatirnaz@hotmail.com.tr> [GPG: 0x8e64942a]
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı tarafından yayımlanan GNU
# Genel Kamu Lisansı’nın sürüm 3 ya da (isteğinize bağlı olarak) daha sonraki
# sürümlerinin hükümleri altında yeniden dağıtabilir ve/veya değiştirebilirsiniz.
#
# Bu program, yararlı olması umuduyla dağıtılmış olup, programın BİR TEMİNATI
# YOKTUR; TİCARETİNİN YAPILABİLİRLİĞİNE VE ÖZEL BİR AMAÇ İÇİN UYGUNLUĞUNA dair
# bir teminat da vermez. Ayrıntılar için GNU Genel Kamu Lisansı’na göz atınız.
#
# Bu programla birlikte GNU Genel Kamu Lisansı’nın bir kopyasını elde etmiş
# olmanız gerekir. Eğer elinize ulaşmadıysa <http://www.gnu.org/licenses/>
# adresine bakınız.

#      _____    _               ____             _
#     |_   _|__| | ___ __   ___/ ___|  ___ _   _(_)_ __
#       | |/ _ \ |/ / '_ \ / _ \___ \ / _ \ | | | | '__|
#       | |  __/   <| | | | (_) |__) |  __/ |_| | | |
#       |_|\___|_|\_\_| |_|\___/____/ \___|\__, |_|_|
#                               _          |___/
#  ____             __ _ _     (_)           _ _      _      _
# |  _ \ _ __ ___  / _(_) |   |_ _|_ __   __| (_)_ __(_) ___(_)
# | |_) | '__/ _ \| |_| | |    | || '_ \ / _` | | '__| |/ __| |
# |  __/| | | (_) |  _| | |    | || | | | (_| | | |  | | (__| |
# |_|   |_|  \___/|_| |_|_|   |___|_| |_|\__,_|_|_|  |_|\___|_|
#
# Betik    : teknoseyir_profil_indirici.py
# Sürüm    : 0.1.1 - Beta
# Açıklama : TeknoSeyir profilinizdeki bilgileri indirmenize yarar.
# Yazar    : Eren Hatırnaz (teknoseyir.com/u/erenhatirnaz)
# Lisans   : GNU General Public License v3

from sys import stderr
from os import path, makedirs

from json import load
from bs4 import BeautifulSoup as bs

from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, urlretrieve

# SABİTLER
# --------
TS_API = "https://teknoseyir.com/wp-json/wp/v2"
TS_AJAX = "https://teknoseyir.com/wp-admin/admin-ajax.php"

# Sürüm numarası
SURUM = "0.1.1 - Beta"

# İndirme limitleri
LIMITLEME=True
DURUM_LIMITI=5
BLOG_LIMITI=5
INCELEME_LIMITI=5
RESIM_LIMITI=5

# API sorgularındaki sayfa başına girdi sayısı.
# Bu sabit durumlar, blog yazıları, resimler ve incelemeler için kullanılıyor.
# Yorumlar ve cevaplar için bu değer 2 ile çarpılıp kullanılıyor.
SAYFALAYICI_LIMITI = 40

# FONKSIYONLAR
# ------------
def sayfalayici(sayfa_no, girdi_limiti=SAYFALAYICI_LIMITI, siralama='desc'):
    """API sorgularındaki sayfalama sistemi için query string üretir.

    Argümanlar:
      sayfa_no(int): Getirilmek istenen sayfa numarası
      girdi_limiti(int): Sayfada başına girdi sayısı (Varsayılan: SAYFALAYICI_LIMITI)
      siralama(string): Girdilerin sıralaması (Varsayılan: desc)
         (Geçerli değerler: asc, desc)

    Dönüş Değeri:
      string: Sayfalayıcı değişkenlerini içeren query string.
              Örnek: &page=1&per_page=2&order=desc
    """

    return "&page={0}&per_page={1}&order={2}".format(sayfa_no,
                                                     girdi_limiti,
                                                     siralama)

def kullanici_getir(kullanici_url):
    """Verilen URL'deki API kaynağından kullanıcı bilgilerini getirir.

    Getirilen bilgiler: Kullanıcı ID, görünen ad, kullanıcı adı, profil resmi
    bağlantısı ve kullanıcıya ait içeriklere erişilebilecek API linkleri.

    Argümanlar:
      kullanici_url(string): teknoseyir.com/wp-json/wp/v2/users/[KULLANICI_ID]
      girdi_limiti(int): Sayfa başına girdi limiti. (Varsayılan: )

    Dönüş değeri:
      dict: Yukarıda belirtilen kullanıcı bilgilerini içeren dictionary nesnesi
    """
    try:
        kullanici_req = urlopen(kullanici_url)
        kullanici = load(kullanici_req)

        return {
            'id': kullanici['id'],
            'gorunen_ad': kullanici['name'],
            'kullanici_adi': kullanici['slug'],
            'profil_resmi': kullanici['avatar_urls']['96'],
            'linkler': {
                'durumlar': TS_API + "/durum?author=" + str(kullanici['id']),
                'blog_yazilari': TS_API + "/blog?author=" + str(kullanici['id']),
                'incelemeler': TS_API + "/inceleme?author=" + str(kullanici['id']),
                'resimler': TS_API + "/media?author=" + str(kullanici['id'])
            }
        }
    except HTTPError as err:
        print("Kullanici bilgileri getirilirken hata oluştu! \"{0} {1}\"".\
              format(err.code, err.reason), file=sys.stderr)
        print("\"Hayatta iyi şeyler olmaz!\" -LP")

def kullanici_url_getir(kullanici_adi):
    """Kullanıcı adı verilen kullanıcının API kaynağının URL'sini getirir.

    Argümanlar:
      kullanici_adi(string): Kullanıcı adı. Boşluk içeremez.

    Dönüş Değeri:
      string: teknoseyir.com/wp-json/wp/v2/users/[KULLANICI_ID]
    """
    try:
        url = "{0}/users?slug={1}".format(TS_API, kullanici_adi)
        return load(urlopen(url))[0]['_links']['self'][0]['href']
    except IndexError:
        print("Kullanıcı bulunamadı.")
        print("\"Hata olmadı ki bu!\" -HK")
        exit()

def kullanici_listesi_getir(tip, kullanici_id):
    """Verilen Kullanıcı ID'sine ait kullanıcının istenen tipdeki listesini
       getirir.

    Listelerdeki kullanıcıların getirilen bilgileri: Kullanıcı ID, görünen ad,
    kullanıcı adı.

    Yetki gerektirdiği için engellenenler listesini getiremiyor. Ayrıca bu
    fonksiyon TS_AJAX değişkeninde tanımlanmış API'yi kullanıyor.

    Argümanlar:
      tip(string): Kullanıcının getirilmek istenen listesi.
         (Geçerli  değerler: takip-eden, takip-edilen)
      kullanici_id(int): Kullanıcı ID.

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen kullanıcı bilgilerini içeren dictionary
                  nesnelerinden oluşan liste.
    """
    sorgu = {
        'action': 'author_takip_stream',
        'is_author': 1,
        'type': tip,
        'user_id': 1568,
        'shown_objects[]': []
    }

    # İlk sorgunun json şeklinde gelebilmesi için bu değişkende bir eleman olması
    # gerekiyor. Listeyi return etmeden önce bunu siliyorum.
    liste = [ { 'id': 0 } ]
    for loop in range(1, 15):
        sorgu['loop'] = loop

        idler = map(lambda kullanici: kullanici['id'], liste)
        for id in idler: sorgu['shown_objects[]'].append(id)

        encoded_sorgu = urlencode(sorgu, True).encode("utf-8")
        cevap = urlopen(TS_AJAX, encoded_sorgu)

        html = load(cevap)['data']['items']
        if not html: break

        html = bs(html, "html.parser")
        liste_html = html.findAll('article', attrs={'class': 'user'})
        for kullanici_html in liste_html:
            kullanici = kullanici_html.find('a',
                                            attrs={'class': 'author'}).\
                                            get_text().split('@')

            liste.append({
                'id': kullanici_html['id'].split('-')[1],
                'gorunen_ad': kullanici[0],
                'kullanici_adi': kullanici[1]
            })
    del liste[0] # İlk verileri çekebilmek için eklediğim elemanı siliyorum
    return liste

def durumlari_getir(durumlar_url, sayfa_no=1):
    """Verilen URL'deki API kaynağının istenen sayfasındaki durumları getirir.

    Getirilen bilgiler: Durum ID, başlık, tarih, link, içerik ve duruma ait diğer
    bilgilere erişilebilecek API kaynaklarının linkleri.

    Argümanlar:
      durumlar_url(string): teknoseyir.com/wp-json/wp/v2/durum?author=[KULLANICI_ID]
      sayfa_no(int): Getirilmek istenen sayfa numarası. (Varsayılan: 1)

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen durum bilgilerini içeren dictionary
                  nesnelerinden oluşan liste.
    """
    durumlar_url = durumlar_url + sayfalayici(sayfa_no)
    durumlar_req = urlopen(durumlar_url)

    durumlar = []
    for durum in load(durumlar_req):
        linkler = durum['_links']
        durum_icerik = bs(durum['content']['rendered'], "html.parser").get_text().strip()

        durumlar.append({
            'id': durum['id'],
            'baslik': durum['guid']['rendered'].split('/')[-1],
            'tarih': durum['date'],
            'link': durum['link'],
            'icerik': durum_icerik,
            'linkler': {
                'resimler': linkler['wp:attachment'][0]['href'],
                'yorumlar': linkler['replies'][0]['href']
            }
        })
    return durumlar

def yorumlari_getir(yorumlar_url):
    """Verilen URL'deki API kaynağından yorumları getirir.

    Getirilen bilgiler: Yorum tarihi, yazarın görünen adı ve kullanıcı adı, yorum
    içeriği ve yoruma ait diğer bilgilere erişilebilecek API kaynaklarının
    linkleri.

    Geliştirici Notu:
      Bu fonksiyona argüman olarak sayfalayıcı eklemedim bunun yerine sayfalayıcı
      limitini 2 katına çıkarıp (80) bir sayfada tüm yorumların gelmesini
      bekliyorum. Durumlarda, incelemelerde ve blog yazılarında o kadar çok yorum
      olmayacağını varsayarak böyle bir karar verdim. Elbette istisnai durumlar
      olabilir fakat yine de kod karmaşıklığını ve API'ye gönderilecek istek
      sayısını arttırmak istemedim.

    Argümanlar:
      yorumlar_url(string): teknoseyir.com/wp-json/wp/v2/comments?post=[DURUM_ID]

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen yorum bilgilerini içeren dictionary
      nesnelerinden oluşan liste.
    """
    yorumlar_url = yorumlar_url + sayfalayici(1, SAYFALAYICI_LIMITI * 2, 'asc')
    yorumlar_req = urlopen(yorumlar_url)

    yorumlar = []
    for yorum in load(yorumlar_req):
        linkler = yorum['_links']

        # Nedenini anlamadığım bir şekilde bazı kullanıcıların bilgilerini
        # getiremediğim için böyle bir çözüm üretmek zorunda kaldım.
        try:
            kullanici = kullanici_getir(linkler['author'][0]['href'])
            kullanici_adi = kullanici['kullanici_adi']
        except:
            kullanici_adi = ""

        yrm = {
            'tarih': yorum['date'],
            'gorunen_ad': yorum['author_name'],
            'kullanici_adi': kullanici_adi,
            'icerik': bs(yorum['content']['rendered'], "html.parser").get_text().strip(),
            'linkler': {}
        }
        if 'children' in linkler:
            yrm['linkler']['cevaplar'] = linkler['children'][0]['href']
        if 'in-reply-to' not in linkler: yorumlar.append(yrm)
    return yorumlar

def cevaplari_getir(cevaplar_url):
    """Verilen URL'deki API kaynağından cevaplari getirir.

    Getirilen bilgiler: Cevap tarihi, yazarın görünen adı ve kullanıcı adı ve
    cevap içeriği.

    Geliştirici Notu:
      Bu fonksiyona argüman olarak sayfalayıcı eklemedim bunun yerine sayfalayıcı
      limitini 2 katına çıkarıp (80) bir sayfada tüm cevapların gelmesini
      bekliyorum. Durumlarda, incelemelerde ve blog yazılarında o kadar çok yorum
      olmayacağını varsayarak böyle bir karar verdim. Elbette istisnai durumlar
      olabilir fakat yine de kod karmaşıklığını ve API'ye gönderilecek istek
      sayısını arttırmak istemedim.

    Argümanlar:
      cevaplar_url(string): teknoseyir.com/wp-json/wp/v2/comments?parent=[YORUM_ID]

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen yorum bilgilerini içeren dictionary
                  nesnelerinden oluşan liste.
    """
    cevaplar_url = cevaplar_url + sayfalayici(1, SAYFALAYICI_LIMITI * 2, 'asc')
    cevaplar_req = urlopen(cevaplar_url)

    cevaplar = []
    for cevap in load(cevaplar_req):
        linkler = cevap['_links']

        # Nedenini anlamadığım bir şekilde bazı kullanıcıların bilgilerini
        # getiremediğim için böyle bir çözüm üretmek zorunda kaldım.
        try:
            kullanici = kullanici_getir(linkler['author'][0]['href'])
            kullanici_adi = kullanici['kullanici_adi']
        except:
            kullanici_adi = ""

        cevaplar.append({
            'tarih': cevap['date'],
            'gorunen_ad': cevap['author_name'],
            'kullanici_adi': kullanici_adi,
            'icerik': bs(cevap['content']['rendered'], "html.parser").get_text().strip()
        })
    return cevaplar

def blog_yazilari_getir(blog_yazilari_url, sayfa_no=1):
    """Verilen URL'deki API kaynağının istenen sayfasındaki blog yazılarını getirir

    Getirilen bilgiler: Blog yazısı ID, tarih, isim, link, başlık, icerik ve blog
    yazısına ait diğer bilgilere erişilebilecek API kaynaklarının linkleri.

    Argümanlar:
      blog_yazilari_url(string): teknoseyir.com/wp-json/wp/v2/blog?author=[KULLANICI_ID]
      sayfa_no(int): Getirilmek istenen sayfa numarası. (Varsayılan: 1)

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen blog yazısı bilgilerini içeren dictinary
                  nesnelerinden oluşan liste.
    """
    blog_yazilari_url = blog_yazilari_url + sayfalayici(sayfa_no)
    blog_yazilari_req = urlopen(blog_yazilari_url)

    blog_yazilari = []
    for blog_yazisi in load(blog_yazilari_req):
        linkler = blog_yazisi['_links']
        blog_icerik = bs(blog_yazisi['content']['rendered'], "html.parser").get_text()

        blog_yazilari.append({
            'id': blog_yazisi['id'],
            'tarih': blog_yazisi['date'],
            'isim': blog_yazisi['slug'],
            'link': blog_yazisi['link'],
            'baslik': blog_yazisi['title']['rendered'],
            'icerik': blog_icerik.strip(),
            'linkler': {
                'yorumlar': linkler['replies'][0]['href'],
                'resimler': linkler['wp:attachment'][0]['href']
            }
        })
    return blog_yazilari

def incelemeleri_getir(incelemeler_url, sayfa_no=1):
    """Verilen URL'deki API kaynağından istenen sayfasındaki incelemeleri getirir.

    Getirilen bilgiler: Inceleme ID, tarih, link, urun (urun_adi_getir), isim,
    baslik, icerik ve incelemeye ait diğer bilgilere erişilebilecek API
    kaynaklarının linkleri.

    Argümanlar:
      incelemer_url(string): teknoseyir.com/wp-json/wp/v2/inceleme?author=[KULLANICI_ID]
      sayfa_no(int): Getirilmek istenen sayfa numarası. (Varsayılan: 1)

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen inceleme bilgilerini içeren dictionary
                  nesnelerinden oluşan liste.
    """
    incelemeler_url = incelemeler_url + sayfalayici(sayfa_no)
    incelemeler_req = urlopen(incelemeler_url)

    incelemeler = []
    for inceleme in load(incelemeler_req):
        linkler = inceleme['_links']
        icerik = bs(inceleme['content']['rendered'], "html.parser").get_text().strip()

        incelemeler.append({
            'id': inceleme['id'],
            'tarih': inceleme['date'],
            'link': inceleme['link'],
            'urun': urun_adi_getir(inceleme['urun'][0]),
            'isim': inceleme['slug'],
            'baslik': inceleme['title']['rendered'],
            'icerik': icerik,
            'linkler': {
                'yorumlar': linkler['replies'][0]['href'],
                'resimler': linkler['wp:attachment'][0]['href']
            }
        })
    return incelemeler

def urun_adi_getir(urun_id):
    """ID numarası verilen ürünün adını getirir.

    Bu fonksiyon, kullanıcıya ait ürün incelemeleri getirilirken ürün
    isminin ayrı şekilde gösterilmesi için kullanılıyor.

    Argümanlar:
      urun_id(int): Ürün ID.

    Dönüş değeri:
      string: Ürün Adı.
    """

    urun_url = TS_API + "/urun/" + str(urun_id)
    urun_req = urlopen(urun_url)

    return load(urun_req)['name']

def resimleri_getir(resimler_url, sayfa_no=1, sira='desc'):
    """Verilen URL'deki API kaynağından istenen sayfa ve sıraya göre resimleri
       getirir.

    Getirilen bilgiler: Resim ID, Resim URL

    Argümanlar:
      resimler_url(string): teknoseyir.com/wp-json/wp/v2/media?parent=[DURUM_ID]
      sayfa_no(int): Getirilmek istenen sayfa numarası. (Varsayılan: 1)
      sira(string): Getirilmek istenen sıralama şekli. (Varsayılan: desc)
                    (Kabul edilen değerler: asc, desc)

    Dönüş değeri:
      list[dict]: Yukarıda belirtilen resim bilgilerini içeren dictionary
                  nesnelerinden oluşan liste.
    """
    TS_UPLOADS = "https://teknoseyir.com/wp-content/uploads/"

    resimler_url = resimler_url + sayfalayici(sayfa_no, siralama=sira)
    resimler_req = urlopen(resimler_url)

    resimler = []
    for resim in load(resimler_req):
        resimler.append({
            'id': resim['id'],
            'url': TS_UPLOADS + resim['media_details']['file']
        })
    return resimler

def yorumlari_yazdir(dosya, yorumlar_url):
    """API kaynağından getirilen yorumları verilen dosyaya yazdırır.

    Yazdırma formatı:
      *  [TARİH] [GORUNEN_AD] ([KULLANICI_ADI]): "[İÇERİK]"

    Argümanlar:
      dosya(file): Yorumların yazdırılması istenen dosya nesnesi. Dosya adı değil!
      yorumlar_url(string): teknoseyir.com/wp-json/wp/v2/comments?post=[DURUM_ID]

    Dönüş değeri:
      int: Verilen dosyaya yazdırılan yorum sayısı. İstatistiklere eklenmesi için
           kullanılıyor.
    """
    sayac = 0
    yorumlar = yorumlari_getir(yorumlar_url)

    if len(yorumlar) == 0: return 0
    sayac += len(yorumlar)

    dosya.write("Yorumlar:\n")
    for yorum in yorumlar:
        dosya.write("  * {0} {1} ({2}): \"{3}\"\n".format(
            yorum['tarih'],
            yorum['gorunen_ad'],
            yorum['kullanici_adi'],
            yorum['icerik']
        ))

        if 'cevaplar' in yorum['linkler']:
            sayac += cevaplari_yazdir(dosya, yorum['linkler']['cevaplar'])
    return sayac

def cevaplari_yazdir(dosya, cevaplar_url):
    """API kaynağından getirilen cevapları verilen dosyaya yazdırır.

    Yazdırma formatı:
      *  [YORUM]
        -  [TARİH] [GORUNEN_AD] ([KULLANICI_ADI]): "[İÇERİK]"

    Argümanlar:
      dosya(file): Cevapların yazdırılması istenen dosya nesnesi. Dosya adı değil!
      cevaplar_url(string): teknoseyir.com/wp-json/wp/v2/comments?parent=[DURUM_ID]

    Dönüş değeri:
      int: Verilen dosyaya yazdırılan cevap sayısı. İstatistiklere eklenmesi için
           kullanılıyor.
    """
    sayac = 0
    cevaplar = cevaplari_getir(cevaplar_url)

    if len(cevaplar) == 0: return 0
    sayac += len(cevaplar)

    for cevap in cevaplar:
        dosya.write("    - {0} {1} ({2}): \"{3}\"\n".format(
            cevap['tarih'],
            cevap['gorunen_ad'],
            cevap['kullanici_adi'],
            cevap['icerik']
        ))
    return sayac

def resimleri_yazdir(dosya, resimler_url):
    """API kaynağından getirilen resimleri verilen dosyaya yazdırır.

    Yazdırma formatı:
      * [RESIM_URL]

    Argümanlar:
      dosya(file): Resimlerin yazdırılması istenen dosya nesnesi. Dosya adı değil!
      resimler_url(string): teknoseyir.com/wp-json/wp/v2/media?parent=[DURUM_ID]
    """

    resimler = resimleri_getir(resimler_url, sira='asc')

    if len(resimler) == 0: return 0

    dosya.write("Resimler:\n")
    for resim in resimler:
        dosya.write("  * {0}\n".format(resim['url']))

# İŞLEMLER
# --------
print("""     _____    _               ____             _
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
                    Sürüm: {0}
        Eren Hatırnaz (teknoseyir.com/u/erenhatirnaz)
                        ---*---
 Bu betik GNU Genel Kamu Lisansı v3 ile lisanslanmıştır ve
 bir özgür yazılımdır. Bazı koşullar altında yeniden dağıtmak
 serbesttir. Lisans detayları için LICENSE dosyasına bakınız.
                        ---*---
""".format(SURUM))

kullanici_adi = input('> Kullanıcı Adın: ')
if kullanici_adi == "":
    print("Kullanıcı adı boş olamaz!")
    exit(1)

evet=['evet', 'e']
if input('> İndirme sayılarını limitlemek istiyor musunuz? (e/H): ').lower() in evet:
    print("Limit belirlemek istemediklerinize -1 yazın.")

    LIMITLEME=True
    DURUM_LIMITI = int(input('> Durum limiti: '))
    BLOG_LIMITI = int(input('> Blog yazısı limiti: '))
    INCELEME_LIMITI = int(input('> İnceleme limiti: '))
    RESIM_LIMITI = int(input('> Resim limiti: '))

print("")

# Klasörleri oluştur
klasorler = ["durumlar", "resimler", "blog_yazilari", "incelemeler"]
for klasor in klasorler:
    if not path.exists(klasor): makedirs(klasor)

kullanici_url = kullanici_url_getir(kullanici_adi)
kullanici = kullanici_getir(kullanici_url)

# Profil resmi indir
presmi_url = kullanici['profil_resmi'].replace('96', '2048')
presmi_dosya_adi = "./profil-resmi.jpg"
print("Profil fotoğrafınız indiriliyor...", end=' ', flush=True)
urlretrieve(presmi_url, presmi_dosya_adi)
print("Kaydedildi: " + presmi_dosya_adi)

# Takipçi ve takip edilenler listesi
listeler = [
    {'tip': 'takip-eden', 'isim': 'Takipçi', 'dosya': './takipciler.txt'},
    {'tip': 'takip-edilen', 'isim': 'Takip edilenler', 'dosya': './takip_edilenler.txt'}
]
for liste in listeler:
    print("{0} listesi indiriliyor... ".format(liste['isim']),
          end=' ', flush=True)

    with open(liste['dosya'], 'w', encoding='utf-8') as dosya:
        for k in kullanici_listesi_getir(liste['tip'], kullanici['id']):
            dosya.write("* {0} ({1})\n".format(k['gorunen_ad'],
                                               k['kullanici_adi']))
    print("Kaydedildi: " + liste['dosya'])

# İstatistik değişkenleri
indirilen_durum_sayisi = 0
indirilen_blog_yazilari = 0
indirilen_inceleme_sayisi = 0
indirilen_resim_sayisi = 0
toplam_yorum_sayisi = 0

# Durumları indir
sayfa_no = 1
while True:
    try:
        durumlar = durumlari_getir(kullanici['linkler']['durumlar'], sayfa_no)

        if len(durumlar) == 0: break
        if LIMITLEME and DURUM_LIMITI == 0: raise StopIteration

        for durum in durumlar:
            print("Durum ID: {0} indiriliyor...".format(durum['id']),
                  end=' ', flush=True)

            dosya_adi = "./durumlar/{0}-{1}.txt".format(durum['id'],
                                                        durum['baslik'])
            with open(dosya_adi, 'w', encoding='utf-8') as dosya:
                dosya.write("Tarih: {0}\n".format(durum['tarih']))
                dosya.write("Bağlantı: {0}\n".format(durum['link']))

                resimleri_yazdir(dosya, durum['linkler']['resimler'])

                dosya.write("İçerik:\n---\n{0}\n---\n".format(durum['icerik']))

                yorumlar_url = durum['linkler']['yorumlar']
                toplam_yorum_sayisi += yorumlari_yazdir(dosya, yorumlar_url)

            print("Kaydedildi: "+ dosya_adi)
            indirilen_durum_sayisi += 1

            if LIMITLEME and DURUM_LIMITI > 0 and indirilen_durum_sayisi >= DURUM_LIMITI:
                raise StopIteration

    except StopIteration:
        print("-!- Durum limitine gelindi! ({0})".format(DURUM_LIMITI))
        break
    except HTTPError as err:
        hata=load(err)
        if hata['code'] == "rest_post_invalid_page_number": break
        else:
            print("Durumlar indirilirken hata oluştu!")
            print("{0} - {1} {2}".format(err.code, hata['code'], hata['message']),
                  file=stderr)
            print("\"Hayatta iyi şeyler olmaz!\" -LP")
            exit(1)
    sayfa_no += 1

# Blog yazilarini indir
sayfa_no = 1
while True:
    try:
        blog_yazilari_url = kullanici['linkler']['blog_yazilari']
        blog_yazilari = blog_yazilari_getir(blog_yazilari_url, sayfa_no)

        if len(blog_yazilari) == 0: break
        if LIMITLEME and BLOG_LIMITI == 0: raise StopIteration

        for blog_yazisi in blog_yazilari:
            print("Blog Yazı ID: {0} indiriliyor...".format(blog_yazisi['id']),
                  end=' ', flush=True)

            dosya_adi = "./blog_yazilari/{0}-{1}.txt".format(blog_yazisi['id'],
                                                             blog_yazisi['isim'])
            with open(dosya_adi, 'w', encoding='utf-8') as dosya:
                dosya.write("Tarih: {0}\n".format(blog_yazisi['tarih']))
                dosya.write("Bağlantı: {0}\n".format(blog_yazisi['link']))
                dosya.write("Başlık: {0}\n".format(blog_yazisi['baslik']))

                resimleri_yazdir(dosya,
                                 blog_yazisi['linkler']['resimler'])

                dosya.write("İçerik:\n---\n{0}\n---\n"
                            .format(blog_yazisi['icerik']))

                yorumlar_url = blog_yazisi['linkler']['yorumlar']
                toplam_yorum_sayisi += yorumlari_yazdir(dosya, yorumlar_url)

            print("Kaydedildi: " + dosya_adi)
            indirilen_blog_yazilari += 1

            if LIMITLEME and BLOG_LIMITI > 0 and indirilen_blog_yazilari >= BLOG_LIMITI:
                raise StopIteration
    except StopIteration:
        print("-!- Blog yazısı limitine gelindi! ({0})".format(BLOG_LIMITI))
        break
    except HTTPError as err:
        hata=load(err)
        if hata['code'] == "rest_post_invalid_page_number": break
        else:
            print("Blog yazıları indirilirken hata oluştu!")
            print("{0} - {1} {2}".format(err.code, hata['code'], hata['message']),
                  file=stderr)
            print("\"Hayatta iyi şeyler olmaz!\" -LP")
            exit(1)
    sayfa_no += 1

# İncelemeleri indir
sayfa_no = 1
while True:
    try:
        incelemeler = incelemeleri_getir(kullanici['linkler']['incelemeler'],
                                         sayfa_no)

        if len(incelemeler) == 0: break
        if LIMITLEME and INCELEME_LIMITI == 0: raise StopIteration

        for inceleme in incelemeler:
            print("Inceleme ID: {0} indiriliyor...".format(inceleme['id']),
                  end=' ', flush=True)

            dosya_adi = "./incelemeler/{0}-{1}.txt".format(inceleme['id'],
                                                           inceleme['isim'])
            with open(dosya_adi, 'w', encoding='utf-8') as dosya:
                dosya.write("Tarih: {0}\n".format(inceleme['tarih']))
                dosya.write("Bağlantı: {0}\n".format(inceleme['link']))
                dosya.write("Ürün: {0}\n".format(inceleme['urun']))
                dosya.write("Başlık: {0}\n".format(inceleme['baslik']))

                resimleri_yazdir(dosya, inceleme['linkler']['resimler'])

                dosya.write("İçerik:\n---\n{0}\n---\n"
                            .format(inceleme['icerik']))

                yorumlar_url = inceleme['linkler']['yorumlar']
                toplam_yorum_sayisi += yorumlari_yazdir(dosya, yorumlar_url)

            print("Kaydedildi: " + dosya_adi)
            indirilen_inceleme_sayisi += 1

            if LIMITLEME and INCELEME_LIMITI > 0 and indirilen_inceleme_sayisi >= INCELEME_LIMITI:
                raise StopIteration
    except StopIteration:
        print("-!- İnceleme limitine gelindi! ({0})".format(INCELEME_LIMITI))
        break
    except HTTPError as err:
        hata=load(err)
        if hata['code'] == "rest_post_invalid_page_number": break
        else:
            print("İncelemeler indirilirken hata oluştu!")
            print("{0} - {1} {2}".format(err.code, hata['code'], hata['message']),
                  file=stderr)
            print("\"Hayatta iyi şeyler olmaz!\" -LP")
            exit(1)
    sayfa_no += 1

# Resimleri indir
sayfa_no = 1
while True:
    try:
        resimler_url = kullanici['linkler']['resimler']
        resimler = resimleri_getir(resimler_url, sayfa_no)

        if len(resimler) == 0: break
        if LIMITLEME and RESIM_LIMITI == 0: raise StopIteration

        for resim in resimler:
            print("Resim ID: {0} indiriliyor... ".format(resim['id']),
                  end='', flush=True)

            resim_dosya_adi = "./resimler/" + resim['url'].split('/')[-1]
            urlretrieve(resim['url'], resim_dosya_adi)

            print("Kaydedildi: " + resim_dosya_adi)
            indirilen_resim_sayisi += 1

            if LIMITLEME and RESIM_LIMITI > 0 and indirilen_resim_sayisi >= RESIM_LIMITI:
                raise StopIteration
    except StopIteration:
        print("-!- Resim limitine gelindi! ({0})".format(RESIM_LIMITI))
        break
    except HTTPError as err:
        hata=load(err)
        if hata['code'] == "rest_post_invalid_page_number": break
        else:
            print("Resimler indirilirken hata oluştu!")
            print("{0} - {1} {2}".format(err.code, hata['code'], hata['message']),
                  file=stderr)
            print("\"Hayatta iyi şeyler olmaz!\" -LP")
            exit(1)
    sayfa_no += 1

print("\n---*---")
print("Özet:")
print("İndirilen durum sayısı       : {0}".format(indirilen_durum_sayisi))
print("İndirilen blog yazısı sayısı : {0}".format(indirilen_blog_yazilari))
print("İndirilen inceleme sayısı    : {0}".format(indirilen_inceleme_sayisi))
print("İndirilen resim sayısı       : {0}".format(indirilen_resim_sayisi))
print("Toplam yorum sayısı          : {0}".format(toplam_yorum_sayisi))
