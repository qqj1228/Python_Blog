#!/usr/bin/env python3
# coding:utf-8

import re, hashlib, json, logging, os

from aiohttp import web
from markdown2 import markdown

from webframe import get, post, user2cookie, Page
from model import next_id, User, Blog, Comment, Category
from configloader import configs
from APIError import APIError, APIValueError, APIPermissionError, APIResourceNotFoundError

@get('/')
async def index(request, *, page='1'):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    page_index = Page.page2int(page)
    num = await Blog.findNumber('*')
    p = Page(num, page_index, item_page=configs.blog_item_page, page_show=configs.page_show)
    p.pagelist()
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
        for blog in blogs:
            blog.html_summary = markdown(blog.summary)
    return {
        '__template__': 'index.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'page': p,
        'blogs': blogs,
        'disqus': configs.use_disqus
    }

@get('/signup')
async def signin():
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'signup.html',
        'web_meta': configs.web_meta,
        'cats': cats
    }

@get('/login')
async def login():
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'login.html',
        'web_meta': configs.web_meta,
        'cats': cats
    }

@get('/logout')
async def logout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.del_cookie(configs.cookie.name)
    logging.info('user logged out.')
    return r

@get('/blog/{id}')
async def get_blog(id, request):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = markdown(c.content)
    blog.html_content = markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'blog': blog,
        'comments': comments,
        'disqus': configs.use_disqus
    }

@get('/user/{id}')
async def get_user(id, request):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    user_show = await User.find(id)
    return {
        '__template__': 'user.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'user_show': user_show
    }

@get('/category/{id}')
async def get_category(id, request, *, page='1'):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    category = await Category.find(id)
    page_index = Page.page2int(page)
    num = await Blog.findNumber('*', 'cat_id=?', [id])
    p = Page(num, page_index, item_page=configs.blog_item_page, page_show=configs.page_show)
    p.pagelist()
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll('cat_id=?', [id], orderBy='created_at desc', limit=(p.offset, p.limit))
        for blog in blogs:
            blog.html_summary = markdown(blog.summary)
    return {
        '__template__': 'category.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'page': p,
        'category': category,
        'blogs': blogs,
        'disqus': configs.use_disqus
    }

@get('/api/blogs/{id}')
async def api_show_blogs(*, id):
    blog = await Blog.find(id)
    return blog

# handler带有默认值的命名关键字参数，用来处理带有查询字符串的url
@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = Page.page2int(page)
    num = await Blog.findNumber('*')
    p = Page(num, page_index, item_page=configs.manage_item_page, page_show=configs.page_show)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)

# handler带有默认值的命名关键字参数，用来处理带有查询字符串的url
@get('/api/comments')
async def api_comments(*, page='1'):
    page_index = Page.page2int(page)
    num = await Comment.findNumber('*')
    p = Page(num, page_index, item_page=configs.manage_item_page, page_show=configs.page_show)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)

# handler带有默认值的命名关键字参数，用来处理带有查询字符串的url
@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = Page.page2int(page)
    num = await User.findNumber('*')
    p = Page(num, page_index, item_page=configs.manage_item_page, page_show=configs.page_show)
    if num == 0:
        return dict(page=p, user=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.password = '******'
    return dict(page=p, users=users)

# handler带有默认值的命名关键字参数，用来处理带有查询字符串的url
@get('/api/categories')
async def api_categories(*, page='1'):
    page_index = Page.page2int(page)
    num = await Category.findNumber('*')
    p = Page(num, page_index, item_page=configs.manage_item_page, page_show=configs.page_show)
    if num == 0:
        return dict(page=p, categories=())
    categories = await Category.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, categories=categories)

@get('/api/categories/{id}')
async def api_show_categories(*, id):
    cat = await Category.find(id)
    return cat

@get('/manage')
def manage():
    return 'redirect:/manage/blogs'

@get('/manage/blogs')
async def manage_blogs(request, *, page='1'):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_blogs.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'page_index': Page.page2int(page)
    }

@get('/manage/blogs/create')
async def manage_blogs_create(request):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_blog_edit.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'id': '',
        'action': '/api/create_blog'
    }

@get('/manage/blogs/edit')
async def manage_blogs_edit(request, *, id):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_blog_edit.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'id': id,
        'action': '/api/blogs/%s' % id
    }

@get('/manage/comments')
async def manage_comments(request, *, page='1'):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_comments.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'page_index': Page.page2int(page)
    }

@get('/manage/users')
async def manage_users(request, *, page='1'):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_users.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'page_index': Page.page2int(page)
    }

@get('/manage/categories')
async def manage_categories(request, *, page='1'):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_categories.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'page_index': Page.page2int(page)
    }

@get('/manage/categories/create')
async def manage_categories_create(request):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_category_edit.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'id': '',
        'action': '/api/create_category'
    }

