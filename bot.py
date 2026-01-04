import os
import discord
from discord.ext import commands
from discord.ui import Button, View
import yfinance as yf
from dotenv import load_dotenv

# ======================
# 環境変数
# ======================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN が設定されていません")

# あなたのチャンネルID
CHANNEL_ID = 1454927517365436648

# ======================
# Discord設定
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# 株価取得
# ======================
def get_jt_price():
    ticker = yf.Ticker("2914.T")
    return ticker.info.get("regularMarketPrice")

# ======================
# ボタンView
# ======================
class JTPriceView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📈 JTの現在株価を取得",
        style=discord.ButtonStyle.primary
    )
    async def get_price(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        price = get_jt_price()

        if price is None:
            await interaction.response.send_message(
                "❌ 株価を取得できませんでした",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"📊 **JT（2914.T）現在株価**\n💴 {price} 円",
            ephemeral=False
        )

# ======================
# 起動時処理
# ======================
@bot.event
async def on_ready():
    print(f"✅ ログイン完了: {bot.user}")

    # 再起動耐性のため fetch_channel を使う
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
    except Exception as e:
        print("❌ チャンネル取得失敗:", e)
        return

    await channel.send(
        "👇 ボタンを押してJTの現在株価を取得できます",
        view=JTPriceView()
    )

# ======================
# 起動
# ======================
bot.run(TOKEN)
