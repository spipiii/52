import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scanner import scan

SETTINGS_FILE = "settings.json"

def load_settings():
    with open(SETTINGS_FILE) as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE,"w") as f:
        json.dump(data,f,indent=4)

TELEGRAM_TOKEN = "8688404030:AAHeM7LBRolyLFQvVWBk7DWE44LKT8KA4AA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
Арбитражный бот

Команды:
/scan - сканировать биржи
/settings - показать текущие настройки
/setspread 1.5 - минимальный спред %
/setamount 1000 - сумма сделки
/setexchanges binance kucoin bybit okx - выбрать биржи
"""
    await update.message.reply_text(msg)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = load_settings()
    text = f"""
Текущие настройки:
Биржи: {s['exchanges']}
Мин спред: {s['min_spread']}
Сумма сделки: {s['trade_amount_usdt']}
"""
    await update.message.reply_text(text)

async def setspread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = load_settings()
    s["min_spread"] = float(context.args[0])
    save_settings(s)
    await update.message.reply_text(f"Мин спред обновлён: {s['min_spread']}%")

async def setamount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = load_settings()
    s["trade_amount_usdt"] = float(context.args[0])
    save_settings(s)
    await update.message.reply_text(f"Сумма сделки обновлена: {s['trade_amount_usdt']} USDT")

async def setexchanges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = load_settings()
    s["exchanges"] = context.args
    save_settings(s)
    await update.message.reply_text(f"Биржи обновлены: {', '.join(s['exchanges'])}")

async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сканирую арбитраж...")
    settings = load_settings()
    results = await scan(settings)
    if not results:
        await update.message.reply_text("Возможности арбитража не найдены")
        return

    text = "TOP-5 арбитраж:\n"
    for r in results:
        text += f"""
{r['symbol']}
BUY: {r['buy']}
SELL: {r['sell']}
Network: {r['network']}
Spread: {r['spread']}%
Trade Amount: {settings['trade_amount_usdt']} USDT
Profit: {r['profit']} USDT
"""
    await update.message.reply_text(text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("setspread", setspread))
app.add_handler(CommandHandler("setamount", setamount))
app.add_handler(CommandHandler("setexchanges", setexchanges))
app.add_handler(CommandHandler("scan", scan_cmd))

app.run_polling()