# coding=utf-8
import json

from flask import Module

from tools.proxy import crawler

proxy = Module(__name__, 'proxy')


@proxy.route("/proxy/shuffle")
def shuffle():
    return crawler.shuffle()
