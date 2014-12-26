# -*- coding: utf-8 -*-
import functools
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
import json
import hashlib


def root(request):
    return HttpResponseRedirect('/blog/')


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        if 'blog_login_sess' in request.session:
            return fn(request, *args, **kwargs)
        else:
            return redirect('blog.views.login_form')
    return wrapper


def index(request, page=1):
    log_in = 'blog_login_sess' in request.session
    page = int(page)
    per_page = 5
    last_page = int(Entries.objects.count()/per_page)
    if Entries.objects.count() % per_page > 0:
        last_page += 1
    last_page = max(last_page, 1)
  #  if not isinstance(page, int):
    if page < 1:
        raise Http404
    if page > last_page:
        raise Http404
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
        'page_range': page_range,
        'login': log_in,
        'location': 'index'
    })
    return HttpResponse(tpl.render(ctx))


def read(request, entry_id=None):
    page_title = '블로그 글 읽기!'
    try:
        current_entry = Entries.objects.get(id=int(entry_id))
    except Entries.DoesNotExist:
        return HttpResponse("해당 글이 없습니다.")
    try:
        prev_entry = current_entry.get_previous_by_created()
    except Entries.DoesNotExist:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created()
    except Entries.DoesNotExist:
        next_entry = None
    comments = Comments.objects.filter(entry=current_entry).order_by('created')
    tpl = loader.get_template('read.html')
    ctx = Context({
        'page_title': page_title,
        'current_entry': current_entry,
        'prev_entry': prev_entry,
        'next_entry': next_entry,
        'comments': comments,
    })
    return HttpResponse(tpl.render(ctx))

@login_required
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
@login_required
def add_post(request):
    title = request.POST.get('title', '')
    if title == '':
        return HttpResponse("제목을 입력하세요")
    content = request.POST.get('content', '')
    if content == '':
        return HttpResponse("본문을 입력하세요")
    category = request.POST.get('category', '')
    if category == '':
        return HttpResponse("카테고리 입력")
    tags = [x for x in
            (x.strip() for x in request.POST.get('tags', '').split(','))
            if x != '']
    tag_list = [TagModel.objects.get_or_create(title=tag)[0] for tag in tags]

    category = Categories.objects.get(id=int(category))
    new_entry = Entries(title=title, content=content, category=category)
    new_entry.save()

    for tag in tag_list:
        new_entry.tags.add(tag)
    if tag_list:
        new_entry.save()

    return redirect('blog.views.read', entry_id=new_entry.id)


@csrf_exempt
@login_required
def delete_post(request, entry_id=None):
    if 'blog_login_sess' in request.session:
        try:
            del_entry = Entries.objects.get(id=int(entry_id))
        except Entries.DoesNotExist:
            return HttpResponse("해당 글이 없습니다")
        del_entry.delete()
        return redirect('blog.views.index', page=1)
    else:
        return login_form(request, 'index', True)


@csrf_exempt
def add_comment(request):
    name = request.POST.get('name', '')
    if name == '':
        return HttpResponse("이름 입력하세요")

    pwd = request.POST.get('password', '')
    if pwd == '':
        return HttpResponse("비밀번호 입력하세요")
    pwd = hashlib.md5(pwd.encode('utf-8')).hexdigest()

    content = request.POST.get("content", '')
    if content == '':
        return HttpResponse("내용 입력하세요")

    entry_id = request.POST.get('entry_id', '')
    if entry_id == '':
        return HttpResponse("댓글 달 글을 지정해야 합니다.")
    entry = Entries.objects.get(id=entry_id)

    new_cmt = Comments(name=name, password=pwd, content=content, entry=entry)
    new_cmt.save()

    comments = Comments.objects.filter(entry=entry).order_by('created')
    entry.comment_num = len(comments)
    entry.save()

    if request.is_ajax():
        return_data = {
            'entry_id': entry.id,
            'msg': get_comments(request, entry.id, True)
        }
        return HttpResponse(json.dumps(return_data))
    else:
        return redirect('blog.views.read', entry_id=entry.id)


@csrf_exempt
def get_comments(request, entry_id=None, is_inner=False):
    current_entry = Entries.objects.get(id=int(entry_id))
    comments = Comments.objects.filter(entry=entry_id).order_by('created')

    if request.is_ajax():
        with_layout = False
    else:
        with_layout = True

    tpl = loader.get_template('comments.html')
    ctx = Context({
        'current_entry': current_entry,
        'comments': comments,
        'with_layout': with_layout
    })
    if is_inner:
        return tpl.render(ctx)
    else:
        return HttpResponse(tpl.render(ctx))


@csrf_exempt
def login_form(request, location='index', with_layout=False):
    page_title = '로그인'
    tpl = loader.get_template('login.html')
    ctx = Context({
        'page_title': page_title,
        'location': location,
        'with_layout': with_layout
    })
    return HttpResponse(tpl.render(ctx))


@csrf_exempt
def login(request, location='index'):
    admin_id = 'real'
    admin_pw = hashlib.md5('1234'.encode('utf-8')).hexdigest()
    u_id = request.POST.get("ID", '')
    u_pwd = hashlib.md5(request.POST.get("PW", '').encode('utf-8')).hexdigest()
    if u_id == admin_id and u_pwd == admin_pw:
        request.session['blog_login_sess'] = u_id
        return redirect('blog.views.'+location)
    else:
        return HttpResponse('아이디 또는 비밀번호가 틀렸습니다.')


@login_required
def logout(request):
    """로그아웃을 합니다.

    :param request:
    :return:
    """
    del request.session['blog_login_sess']
    return redirect('blog.views.index')
