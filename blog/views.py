# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
import hashlib


def index(request, page=1):
    page = int(page)
    per_page = 5
    last_page = int(Entries.objects.count()/per_page) + 1
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
    page_range = range(1, last_page)
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
    try:
        current_entry = Entries.objects.get(id=int(entry_id))
    except:
        return HttpResponse("해당 글이 없습니다.")
    try:
        prev_entry = current_entry.get_previous_by_created()
    except:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created()
    except:
        next_entry = None

    comments = Comments.objects.filter(Entry=current_entry).order_by('created')
    current_entry.Comments = len(comments)
    tpl = loader.get_template('read.html')
    ctx = Context({
        'page_title': page_title,
        'current_entry': current_entry,
        'prev_entry': prev_entry,
        'next_entry': next_entry,
        'comments': comments
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
    tags = filter(lambda x: x != '', map(lambda x: x.strip(), request.POST.get('tags', '').split(',')))
    tag_list = map(lambda tag: TagModel.objects.get_or_create(Title=tag)[0], tags)

    entry_category = Categories.objects.get(id=int(entry_category))
    new_entry = Entries(Title=entry_title, Content=entry_content, Category=entry_category)
    new_entry.save()

    for tag in tag_list:
        new_entry.Tags.add(tag)
    if tag_list:
        new_entry.save()

    return redirect('blog.views.read', entry_id=new_entry.id)


@csrf_exempt
def delete_post(request, entry_id=None):
    try:
        del_entry = Entries.objects.get(id=int(entry_id))
    except:
        return HttpResponse("해당 글이 없습니다")
    del_entry.delete()

    return redirect('blog.views.index', page=1)

@csrf_exempt
def add_comment(request):
    cmt_name = request.POST.get('name', '')
    if cmt_name == '':
        return HttpResponse("이름 입력하세요")

    cmt_password = request.POST.get('password', '')
    if cmt_password == '':
        return HttpResponse("비밀번호 입력하세요")
    cmt_password = hashlib.md5(cmt_password.encode('utf-8')).hexdigest()

    cmt_content = request.POST.get("content", '')
    if cmt_content == '':
        return HttpResponse("내용 입력하세요")

    entry_id = request.POST.get('entry_id', '')
    if entry_id == '':
        return HttpResponse("댓글 달 글을 지정해야 합니다.")
    entry = Entries.objects.get(id=entry_id)

    new_cmt = Comments(Name=cmt_name, Password=cmt_password, Content=cmt_content, Entry=entry)
    new_cmt.save()

    return redirect('blog.views.read', entry_id=entry.id)

@csrf_exempt
def get_comments(request, entry_id=None):
    comments = Comments.objects.filter(Entry=entry_id).order_by('created')

    tpl = loader.get_template('comments.html')
    ctx = Context({'comments': comments})

    if request.is_ajax():
        with_layout = False
    else:
        with_layout = True
    return HttpResponse(tpl.render(ctx))
