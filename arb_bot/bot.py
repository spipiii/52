import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from keyboards import main_menu
from scanner import scan
from utils import load_settings, save_settings

TOKEN = os.getenv("TG_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Arbitrage bot started",
        reply_markup=main_menu()
    )


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):

    s = load_settings()

    text = f"""
Spread: {s['min_spread']}%
Trade amount: {s['trade_amount_usdt']} USDT
Exchanges: {', '.join(s['exchanges'])}
"""

    await update.message.reply_text(text)


async def setspread(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /setspread 1.5")
        return

    s = load_settings()
    s["min_spread"] = float(context.args[0])
    save_settings(s)

    await update.message.reply_text("Spread updated")


async def setamount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /setamount 1000")
        return

    s = load_settings()
    s["trade_amount_usdt"] = float(context.args[0])
    save_settings(s)

    await update.message.reply_text("Amount updated")


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Scanning...")

    results = await scan()

    if not results:
        await update.message.reply_text("No arbitrage found")
        return

    message = ""

    for r in results:

        message += f"""
{r['symbol']}
BUY {r['buy_exchange']} {r['buy_price']}
SELL {r['sell_exchange']} {r['sell_price']}
SPREAD {r['spread']}%

"""

    await update.message.reply_text(message)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "scan":

        await query.edit_message_text("Scanning...")

        results = await scan()

        if not results:
            await query.message.reply_text("No arbitrage")
            return

        msg = ""

        for r in results:

            msg += f"""
{r['symbol']}
BUY {r['buy_exchange']} {r['buy_price']}
SELL {r['sell_exchange']} {r['sell_price']}
SPREAD {r['spread']}%

"""

        await query.message.reply_text(msg)


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("scan", scan_command))
    app.add_handler(CommandHandler("setspread", setspread))
    app.add_handler(CommandHandler("setamount", setamount))

    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    main()
