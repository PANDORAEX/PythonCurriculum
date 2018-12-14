from django.shortcuts import render, redirect
from . import models
from login.forms import UserForm, ProjectForm, UrlForm, EmotionForm
import re
import datetime
from sequences import get_next_value
from django import forms
from sequences.models import Sequence
import requests

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            if len(username) < 8:
                message = "ユーザ名は8桁で入力してください。"
            elif not isalnum(username):
                message = "ユーザ名は半角英数字で入力してください。"
            else:
                try:
                    user = models.User.objects.get(USERID=username)
                    if user.PASSWORD == password:
                        return render(request, 'index.html')
                    else:
                        message = "ユーザ名またはパスワードに誤りがあります。"
                except Exception:
                    message = "ユーザ名またはパスワードに誤りがあります。"
            login_form = UserForm(initial={'username': username,
                                           'password': password})
        return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())


def add(request):
    if request.method == "POST":
        add_form = ProjectForm(request.POST)
        if add_form.is_valid():
            start_date = add_form.cleaned_data['start_date']
            project_no = add_form.cleaned_data['project_no']
            project_name = add_form.cleaned_data['project_name']
            protype_code = add_form.cleaned_data['protype_code'].PROTYPE_CODE
            language_code = add_form.cleaned_data['language_code'].LANGUAGE_CODE
            summary = add_form.cleaned_data['summary']
            status_code = add_form.cleaned_data['status_code'].STATUS_CODE
            customer = add_form.cleaned_data['customer']
            charge = add_form.cleaned_data['charge']
            reviewer = add_form.cleaned_data['reviewer']
            release_date = add_form.cleaned_data['release_date']
            remarks = add_form.cleaned_data['remarks']
            message_add = ""
            if not isdateformat(start_date):
                message_add = "発生日は yyyy/MM/dd の形式で入力してください。\n"
            elif not isdate(start_date):
                message_add = "発生日は カレンダーに存在しない日付です。\n"
            if protype_code == "":
                message_add = message_add + "工程区分が選択されていません。\n"
            if language_code == "":
                message_add = message_add + "開発言語が選択されていません。\n"
            if status_code == "":
                message_add = message_add + "状態が選択されていません。\n"
            if release_date != "":
                if not isdateformat(release_date):
                        message_add = message_add + "リリース日は yyyy/MM/dd の形式で入力してください。\n"
                elif not isdate(release_date):
                        message_add = message_add + "リリース日はカレンダーに存在しない日付です。\n"
            #try:
                #incident = models.Project.objects.get(PROJECT_ID=9999)
            if Sequence.objects.get(name="festival_classification_seq").last >= 9999:
                message_add = "登録可能な一連番号が無いため、登録を行えません。"
            #except Exception:
                #pass
            if not message_add:
                start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                if release_date != "":
                    release_date = datetime.datetime.strptime(release_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                    models.Project.objects.create(PROJECT_ID=get_next_value('festival_classification_seq'),
                                                  START_DATE=start_date, PROJECT_NO=project_no,
                                                  PROJECT_NAME=project_name, PROTYPE_CODE_id=protype_code,
                                                  LANGUAGE_CODE_id=language_code, SUMMARY=summary,
                                                  STATUS_CODE_id=status_code, CUSTOMER=customer, CHARGE=charge,
                                                  REVIEWER=reviewer, RELEASE_DATE=release_date, REMARKS=remarks)
                    return redirect('/add/')
                else:
                    models.Project.objects.create(PROJECT_ID=get_next_value('festival_classification_seq'),
                                                  START_DATE=start_date, PROJECT_NO=project_no,
                                                  PROJECT_NAME=project_name, PROTYPE_CODE_id=protype_code,
                                                  LANGUAGE_CODE_id=language_code, SUMMARY=summary,
                                                  STATUS_CODE_id=status_code, CUSTOMER=customer, CHARGE=charge,
                                                  REVIEWER=reviewer, REMARKS=remarks)
                    return redirect('/add/')
        return render(request, 'add.html', locals())
    add_form = ProjectForm()
    return render(request, 'add.html', locals())


def list_req(request):
    projects = models.Project.objects.all().order_by('PROJECT_ID')
    message_list = ""
    if projects.count() == 0:
        message_list = "レコードが登録されていません。"
        return render(request, 'list.html', {'message_list': message_list})
    for p in projects:
        p.PROTYPE_CODE_id = models.ProjectType.objects.get(PROTYPE_CODE=p.PROTYPE_CODE_id).PROTYPE_NAME
        p.LANGUAGE_CODE_id = models.Language.objects.get(LANGUAGE_CODE=p.LANGUAGE_CODE_id).LANGUAGE_NAME
        p.STATUS_CODE_id = models.Status.objects.get(STATUS_CODE=p.STATUS_CODE_id).STATUS_NAME
        p.PROJECT_ID = '{:0=4}'.format(p.PROJECT_ID)
        if p.RELEASE_DATE is None:
            p.RELEASE_DATE = ""
    url_form = UrlForm(initial={'now_url': request.path})
    url_form.fields['now_url'].widget = forms.HiddenInput()
    d = {
        'projects': projects,
        'message_list': message_list,
        'url_form': url_form,
    }
    return render(request, 'list.html', d)


def isalnum(s):
    return re.compile(r'^[a-zA-Z0-9]+$').match(s) is not None


def isdateformat(date_text):
    return re.compile(r'^\d{4}/\d{2}/\d{2}$').match(date_text) is not None


def isdate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y/%m/%d')
    except ValueError:
        return False
    return True


def edit(request, project_id):
    if request.method == 'GET':
        url_form = UrlForm(request.GET)
        if url_form.is_valid():
            if url_form.cleaned_data['now_url'] == "":
                return render(request, 'error.html')
        else:
            return render(request, 'error.html')
    project = models.Project.objects.get(PROJECT_ID=project_id)
    message_add = ""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.fields['start_date'].required = False
        form.fields['project_no'].required = False
        form.fields['project_name'].required = False
        form.fields['protype_code'].required = False
        if form.is_valid():
            language_code = form.cleaned_data['language_code'].LANGUAGE_CODE
            summary = form.cleaned_data['summary']
            status_code = form.cleaned_data['status_code'].STATUS_CODE
            customer = form.cleaned_data['customer']
            charge = form.cleaned_data['charge']
            reviewer = form.cleaned_data['reviewer']
            release_date = form.cleaned_data['release_date']
            remarks = form.cleaned_data['remarks']
            if language_code == "":
                message_add = message_add + "開発言語が選択されていません。\n"
            if status_code == "":
                message_add = message_add + "状態が選択されていません。\n"
            if release_date != "":
                if not isdateformat(release_date):
                        message_add = message_add + "リリース日は yyyy/MM/dd の形式で入力してください。\n"
                elif not isdate(release_date):
                        message_add = message_add + "リリース日はカレンダーに存在しない日付です。\n"
            if message_add == "":
                project.LANGUAGE_CODE_id = language_code
                project.SUMMARY = summary
                project.STATUS_CODE_id = status_code
                project.CUSTOMER = customer
                project.CHARGE = charge
                project.REVIEWER = reviewer
                if release_date != "":
                    release_date = datetime.datetime.strptime(release_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                    project.RELEASE_DATE = release_date
                project.REMARKS = remarks
                project.save()
                return redirect('/list/')
            else:
                form = ProjectForm(initial={
                    'project_id': project.PROJECT_ID,
                    'start_date': project.START_DATE.strftime('%Y/%m/%d'),
                    'project_no': project.PROJECT_NO,
                    'project_name': project.PROJECT_NAME,
                    'protype_code': project.PROTYPE_CODE_id,
                    'language_code': language_code,
                    'summary': summary,
                    'status_code': status_code,
                    'customer': customer,
                    'charge': charge,
                    'reviewer': reviewer,
                    'release_date': release_date,
                    'remarks': remarks,
                })
                form.fields['start_date'].disabled = True
                form.fields['project_no'].disabled = True
                form.fields['project_name'].disabled = True
                form.fields['protype_code'].disabled = True
                d = {
                    'project': form,
                    'project_id': project.PROJECT_ID,
                    'message_add': message_add,
                }
                return render(request, 'change.html', d)
    if project.RELEASE_DATE is None:
        rel_date = ""
    else:
        rel_date = project.RELEASE_DATE.strftime('%Y/%m/%d')
    form = ProjectForm(initial={
        'project_id': project.PROJECT_ID,
        'start_date': project.START_DATE.strftime('%Y/%m/%d'),
        'project_no': project.PROJECT_NO,
        'project_name': project.PROJECT_NAME,
        'protype_code': project.PROTYPE_CODE_id,
        'language_code': project.LANGUAGE_CODE_id,
        'summary': project.SUMMARY,
        'status_code': project.STATUS_CODE_id,
        'customer': project.CUSTOMER,
        'charge': project.CHARGE,
        'reviewer': project.REVIEWER,
        'release_date': rel_date,
        'remarks': project.REMARKS,
    })
    form.fields['start_date'].disabled = True
    form.fields['project_no'].disabled = True
    form.fields['project_name'].disabled = True
    form.fields['protype_code'].disabled = True
    d = {
        'project': form,
        'project_id': project.PROJECT_ID,
        'message_add': message_add,
    }
    return render(request, 'change.html', d)


def delete(request, project_id):
    project = models.Project.objects.get(PROJECT_ID=project_id)
    project.delete()
    return redirect('/list/')


def emotion(request):
    if request.method == 'POST':
        key = "AIzaSyBbKSOqrwtXdRLV-owLDaP4shCoV8o_V7U"
        url = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=' + key
        emotion_form = EmotionForm(request.POST)
        result = ""
        detail = {}
        if emotion_form.is_valid():
            text = emotion_form.cleaned_data['input_text']
            header = {'Content-Type': 'application/json'}
            body = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "language": "JA",
                    "content": text
                },
                "encodingType": "UTF8"
            }
            response = requests.post(url, headers=header, json=body).json()
            result = result + "総合振れ幅:" + str(response["documentSentiment"]["magnitude"]) + "\n"
            result = result + "総合score(顧客満足度)：" + str(response["documentSentiment"]["score"]) + "\n"
            for i in response["sentences"]:
                detail[i["text"]["content"]] = [str(i["sentiment"]["score"]), i["sentiment"]["magnitude"]]
            retresult = {
                'result': result,
                'emotion_form': emotion_form,
                'detail': detail,
            }
            return render(request, 'emotion.html', retresult)
    emotion_form = EmotionForm()
    return render(request, 'emotion.html', {'emotion_form': emotion_form})
