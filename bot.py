import discord
from discord import app_commands
from discord.ext import commands
import json
import random
import os
from dotenv import load_dotenv
import io
import asyncio

# Load environment variables
TOKEN = "MTM3MDA4MDcxNDk1MDcwNTI5Mw.G2RXPy.EfDJuKgb4Ds3_iZRaiVBgM6dwMoQS4lkkmFIqU"

print(f"Token loaded: {TOKEN is not None}")
print(f"Token length: {len(TOKEN) if TOKEN else 0}")
print(f"Token first 10 chars: {TOKEN[:10] if TOKEN else 'None'}")

if not TOKEN:
    print("Error: DISCORD_TOKEN not found")
    exit(1)

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# تعريف الصلاحيات المطلوبة للبوت
bot_permissions = discord.Permissions(
    send_messages=True,
    embed_links=True,
    read_messages=True,
    read_message_history=True,
    manage_messages=True,
    attach_files=True,
    use_external_emojis=True
)

# Data storage
CUTS_FILE = 'cuts.txt'
POINTS_FILE = 'points.json'

# Load cuts from file
def load_cuts():
    try:
        with open(CUTS_FILE, 'r', encoding='utf-8') as f:
            cuts = [line.strip() for line in f if line.strip()]
        print(f"تم تحميل {len(cuts)} كت")
        return cuts
    except FileNotFoundError:
        print("لم يتم العثور على ملف الكتات، سيتم إنشاء ملف جديد")
        return []

# Save cuts to file
def save_cuts(cuts):
    try:
        # التأكد من أن الملف موجود
        if not os.path.exists(CUTS_FILE):
            print(f"إنشاء ملف جديد: {CUTS_FILE}")
            open(CUTS_FILE, 'w', encoding='utf-8').close()
        
        # حفظ الكتات في الملف
        with open(CUTS_FILE, 'w', encoding='utf-8') as f:
            for cut in cuts:
                f.write(f"{cut}\n")
        
        print(f"تم حفظ {len(cuts)} كت في الملف {CUTS_FILE}")
        
        # التحقق من أن الكتات تم حفظها
        with open(CUTS_FILE, 'r', encoding='utf-8') as f:
            saved_cuts = [line.strip() for line in f if line.strip()]
            print(f"عدد الكتات في الملف بعد الحفظ: {len(saved_cuts)}")
            
    except Exception as e:
        print(f"حدث خطأ أثناء حفظ الكتات: {str(e)}")
        raise e

