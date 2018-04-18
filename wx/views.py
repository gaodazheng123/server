import hashlib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .secret import secret
import xml.etree.ElementTree as ET
import time


def checksignature(request):
    # if request.method != 'GET':
    #     return HttpResponse('only get method is available for check signature')
    # print(request.GET)
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    echostr = request.GET.get('echostr')
    nonce = request.GET.get('nonce')
    if signature and timestamp and echostr:
        l = [secret['check_signature_token'], nonce, timestamp]
        l.sort()
        s = ''.join(l)
        s = hashlib.sha1(s.encode('utf-8')).hexdigest()
        if s == signature:
            return HttpResponse(echostr)
    return HttpResponse('Fail')


def reply(request):
    data = request.body
    print(data)
    tree = ET.fromstring(data)
    msg = {}
    for t in tree:
        msg[t.tag] = t.text
    # if msg['MsgType'] != 'text':
    #     msg['Content'] = '不支持的消息类型: %s' % msg['MsgType']
    response = '<xml> ' \
               '<ToUserName>%s</ToUserName> ' \
               '<FromUserName>%s</FromUserName> ' \
               '<CreateTime>%d</CreateTime> ' \
               '<MsgType>text</MsgType> <Content>' \
               '%s</Content>' \
               '</xml> ' % (msg['FromUserName'], msg['ToUserName'], time.time(), msg['Content'])
    return HttpResponse(response)


@csrf_exempt
def wx(request):
    if request.method == 'GET':
        return checksignature(request)
    elif request.method == 'POST':
        return reply(request)