from web_shop.bot.main import app, set_webhook

if __name__ == '__main__':
    set_webhook()
    app.run(port=9000, debug=True)