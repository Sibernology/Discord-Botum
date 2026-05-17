Gelişmiş Moderasyon ve Yapay Zeka Discord Botu

Bu proje; sunucu güvenliğini sağlamak, kullanıcı etkileşimlerini otomatikleştirmek ve yapay zeka entegrasyonu sunmak amacıyla geliştirilmiş, çok işlevli bir Discord botudur. Proje, hem geleneksel metin tabanlı komutları (prefix) hem de Discord'un modern Slash (/) komut mimarisini destekler.

Özellikle Replit gibi bulut tabanlı geliştirme ortamlarında sorunsuz bir şekilde sunucu modunda çalıştırılmak üzere optimize edilmiştir.
Özellikler
🛡️ Gelişmiş Sunucu Koruması ve Moderasyon

    Regex Tabanlı Akıllı Filtreleme: Küfür ve hakaret içeren kelimeleri sadece düz metin olarak değil; aralara konulan özel karakterleri (nokta, yıldız, boşluk vb.) ve harf uzatmalarını analiz eden Regex (Düzenli İfadeler) yapısıyla tespit eder, mesajı siler ve kullanıcıyı otomatik olarak susturur (timeout).

    Çift Kademeli Dinamik Spam Koruması: Kullanıcıların belirli bir zaman diliminde (örneğin 10 saniye) gönderebileceği maksimum mesaj sınırını kontrol eder. Hem tekrarlanan mesajları hem de hızlı mesaj gönderimini tespit ederek sunucu güvenliğini sağlar.

    Esnek Ceza Sistemi: /isimceza komutu veya otomatik koruma sistemleri aracılığıyla kural ihlali yapan kullanıcılara esnek sürelerde timeout uygular.

🤖 Yapay Zeka Entegrasyonu (OpenRouter)

    Mixtral-8x7b Modeli: Bot, OpenRouter API aracılığıyla mistralai/mixtral-8x7b-instruct yapay zeka modelini kullanır. /yz komutuyla tetiklenen yapay zeka, sunucu kurallarına uyum sağlaması için tamamen Türkçe, doğrudan, net ve argo ifadelerden izole edilmiş şekilde cevap vermeye programlanmıştır.

    Gelişmiş Kullanıcı Engelleme: Yöneticiler, yapay zeka komutunu kötüye kullanan kişileri /yz-engel komutuyla kara listeye alabilir. Bu liste yz_engel.json dosyasında kalıcı olarak saklanır.

📊 Yönetici ve İstatistik Araçları

    Detaylı Sunucu Analizi: /kişisayısı komutu ile sunucudaki insan, bot, rol, kanal ve moderatör sayılarını şık bir Embed arayüzü ile listeler. Bu komut sadece belirlenen geliştirici rolüne sahip kişiler tarafından kullanılabilir.

    Toplu Rol Yönetimi: Sunucudaki belirli bir üyeye veya özel role sahip olmayan tüm sunucu üyelerine toplu şekilde rol verme (/rolver) veya rol geri alma (/rolgerial) işlemlerini asenkron olarak gerçekleştirir.

    Mesaj Temizleme ve Günlük (Log): /sil komutuyla kanaldaki mesajları toplu temizler. Silinen son mesajı hafızasında tutarak !silinen komutuyla yöneticilere gösterir. Yapılan tüm kritik işlemler belirlenen log kanalına anlık olarak raporlanır.

Kullanılan Teknolojiler ve Bağımlılıklar

    Python 3

    discord.py: Discord API ile etkileşim kurmak ve komut ağaçlarını (App Commands) yönetmek için.

    aiohttp: OpenRouter API'sine asenkron HTTP talepleri göndererek botun performansının düşmesini engellemek için.

    python-dotenv: Token ve API anahtarlarının kaynak koddan izole edilerek .env dosyasında güvenli tutulması için.

Kurulum ve Dağıtım (Deployment)
1. Ortam Değişkenlerinin Hazırlanması

Projenizin kök dizininde bir .env dosyası oluşturun (Replit kullanıyorsanız sol menüdeki Tools -> Secrets kısmını kullanın) ve aşağıdaki bilgileri tanımlayın:
Kod snippet'i

Discord_TOKEN=YOUR_DISCORD_BOT_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY

2. Log Kanalı ve Rol Ayarları

    Kodun içerisindeki LOG_CHANNEL_ID listesine, botun log mesajlarını göndermesini istediğiniz Discord kanal ID'sini yazın.

    /kişisayısı, /rolver ve /rolgerial komutlarının içerisindeki DEVELOPER_ROLE_ID, MOD_ROLE_ID ve ozel_rol_id değerlerini kendi sunucunuzun rol ID'leri ile güncelleyin.

3. Replit Üzerinde Çalıştırma

Projeyi Replit üzerinde bir sunucu gibi kesintisiz çalıştırmak için:

    Proje dosyalarını Replit'e aktarın.

    main.py içerisindeki paketlerin otomatik yüklenmesi için projenizi başlatın veya paketi manuel kurun:
    Bash

    pip install discord.py aiohttp python-dotenv

    Bot, on_ready eventi gerçekleştikten sonra otomatik olarak slash komutlarını Discord API'sine senkronize edecektir.

    Projenin Replit uyku moduna geçmeden 7/24 aktif kalması için harici bir "Uptime" servisi (UptimeRobot vb.) kullanılması önerilir.

Lisans / Telif Hakkı

Bu projenin tüm hakları saklıdır (All Rights Reserved). Kodlar yalnızca inceleme, kişisel kullanım ve eğitim amacıyla paylaşılmıştır. Yazılı izin olmaksızın kodların kopyalanması, dağıtılması veya turnuva/yarışma gibi platformlarda ticari veya kişisel kazanç amacıyla hazır proje olarak sunulması yasaktır.
