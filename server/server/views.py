import requests
import json

from django.http import HttpResponseRedirect, JsonResponse

from ccg_nlpy import remote_pipeline

def availableViews(request):
    return JsonResponse({"images": []})

pipeline = remote_pipeline.RemotePipeline()

def annotate(request):
    if request.method == "POST":
        text = request.POST['text']
        views=request.POST['views']
    else:
        text = request.GET['text']
        views = request.GET['views']

    doc = pipeline.doc(text)

    if 'NITISH_VIEW' in views:
        pass # if the view is requested add it to the document.  


    return JsonResponse(doc.as_json)
