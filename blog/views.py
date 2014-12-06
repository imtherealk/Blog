# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from blog.models import Entries, Categories
from django.template import Context, loader

def index(request, page=1):
    page = int(page)
    per_page = 5
    last_page = int(Entries.objects.count()/per_page)
    if Entries.objects.count() % per_page > 0:
        last_page += 1
    if not isinstance(page, int):
        return redirect('blog.views.index', page=1)
    if page < 1:
        return redirect('blog.views.index', page=1)
    if page > last_page:
        return redirect('blog.views.index', page=last_page)
    start_pos = (page-1)*per_page
    end_pos = start_pos + per_page
    page_title = '블로그 글 목록'
    page_range = range(1, last_page+1)
    entries = Entries.objects.all().order_by('-created')[start_pos:end_pos]
    tpl = loader.get_template('list.html')
    ctx = Context({
        'page_title': page_title,
        'entries': entries,
        'current_page': page,
        'page_range': page_range
    })
    return HttpResponse(tpl.render(ctx))

def read(request, entry_id=None):
    page_title = '블로그 글 읽기!'
    current_entry = Entries.objects.get(id=int(entry_id))
    try:
        prev_entry = current_entry.get_previous_by_created()
    except:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created()
    except:
        next_entry = None
    tpl = loader.get_template('read.html')
    ctx = Context({
        'page_title': page_title,
        'current_entry': current_entry,
        'prev_entry': prev_entry,
        'next_entry': next_entry
    })
    return HttpResponse(tpl.render(ctx))

def write_form(request):
    page_title = '블로그 글 쓰기'
    categories = Categories.objects.all()
    tpl = loader.get_template('write.html')
    ctx = Context({
        'page_title': page_title,
        'categories': categories
    })
    return HttpResponse(tpl.render(ctx))

@csrf_exempt
def add_post(request):
    entry_title = request.POST.get('title', '')
    if entry_title == '':
        return HttpResponse("제목을 입력하세요")
    entry_content = request.POST.get('content', '')
    if entry_content == '':
        return HttpResponse("본문을 입력하세요")
    entry_category = request.POST.get('category', '')
    if entry_category == '':
        return HttpResponse("카테고리 입력")

    entry_category = Categories.objects.get(id=int(entry_category))
    new_entry = Entries(Title=entry_title, Content=entry_content, Category=entry_category)
    new_entry.save()

    return redirect('blog.views.read', entry_id = new_entry.id)