from django import views
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from detect.predict import main
# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        email = request.POST['name']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user is not None:
            request.session['email'] = email
            if user.is_active:
                if user.is_superuser:
                    return redirect("/adminHome")
                else:
                    sf = Users.objects.get(email=email)
                    request.session['id'] = sf.id
                    return redirect("/sfHome")
            else:
                msg = "Account is not Active..."
                return render(request, "login.html", {"msg": msg})
        else:
            msg = "User Dosent Exists..."
            return render(request, "login.html", {"msg": msg})
    else:
        return render(request, "login.html")


def sfReg(request):
    flag = 0
    msg = ""
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        img = request.FILES["file"]

        if User.objects.filter(username=email).exists():
            msg = "Email already exists..."

        else:
            user = User.objects.create_user(
                username=email, password=password, is_active=1)
            user.save()
            sf = Users.objects.create(
                name=name, email=email, phone=phone, address=address, document=img, user=user)
            sf.save()
            msg = "Registration Successful..."
            flag = 1

    return render(request, "sfReg.html", {"msg": msg, "flag": flag})


def adminHome(request):
    return render(request, "adminHome.html")


def adminStartUp(request):
    data = Users.objects.filter(user__is_active=0)
    dataActive = Users.objects.filter(user__is_active=1)
    return render(request, "adminStartup.html", {"data": data, "dataActive": dataActive})


def approveStartUp(request):
    id = request.GET['id']
    status = request.GET['status']
    sf = User.objects.get(id=id)
    sf.is_active = status
    sf.save()
    return redirect("/adminStartUp")


def adminViewFeedback(request):

    data = Feedback.objects.all()
    return render(request, "adminViewFeedback.html", {"data": data})


def adminViewDetections(request):

    data = Detection.objects.all().order_by("-id")
    if request.POST:
        search = request.POST.get("search")
        data = Detection.objects.filter(Q(post__idea__contains=search) | Q(post__desc__contains=search) | Q(post__tags__desc__contains=search) | Q(post__tags__name__contains=search) | Q(results=search.capitalize())).order_by("-id")

    return render(request, "adminViewDetections.html", {"data": data})

def adminTags(request):
    msg = ''
    if request.POST:
        tag = request.POST['tag']
        desc = request.POST['desc']
        ta = Tags.objects.create(name=tag,desc=desc)
        ta.save()
        msg = "Tag created"
    data = Tags.objects.all()
    return render(request, "adminTags.html", {"msg":msg, "data":data})

def adminDeleteTag(request):
    id = request.GET['id']
    data = Tags.objects.get(id=id)
    data.delete()
    return redirect("/adminTags")

def sfHome(request):
    id = request.session['id']

    data = Users.objects.get(id=id)
    post = Post.objects.exclude(user=id)
    if request.method == "POST":
        search = request.POST['search']
        post = Post.objects.filter(Q(idea__contains=search) | Q(desc__contains=search) | Q(tags__name__contains=search) | Q(tags__desc__contains=search)).exclude(user=id)
    return render(request, "sfHome.html", {"data": data, "post": post})

def sfViewPost(request):
    id = request.session['id']
    tag = request.GET['id']
    cat = request.GET['cat']
    data = Users.objects.get(id=id)
    det = []
    if cat == 'po':
        dets = Detection.objects.filter(post__tags__id=tag, results='Positive')
    elif cat == 'ne':
        dets = Detection.objects.filter(post__tags__id=tag, results='Negative')
    elif cat == 'nu':
        dets = Detection.objects.filter(post__tags__id=tag, results='Neutral')
    else:
        dets = Detection.objects.filter(post__tags__id=tag)
    
    print(dets)

    for d in dets:
        det.append(d.post.id)

    print(det)
    post = Post.objects.filter(id__in=det).exclude(user=id,)
    if request.method == "POST":
        search = request.POST['search']
        post = Post.objects.filter(Q(Q(idea__contains=search) | Q(desc__contains=search)) & Q(id__in=det)).exclude(user=id)
    return render(request, "sfHome.html", {"data": data, "post": post})


def sfProfile(request):
    id = request.session['id']

    data = Users.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        proUp = Users.objects.get(id=id)
        proUp.name = name
        proUp.email = email
        proUp.phone = phone
        proUp.address = address
        proUp.save()
        logUp = User.objects.get(username=data.user)
        logUp.set_password(password)
        logUp.username = email
        logUp.save()
        return redirect("/sfHome")
    return render(request, "sfProfile.html", {"data": data})


