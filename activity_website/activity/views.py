from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect, Http404
from activity.models import *
from django.template import RequestContext
import re, datetime
from django import forms

# Create your views here.

class ImageForm(forms.Form):
    #username = forms.CharField()
    image = forms.FileField()

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
                errors['password'] = '密码错误'
                return render_to_response("login_form.html", {
                    'user': getUserObj(user.id),
                    'errors': errors,
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
        if (not 'password2' in request.POST) or (not request.POST['password2']):
            errors['password2'] = '请再次输入密码'
        elif (not request.POST['password1'] == request.POST['password2']):
            errors['password2'] = '两次密码输入不一致'
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
            password = request.POST.get('password1', ''),
            nickname = request.POST.get('nickname', ''),
            sex = request.POST.get('sex', ''), #male/female
            age = int(request.POST.get('age', '')),
            email = request.POST.get('email', ''),
            phone = request.POST.get('phone', ''),
            interest = request.POST.get('interest', ''),
        )
        user.save()
        request.session['user_id'] = user.id
        return HttpResponseRedirect('/register_success/')
    else:
        return render_to_response("register.html", {
        }, context_instance = RequestContext(request))

def register_success(request):
    return render_to_response("register_success.html")

def welcome(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    return HttpResponseRedirect("/all_activities/")

    #return HttpResponse(getUserObj(user.id)["nickname"])
    #return render_to_response("welcome.html", {
    #    'user': getUserObj(user.id),
    #}, context_instance = RequestContext(request))

def change_userinfo(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    errors = {}
    alerts = []
    if (request.method == "POST"):
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

        uf = ImageForm(request.POST, request.FILES)
        #return HttpResponse(uf.cleaned_data['image'])

        if (not errors):
            user.nickname = request.POST.get('nickname')
            user.age = int(request.POST.get('age'))
            #user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.sex = request.POST.get('sex')
            user.interest = request.POST.get('interest')
            if (uf.is_valid()):
                user.headImg = uf.cleaned_data['image']
                alerts.append('头像修改成功')
            user.save()
            alerts.append('修改成功')

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
        'errors': errors,
        'alerts': alerts,
    }, context_instance = RequestContext(request))

def change_userpwd(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    errors = {}
    alerts = []
    if (request.method == 'POST'):
        old_password = ''
        new_password = ''
        if ('old_password' in request.POST) and (request.POST['old_password']):
            old_password = request.POST['old_password']
        else:
            errors['old_password'] = '请输入旧密码'
        if (not 'new_password1' in request.POST) or (not request.POST['new_password1']):
            errors['new_password1'] = '请输入新密码'
        if (not 'new_password2' in request.POST) or (not request.POST['new_password2']):
            errors['new_password2'] = '请再次输入新密码'
        if (not 'new_password1' in errors) and (not 'new_password2' in errors):
            if (request.POST['new_password1'] == request.POST['new_password2']):
                new_password = request.POST['new_password1']
            else:
                errors['new_password2'] = '两次输入密码不一致'

        if (not errors):
            if (old_password == user.password):
                User.objects.filter(id = user.id).update(password = new_password)
            else:
                errors['old_password'] = '旧密码错误'
        if (errors):
            return render_to_response("change_userpwd_form.html", {
                'user': getUserObj(user.id),
                'errors': errors
            }, context_instance = RequestContext(request))
        else:
            alerts.append('密码修改成功')
    else:
        return render_to_response("change_userpwd_form.html", {
            'user': getUserObj(user.id),
            'errors': errors,
            'alerts': alerts,
        }, context_instance = RequestContext(request))

def user_info(request, user_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        user_id = int(user_id)
    except ValueError:
        raise Http404()
    try:
        tar = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404()

    alerts = []
    if (request.method == "POST"):
        if (request.POST['form_type'] == 'add_friend'):
            if (tar == user):
                alerts.append("这是您自己的账号")
            else:
                if (tar in user.friends.all()):
                    alerts.append("你们已经是好友关系了")
                else:
                    req = Request(
                        type = "friend_application",
                        title = "来自 " + user.nickname + " 的好友请求",
                        content = "账号 " + user.account + " 想加你为好友",
                        poster = user,
                        receiver = tar,
                        status = "unread",
                        goal = tar.id,
                        target = user.nickname,
                        time = datetime.datetime.now(),
                    )
                    req.save()
                    alerts.append("请求已发送")


    return render_to_response("user_info.html", {
        "user": getUserObj(user.id),
        "tar": tar,
        "alerts": alerts,
    })

def user_activities(request, user_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        user_id = int(user_id)
    except ValueError:
        raise Http404()
    try:
        tar = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404()

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
            else:
                alerts.append("请求已发送")

    acts = []
    for act in tar.activity_organizer.all().order_by("-post_time"):
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

    return render_to_response("user_activities.html", {
        "user": getUserObj(user.id),
        "tar": tar,
        "useractivities": acts,
        "alerts": alerts,
    })

def user_friends(request, user_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        user_id = int(user_id)
    except ValueError:
        raise Http404()
    try:
        tar = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404()

    return render_to_response("user_friends.html", {
        "user": getUserObj(user.id),
        "tar": tar,
        "userfriends": tar.friends.all(),
    })

def user_groups(request, user_id):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    try:
        user_id = int(user_id)
    except ValueError:
        raise Http404()
    try:
        tar = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404()

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_group'):
            alerts.append(applyGroup(user.id, request.POST['group_id']))

    grps = []
    for grp in tar.group_member.all():
        grps.append({
            "id": grp.id,
            "name": grp.name,
            "owner": grp.owner.nickname,
            "explanation": grp.explanation,
            "attend": True if (user in grp.members.all())or(user == grp.owner) else False,
        })
    for grp in tar.group_owner.all():
        grps.append({
            "id": grp.id,
            "name": grp.name,
            "owner": grp.owner.nickname,
            "explanation": grp.explanation,
            "attend": True if (user in grp.members.all())or(user == grp.owner) else False,
        })

    return render_to_response("user_groups.html", {
        "user": getUserObj(user.id),
        "tar": tar,
        "usergroups": grps,
    })



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
                        target = " ",
                        time = datetime.datetime.now(),
                    )
                    tmp_req.save()
                if (req.type == 'activity_invitation'):
                    act = Activity.objects.get(id = req.goal)
                    #if (act.add_member(req.poster) == 'success'):
                    act.members.add(user)
                    act.current_size += 1
                    act.save()
                    tmp_req = Request(
                        type = "notice",
                        title = "提醒",
                        content = "账号 " + user.account + " 接受了你的邀请, 参加了活动'" + act.name + "'",
                        poster = req.receiver,
                        receiver = req.poster,
                        status = "unread",
                        goal = " ",
                        target = " ",
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
                        target = " ",
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
                        target = " ",
                        time = datetime.datetime.now(),
                    )
                    tmp_req.save()
                if (req.type == "group_application"):
                    grp = Group.objects.get(id = req.goal)
                    grp.members.add(req.poster)
                    grp.current_size += 1
                    grp.save()
                    tmp_req = Request(
                        type = "notice",
                        title = user.nickname + " 接受了你的请求",
                        content = "账号 " + user.account + " 接受了你的加群请求, 你已加入群组'" + grp.name + "'",
                        poster = req.receiver,
                        receiver = req.poster,
                        status = "unread",
                        goal = " ",
                        target = " ",
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
        target = acti.name,
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
        if (not 'min_age' in errors) and(not 'max_age' in errors) and (int(request.POST['min_age']) > int(request.POST['max_age'])):
            errors['max_age'] = '最大年龄应不小于最小年龄'
        if (not 'max_size' in request.POST) or (not request.POST['max_size']):
            errors['max_size'] = '请输入最大参与人数'
        elif (not isSize(request.POST['max_size'], 1000)):
            errors['max_size'] = '最大参与人数应为不大于1000的正整数'
        if (not 'applyend_date' in request.POST) or (not request.POST['applyend_date']) or (not 'applyend_time' in request.POST) or (not request.POST['applyend_time']):
            errors['applyend_time'] = '请输入报名截止时间'
        if (not 'start_date' in request.POST) or (not request.POST['start_date']) or (not 'start_time' in request.POST) or (not request.POST['start_time']):
            errors['start_time'] = '请输入活动开始时间'
        if (not 'end_date' in request.POST) or (not request.POST['end_date']) or (not 'end_time' in request.POST) or (not request.POST['end_time']):
            errors['end_time'] = '请输入活动结束时间'

        if (not 'applyend_time' in errors) and (not 'start_time' in errors) and (not 'end_time' in errors):
            applyend_time = datetime.datetime.strptime(request.POST['applyend_date'] + ' ' + request.POST['applyend_time'], '%Y/%m/%d %H:%M')
            start_time = datetime.datetime.strptime(request.POST['start_date'] + ' ' + request.POST['start_time'], '%Y/%m/%d %H:%M')
            end_time = datetime.datetime.strptime(request.POST['end_date'] + ' ' + request.POST['end_time'], '%Y/%m/%d %H:%M')
            if (applyend_time > start_time):
                errors['applyend_time'] = '报名结束时间应早于活动开始时间'
            if (start_time > end_time):
                errors['start_time'] = '活动开始时间应早于结束时间'

        if (errors):
            return render_to_response("add_activity.html", {
                'user': getUserObj(user.id),
                'errors': errors,
                'friends': user.friends.all(),
                'name': request.POST.get('name'),
                'start_date': request.POST.get('start_date'),
                'start_time': request.POST.get('start_time'),
                'end_date': request.POST.get('end_date'),
                'end_time': request.POST.get('end_time'),
                'applyend_date': request.POST.get('applyend_date'),
                'applyend_time': request.POST.get('applyend_time'),
                'place': request.POST.get('place'),
                'explanation': request.POST.get('explanation'),
                'min_age': request.POST.get('min_age'),
                'max_age': request.POST.get('max_age'),
                'max_size': request.POST.get('max_size'),
            }, context_instance = RequestContext(request))
        else:
            act = Activity(
                type = request.POST['type'],
                name = request.POST['name'],
                explanation = request.POST['explanation'],
                organizer = User.objects.get(id = request.session['user_id']),
                post_time = datetime.datetime.now(),
                applyend_time = applyend_time,
                start_time = start_time,
                end_time = end_time,
                place = request.POST['place'],
                min_age = int(request.POST['min_age']),
                max_age = int(request.POST['max_age']),
                sex_requirement = request.POST['sex_requirement'],
                status = 'Null',
                max_size = int(request.POST['max_size']),
                current_size = 0,
            )
            uf = ImageForm(request.POST, request.FILES)
            if (uf.is_valid()):
                act.picture = uf.cleaned_data['image']
            act.save()
            for friend in user.friends.all():
                if (("add_friend_to_activity_" + str(friend.id)) in request.POST):
                    req = Request(
                        type = "activity_invitation",
                        title = user.nickname + " 邀请您参加活动",
                        content = "账号 " + user.account + " 刚刚发起了活动'" + act.name + "', 并邀请你参加",
                        poster = user,
                        receiver = friend,
                        status = "unread",
                        goal = str(act.id),
                        target = act.name,
                        time = datetime.datetime.now(),
                    )
                    req.save()
            return HttpResponseRedirect("/activity_detail/" + str(act.id) + "/")
    else:
        return render_to_response("add_activity.html", {
            'user': getUserObj(user.id),
            'friends': user.friends.all(),
        }, context_instance = RequestContext(request))

def all_activities(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    alerts = []
    all_acts = Activity.objects.all().order_by("-post_time")
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
            else:
                alerts.append("请求已发送")
        if (request.POST['form_type'] == 'search_activity'):
            all_acts = all_acts.filter(name__contains = request.POST['search_word'])

    acts = []
    for act in all_acts:
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
            "picture": act.picture,
        })

    return render_to_response("all_activities_new.html", {
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
    all_acts = user.activity_member.all().order_by("-post_time")
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
        if (request.POST['form_type'] == 'search_activity'):
            all_acts = all_acts.filter(name__contains = request.POST['search_word'])

    acts = []
    for act in all_acts:
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
    all_acts = user.activity_organizer.all().order_by("-post_time")
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
        if (request.POST['form_type'] == 'search_activity'):
            all_acts = all_acts.filter(name__contains = request.POST['search_word'])

    acts = []
    for act in all_acts:
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
    actss = []
    for friend in user.friends.all():
        for act in friend.activity_member.all():
            if (not act in actss):
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
                actss.append(act)

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
            else:
                alerts.append("请求已发送")
        if (request.POST['form_type'] == 'search_activity'):
                acts = []
                actss = []
                for friend in user.friends.all():
                    for act in friend.activity_member.all().filter(name__contains = request.POST['search_word']):
                        if (not act in actss):
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
                            actss.append(act)


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
            else:
                alerts.append("请求已发送")
        if (request.POST['form_type'] == 'search_activity'):
            acts = []
            for friend in user.friends.all():
                for act in friend.activity_organizer.all().filter(name__contains = request.POST['search_word']):
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

    return render_to_response("friend_activities_launch.html", {
        'user': getUserObj(user.id),
        "friend_launch_activities": acts,
        "alerts": alerts,
    })

def my_group_activities(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    acts = []
    for group in user.group_member.all():
        for act in group.activities.all():
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
                    "group": group.name,
                })
    for group in user.group_owner.all():
        for act in group.activities.all():
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
                    "group": group.name,
                })

    alerts = []
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_activity'):
            response = applyActivity(user.id, request.POST['activity_id'])
            if (response != 'success'):
                alerts.append(response)
        if (request.POST['form_type'] == 'search_activity'):
            acts = []
            for group in user.group_member.all():
                for act in group.activities.all().filter(name__contains = request.POST['search_word']):
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
                            "group": group.name,
                        })
            for group in user.group_owner.all():
                for act in group.activities.all().filter(name__contains = request.POST['search_word']):
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
                            "group": group.name,
                        })

    return render_to_response("my_group_activities.html", {
        'user': getUserObj(user.id),
        "groupactivities": acts,
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

    alerts = []
    if (request.method == "POST"):
        if (request.POST['form_type'] == 'add_friend_to_activity'):
            for friend in user.friends.all():
                if (("add_friend_to_activity_" + str(friend.id)) in request.POST) and (not friend in act.members.all()):
                    req = Request(
                        type = "activity_invitation",
                        title = user.nickname + " 邀请您参加活动",
                        content = "账号 " + user.account + " 邀请你参加活动'" + act.name + "'",
                        poster = user,
                        receiver = friend,
                        status = "unread",
                        goal = str(act.id),
                        target = act.name,
                        time = datetime.datetime.now(),
                    )
                    req.save()
            alerts.append('请求已发送')
        if (request.POST['form_type'] == 'new_comment'):
            comm = Comment(
                poster = user,
                act = act,
                content = request.POST['content'],
                time = datetime.datetime.now(),
            )
            comm.save()
            alerts.append('评论成功')

    return render_to_response("activity_detail.html", {
        "user": getUserObj(user.id),
        "organizer": True if (act.organizer == user) else False,
        "activity": act,
        "friends": user.friends.all(),
        'alerts': alerts,
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
                    req = Request(
                        type = "notice",
                        title = "提醒",
                        content = "你已被从活动'" + act.name + "'中移除",
                        poster = user,
                        receiver = tar,
                        status = "unread",
                        goal = " ",
                        target = " ",
                        time = datetime.datetime.now(),
                    )
                    req.save()

    return render_to_response("activity_attendance.html", {
        "user": getUserObj(user.id),
        "organizer": True if (act.organizer == user) else False,
        "activity": act,
        "attendances": act.members.all(),
        "friends": user.friends.all(),
        "alerts": alerts,
    })



def applyGroup(user_id, group_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return "用户不存在，请您先登录"
    try:
        group = Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        return "该群组不存在"

    if (group.current_size >= group.max_size):
        return "该活动人数已满"

    req = Request(
        type = "group_application",
        title = user.nickname + "的加群申请",
        content = "账号" + user.account + "想加入群组 '" + group.name + "'",
        poster = user,
        receiver = group.owner,
        status = "unread",
        time = datetime.datetime.now(),
        goal = group.id,
        target = group.name,
    )
    req.save()
    return "请求已发送"

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
                        goal = group.id,
                        target = group.name,
                        time = datetime.datetime.now(),
                    )
                    req.save()
            return HttpResponseRedirect('/group_info/' + str(group.id) + '/')

    return render_to_response('add_group.html',{
        'user': getUserObj(user.id),
        'responses': responses,
        'errors': errors,
        'friends': user.friends.all(),
    })

def add_group_activity(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    errors = {}
    alerts = []

    group = Group.objects.get(id = request.POST['group_id'])
    if (request.POST['form_type'] == 'add'):
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
        if (not 'min_age' in errors) and(not 'max_age' in errors) and (int(request.POST['min_age']) > int(request.POST['max_age'])):
            errors['max_age'] = '最大年龄应不小于最小年龄'
        if (not 'max_size' in request.POST) or (not request.POST['max_size']):
            errors['max_size'] = '请输入最大参与人数'
        elif (not isSize(request.POST['max_size'], 1000)):
            errors['max_size'] = '最大参与人数应为不大于1000的正整数'
        if (not 'applyend_date' in request.POST) or (not request.POST['applyend_date']) or (not 'applyend_time' in request.POST) or (not request.POST['applyend_time']):
            errors['applyend_time'] = '请输入报名截止时间'
        if (not 'start_date' in request.POST) or (not request.POST['start_date']) or (not 'start_time' in request.POST) or (not request.POST['start_time']):
            errors['start_time'] = '请输入活动开始时间'
        if (not 'end_date' in request.POST) or (not request.POST['end_date']) or (not 'end_time' in request.POST) or (not request.POST['end_time']):
            errors['end_time'] = '请输入活动结束时间'

        if (not 'applyend_time' in errors) and (not 'start_time' in errors) and (not 'end_time' in errors):
            applyend_time = datetime.datetime.strptime(request.POST['applyend_date'] + ' ' + request.POST['applyend_time'], '%Y/%m/%d %H:%M')
            start_time = datetime.datetime.strptime(request.POST['start_date'] + ' ' + request.POST['start_time'], '%Y/%m/%d %H:%M')
            end_time = datetime.datetime.strptime(request.POST['end_date'] + ' ' + request.POST['end_time'], '%Y/%m/%d %H:%M')
            if (applyend_time > start_time):
                errors['applyend_time'] = '报名结束时间应早于活动开始时间'
            if (start_time > end_time):
                errors['start_time'] = '活动开始时间应早于结束时间'

        if (not errors):
            act = Activity(
                type = request.POST['type'],
                name = request.POST['name'],
                explanation = request.POST['explanation'],
                organizer = User.objects.get(id = request.session['user_id']),
                post_time = datetime.datetime.now(),
                applyend_time = applyend_time,
                start_time = start_time,
                end_time = end_time,
                place = request.POST['place'],
                min_age = int(request.POST['min_age']),
                max_age = int(request.POST['max_age']),
                sex_requirement = request.POST['sex_requirement'],
                status = 'Null',
                max_size = int(request.POST['max_size']),
                current_size = 0,
            )
            act.save()
            group.activities.add(act)
            if ("send_invitation_to_members" in request.POST):
                for member in group.members.all():
                    req = Request(
                        type = "activity_invitation",
                        title = user.nickname + " 邀请您参加活动",
                        content = "账号 " + user.account + " 刚刚发起了活动'" + act.name + "', 并邀请你参加",
                        poster = user,
                        receiver = member,
                        status = "unread",
                        goal = str(act.id),
                        target = act.name,
                        time = datetime.datetime.now(),
                    )
                    req.save()
            alerts.append("群组活动创建成功")
            return HttpResponseRedirect("/activity_detail/" + str(act.id) + "/")
        else:
            return render_to_response("add_group_activity.html", {
                "group": group,
                "user": getUserObj(user.id),
                "errors": errors,
                "alerts": alerts,
                'name': request.POST.get('name'),
                'start_date': request.POST.get('start_date'),
                'start_time': request.POST.get('start_time'),
                'end_date': request.POST.get('end_date'),
                'end_time': request.POST.get('end_time'),
                'applyend_date': request.POST.get('applyend_date'),
                'applyend_time': request.POST.get('applyend_time'),
                'place': request.POST.get('place'),
                'explanation': request.POST.get('explanation'),
                'min_age': request.POST.get('min_age'),
                'max_age': request.POST.get('max_age'),
                'max_size': request.POST.get('max_size'),
            })

    return render_to_response("add_group_activity.html", {
        "group": group,
        "user": getUserObj(user.id),
        "errors": errors,
        "alerts": alerts,
    })

def my_groups_create(request):
    if (not 'user_id' in request.session):
        return HttpResponseRedirect("/login/")
    try:
        user = User.objects.get(id = request.session['user_id'])
    except User.DoesNotExist:
        return HttpResponseRedirect("/login/")

    all_grps = user.group_owner.all()
    if (request.method == "POST"):
        if (request.POST['form_type'] == 'search_group'):
            all_grps = all_grps.filter(name__contains = request.POST['search_word'])

    grps = []
    for grp in all_grps:
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

    all_grps = user.group_member.all()
    if (request.method == "POST"):
        if (request.POST['form_type'] == 'search_group'):
            all_grps = all_grps.filter(name__contains = request.POST['search_word'])

    grps = []
    for grp in all_grps:
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

    alerts = []
    all_grps = Group.objects.all()
    if (request.method == 'POST'):
        if (request.POST['form_type'] == 'apply_group'):
            alerts.append(applyGroup(user.id, request.POST['group_id']))
        if (request.POST['form_type'] == 'search_group'):
            all_grps = all_grps.filter(name__contains = request.POST['search_word'])

    grps = []
    for grp in all_grps:
        grps.append({
            "id": grp.id,
            "name": grp.name,
            "explanation": grp.explanation,
            "owner": grp.owner.nickname,
            "attend": True if (user in grp.members.all())or(user == grp.owner) else False,
        })

    return render_to_response("all_groups.html", {
        "user": getUserObj(user.id),
        "groups": grps,
        "alerts": alerts,
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

    alerts = []
    if (request.method == "POST"):
        if (request.POST['form_type'] == 'invite_friend_into_group'):
            for friend in user.friends.all():
                if (("add_friend_to_group_" + str(friend.id)) in request.POST) and (not friend in group.members.all()):
                    req = Request(
                        type = "group_invitation",
                        title = user.nickname + " 邀请您加入群组",
                        content = "账号 " + user.account + " 邀请你加入群组'" + group.name + "'",
                        poster = user,
                        receiver = friend,
                        status = "unread",
                        goal = str(group.id),
                        target = group.name,
                        time = datetime.datetime.now(),
                    )
                    req.save()
            alerts.append('请求已发送')

    return render_to_response('group_info.html',{
        'user': getUserObj(user.id),
        'group': group,
        "organizer": True if (group.owner == user) else False,
        "friends": user.friends.all(),
        "alerts": alerts,
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
                    req = Request(
                        type = "notice",
                        title = "提醒",
                        content = "你已被从群组'" + group.name + "'中移除",
                        poster = user,
                        receiver = tar,
                        status = "unread",
                        goal = " ",
                        target = " ",
                        time = datetime.datetime.now(),
                    )
                    req.save()


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

    acts = []
    for act in group.activities.all().order_by("-post_time"):
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

    return render_to_response('group_activities.html',{
        'user': getUserObj(user.id),
        'group': group,
        'groupactivities': acts,
    })





def upload_headimg(request):
    if request.method == "POST":
        uf = ImageForm(request.POST, request.FILES)
        if (uf.is_valid()):
            user = User.objects.get(id = 1)
            user.headImg = uf.cleaned_data['image']
            user.save()
            return HttpResponse('ok!')
        else:
            return HttpResponse('no')
    else:
        uf = ImageForm()
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
    try:
        current_talker = user.friends.all().order_by("nickname")[0].id
    except:
        current_talker = 0
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
                        goal = user.id,
                        target = user.nickname,
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

