from flask import Flask

from web.proxy.ctrl import proxy
from web.ticket.wepiao.ctrl import wepiao

app = Flask(__name__)
app.register_module(wepiao)
app.register_module(proxy)


@app.route("/")
def hello():
    return "Hello Crawlers!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
