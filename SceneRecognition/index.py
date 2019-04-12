from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_exempt

from SceneRecognition.model import run_placesCNN_web

@csrf_exempt
def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        print(request.FILES)
        filename = os.path.dirname(__file__)
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
            #return HttpResponse(request,"upload_form.html")
        img_name = os.path.join(filename+"/upload/",myFile.name)
        #img_name = os.path.join("/home/lfh/Desktop/SceneRecognition/templates/file/", myFile.name)

        destination = open(img_name,'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        # 放入CNN模块计算
        result = run_placesCNN_web.run_placesCNN(img_name)
        ctx = {}
        ctx['image_name'] = "/static/upload/"+ myFile.name
        ctx['result'] = result
        return render(request, "upload_form.html", ctx)
        #return HttpResponse("upload over!"+result)
    return HttpResponse("error!!")
@csrf_exempt

def sceneRecognition(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理

        filename = os.path.dirname(__file__)
        myFile =request.FILES.get("files[]", None)    # 获取上传的文件，如果没有文件，则默认为None
        print(myFile)
        if not myFile:
            return HttpResponse("no files for upload!")
            #return HttpResponse(request,"upload_form.html")
        img_name = os.path.join(filename+"/upload/",myFile.name)

        destination = open(img_name,'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 放入CNN模块计算
        result = run_placesCNN_web.run_placesCNN(img_name)
        ctx = {}
        ctx['image_name'] = "/upload/"+ myFile.name
        ctx['result'] = result
        return JsonResponse(ctx)
    return HttpResponse("error!!")
@csrf_exempt
def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)
