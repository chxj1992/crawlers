# coding=utf-8
import json

from flask import Module, request

from tools.proxy import crawler

proxy = Module(__name__, 'proxy')


@proxy.route("/proxy/samair")
def samair():
    try:
        return json.dumps(crawler.samair())
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}


@proxy.route("/proxy/samair/shuffle")
def samair_shuffle():
    try:
        return json.dumps(crawler.shuffle(crawler.samair()))
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}


@proxy.route("/proxy/sslproxies")
def sslproxies():
    try:
        return json.dumps(crawler.ssl_proxies())
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}


@proxy.route("/proxy/sslproxies/shuffle")
def sslproxies_shuffle():
    try:
        return json.dumps(crawler.shuffle(crawler.ssl_proxies()))
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}


@proxy.route("/proxy/hidemyass")
def hidemyass():
    try:
        protocol = request.args.get('protocol', 'http')
        return json.dumps(crawler.hide_my_ass(protocol))
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}


@proxy.route("/proxy/hidemyass/shuffle")
def hidemyass_shuffle():
    try:
        protocol = request.args.get('protocol', 'http')
        return json.dumps(crawler.shuffle(crawler.hide_my_ass(protocol)))
    except Exception as e:
        return {'error': 'system error', 'msg': e.message}