# Load points from file
def load_points():
    try:
        with open(POINTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save points to file
def save_points(points):
    with open(POINTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(points, f, ensure_ascii=False, indent=4)

# Initialize points file if it doesn't exist
if not os.path.exists(POINTS_FILE):
    save_points({})

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        
        # طباعة رابط دعوة البوت مع الصلاحيات المطلوبة
        invite_link = discord.utils.oauth_url(
            bot.user.id,
            permissions=bot_permissions,
            scopes=["bot", "applications.commands"]
        )
        print(f"\nرابط دعوة البوت مع الصلاحيات المطلوبة:\n{invite_link}")
        
    except Exception as e:
        print(e)

@bot.tree.command(name="كت", description="يرسل كت عشوائي")
async def random_cut(interaction: discord.Interaction):
    """يرسل كت عشوائي"""
    try:
        # اختيار كت عشوائي
        cuts = load_cuts()
        if not cuts:
            await interaction.response.send_message("لا يوجد كتات حالياً! استخدم /اضافة_كت لإضافة كت جديد.", ephemeral=True)
            return
            
        random_quote = random.choice(cuts)
        
        # إنشاء Embed جميل للكت
        embed = discord.Embed(
            description=random_quote,
            color=discord.Color.from_rgb(233, 98, 62)
        )
        
        # إرسال الكت في القناة
        await interaction.response.send_message(embed=embed)
        
        # تحديث النقاط
        user_id = str(interaction.user.id)
        points = load_points()
        if user_id in points:
            points[user_id] += 1
        else:
            points[user_id] = 1
        save_points(points)
        
    except Exception as e:
        print(f"حدث خطأ أثناء إرسال الكت: {str(e)}")
        if not interaction.response.is_done():
            await interaction.response.send_message("حدث خطأ أثناء إرسال الكت. الرجاء المحاولة مرة أخرى.", ephemeral=True)

class CustomCutModal(discord.ui.Modal, title="أدخل الكت الخاص بك"):
    cut_text = discord.ui.TextInput(
        label="النص",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("تم استلام الكت بنجاح! سيتم إرساله الآن في القناة.", ephemeral=True)
        channel = interaction.guild.get_channel(interaction.channel_id)
        if channel is not None:
            embed = discord.Embed(
                description=self.cut_text.value,
                color=discord.Color.from_rgb(233, 98, 62)
            )
            await channel.send(embed=embed)
        else:
            print("لم يتم العثور على القناة لإرسال الكت!")

@bot.tree.command(name="كت-بنفسك", description="يرسل كت لمرة واحدة دون حفظه وبدون ذكر اسم الكاتب وبنفس تصميم أمر كت")
async def custom_cut(interaction: discord.Interaction):
    await interaction.response.send_modal(CustomCutModal())

@bot.tree.command(name="اضافة_كت", description="يضيف كت جديد")
async def add_cut(interaction: discord.Interaction, cut: str):
    """يضيف كت جديد"""
    try:
        # قراءة الكتات الحالية
        cuts = load_cuts()
        
        # إضافة الكت الجديد
        cuts.append(cut)
        save_cuts(cuts)
        
        # إنشاء Embed جميل لتأكيد إضافة الكت
        embed = discord.Embed(
            title="✨ تم إضافة الكت بنجاح",
            description=cut,
            color=discord.Color.from_rgb(233, 98, 62)
        )
        embed.set_footer(text=f"تمت الإضافة بواسطة {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        print(f"حدث خطأ أثناء إضافة الكت: {str(e)}")
        await interaction.response.send_message("حدث خطأ أثناء إضافة الكت. الرجاء المحاولة مرة أخرى.", ephemeral=True)

@bot.tree.command(name="المتصدرين", description="يعرض أعلى 10 مستخدمين")
async def leaderboard(interaction: discord.Interaction):
    """يعرض أعلى 10 مستخدمين"""
    try:
        points = load_points()
        if not points:
            await interaction.response.send_message("لا يوجد نقاط حالياً.", ephemeral=True)
            return

        # ترتيب المستخدمين حسب النقاط
        sorted_users = sorted(points.items(), key=lambda x: x[1], reverse=True)
        top_10 = sorted_users[:10]

        embed = discord.Embed(
            title="🏆 المتصدرين",
            description="",
            color=discord.Color.from_rgb(233, 98, 62)
        )

        # إضافة المستخدمين في كود بلوك واحد
        for i, (user_id, score) in enumerate(top_10, 1):
            user = await bot.fetch_user(int(user_id))
            embed.description += f"{i}. {user.name:<20} {score:>3} نقطة\n"

        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"حدث خطأ أثناء عرض المتصدرين: {str(e)}")
        await interaction.response.send_message("حدث خطأ أثناء عرض المتصدرين. الرجاء المحاولة مرة أخرى.", ephemeral=True)

@bot.tree.command(name="نقاطي", description="يعرض نقاطك الحالية")
async def my_points(interaction: discord.Interaction):
    """يعرض نقاطك الحالية"""
    try:
        points = load_points()
        user_id = str(interaction.user.id)
        user_points = points.get(user_id, 0)
        
        embed = discord.Embed(
            title="💫 نقاطك",
            description=f"لديك {user_points} نقطة",
            color=discord.Color.from_rgb(233, 98, 62)
        )
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"حدث خطأ أثناء عرض النقاط: {str(e)}")
        await interaction.response.send_message("حدث خطأ أثناء عرض النقاط. الرجاء المحاولة مرة أخرى.", ephemeral=True)

@bot.tree.command(name="مساعدة", description="يعرض قائمة الأوامر المتاحة")
async def help_command(interaction: discord.Interaction):
    """يعرض قائمة الأوامر المتاحة"""
    try:
        embed = discord.Embed(
            title="📚 قائمة الأوامر",
            description="",
            color=discord.Color.from_rgb(233, 98, 62)
        )
        
        commands = [
            ("/كت", "يرسل كت عشوائي"),
            ("/كت-بنفسك", "يرسل كت لمرة واحدة دون حفظه"),
            ("/اضافة_كت", "يضيف كت جديد"),
            ("/المتصدرين", "يعرض أعلى 10 مستخدمين"),
            ("/نقاطي", "يعرض نقاطك الحالية"),
            ("/مساعدة", "يعرض هذه القائمة")
        ]
        
        # إضافة الأوامر في كود بلوك واحد
        for cmd, desc in commands:
            embed.description += f"{cmd:<15} {desc}\n"
            
        embed.set_footer(text=f"تم الطلب بواسطة {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        print(f"حدث خطأ أثناء عرض قائمة المساعدة: {str(e)}")
        await interaction.response.send_message("حدث خطأ أثناء عرض قائمة المساعدة. الرجاء المحاولة مرة أخرى.", ephemeral=True)

# Run the bot
bot.run(TOKEN) 