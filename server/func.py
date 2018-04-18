import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def deploy(request):
    if request.method != 'POST':
        return HttpResponse('POST ONLY')
    if request.META.get('HTTP_X_GITHUB_EVENT', 'unk') != 'push':
        return HttpResponse('NOT PUSH')
    print('deploying')
    os.system('cd /web-server/cloud-server/ && git pull origin master')
    return HttpResponse('OVER')