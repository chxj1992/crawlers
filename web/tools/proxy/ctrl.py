# coding=utf-8
import json

from flask import Module

from tools.proxy import crawler

proxy = Module(__name__, 'proxy')


@proxy.route("/proxy/samair")
def samair():
    return json.dumps(crawler.samair())


@proxy.route("/proxy/samair/shuffle")
def samair_shuffle():
    return json.dumps(crawler.shuffle(crawler.samair()))


@proxy.route("/proxy/sslproxies")
def sslproxies():
    return json.dumps(crawler.ssl_proxies())


@proxy.route("/proxy/sslproxies/shuffle")
def sslproxies_shuffle():
    return json.dumps(crawler.shuffle(crawler.ssl_proxies()))


@proxy.route("/proxy/hidemyass")
def hidemyass():
    return json.dumps(crawler.hide_my_ass())


@proxy.route("/proxy/hidemyass/shuffle")
def hidemyass_shuffle():
    return json.dumps(crawler.shuffle(crawler.hide_my_ass()))
