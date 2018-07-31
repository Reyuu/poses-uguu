from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Devs, DoneDevs, ReportedPics, IgnoredPics, SuggestionBox, FeedbackBox
from random import randint
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
from ratelimit.decorators import ratelimit
from ratelimit.utils import is_ratelimited
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import serializers
from configparser import ConfigParser
# Create your views here.

import importlib.machinery

loader = importlib.machinery.SourceFileLoader('da-get', '/home/rey44/da-tool/da-get.py')
da_get = loader.load_module('da-get')
auth_url = "https://www.deviantart.com/oauth2/"
base_url = "https://www.deviantart.com/api/v1/oauth2/"
headers = {"user-agent": "my-app/1-20180714", "Accept-Encoding": "gzip, deflate"}
config = ConfigParser()
config.read("/home/rey44/da-tool/config.ini")


api = da_get.Api(auth_url, base_url, config, headers)

allowedIps = ['129.0.0.1', '127.0.0.1', '109.196.43.32']

def allow_by_ip(view_func):
    def authorize(request, *args, **kwargs):
        user_ip = request.META['REMOTE_ADDR']
        for ip in allowedIps:
            if ip==user_ip:
                return view_func(request, *args, **kwargs)
        return HttpResponse('Invalid Ip Access!')
    return authorize

def get_random_item(model):
    i = IgnoredPics.objects.all().values("deviationid")
    r = model.objects.all().exclude(deviationid__in=i)
    count = r.count()
    random_object = r.all()[randint(0, count - 1)]
    return random_object

def get_random_pose(request):
    random_item = get_random_item(Devs)
    data = {"deviation_id": random_item.deviationid, "content_src": random_item.content_src, "viewable": random_item.viewable, "url":random_item.url}
    return JsonResponse(data)

#@ratelimit(key='ip', rate='1/d')

@csrf_protect
@ratelimit(key='post:deviation_id', rate='1/d', method=['POST'], block=False, group="report")
def report_image(request):
    print(request.POST)
    dev_id = request.POST.get("deviation_id", "")
    if dev_id == "":
        return JsonResponse({"error": "deviation_id is empty!"})

    was_limited = getattr(request, 'limited', False)
    if was_limited:
        print(was_limited)
        return JsonResponse({"error": "you already voted for this deviation today!"})

    rep = ReportedPics.objects.filter(deviationid=dev_id)
    if rep.exists():
        report= rep[0]
        report.report_count += 1
        print(report.report_count)
        report.save()
        return JsonResponse({"ok": "added to existing!"})
    else:
        rep = ReportedPics.objects.create(deviationid=dev_id, report_count=1)
        return JsonResponse({"ok": "created new report!"})

#@ratelimit(key='ip', rate='1/d')
@csrf_protect
@ratelimit(key='post:username', rate='1/d', method=['POST'], block=False, group="suggest")
def suggest(request):
    print(request.POST)
    username = request.POST.get("username", "")
    if username == "":
        return JsonResponse({"error": "username is empty!"})
    else:
        resp = api.get_resource("user/profile/%s" % username, {})
        if resp.status_code >= 400:
            return JsonResponse({"error": "couldn't find this user!"})
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({"error": "you already voted for this user today!"})
    u = SuggestionBox.objects.filter(username=username)
    if u.exists():
        usr = u[0]
        usr.suggest_count += 1
        usr.save()
        return JsonResponse({"ok": "added to existing!"})
    else:
        SuggestionBox.objects.create(username=username, suggest_count=1)
        return JsonResponse({"ok": "created new suggestion!"})

def should_reset(group, request):
    if request.POST.get("feedback", "") == "":
        return "20/s"
    else:
        return "1/d"

@csrf_protect
@ratelimit(key='ip', rate=should_reset, block=False, group="feedback")
def feedback(request):
    print(request.POST)
    feedback = request.POST.get("feedback", "")
    if feedback == "":
        return JsonResponse({"error": "feedback is empty!"})
    was_limited = getattr(request, 'limited', False)
    print(was_limited)
    if was_limited:
        return JsonResponse({"error": "you already submitted feedback today!"})
    FeedbackBox.objects.create(feedback = feedback)
    return JsonResponse({"ok": "created new feedback!"})

@allow_by_ip
@login_required
def mod_index(request):
    return render(request, "mod_index.html", {})

@login_required
def mod_get_all_reports(request):
    r = ReportedPics.objects.all()
    i = IgnoredPics.objects.all().values("deviationid")
    x = r.exclude(deviationid__in=i)
    data = serializers.serialize("json", x)
    return JsonResponse({"ok": "got data!", "data": data})

@login_required
@csrf_exempt
def mod_get_pic_by_id(request):
    devid = request.POST.get("deviationid", "")
    ignored = IgnoredPics.objects.filter(deviationid=devid)
    if ignored.exists():
        return JsonResponse({"error": "ignored"})
    data = Devs.objects.filter(deviationid=devid)
    return JsonResponse({"ok": "got data!", "data": data[0].content_src})

@login_required
@csrf_exempt
def mod_handle_report(request):
    devid = request.POST.get("deviationid", "")
    typ = request.POST.get("type", "")
    print(typ)
    typ = True if typ == "'true'" else False
    x = Devs.objects.filter(deviationid=devid)[0]
    x.viewable = typ
    x.save()
    y = IgnoredPics.objects.create(deviationid=devid)
    return JsonResponse({"ok": "done!"})

def main_view(request):
    return render(request, 'main_view.html', {})

def logout_view(request):
    logout(request)
    return redirect(index)

@ensure_csrf_cookie
def index(request):
    c = Devs.objects.count()
    return render(request, "index2.html", {"count": c})