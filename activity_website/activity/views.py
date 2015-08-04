from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect, Http404
from activity.models import *
from django.template import RequestContext
import re, datetime
from django import forms

# Create your views here.

def isAge(s):
    return (re.match(r'^[0-9]*$', s)) and (int(s) < 150)

def isSize(s, t):
    return (re.match(r'^[0-9]*$', s)) and (int(s) <= t)

def isEmail(s):
    return (re.match(r'^(\w+.)*\w+@(\w+.)+[a-z]{2,3}$', s))

def isPhone(s):
    return (re.match(r'^((13[0-9])|(15[^4,\D])|(18[0,5-9]))\d{8}$', s))

def getUser(request):
#    if ('user_id' in request.session):
#        user = User.objects.get(id == request.session['user_id'])
#        return user
#        return {
#            'nickname': user.nickname,
#            'request_num': Request.objects.filter(receiver = user, statuts = 'unread').count(),
#        }
#    else:
        return {}

def getPOST(request, t, max_len):
    if (t in request.POST) and (len(request.POST[t]) <= max_len):
        return request.POST[t]
    else:
        return False

def login(request):
    if (request.method == 'POST'):
        errors = {}
        try:
            user = User.objects.get(account = request.POST.get('account', ''))
            if user.password == request.POST.get('password', ''):
                request.session['user_id'] = user.id
                return HttpResponseRedirect('/welcome/')
            else:
                errors['password'] = 'Your password is wrong!'
                return render_to_response("login_form.html", {
                    'errors': errors
                }, context_instance = RequestContext(request))
        except User.DoesNotExist:
            errors['account'] = '该账号不存在'
            return render_to_response("login_form.html", {
                'errors': errors
            }, context_instance = RequestContext(request))
    else:
        return render_to_response("login_form.html", {
        }, context_instance = RequestContext(request))

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return HttpResponseRedirect('/welcome/')

def register(request):
    if (request.method == 'POST'):
        errors = {}
        if (not 'account' in request.POST) or (not request.POST['account']):
            errors['account'] = '请输入账号'
            #return HttpResponse('请输入账号')
        else:
            if (len(request.POST['account']) < 6) or (len(request.POST['account']) > 20) or (not re.match(r'^\w*$', request.POST['account'])):
                errors['account'] = '账号应为6-20位纯字母数字'
            elif (User.objects.filter(account = request.POST['account']).count() > 0):
                errors['account'] = '该账号已存在'
        if (not 'password1' in request.POST) or (not request.POST['password1']):
            errors['password1'] = '请输入密码'
        elif (len(request.POST['password1']) < 6) or (len(request.POST['password1']) > 20):
            errors['password1'] = '密码应为6-20位'
        if (not 'nickname' in request.POST) or (not request.POST['nickname']):
            errors['nickname'] = '请输入昵称'
        if (not 'sex' in request.POST) or (not request.POST['sex']):
            errors['sex'] = '请选择性别'
        if (not 'age' in request.POST) or (not request.POST['age']):
            errors['age'] = '请输入年龄'
        elif (not isAge(request.POST['age'])):
            errors['age'] = '请输入正确的年龄'
        if (not 'email' in request.POST) or (not request.POST['email']):
            errors['email'] = '请输入邮件'
        elif (not isEmail(request.POST['email'])):
            errors['email'] = '请输入正确的邮件'
        if (not 'phone' in request.POST) or (not request.POST['phone']):
            errors['phone'] = '请输入手机号'
        elif (not isPhone(request.POST['phone'])):
            errors['phone'] = '请输入正确的手机号'

        if (not 'interest' in request.POST) or (not request.POST['interest']):
            errors['interest'] = '请输入兴趣'

        if (errors):
            #return HttpResponse(errors)
            return render_to_response("register.html", {
                'errors': errors,
                'account': request.POST.get('account', ''),
                'password': request.POST.get('password', ''),
                'nickname': request.POST.get('nickname', ''),
                'sex': request.POST.get('sex', ''), #male/female
                'age': request.POST.get('age', ''),
                'email': request.POST.get('email', ''),
                'phone': request.POST.get('phone', ''),
                'interest': request.POST.get('interest', ''),
            }, context_instance = RequestContext(request))

        user = User(
            account = request.POST.get('account', ''),
            password = request.POST.get('password', ''),
            nickname = request.POST.get('nickname', ''),
            sex = request.POST.get('sex', ''), #male/female
            age = int(request.POST.get('age', '')),
            email = request.POST.get('email', ''),
            phone = request.POST.get('phone', ''),
            interest = request.POST.get('interest', ''),
        )
        user.save()
        request.session['user_id'] = user.id
        return HttpResponseRedirect('/welcome/')
    else:
        return render_to_response("register.html", {
        }, context_instance = RequestContext(request))