def sfChangeImage(request):
    id = request.session['id']
    data = Users.objects.get(id=id)
    if request.method == "POST":
        img = request.FILES["file"]

        data.document = img
        data.save()
        return redirect("/sfHome")
    return render(request, "sfChangeImage.html", {"data": data})


def sfPost(request):
    id = request.session['id']
    user = Users.objects.get(id=id)
    msg = ''
    if request.method == "POST":
        idea = request.POST['idea']
        description = request.POST['description']
        image = request.FILES['image']
        tag = request.POST['tag']
        ta = Tags.objects.get(id=tag)

        sid = SentimentIntensityAnalyzer()
        scores1 = sid.polarity_scores(idea)
        scores2 = sid.polarity_scores(description)

        db = Post.objects.create(idea=idea, desc=description, user=user,image=image,tags=ta)
        db.save()

        det = Detection.objects.create(
            user=user, post=db,scoreTitle=scores1['compound'],scoreDesc=scores2['compound'])
        det.save()

        total = ta.totalCount
        po = ta.poCount
        ne = ta.neCount
        nu = ta.nuCount
        res = main(description)

        print(f"Score 1: {scores1["compound"]}, Score 2: {scores2["compound"]}, Res: {res}")

        if scores1['compound'] > 0 and scores2['compound'] >= 0.05 and res == 'Positive':
            ta.totalCount += 1
            ta.poCount += 1
            det.results = "Positive"
        elif scores1['compound'] < 0 and scores2['compound'] <= -0.05 and res == 'Negative':
            ta.totalCount += 1
            ta.neCount += 1
            det.results = "Negative"
        else:
            ta.totalCount += 1
            ta.nuCount += 1
            det.results = "Neutral"
        det.save()
        ta.save()
    data = Tags.objects.all()
    return render(request, "sfPost.html", {"msg": msg, "data":data})



def sfViewSelfPost(request):
    id = request.session['id']

    data = Post.objects.filter(user=id)
    return render(request, "sfViewSelfPost.html", {"data": data})


def sfUpdateIdea(request):
    id = request.GET['id']
    data = Post.objects.get(id=id)
    if request.method == "POST":
        idea = request.POST['idea']
        description = request.POST['description']
        data.idea = idea
        data.desc = description
        data.save()
        return redirect("/sfViewSelfPost")
    return render(request, "sfUpdateIdea.html", {"data": data})


def sfDeleteIdea(request):
    id = request.GET['id']
    data = Post.objects.get(id=id)
    data.delete()

    return redirect("/sfViewSelfPost")


def sfViewIdea(request):
    id = request.GET['post']
    sfid = request.session['id']

    data = Post.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST['comment']

        user = Users.objects.get(id=sfid)
        db = Comments.objects.create(comment=comment, idea=data, user=user)
        db.save()

    comments = Comments.objects.filter(idea=id)
    return render(request, "sfViewIdea.html", {"data": data, "comments": comments})


def sfViewSf(request):
    id = request.GET['sfid']
    user = Users.objects.get(id=id)

    post = Post.objects.filter(user=id)
    return render(request, "sfViewSf.html", {"user": user, "post": post})


def sfAddFeedBack(request):
    id = request.session['id']
    if request.method == "POST":
        feedback = request.POST['feedback']
        user = Users.objects.get(id=id)

        db = Feedback.objects.create(feedback=feedback, user=user)
        db.save()
    data = Feedback.objects.filter(user=id)
    return render(request, "sfAddFeedBack.html", {"data": data})


def sfChat(request):
    sender = request.session["email"]
    data = Chat.objects.filter(
        Q(sender=sender) | Q(receiver=sender)).distinct()
    print(data)
    newData = set()
    for d in data:
        newData.add(d.sender)
        newData.add(d.receiver)
    return render(request, "sfChat.html", {"data": newData, "user": sender})


def sfChatPer(request):
    sender = request.session['email']
    receiver = request.GET['email']
    if request.method == "POST":
        msg = request.POST['msg']
        db = Chat.objects.create(sender=sender, receiver=receiver, message=msg)
        db.save()
    messages = Chat.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
    return render(request, "sfChatPer.html", {"messages": messages, "user": sender})
