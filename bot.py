import os
import discord
from discord.ext import commands
import yfinance as yf
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN が設定されていません")

# Intents設定
intents = discord.Intents.default()
intents.message_content = True  # !jt コマンド用

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

@bot.command()
async def jt(ctx):
    """
    JT（2914.T）の現在株価を取得
    """
    try:
        ticker = yf.Ticker("2914.T")
        price = ticker.info.get("regularMarketPrice")

        if price is None:
            await ctx.send("株価を取得できませんでした")
            return

        await ctx.send(f"📈 JT（2914.T）の現在株価: **{price} 円**")

    except Exception as e:
        await ctx.send("エラーが発生しました")
        print(e)

bot.run(TOKEN)
