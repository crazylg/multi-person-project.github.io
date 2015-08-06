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

def getUserObj(id):
    try:
        user = User.objects.get(id = id)
        return {
            "nickname": user.nickname,
            "request_num": user.request_receiver.filter(status = "unread").count(),
        }
    except User.DoesNotExist:
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
                    'user': getUserObj(user.id),
                    'errors': errors
                }, context_instance = RequestContext(request))
        except User.DoesNotExist:
            errors['account'] = '该账号不存在'
            return render_to_response("login_form.html", {
                'user': getUserObj(user.id),
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
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    #return HttpResponse(getUserObj(user.id)["nickname"])
    return render_to_response("welcome.html", {
        'user': getUserObj(user.id),
    }, context_instance = RequestContext(request))

def change_userinfo(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    if (request.method == "POST"):
        user.nickname = request.POST.get('nickname')
        user.age = int(request.POST.get('age'))
        #user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.sex = request.POST.get('sex')
        user.interest = request.POST.get('interest')
        user.save()
        return HttpResponseRedirect('/welcome/')
    else:
        return render_to_response("change_userinfo_form.html", {
            'user': getUserObj(user.id),
            'account': user.account,
            'password': user.password,
            'nickname': user.nickname,
            'sex': user.sex, #male/female
            'age': user.age,
            'email': user.email,
            'phone': user.phone,
            'interest': user.interest,
        }, context_instance = RequestContext(request))

def change_userpwd(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    if (request.method == 'POST'):
        errors = []
        old_password = ''
        new_password = ''
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
                'user': getUserObj(user.id),
                'errors': errors
            }, context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/welcome/')
    else:
        return render_to_response("change_userpwd_form.html", {
            'user': getUserObj(user.id),
        }, context_instance = RequestContext(request))



def my_request(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

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
                    act.current_size += 1
                    act.save()
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
                if (req.type == 'friend_application'):
                    user.friends.add(req.poster)
                    tmp_req = Request(
                        type = "notice",
                        title = "提醒",
                        content = "你向 " + user.nickname + " 提交的好友请求已通过",
                        poster = req.receiver,
                        receiver = req.poster,
                        status = "unread",
                        goal = " ",
                        time = datetime.datetime.now(),
                    )
                    tmp_req.save()
                if (req.type == 'group_invitation'):
                    grp = Group.objects.get(id = req.goal)
                    grp.members.add(user)
                    grp.current_size += 1
                    grp.save()
                    tmp_req = Request(
                        type = "notice",
                        title = user.nickname + " 接受了你的邀请",
                        content = "账号 " + user.account + " 接受了你的邀请, 加入了群组'" + grp.name + "'",
                        poster = req.receiver,
                        receiver = req.poster,
                        status = "unread",
                        goal = " ",
                        time = datetime.datetime.now(),
                    )
                    tmp_req.save()

        req.save()

        reqs = [req for req in Request.objects.filter(receiver = user)]
        reqs.reverse()
        return render_to_response("my_request.html", {
            'user': getUserObj(user.id),
            'requests': reqs,
        })
    else:
        reqs = [req for req in Request.objects.filter(receiver = user)]
        reqs.reverse()
        return render_to_response("my_request.html", {
            'user': getUserObj(user.id),
            'requests': reqs,
        })


def applyActivity(user_id, activity_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return "用户不存在，请您先登录"
    try:
        acti = Activity.objects.get(id = activity_id)
    except Activity.DoesNotExist:
        return "该活动不存在"

    if (acti.sex_requirement != 'unlimit') and (acti.sex_requirement != user.sex):
        return "您的性别不符合该活动要求"
    if (acti.min_age > user.age) or (acti.max_age < user.age):
        return "您的年龄不符合该活动要求"
    if (acti.current_size >= acti.max_size):
        return "该活动人数已满"

    req = Request(
        type = "activity_application",
        title = user.nickname + "的活动参加申请",
        content = "账号" + user.account + "想参加活动 '" + acti.name + "'",
        poster = user,
        receiver = acti.organizer,
        status = "unread",
        time = datetime.datetime.now(),
        goal = acti.id,
    )
    req.save()
    return "success"

def add_activity(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    if (request.method == 'POST'):
        #return HttpResponse(request.POST['sex_requirement'])
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
                'user': getUserObj(user.id),
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
            'user': getUserObj(user.id),
        }, context_instance = RequestContext(request))

def all_activities(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
            else:
                alerts.append("请求已发送")

    acts = []
    for act in Activity.objects.all().order_by("-post_time"):
        if (act in user.activity_member.all())or(act.organizer == user):
            status = "already_in"
        else:
            if (act.applyend_time.replace(tzinfo=None) <= datetime.datetime.now()):
                status = "expired"
            else:
                status = "available"
        acts.append({
            "id": act.id,
            "name": act.name,
            "place": act.place,
            "start_time": act.start_time,
            "explanation": act.explanation,
            "status": status,
        })

    return render_to_response("all_activities.html", {
        'user': getUserObj(user.id),
        "activities": acts,
        "alerts": alerts,
    }, context_instance = RequestContext(request))

def my_activities_attend(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)

    acts = []
    for act in user.activity_member.all().order_by("-post_time"):
        if (act in user.activity_member.all())or(act.organizer == user):
            status = "already_in"
        else:
            if (act.applyend_time.replace(tzinfo=None) <= datetime.datetime.now()):
                status = "expired"
            else:
                status = "available"
        acts.append({
            "id": act.id,
            "name": act.name,
            "place": act.place,
            "start_time": act.start_time,
            "explanation": act.explanation,
            "status": status,
        })

    return render_to_response("my_activities_attend.html", {
        'user': getUserObj(user.id),
        "my_attend_activities": acts,
        "alerts": alerts,
    })

def my_activities_launch(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)

    acts = []
    for act in user.activity_organizer.all().order_by("-post_time"):
        if (act in user.activity_member.all())or(act.organizer == user):
            status = "already_in"
        else:
            if (act.applyend_time.replace(tzinfo=None) <= datetime.datetime.now()):
                status = "expired"
            else:
                status = "available"
        acts.append({
            "id": act.id,
            "name": act.name,
            "place": act.place,
            "start_time": act.start_time,
            "explanation": act.explanation,
            "status": status,
        })

    return render_to_response("my_activities_launch.html", {
        'user': getUserObj(user.id),
        "my_launch_activities": acts,
        "alerts": alerts,
    })

def friend_activities_attend(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    acts = []
    for friend in user.friends.all():
        for act in friend.activity_member.all():
            if (act in user.activity_member.all())or(act.organizer == user):
                status = "already_in"
            else:
                if (act.applyend_time.replace(tzinfo=None) <= datetime.datetime.now()):
                    status = "expired"
                else:
                    status = "available"
            acts.append({
                "id": act.id,
                "name": act.name,
                "place": act.place,
                "start_time": act.start_time,
                "explanation": act.explanation,
                "status": status,
                "post_time": act.post_time.replace(tzinfo=None),
            })

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)


    return render_to_response("friend_activities_attend.html", {
        'user': getUserObj(user.id),
        "friend_attend_activities": acts,
        "alerts": alerts,
    })

def friend_activities_launch(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    acts = []
    for friend in user.friends.all():
        for act in friend.activity_organizer.all():
            if not act in acts:
                if (act in user.activity_member.all())or(act.organizer == user):
                    status = "already_in"
                else:
                    if (act.applyend_time.replace(tzinfo=None) <= datetime.datetime.now()):
                        status = "expired"
                    else:
                        status = "available"
                acts.append({
                    "id": act.id,
                    "name": act.name,
                    "place": act.place,
                    "start_time": act.start_time,
                    "explanation": act.explanation,
                    "status": status,
                })

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)

    return render_to_response("friend_activities_launch.html", {
        'user': getUserObj(user.id),
        "friend_launch_activities": acts,
        "alerts": alerts,
    })

def activity_detail(request, act_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        act_id = int(act_id)
    except ValueError:
        raise Http404()
    try:
        act = Activity.objects.get(id = act_id)
    except Activity.DoesNotExist:
        raise Http404()

    return render_to_response("activity_detail.html", {
        "user": getUserObj(user.id),
        "organizer": True if (act.organizer == user) else False,
        "activity": act,
        "friends": user.friends.all(),
    })

def activity_attendance(request, act_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        act_id = int(act_id)
    except ValueError:
        raise Http404()
    try:
        act = Activity.objects.get(id = act_id)
    except Activity.DoesNotExist:
        raise Http404()

    alerts = []
    if (request.method == 'POST'):
        if (request.POST["form_type"] == "cancel_attendance"):
            try:
                tar = User.objects.get(id = request.POST['attendance_id'])
            except User.DoesNotExist:
                alerts.append('该用户不存在')
            if (not alerts):
                if (not tar in act.members.all()):
                    alerts.append('该用户未参加此活动')
                else:
                    act.members.remove(tar)
                    act.current_size -= 1
                    act.save()
                    alerts.append('用户 ' + tar.nickname + ' 已从活动中移除')

    return render_to_response("activity_attendance.html", {
        "user": getUserObj(user.id),
        "organizer": True if (act.organizer == user) else False,
        "activity": act,
        "attendances": act.members.all(),
        "friends": user.friends.all(),
        "alerts": alerts,
    })




def add_group(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    errors = {}
    responses = {}
    if (request.method == 'POST'):
        #return HttpResponse("Jiang: " + request.POST["add_friend_to_group_3"] + " Ligen: " + request.POST["add_friend_to_group_4"])
        if (not 'name' in request.POST) or (not request.POST['name']):
            errors['name'] = '请输入群组名称'
        elif (len(request.POST['name']) > 20):
            errors['name'] = '群组名称应不大于20'
        if (not 'explanation' in request.POST) or (not request.POST['explanation']):
            errors['explanation'] = '请输入群组说明'
        elif (len(request.POST['explanation']) > 400):
            errors['explanation'] = '群组说明应不大于400字'
        if (not errors):
            group = Group(
                name = request.POST['name'],
                owner = user,
                explanation = request.POST['explanation'],
                found_time = datetime.datetime.now(),
                current_size = 0,
                max_size = 100,
            )
            group.save()
            for friend in user.friends.all():
                if (("add_friend_to_group_" + str(friend.id)) in request.POST):
                    req = Request(
                        type = "group_invitation",
                        title = user.nickname + " 邀请您参加群组",
                        content = "账号 " + user.account + " 刚刚创建了群组'" + group.name + "', 并邀请你加入",
                        poster = user,
                        receiver = friend,
                        status = "unread",
                        goal = str(group.id),
                        time = datetime.datetime.now(),
                    )
                    req.save()

    return render_to_response('add_group.html',{
        'user': getUserObj(user.id),
        'responses': responses,
        'errors': errors,
        'friends': user.friends.all(),
    })

#def add_group_activity(request, group_id):


def my_groups_create(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    grps = []
    for grp in user.group_owner.all():
        grps.append({
            "id": grp.id,
            "name": grp.name,
            "explanation": grp.explanation,
            "owner": grp.owner.nickname,
            "attend": True if (user in grp.members.all())or(user == grp.owner) else False,
        })

    return render_to_response("my_groups_create.html", {
        'user': getUserObj(user.id),
        "my_create_groups": grps,
    })

def my_groups_attend(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    grps = []
    for grp in user.group_member.all():
        grps.append({
            "id": grp.id,
            "name": grp.name,
            "explanation": grp.explanation,
            "owner": grp.owner.nickname,
            "attend": True if (user in grp.members.all())or(user == grp.owner) else False,
        })

    return render_to_response("my_groups_attend.html", {
        'user': getUserObj(user.id),
        "my_attend_groups": grps,
    })

def all_groups(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    grps = []
    for grp in Group.objects.all():
        grps.append({
            "id": grp.id,
            "name": grp.name,
            "explanation": grp.explanation,
            "owner": grp.owner.nickname,
            "attend": True if (user in grp.members.all())or(user == grp.owner) else False,
        })

    return render_to_response("all_groups.html", {
        "user": getUserObj(user.id),
        "groups" : grps,
    })

def group_info(request, group_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        group_id = int(group_id)
    except ValueError:
        raise Http404()
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise Http404()

    return render_to_response('group_info.html',{
        'user': getUserObj(user.id),
        'group': group,
    })

def group_members(request, group_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        group_id = int(group_id)
    except ValueError:
        raise Http404()
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise Http404()

    alerts = []
    if (request.method == 'POST'):
        if (request.POST["form_type"] == "cancel_member"):
            try:
                tar = User.objects.get(id = request.POST['member_id'])
            except User.DoesNotExist:
                alerts.append('该用户不存在')
            if (not alerts):
                if (not tar in group.members.all()):
                    alerts.append('该用户未参加此群组')
                else:
                    group.members.remove(tar)
                    group.current_size -= 1
                    group.save()
                    alerts.append('用户 ' + tar.nickname + ' 已从群组中移除')


    return render_to_response('group_members.html',{
        'user': getUserObj(user.id),
        'group': group,
        'owner': True if (user == group.owner) else False,
        'groupmembers': group.members.all(),
        'alerts': alerts,
    })

def group_activities(request, group_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        group_id = int(group_id)
    except ValueError:
        raise Http404()
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise Http404()

    return render_to_response('group_activities.html',{
        'user': getUserObj(user.id),
        'group': group,
        'groupactivities': group.activities.all(),
    })



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
    return render_to_response('upload_headimg.html',{
        'uf': uf,
    })



def my_friends(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    errors = {}
    responses = {}
    alerts = []
    current_talker = user.friends.all().order_by("nickname")[0].id
    if (request.method == "POST"):
        if (request.POST['form_type'] == 'add_friend'):
            if (not 'account' in request.POST) or (not request.POST['account']):
                errors['search_friend'] = "请输入搜索账号"
            elif (len(request.POST['account']) > 30):
                errors['search_friend'] = "账号不存在"
            if (not errors):
                try:
                    tar = User.objects.get(account = request.POST['account'])
                    req = Request(
                        type = "friend_application",
                        title = "来自 " + user.nickname + " 的好友请求",
                        content = "账号 " + user.account + " 想加你为好友",
                        poster = user,
                        receiver = tar,
                        status = "unread",
                        goal = tar.id,
                        time = datetime.datetime.now(),
                    )
                    req.save()
                    responses['search_friend'] = "请求已发送"
                except User.DoesNotExist:
                    errors['search_friend'] = "账号不存在"
        if (request.POST['form_type'] == 'change_talker'):
            return HttpResponse(request.POST['click_friend_id'])
        if (request.POST['form_type'] == 'search_talker'):
            #return HttpResponse(request.POST['search_word'])
            #try:
            frds = user.friends.all().filter(nickname__contains = request.POST['search_word'])
            if (not frds):
                alerts.append('未找到该用户')
            else:
                current_talker = frds[0].id

    friends = []
    for frd in user.friends.all().order_by("nickname"):
        friends.append({
            "id": frd.id,
            "nickname": frd.nickname,
            "current_talker": True if (frd.id == current_talker) else False,
        })

    return render_to_response("my_friends.html", {
        'user': getUserObj(user.id),
        "errors": errors,
        "responses": responses,
        "alerts": alerts,
        "friend_list": friends,
    })

