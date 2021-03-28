from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from .models import TubesearchModel
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.conf import settings
from apiclient import discovery
import json


# youtube検索の関数
def get_search(keyword):
    # keyword = self.keyword
    youtube = discovery.build('youtube', 'v3', developerKey=settings.YOUTUBE_DATA_V3_API_KEY)
    youtube_query = youtube.search().list(q=keyword, part='id,snippet', maxResults=3)
    youtube_res = youtube_query.execute()
    return youtube_res.get('items', [])

    # 以下のように取り出せる
    #    items = get_search(keyword)
    #    for item in items:
    #        print(item['snippet']['title'])
    #        print("https://www.youtube.com/watch?v="+item['id']['videoId'])


# Create your views here.

@login_required
def TubesearchListfunc(request):
    object_list = TubesearchModel.objects.all()
    return render(request, 'list.html', { 'object_list': object_list })

def Detailfunc(request, pk):
    object = get_object_or_404(TubesearchModel, pk=pk)

    items = get_search(object.keyword)
    # print(type(items))
    videos = []
    for item in items:
        video = {
            'title': item['snippet']['title'],
            # 視聴用URL
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            # 埋込用URL
            'emb': f"https://www.youtube.com/embed/{item['id']['videoId']}?loop=1&rel=0&modestbranding=1"
        }
        videos.append(video)

    return render(request, 'detail.html', {'object': object, 'videos': videos})

class Create(CreateView):
    template_name = 'create.html'
    model = TubesearchModel
    fields = ('title', 'memo', 'keyword')
    # success_url = reverse_lazy('list')
    success_url = reverse_lazy('create')


class Delete(DeleteView):
    template_name = 'delete.html'
    model = TubesearchModel
    success_url = reverse_lazy('list')

class Update(UpdateView):
    template_name = 'update.html'
    model = TubesearchModel
    fields = ('title', 'memo', 'keyword', 'last_date')
    success_url = reverse_lazy('list')


# サインイン機能
def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username,'', password)
            return render(request, 'signup.html', {'text': '登録しました'})
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザーネームはすでに使われています．'})

    return render(request, 'signup.html', {})

# ログイン
def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('list')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'context': 'ログインできませんでした．'})

    return render(request, 'login.html', {})

# ログアウト
def logoutfunc(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')