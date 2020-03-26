"""
 Created by 七月 on 2018/1/26.
 微信公众号：林间有风
"""
from . import web
from flask import render_template, request, redirect, url_for, session, make_response

__author__ = '七月'


@web.route('/set/cookie')
def set_cookie():
    response = make_response('Hello MR.7')
    response.set_cookie('name', 'MR.7', 100)
    return response


@web.route('/set/session')
def set_session():
    session['t'] = 1
    return 'over'


@web.route('/get/session')
def get_session():
    return str(session['t'])
