from flask import Flask

from web.ticket.wepiao.ctrl import wepiao
from web.tools.proxy.ctrl import proxy

app = Flask(__name__)
app.register_module(wepiao)
app.register_module(proxy)


@app.route("/")
def hello():
    return "Hello Crawlers!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
