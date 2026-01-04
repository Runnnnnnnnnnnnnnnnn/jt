import os
import discord
from discord.ext import commands
from discord.ui import Button, View
import yfinance as yf
from dotenv import load_dotenv

# ======================
# 設定
# ======================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ← あなたが指定したチャンネルID
CHANNEL_ID = 1454927517365436648

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN が .env に設定されていません")

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
# Button View
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
                "株価を取得できませんでした",
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
    print(f"ログイン完了: {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("指定チャンネルが見つかりません")
        return

    await channel.send(
        "👇 ボタンを押してJTの現在株価を取得できます",
        view=JTPriceView()
    )

bot.run(TOKEN)
