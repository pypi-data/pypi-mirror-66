from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseNotAllowed
from .thvisual import THVClient
from django.conf import settings
# Create your views here.

@login_required
def launchTerminal(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed("method not allowed")

    vapp = request.GET.get("vapp")
    if not vapp == "shell":
        return HttpResponseNotAllowed("shell must be setted as vapp params")
    #appid = "92895609"
    #appkey = "Bb0fqxdlKaU9Ct2fLwXtqNXGpKLVwlit"
    appid = settings.THTERMCONF['appid']
    appkey = settings.THTERMCONF['appkey']

    cluster = request.session.get('cluster','')
    server = settings.THTERMCONF['server']
    user = request.session.get('systemUsername','')
    client = THVClient(appid, appkey, server, cluster, user)
    token = client.launchApp(vapp)

    ws_url = "ws://%s/visual/v1/%s/%s/visual/%s/ws?token=%s" % (request.META['HTTP_HOST'],
        cluster, user, vapp, token.get('token'))

    return JsonResponse({"success":"yes","ws_url":ws_url})

@login_required
def thWTerm(request):
    return render(request,"thwterm.html",{})