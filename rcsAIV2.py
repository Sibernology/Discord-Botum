import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from datetime import datetime, timedelta, timezone
import asyncio
import aiohttp
import json
from datetime import timezone
import re
from dotenv import load_dotenv
# Bot ayarları
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
YZ_ENGEL_DOSYA = "yz_engel.json"

# API Anahtarları
DISCORD_TOKEN = os.getenv("Discord_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "mistralai/mixtral-8x7b-instruct"
# Log kanalı
LOG_CHANNEL_ID = [
    "XXXXXXXXXXXXXXXXXXX",] # Buraya kendi oluşturduğunuz log kanalın id sini yapıştırıyorsunuz
 
""
# Spam koruması
spam_dict = {}
spam_tracker = {}
spam_limit = 10
timeout_duration = 3600 # saniye

# Kelime listeleri
KUFURLER =  [
    "amk", "a.m.k", "a*m*k", "a m k", "a-m-k", "a+k", "a_k", "a.k",
    "aq", "a.q", "a*q", "a_q", "a q", "a-q",
    "orospu", "o.r.o.s.p.u", "o*r*o*s*p*u", "o r o s p u",
    "sik", "s.i.k", "s*i*k", "s i k", "s-i-k",
    "piç", "p.i.ç", "p*i*ç", "p i ç",
    "anan", "ananı", "ananı sikiyim", "ananız", "ananı avradını",
    "sikerim", "s.i.k.e.r.i.m", "s*i*k*e*r*i*m", "s i k e r i m",
    "göt", "g.o.t", "g*t", "g o t", "götveren",
    "yarrak", "y.a.r.r.a.k", "y*a*r*r*a*k", "y a r r a k",
    "mal", "m.a.l", "m*a*l", "m a l", "gerizekalı",
    "salak", "s.a.l.a.k", "s*a*l*a*k", "s a l a k",
    "aptal", "a.p.t.a.l", "a*p*t*a*l", "a p t a l",
    "kaşar", "k.a.ş.a.r", "k*a*ş*a*r", "k a ş a r",
    "ibne", "i.b.n.e", "i*b*n*e", "i b n e",
    "yarrağım", "y.a.r.r.a.ğ.ı.m", "y*a*r*r*a*ğ*ı*m", "y a r r a ğ ı m",
    "oç", "o.ç", "o*ç", "o ç",
    "pezevenk", "p.e.z.e.v.e.n.k", "p*e*z*e*v*e*n*k", "p e z e v e n k",
    "sürtük", "s.ü.r.t.ü.k", "s*ü*r*t*ü*k", "s ü r t ü k",
    "amına", "a.m.ı.n.a", "a*m*ı*n*a", "a m ı n a",
    "gavat", "g.a.v.a.t", "g*a*v*a*t", "g a v a t",
    "dalyarak", "d.a.l.y.a.r.a.k", "d*a*l*y*a*r*a*k", "d a l y a r a k",
    "kaltak", "k.a.l.t.a.k", "k*a*l*t*a*k", "k a l t a k",
    "godoş", "g.o.d.o.ş", "g*o*d*o*ş", "g o d o ş",
    "hıyar", "h.ı.y.a.r", "h*ı*y*a*r", "h ı y a r",
    "taşak", "t.a.ş.a.k", "t*a*ş*a*k", "t a ş a k",
    "dingil", "d.i.n.g.i.l", "d*i*n*g*i*l", "d i n g i l",
    "amcık", "a.m.c.ı.k", "a*m*c*ı*k", "a m c ı k",
    "şerefsiz", "ş.e.r.e.f.s.i.z", "ş*e*r*e*f*s*i*z", "ş e r e f s i z", "amk", "a*k", "*mk", "AMK", "MK","mk",
    "fuck", "f*ck", "fu*k", "fuc*k",  "f*u*c*k", "f*u*c*k",  "f*u*c*k"
    "Fuck", "F*ck", "Fu*k", "Fuc*k",  "F*u*c*k", "F*u*c*k",
    "FUCK", "F*CK", "FU*K", "FUC*K",  "F*U*C*K", "F*U*C*K",
]
def kufur_to_regex(word):
    chars = list(word)
    pattern = r'\b'  # Kelime başlangıcı
    for c in chars:
        pattern += f"{re.escape(c)}[\W_]*"
    pattern = pattern.rstrip(r"[\W_]*") + r'\b'  # Kelime sonu
    return pattern

# Tüm regex desenleri
kufur_regexler = [re.compile(kufur_to_regex(k), re.IGNORECASE) for k in KUFURLER]

# Mesaj analiz fonksiyonu
def kufur_var_mi(mesaj):
    for regex in kufur_regexler:
        if regex.search(mesaj):
            return True
    return False


EYVALLAH_SORGULAR = ["eyvallah", "eyv"]
EYVALLAH_CEVAPLAR = ["Eyvallahınla yaşa!"]
NOKTA_SORGULAR = [".", " .", " . ", "..", "..."]
NOKTA_CEVAPLAR = [
    "Noktanı koydun, devam edelim!",
    "Bir nokta koymuşsun, şaşırdım doğrusu!",
    "Noktalı mesaj da olurmuş!",
    "Nokta mı? Nokta!",
]
YASIYAN_SORGULAR = [
    "ne yaşıyon sen",
    "aga sen ne yaşıyosun ya",
    "ne yaşıyorsun sen",
    "sen ne yaşıyosun ya",
    "sen ne yaşıyon ya"
]
YASIYAN_CEVAPLAR = [
    "Hayatı yaşıyorum.",
    "Sadece hayatın içinde yaşıyorum.",
    "Ne yapayım, hayatı yaşıyorum işte.",
    "Hayatı yaşamaya devam ediyorum."
]

GREETINGS = {
    "sa": "Aleyküm selam, hoş geldin!",
    "s.a": "Aleyküm selam, hoş geldin!",
    "selam": "Selam! Nasılsın?",
    "slm": "Selam! Nasılsın?",
    "selamın aleyküm": "Ve aleyküm selam, sefalar getirdin!",
    "sea": "Aleyküm selam, hoş geldin!",
    "selamün aleyküm": "Ve aleyküm selam, nasılsın?",
    "selams": "Selamlar!",
    "saa": "Aleyküm selam!",
    "merhaba": "Merhaba! Keyifler nasıl?",
    "mrh": "Merhaba! Nasılsın?",
    "mrb": "Merhaba! Hoş geldin!",
    "hey": "Hey! Hoş geldin!",
    "heyy": "Heey, naber?",
    "hi": "Hi there! Welcome!",
    "hello": "Hello! How can I help you?",
    "hll": "Hey selam!",
    "selamm": "Selam! Neler var neler yok?",
    "s.a.": "Aleyküm selam!",
    "asl": "Aleyküm selam!",
    "ss": "Selamlar!",
    "sls": "Selam!",
    "yo": "Yo! Hoş geldin!",
    "naber": "Selam! İyiyim sen?",
    "n'aber": "N'aber! Keyifler yerindedir umarım.",
    "naberr": "Naber! Hoş geldin!",
    "günaydın": "Günaydın! Harika bir gün olsun!",
    "tünaydın": "Tünaydın! Ne var ne yok?",
    "iyi akşamlar": "İyi akşamlar! Hoş geldin!",
    "iyi geceler": "İyi geceler! Yatmadan önce geldin demek :)",
    "yoo": "Yoo! Kimleri görüyorum?",
    "o selam": "Selam! Hazırım seni dinlemeye.",
    "selam gençlik": "Selamlar! Enerji yüksek gibi.",
    "ne haber": "İyi senden ne haber?",
    
}

FAREWELLS = {
    "allah'a emanet": "Görüşürüz {user}, kendine iyi bak!",
    "allaha emanet": "Hoşça kal {user}, Allah'a emanet ol!",
    "bye": "Bye bye {user}, take care!",
    "bay": "Görüşmek üzere {user}!",
    "hoşçakal": "Hoşçakal {user}, yine bekleriz!",
    "hosçakal": "Hoşçakal {user}, dikkat et kendine!",
    "görüşürüz": "Görüşmek üzere {user}!",
    "gorusuruz": "Görüşürüz {user}!",
    "gorüşürüz": "Görüşürüz {user}, sağlıcakla kal!",
    "güle güle": "Güle güle {user}, dikkat et kendine!",
    "kendine iyi bak": "Sen de kendine iyi bak {user}!",
    "iyi geceler": "İyi geceler {user}, tatlı rüyalar!",
    "iyi akşamlar": "İyi akşamlar {user}, kendine dikkat et!",
    "hadi bye": "Bye bye {user}!",
    "bye bye": "Görüşürüz {user}!",
    "bb": "Görüşürüz {user}!",
    "bby": "Bye {user}!",
    "çıkıyorum": "Görüşürüz {user}, yine bekleriz!",
    "gidiyorum": "Hoşçakal {user}, yolun açık olsun!",
    "çıktım": "Görüşmek üzere {user}!",
    "baybay": "Bay bay {user}, kendine dikkat et!",
    "hadi görüşürüz": "Görüşürüz {user}!",
    "görüşmek üzere": "Görüşmek üzere {user}!",
    "görüşcez": "Elbette {user}, görüşeceğiz!",
    "sonra görüşürüz": "Görüşürüz {user}, başarılar!",
    "daha sonra": "Daha sonra görüşmek üzere {user}!",
    "çüss": "Hoşçakal {user}!",
    "see ya": "See ya later {user}!",
    "see you": "See you soon {user}!",
    "cya": "Cya {user}!",
    "gtg": "Tamamdır {user}, görüşürüz!",
    "g2g": "Hadi eyvallah {user}!",
    "hadi eyvallah": "Eyvallah {user}, kendine iyi bak!",
    "sg" :"bak bi {user} *GÖTÜN YUMUŞAKMI*",
    "siktir git" : "Aaaa senden {user} beklemezdim",
   
}

@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı.")
    while True:
        hacker_status = [
            "🌏 R/CS.AI V2 devriye geziyor",
            "👨‍💻 Sistemleri tarıyor",
            "🔓 Zafiyet arıyor",
            "💉 SQL enjeksiyonu yapıyor",
            "📡 Port taraması yapıyor",
            "🛡️ Firewall aşılıyor",
            "🔑 Parola kırıyor",
            "🌐 Ağ dinlemede",
            "💣 DDOS hazırlıyor"
        ]
        await bot.change_presence(
            status=discord.Status.dnd,  # <- Burayı ekledik
            activity=discord.Game(name=random.choice(hacker_status))
        )
        await asyncio.sleep(60)

        try:
            synced = await bot.tree.sync()
            print(f"{len(synced)} adet slash komutu senkronize edildi.")
        except Exception as e:
            print(f"Slash komut senkronizasyon hatası: {e}")


# Dosyadan engel listesini yükle
def engel_listesi_yukle():
    try:
        if os.path.exists(YZ_ENGEL_DOSYA):
            with open(YZ_ENGEL_DOSYA, 'r') as f:
                if os.stat(YZ_ENGEL_DOSYA).st_size == 0:
                    return set()
                return set(json.load(f))
        return set()
    except (json.JSONDecodeError, Exception) as e:
        print(f"[UYARI] engel_listesi_yukle hatası: {e}")
        return set()

def engel_listesi_kaydet(engel_listesi):
    try:
        with open(YZ_ENGEL_DOSYA, 'w') as f:
            json.dump(list(engel_listesi), f)
    except Exception as e:
        print(f"[UYARI] engel_listesi_kaydet hatası: {e}")

# Engel listesini yükle (dosya yoksa otomatik oluştur)
if not os.path.exists(YZ_ENGEL_DOSYA):
    with open(YZ_ENGEL_DOSYA, 'w') as f:
        f.write("[]")

engellenen_kullanicilar = engel_listesi_yukle()

# SLASH KOMUTU (/yz-engel)
@bot.tree.command(name="yz-engel", description="Kullanıcının yapay zeka kullanımını engeller/kaldırır")
@app_commands.describe(kullanici="Engellenecek/kaldırılacak kullanıcı")
@app_commands.checks.has_permissions(administrator=True)
async def yz_engel_slash(interaction: discord.Interaction, kullanici: discord.Member):
    try:
        if kullanici.id in engellenen_kullanicilar:
            engellenen_kullanicilar.remove(kullanici.id)
            mesaj = f"✅ {kullanici.mention} artık yapay zekayı kullanabilir."
        else:
            engellenen_kullanicilar.add(kullanici.id)
            mesaj = f"⛔ {kullanici.mention} artık yapay zekayı **kullanamaz**."

        engel_listesi_kaydet(engellenen_kullanicilar)

        await interaction.response.send_message(mesaj, ephemeral=True)

        # Log kanalına bildirim
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🤖 YZ Engel Durumu",
                description=mesaj,
                color=discord.Color.orange()
            )
            embed.add_field(name="Yetkili", value=interaction.user.mention)
            await log_channel.send(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"❌ Hata: {str(e)}", ephemeral=True)
        print(f"[YZ-ENGEL HATA] {e}")

