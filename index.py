import discord
from PIL import Image
import io
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ボットの準備
client = discord.Client()

# Seleniumの設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモードで動作するように設定

@client.event
async def on_ready():
    print(f'ログイン完了')

@client.event
async def on_message(message):
    if message.content.lower().startswith('!screenshot'):
        url = message.content[12:]  # メッセージの先頭に '!screenshot ' を付けてURLを指定

        # Seleniumを使用してウェブページのスクリーンショットを撮影
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)

        driver.get(url)
        screenshot = driver.get_screenshot_as_png()
        driver.quit()

        # スクリーンショットをPILのImageオブジェクトに変換
        image = Image.open(io.BytesIO(screenshot))

        # 画像をバイナリデータに変換
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        # 生成した画像をDiscordに送信
        await message.channel.send(file=discord.File(image_bytes, filename='screenshot.png'))

    await client.process_commands(message)

TOKEN = "MTExOTIxOTYzMTIzNjg1Nzk2Nw.GFXuvA.0Lbx6FgPLS-pBO4PEpQKKsDtMsZVB8dypVGDI4"  # 生成したBotのトークンに置き換える
client.run(TOKEN)
