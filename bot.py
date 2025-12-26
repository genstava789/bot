import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 2589472
API_HASH = "5243628014db9798d6775b330e542602"
BOT_TOKEN = "6100847173:AAE1Ph_WWGEJhENvKKIzPhziO63cv3ruYKs"

OWNER_ID = 123456789  # your Telegram user ID

app = Client(
    "shell-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


async def run_shell(cmd: str):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    output = ""
    async for line in process.stdout:
        line = line.decode()
        output += line
        if len(output) > 3500:
            break

    await process.wait()
    return output or "Done."


@app.on_message(filters.command("sh") & filters.user(OWNER_ID))
async def shell_exec(_, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /sh <command>")
        return

    cmd = message.text.split(" ", 1)[1]
    await message.reply("▶️ Executing...")

    try:
        output = await run_shell(cmd)
        await message.reply(f"```\n{output}\n```")
    except Exception as e:
        await message.reply(f"Error:\n`{e}`")


@app.on_message(filters.command("ffmpeg") & filters.user(OWNER_ID))
async def ffmpeg_exec(_, message: Message):
    cmd = message.text.split(" ", 1)[1]
    full_cmd = f"ffmpeg {cmd}"

    await message.reply("🎬 FFmpeg started...")
    output = await run_shell(full_cmd)
    await message.reply(f"```\n{output}\n```")


@app.on_message(filters.command("rclone") & filters.user(OWNER_ID))
async def rclone_exec(_, message: Message):
    cmd = message.text.split(" ", 1)[1]
    full_cmd = f"rclone {cmd}"

    await message.reply("☁️ Rclone started...")
    output = await run_shell(full_cmd)
    await message.reply(f"```\n{output}\n```")


app.run()