# PREFIX KOMUTU (!yz-engel)
@bot.command(name="yz-engel")
@commands.has_permissions(administrator=True)
async def yz_engel_prefix(ctx, kullanici: discord.Member):
    try:
        if kullanici.id in engellenen_kullanicilar:
            engellenen_kullanicilar.remove(kullanici.id)
            mesaj = f"✅ {kullanici.mention} artık yapay zekayı *kullanabilir*."
        else:
            engellenen_kullanicilar.add(kullanici.id)
            mesaj = f"⛔ {kullanici.mention} artık yapay zekayı **kullanamaz**."

        engel_listesi_kaydet(engellenen_kullanicilar)
        await ctx.send(mesaj)

    except Exception as e:
        await ctx.send(f"❌ Hata: {str(e)}")

@bot.command(name="yz")
async def yz(ctx, *, prompt: str):
    # Kullanıcı engellenmiş mi kontrol et
    if ctx.author.id in engellenen_kullanicilar:
        await ctx.send(f"{ctx.author.mention} Yapay zeka kullanımın engellenmiş! Beni kullanamazsın!")
        return

    async with ctx.typing():
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            data = { 
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages" : [
                    {
                        "role" : "system", 
                        "content" : ("YALNIZCA Türkçe konuş. Başka dil KESİNLİKLE kullanma. "
                "Kısa, öz ve net cevaplar ver. "
                "Soru neyse direkt onu cevapla; ek açıklama, ön yazı veya uyarı ekleme. "
                "Asla 'Türkçe cevap veriyorum' gibi ifadeler kullanma. "
                "Dürüst ve doğrudan ol; gereksiz nezaket süslemeleri yapma. "
                "Türkçe'yi profesyonel, anlaşılır ve hatasız kullan. "
                "Argo, mizahi ifade veya yaratıcılık içeren kelimelerden kaçın."
                )
                    }, {"role" : "user", "content" : prompt}
                ],
                "temperature" : 0.3,
                "max_tokens" : 400,
                
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        reply = result['choices'][0]['message']['content']
                        if len(reply) > 2000:
                            chunks = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                            for chunk in chunks:
                                await ctx.send(chunk)
                        else:
                            await ctx.send(reply)
                    else:
                        await ctx.send(f"API hatası: {response.status}")
        except Exception as e:
            await ctx.send(f"Bir hata oluştu: {str(e)}")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_content = message.content.lower().strip()
    user_id = message.author.id

    # Prefix ile başlayan komutlar varsa önce işle
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    # Özel komutlar (prefix'siz mesajlar)
    if any(sorgu in msg_content for sorgu in YASIYAN_SORGULAR):
        await message.channel.send(f"{message.author.mention} {random.choice(YASIYAN_CEVAPLAR)}")
        return

    if msg_content in EYVALLAH_SORGULAR:
        await message.channel.send(f"{message.author.mention} {random.choice(EYVALLAH_CEVAPLAR)}")
        return

    if msg_content in NOKTA_SORGULAR:
        await message.channel.send(f"{message.author.mention} {random.choice(NOKTA_CEVAPLAR)}")
        return

    # Küfür kontrolü
    if kufur_var_mi(msg_content):
        try:
            await message.delete()
            await message.author.timeout(timedelta(seconds=timeout_duration), reason="Küfür")
            await message.channel.send(f"{message.author.mention} küfür yasak! {timeout_duration}s timeout.")
        except Exception as e:
            print(f"Küfür timeout/silme hatası: {e}")
        return

    # Spam kontrolü (yeni sistem)
    spam_tracker.setdefault(user_id, [])
    spam_tracker[user_id].append(message.created_at.timestamp())
    # Son 10 saniyedeki mesajları tut
    spam_tracker[user_id] = [t for t in spam_tracker[user_id] if datetime.utcnow().timestamp() - t < 10]

    if len(spam_tracker[user_id]) >= spam_limit:
        try:
            await message.author.timeout(timedelta(seconds=timeout_duration), reason="Spam")
            await message.channel.send(f"{message.author.mention} spam yasak! {timeout_duration}s timeout.")
        except Exception as e:
            print(f"Spam timeout hatası: {e}")
        spam_tracker[user_id] = []
        return

    # Selamlaşma (tam eşleşme)
    if msg_content in GREETINGS:
        await message.channel.send(GREETINGS[msg_content])
        return

    # Vedalaşma (tam eşleşme)
    if msg_content in FAREWELLS:
        await message.channel.send(FAREWELLS[msg_content].format(user=message.author.mention))
        return

    # Spam koruması (eski sistem)
    now = datetime.utcnow()
    user_spam = spam_dict.get(user_id)

    if not user_spam:
        spam_dict[user_id] = {
            'count': 1,
            'last_message': message.content,
            'time': now
        }
    else:
        time_diff = (now - user_spam['time']).total_seconds()
        if time_diff < 60:
            if message.content == user_spam['last_message']:
                user_spam['count'] += 1
            else:
                spam_dict[user_id] = {
                    'count': 1,
                    'last_message': message.content,
                    'time': now
                }
        else:
            spam_dict[user_id] = {
                'count': 1,
                'last_message': message.content,
                'time': now
            }

        if user_spam['count'] > 5:
            try:
                duration = timedelta(hours=1)
                await message.author.timeout(duration, reason="Spam yapmak")

                log_channel = bot.get_channel(LOG_CHANNEL_ID)
                if log_channel:
                    embed = discord.Embed(
                        title="⛔ Timeout Uygulandı",
                        description=f"{message.author.mention} spam yaptığı için 1 saat timeout yedi.",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="Kullanıcı", value=f"{message.author}", inline=True)
                    embed.add_field(name="Sebep", value="Spam", inline=True)
                    embed.set_footer(text=f"ID: {message.author.id}")
                    await log_channel.send(embed=embed)

                warning = await message.channel.send(f"{message.author.mention}, spam yapmayın! Timeout verildi.")
                await asyncio.sleep(5)
                await warning.delete()

                del spam_dict[user_id]
            except discord.Forbidden:
                await message.channel.send("Spam yapıldı ama timeout atma yetkim yok!")
            except Exception as e:
                print(f"Timeout hatası: {e}")

    # Son olarak komutları işle
    await bot.process_commands(message)