def welcome(request):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        return render_to_response("welcome.html", {
            'nickname': user.nickname
        }, context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def my_request(request):
    user = User.objects.get(id = request.session['user_id'])

    if (request.method == "POST"):
        req = Request.objects.get(id = request.POST["request_id"])
        if (req.type == 'notice'):
            req.status = 'read'
        else:
            req.status = request.POST['reply']
            if (req.status == 'accept'):
                if (req.type == 'activity_application'):
                    act = Activity.objects.get(id = req.goal)
                    #if (act.add_member(req.poster) == 'success'):
                    act.members.add(req.poster)
                    tmp_req = Request(
                        type = "notice",
                        title = "提醒",
                        content = "你参加活动'" + act.name + "'的申请已经通过",
                        poster = req.receiver,
                        receiver = req.poster,
                        status = "unread",
                        goal = " ",
                        time = datetime.datetime.now(),
                    )
                    tmp_req.save()
        req.save()

        return render_to_response("my_request.html", {
            'requests': [req for req in Request.objects.filter(receiver = user)],
        })
    else:
        return render_to_response("my_request.html", {
            'requests': [req for req in Request.objects.filter(receiver = user)],
        })

def apply_activity(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    act = Activity.objects.get(id = request.POST["id"])

    req = Request(
        type = "activity_application",
        title = user.nickname + "的活动参加申请",
        content = "账号" + user.account + "想参加活动 '" + act.name + "'",
        poster = user,
        receiver = act.organizer,
        status = "unread",
        time = datetime.datetime.now(),
        goal = act.id,
    )
    req.save()

    return HttpResponseRedirect('/welcome/')

def all_activities(request):
    if (request.method == 'POST'):
        #user = request.user
        #return HttpResponse(user.nickname)
        #if (not user):
        #    return HttpResponseRedirect('/login/')
        search_word = getPOST(request, 'search_word', 20)
        if (search_word):
            return render_to_response("all_activities.html", {
                "activities": [act for act in Activity.objects.filter(name__contains = search_word)]
            })
    else:
        return render_to_response("all_activities.html", {
            "activities": [act for act in Activity.objects.all()],
        }, context_instance = RequestContext(request))

def add_activity(request):
    if (request.method == 'POST'):
        #return HttpResponse(request.POST['startDate'] + '    ' + request.POST['startTime'])
        errors = {}
        if (not 'name' in request.POST) or (not request.POST['name']):
            errors['name'] = '请输入活动名称'
        elif (len(request.POST['name']) > 20):
            errors['name'] = '活动名称应少于20字'
        if (not 'type' in request.POST) or (not request.POST['type']):
            errors['type'] = '请选择活动类型'
        if (not 'explanation' in request.POST) or (not request.POST['explanation']):
            errors['explanation'] = '请输入活动内容'
        elif (len(request.POST['explanation']) > 400):
            errors['explanation'] = '活动内容应少于400字'
        if (not 'place' in request.POST) or (not request.POST['place']):
            errors['place'] = '请输入活动地点'
        elif (len(request.POST['place']) > 100):
            errors['place'] = '活动地点应少于100字'
        if (not 'min_age' in request.POST) or (not request.POST['min_age']):
            errors['min_age'] = '请输入最小年龄要求'
        elif (not isAge(request.POST['min_age'])):
            errors['min_age'] = '请输入正确的最小年龄'
        if (not 'max_age' in request.POST) or (not request.POST['max_age']):
            errors['max_age'] = '请输入最大年龄要求'
        elif (not isAge(request.POST['max_age'])):
            errors['max_age'] = '请输入正确的最大年龄'
        elif (int(request.POST['min_age']) > int(request.POST['max_age'])):
            errors['max_age'] = '最大年龄应不小于最小年龄'
        if (not 'max_size' in request.POST) or (not request.POST['max_size']):
            errors['max_size'] = '请输入最大参与人数'
        elif (not isSize(request.POST['max_size'], 1000)):
            errors['max_size'] = '最大参与人数应为不大于1000的正整数'

        if (errors):
            return render_to_response("add_activity.html", {
                'errors': errors
            }, context_instance = RequestContext(request))
        else:
            act = Activity(
                type = request.POST['type'],
                name = request.POST['name'],
                explanation = request.POST['explanation'],
                organizer = User.objects.get(id = request.session['user_id']),
                post_time = datetime.datetime.now(),
                applyend_time = datetime.datetime.strptime(request.POST['applyend_date'] + ' ' + request.POST['applyend_time'], '%Y/%m/%d %H:%M'),
                start_time = datetime.datetime.strptime(request.POST['start_date'] + ' ' + request.POST['start_time'], '%Y/%m/%d %H:%M'),
                end_time = datetime.datetime.strptime(request.POST['end_date'] + ' ' + request.POST['end_time'], '%Y/%m/%d %H:%M'),
                place = request.POST['place'],
                min_age = int(request.POST['min_age']),
                max_age = int(request.POST['max_age']),
                sex_requirement = request.POST['sex_requirement'],
                status = 'Null',
                max_size = int(request.POST['max_size']),
                current_size = 0,
            )
            act.save()
            return HttpResponseRedirect('/welcome/')
    else:
        return render_to_response("add_activity.html", {
        }, context_instance = RequestContext(request))

def change_userinfo(request):
    if (request.method == "POST"):
        if 'user_id' in request.session:
            user = User.objects.get(id = request.session['user_id'])
            user.nickname = request.POST.get('nickname')
            user.age = int(request.POST.get('age'))
            #user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.sex = request.POST.get('sex')
            user.interest = request.POST.get('interest')
            user.save()
            return HttpResponseRedirect('/welcome/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        if 'user_id' in request.session:
            user = User.objects.get(id = request.session['user_id'])
            return render_to_response("change_userinfo_form.html", {
                'account': user.account,
                'password': user.password,
                'nickname': user.nickname,
                'sex': user.sex, #male/female
                'age': user.age,
                'email': user.email,
                'phone': user.phone,
                'interest': user.interest,
            }, context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/login/')

def change_userpwd(request):
    if (request.method == 'POST'):
        errors = []
        old_password = ''
        new_password = ''
        if 'user_id' in request.session:
            user = User.objects.get(id = request.session['user_id'])
            if ('old_password' in request.POST) and (request.POST['old_password']):
                old_password = request.POST['old_password']
            else:
                errors.append('Please enter your old password.')
            if ('new_password1' in request.POST) and ('new_password2' in request.POST) and (request.POST['new_password1']) and (request.POST['new_password1'] == request.POST['new_password2']):
                new_password = request.POST['new_password1']
            else:
                errors.append('Please enter your new password correctly.')
            if (not errors):
                if (old_password == user.password):
                    User.objects.filter(id = user.id).update(password = new_password)
                else:
                    errors.append('Your old password is wrong.')
            if (errors):
                return render_to_response("change_userpwd_form.html", {
                    'errors': errors
                }, context_instance = RequestContext(request))
            else:
                return HttpResponseRedirect('/welcome/')
        else:
            errors.append('Please login.')
            return HttpResponseRedirect('/login/')
    else:
        return render_to_response("change_userpwd_form.html", {
        }, context_instance = RequestContext(request))

def add_group(request):
    return render_to_response('add_group.html',{
    })

def group_info(request, group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        raise Http404()
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise Http404()
    return render_to_response('group_info.html',{
        'group_time': group.found_time,
        'group_number': group.size,
        'group_content': group.explanation,
    })

def group_members(request, group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        raise Http404()
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise Http404()
    return render_to_response('group_members.html',{
        'group_usernamelist': [user.nickname for user in group.members],
    })

def group_activities(request, group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        raise Http404()
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise Http404()
    return render_to_response('group_activities.html',{
        'group_activity_list': [{
            'act_name': act.name,
            'act_content': act.explanation,
            'date': act.start_time.date,
            'time': act.start_time.time,
        } for act in group.activities],
    })

def home(request):
    activities = Activity.objects.all()
    return render_to_response("index.html", {
        'activities': activities
    }, context_instance = RequestContext(request))

class UserForm(forms.Form):
    username = forms.CharField()
    headimg = forms.FileField()

def upload_headimg(request):
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if (uf.is_valid()):
            user = User.objects.get(id = 2)
            user.headimg = uf.cleaned_data['headimg']
            user.save()
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render_to_response('upload_headimg.html',{'uf': uf})



def my_activities_attend(request):
    user = User.objects.get(id = request.session["user_id"])
    return render_to_response("my_attend.html", {
        "my_attend_activities": [act for act in user.activity_member.all()],
    })


def my_activities_launch(request):
    user = User.objects.get(id = request.session["user_id"])
    return render_to_response("my_launch.html", {
        "my_launch_activities": [act for act in user.activity_organizer.all()],
    })

def friend_activities_attend(request):
    user = User.objects.get(id = request.session["user_id"])
    acts = []
    for friend in user.friends.all():
        for act in friend.activity_member.all():
            if not act in acts:
                acts.append(act)
    return render_to_response("friend_attend.html", {
        "friend_attend_activities": acts,
    })

def friend_activities_launch(request):
    user = User.objects.get(id = request.session["user_id"])
    acts = []
    for friend in user.friends.all():
        for act in friend.activity_organizer.all():
            if not act in acts:
                acts.append(act)
    return render_to_response("friend_launch.html", {
        "friend_launch_activities": acts,
    })