@get('/manage/categories/edit')
async def manage_categories_edit(request, *, id):
    user = request.__user__
    cats = await Category.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_category_edit.html',
        'web_meta': configs.web_meta,
        'user': user,
        'cats': cats,
        'id': id,
        'action': '/api/categories/%s' % id
    }

RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/signup')
async def api_signin(*, email, name, password):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not RE_SHA1.match(password):
        raise APIValueError('password')

    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('signin:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_password = '%s:%s' % (uid, password)
    user = User(id=uid, name=name.strip(), email=email, password=hashlib.sha1(sha1_password.encode('utf-8')).hexdigest(), image=configs.web_meta.user_image)
    await user.save()
    # 设置cookie
    r = web.Response()
    r.set_cookie(configs.cookie.name, user2cookie(user, configs.cookie.max_age), max_age=configs.cookie.max_age, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@post('/api/login')
async def api_login(*, email, password, rememberme):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not password:
        raise APIValueError('password', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # 检查密码
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(password.encode('utf-8'))
    logging.info('password:%s' % user.password)
    logging.info('sha1:%s' % sha1.hexdigest())
    if user.password != sha1.hexdigest():
        raise APIValueError('password', 'Invalid password.')
    # 密码正确，设置cookie
    r = web.Response()
    if rememberme:
        max_age = configs.cookie.max_age_long
    else:
        max_age = configs.cookie.max_age
    r.set_cookie(configs.cookie.name, user2cookie(user, max_age), max_age=max_age, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@post('/api/create_blog')
async def api_create_blog(request, *, title, summary, content, cat_name):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    if not title or not title.strip():
        raise APIValueError('title', 'Title can not be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'Content can not be empty.')
    if not summary or not summary.strip():
        summary = content.strip()[:200]
    if not cat_name.strip():
        cat_id = None
    else:
        cats = await Category.findAll('name=?', [cat_name.strip()])
        if (len(cats) == 0):
            raise APIValueError('cat_name', 'cat_name is not belong to Category.')
        cat_id = cats[0].id
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, title=title.strip(), summary=summary.strip(), content=content.strip(), cat_id=cat_id, cat_name=cat_name.strip())
    await blog.save()
    return blog

@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, title, summary, content, cat_name):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    if not title or not title.strip():
        raise APIValueError('title', 'Title can not be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'Content can not be empty.')
    if not summary or not summary.strip():
        summary = content.strip()[:200]
    blog = await Blog.find(id)
    blog.title = title.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    blog.cat_name = cat_name.strip()
    if not cat_name.strip():
        blog.cat_id = None
    else:
        cats = await Category.findAll('name=?', [cat_name.strip()])
        if (len(cats) == 0):
            raise APIValueError('cat_name', 'cat_name is not belong to Category.')
        blog.cat_id = cats[0].id
    await blog.update()
    return blog

@post('/api/blogs/{id}/delete')
async def api_delete_blog(request, *, id):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    await blog.remove()
    return dict(id=id)

@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None or not user.admin:
        raise APIPermissionError()
    if not content or not content.strip():
        raise APIValueError('comment', 'Comment can not be empty.')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    await comment.save()
    return comment

@post('/api/comments/{id}/delete')
async def api_delete_comment(id, request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    comment = await Comment.find(id)
    if comment is None:
        raise APIResourceNotFoundError('Comment')
    await comment.remove()
    return dict(id=id)

@post('/api/users/{id}/delete')
async def api_delete_user(id, request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    user = await User.find(id)
    if user is None:
        raise APIResourceNotFoundError('User')
    await user.remove()
    return dict(id=id)

@post('/upload')
async def upload(request, *, file):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    filename = path + '/upload/' + file.filename
    ext = os.path.splitext(filename)
    # 处理重名文件
    n = 1
    while os.path.exists(filename):
        filename = '%s~%d%s' % (ext[0], n, ext[1])
        n = n+1

    with open(filename, 'wb') as f:
        f.write(file.file.read())
    return dict(filename=os.path.basename(filename))

@post('/api/create_category')
async def api_create_category(request, *, name):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    if not name or not name.strip():
        raise APIValueError('name', 'Name can not be empty.')
    cat = Category(name=name.strip())
    await cat.save()
    return cat

@post('/api/categories/{id}')
async def api_update_category(id, request, *, name):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    if not name or not name.strip():
        raise APIValueError('name', 'Name can not be empty.')
    cat = await Category.find(id)
    cat.name = name.strip()
    await cat.update()
    return cat

@post('/api/categories/{id}/delete')
async def api_delete_category(id, request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()
    cat = await Category.find(id)
    if cat is None:
        raise APIResourceNotFoundError('Category')
    await cat.remove()
    return dict(id=id)