async def log_timeout(user: discord.Member, duration: timedelta, reason: str, moderator: discord.Member):
    """Timeout işlemlerini log kanalına kaydeder"""
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        total_seconds = duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        duration_str = ""
        if hours > 0:
            duration_str += f"{hours} saat "
        duration_str += f"{minutes} dakika"

        embed = discord.Embed(
            title="⏳ Timeout Uygulandı",
            description=f"{user.mention} kullanıcısına timeout uygulandı.",
            color=discord.Color.orange(),
            timestamp=datetime.now(timezone.utc))
        embed.add_field(name="Yetkili", value=moderator.mention, inline=True)
        embed.add_field(name="Süre", value=duration_str.strip(), inline=True)
        embed.add_field(name="Sebep", value=reason, inline=False)
        embed.set_footer(text=f"ID: {user.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    """Timeout uygulandığında veya kaldırıldığında log atar"""
    try:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return

        # Timeout UYGULANDIYSA
        if before.timed_out_until != after.timed_out_until and after.timed_out_until is not None:
            now = datetime.now(timezone.utc)
            duration = after.timed_out_until - now
            reason = "Sebep belirtilmemiş"

            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if entry.target.id == after.id:
                    reason = entry.reason or "Sebep belirtilmemiş"
                    moderator = entry.user
                    break

            await log_timeout(
                user=after,
                duration=duration,
                reason=reason,
                moderator=moderator
            )

        # Timeout KALDIRILDIYSA
        elif before.timed_out_until is not None and after.timed_out_until is None:
            embed = discord.Embed(
                title="✅ Timeout Kaldırıldı",
                description=f"{after.mention} kullanıcısının timeout'u kaldırıldı.",
                color=discord.Color.green(),
                timestamp=datetime.now(timezone.utc)
            )
            await log_channel.send(embed=embed)

    except Exception as e:
        print(f"[LOG HATASI] on_member_update: {e}")

@bot.tree.command(name="isimceza", description="Kullanıcıya timeout uygular")
@app_commands.describe(
    user="Timeout uygulanacak kullanıcı",
    minutes="Süre (dakika)",
    reason="Sebep (opsiyonel)"
)
@app_commands.checks.has_permissions(moderate_members=True)
async def isimceza(interaction: discord.Interaction, user: discord.Member, 
                  minutes: app_commands.Range[int, 1, 40320], 
                  reason: str = "Sebep belirtilmedi"):
    try:
        duration = timedelta(minutes=minutes)
        await user.timeout(duration, reason=f"{reason} (Yetkili: {interaction.user})")

        await log_timeout(
            user=user,
            duration=duration,
            reason=reason,
            moderator=interaction.user
        )

        await interaction.response.send_message(
            f"✅ {user.mention} kullanıcısına {minutes} dakika timeout uygulandı.",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Hata: {str(e)}",
            ephemeral=True
        )
        print(f"[isimceza HATASI] {e}")

# Slash komut: /set_spam_limit <adet>
@bot.tree.command(name="set_spam_limit", description="Spam mesaj limiti ayarlar")
@app_commands.describe(adet="Spam mesaj limiti")
async def set_spam_limit(interaction: discord.Interaction, adet: int):
    global spam_limit
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Bu komutu kullanmak için yönetici olmalısın.", ephemeral=True)
        return
    if adet < 1 or adet > 20:
        await interaction.response.send_message("Limit 1 ile 20 arasında olmalı.", ephemeral=True)
        return
    spam_limit = adet
    await interaction.response.send_message(f"Spam mesaj limiti {spam_limit} olarak ayarlandı.")

# Slash komut: /set_timeout_duration <saniye>
@bot.tree.command(name="set_timeout_duration", description="Timeout süresini saniye olarak ayarlar")
@app_commands.describe(saniye="Timeout süresi (saniye)")
async def set_timeout_duration(interaction: discord.Interaction, saniye: int):
    global timeout_duration
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Bu komutu kullanmak için yönetici olmalısın.", ephemeral=True)
        return
    if saniye < 10 or saniye > 3600:
        await interaction.response.send_message("Timeout süresi 10 ile 3600 saniye arasında olmalı.", ephemeral=True)
        return
    timeout_duration = saniye
    await interaction.response.send_message(f"Timeout süresi {timeout_duration} saniye olarak ayarlandı.")

# Slash komut: /say <mesaj>
@bot.tree.command(name="say", description="Bot aracılığıyla mesaj gönderir")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, mesaj: str):
    try:
        # Önce yanıt veriyoruz (deferred)
        await interaction.response.defer(ephemeral=True)

        # Mesajı gönderiyoruz
        await interaction.channel.send(mesaj)

        # Kullanıcıya onay mesajı gönderiyoruz
        await interaction.followup.send("Mesaj başarıyla gönderildi!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Hata oluştu: {str(e)}", ephemeral=True)


son_silinen_mesaj = None

@bot.event
async def on_message_delete(message):
    global son_silinen_mesaj
    son_silinen_mesaj = message

@bot.command(name="silinen")
async def silinen(ctx):
    global son_silinen_mesaj
    if son_silinen_mesaj:
        await ctx.send(f"En son silinen mesaj: '{son_silinen_mesaj.content}'    - Gönderen:     {son_silinen_mesaj.author}")
    else:
        await ctx.send("Henüz silinmiş bir mesaj yok.")

@bot.tree.command(name="sil", description="Belirtilen sayıda mesajı siler.")
@app_commands.describe(miktar="Silinecek mesaj sayısı (1-100 arası)")
@app_commands.checks.has_permissions(manage_messages=True)
async def sil(interaction: discord.Interaction, miktar: int):
    # Giriş kontrolleri
    if miktar < 1 or miktar > 500:
        await interaction.response.send_message("Lütfen 1 ile 500 arasında bir sayı girin.", ephemeral=True)
        return

    # Mesajları sil
    await interaction.response.defer(ephemeral=True)  # Kullanıcıya geçici yükleniyor mesajı
    silinen = await interaction.channel.purge(limit=miktar)

    # Bilgilendirme
    await interaction.followup.send(f"{len(silinen)} mesaj silindi.")

@bot.tree.command(name="kişisayısı", description="Sunucu istatistiklerini gösterir (Geliştirici rolü gerektirir)")
async def kişisayısı(interaction: discord.Interaction):
    # Hızlı erişim için cache'lenmiş member kontrolü
    if not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message("❌ Bu komut sadece sunucularda kullanılabilir.", ephemeral=True)
        return

    # Yetki kontrolü (DEVELOPER_ROLE_ID yerine sabit değer kullanılmıştır)
    DEVELOPER_ROLE_ID = 1383349421898731581  # Gerçek rol ID'nizle değiştirin
    if not any(role.id == DEVELOPER_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("❌ Yetkiniz yok!", ephemeral=True)
        return

    guild = interaction.guild

    # Verileri tek seferde topla
    bot_count = sum(1 for m in guild.members if m.bot)
    human_count = guild.member_count - bot_count

    # Yetkili sayısı için optimize çözüm
    MOD_ROLE_ID = 1383349421898731581  # Moderasyon Ekibi rol ID
    mod_role = discord.utils.get(guild.roles, id=MOD_ROLE_ID)
    mod_count = len(mod_role.members) if mod_role else 0

    # Premium embed yapısı
    embed = discord.Embed(
        title=f"📊 {guild.name} | Detaylı İstatistikler",
        color=discord.Color.dark_gold(),
        timestamp=discord.utils.utcnow()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    # Düzenli field grupları
    embed.add_field(name="👥 Kullanıcılar", 
                   value=f"🌏 Toplam: {guild.member_count}\n👨‍💼 İnsan: {human_count}\n🛡 Bot: {bot_count}",
                   inline=True)

    embed.add_field(name="⚙️ Sunucu Yapısı",
                   value=f"\n🎭 Roller: {len(guild.roles)}\n📺 Kanallar: {len(guild.channels)}",
                   inline=True)

    embed.add_field(name="\n🔐 Yetkililer",
                   value=f"\n💼 Moderasyon Ekibi: {mod_count}",
                   inline=False)

    # Formatlı tarih bilgisi
    created_at = guild.created_at.strftime("%d %B %Y %H:%M")
    embed.add_field(name="\n📅 Kuruluş Tarihi",
                   value=f"```{created_at}```",
                   inline=False)

    # Footer ve author bilgileri
    embed.set_footer(text=f"Komut kullanıcısı: {interaction.user.display_name}",
                    icon_url=interaction.user.display_avatar.url) 


    embed.set_author(name="Sunucu İstatistikleri",
                    icon_url= "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"  )  # Özel bir icon ekleyebilirsiniz

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rolver", description="Bir kişiye veya herkese rol verir.")
@app_commands.describe(
    rol="Verilecek rol",
    kisi="Rol verilecek kişi (boş bırakılırsa herkese verilir)"
)
@app_commands.checks.has_permissions(manage_roles=True)
async def rolver(interaction: discord.Interaction, rol: discord.Role, kisi: discord.Member = None):
    await interaction.response.defer(thinking=True, ephemeral=True)

    # Özel rol ID'si
    ozel_rol_id = 1376364202129625178

    if kisi:
        try:
            # Eğer kişi özel role sahipse işlem yapma
            if ozel_rol_id in [r.id for r in kisi.roles]:
                await interaction.followup.send(f"{kisi.mention} özel role sahip olduğu için işlem yapılamadı.")
                return

            await kisi.add_roles(rol)
            await interaction.followup.send(f"{kisi.mention} kişisine `{rol.name}` rolü verildi.")
        except discord.Forbidden:
            await interaction.followup.send("Bu rolü veremem, yetkim yetersiz.")
    else:
        basarili = 0
        for member in interaction.guild.members:
            try:
                # Özel role sahip olanları atla
                if ozel_rol_id in [r.id for r in member.roles]:
                    continue

                await member.add_roles(rol)
                basarili += 1
            except:
                continue
        await interaction.followup.send(f"`{rol.name}` rolü {basarili} kişiye verildi (özel role sahip olanlar hariç).")

# ROL GERİ AL (aynı mantık burada da uygulandı)
@bot.tree.command(name="rolgerial", description="Bir kişiden veya herkesten rol alır.")
@app_commands.describe(
    rol="Geri alınacak rol",
    kisi="Rol alınacak kişi (boş bırakılırsa herkesten alınır)"
)
@app_commands.checks.has_permissions(manage_roles=True)
async def rolgerial(interaction: discord.Interaction, rol: discord.Role, kisi: discord.Member = None):
    await interaction.response.defer(thinking=True, ephemeral=True)

    # Özel rol ID'si
    ozel_rol_id = 1376364202129625178

    if kisi:
        try:
            # Eğer kişi özel role sahipse işlem yapma
            if ozel_rol_id in [r.id for r in kisi.roles]:
                await interaction.followup.send(f"{kisi.mention} özel role sahip olduğu için işlem yapılamadı.")
                return

            await kisi.remove_roles(rol)
            await interaction.followup.send(f"{kisi.mention} kişisinden `{rol.name}` rolü geri alındı.")
        except discord.Forbidden:
            await interaction.followup.send("Bu rolü geri alamam, yetkim yetersiz.")
    else:
        basarili = 0
        for member in interaction.guild.members:
            try:
                # Özel role sahip olanları atla
                if ozel_rol_id in [r.id for r in member.roles]:
                    continue

                await member.remove_roles(rol)
                basarili += 1
            except:
                continue
        await interaction.followup.send(f"`{rol.name}` rolü {basarili} kişiden geri alındı .")
load_dotenv()
bot.run(os.getenv("Discord_TOKEN"))

