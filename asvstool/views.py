from django.shortcuts import render, redirect
from .models import Chapter, Subsection, Requirement, Project, ReqsProject
from users.models import Account
from .forms import AddProject, AddComment
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html')


@login_required
def project(request):
    if request.method == "POST":
        obiekt = Project.objects.get(id=request.POST.get('id'))
        obiekt.delete()
    context_klient = {
        'Obiekty': Project.objects.all().filter(klient=request.user).order_by('date_made').reverse(),
        'title': 'Project',
    }
    context_pentester = {
        'Obiekty': Project.objects.all().filter(Pentester=request.user).order_by('date_made').reverse(),
        'title': 'Project'
    }
    typ_konta = Account.objects.get(username=request.user.username).type_account
    if typ_konta == 0:
        return render(request, 'project.html', context_klient)
    else:
        return render(request, 'project.html', context_pentester)

@login_required
def add_project(request):
    typ_konta = Account.objects.get(username=request.user.username).type_account
    if typ_konta == 0:
        if request.method == 'POST':
            form = AddProject(request.POST)
            if form.is_valid():
                # przypisanie aktualnego użytkownika jako tworce danego projektu,
                # wykorzystano do tego pomocniczą zmienną form_tmp
                form_tmp = form.save(commit=False)
                form_tmp.klient = request.user
                Obiekty = Project.objects.all()
                for obiekt in Obiekty:
                    if (form_tmp.klient == obiekt.klient) and (form_tmp.project_name == obiekt.project_name):
                        form = AddProject()
                        context = {
                            'info': 'Projekt o podanej nazwie został już utworzony! Prosze podac inną nazwę projektu',
                            'form': form
                        }
                        return render(request, 'add_project.html', context)
                # form_tmp.requirements = Requirement.objects.all()
                form_tmp.save()
                return redirect('tool-project')
        else:
            form = AddProject()
        return render(request, 'add_project.html', {'title': 'New project', 'form': form})
    else:
        return redirect('tool-project')


@login_required
def details_project(request, id):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).klient == email) or (Project.objects.get(id=id).Pentester == email):
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'title': 'Project Details'
        }
        return render(request, 'details_project.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Project Details'
        }
        return render(request, 'details_project.html', context)


@login_required
def checklist(request, id, id_state):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).klient == email) or (Project.objects.get(id=id).Pentester == email):
        chapter = Chapter.objects.get(id=id_state).chapter_title
        Obiekty = ReqsProject.objects.all().filter(project=id).filter(status=1)
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'chapter': chapter,
            'Obiekty': Obiekty,
            'title': 'Checklist'
        }
        return render(request, 'checklist.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'checklist'
        }
        return render(request, 'checklist.html', context)

@login_required
def rejected(request, id):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).klient == email) or (Project.objects.get(id=id).Pentester == email):
        chapter = 'Rejected requirements'
        Obiekty = ReqsProject.objects.all().filter(project=id).filter(status=0)
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'chapter': chapter,
            'Obiekty': Obiekty,
            'title': 'Rejected Requirements'
        }
        return render(request, 'rejected.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Rejected Requirements'
        }
        return render(request, 'rejected.html', context)


@login_required
def add_comment(request, id_project, id_requirement, pk):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id_project).klient == email) or (Project.objects.get(id=id_project).Pentester == email):
        if request.method == 'POST':
            form_tmp = ReqsProject.objects.get(id=id_requirement)
            form_tmp.comment = request.POST['comment']
            form_tmp.save()
            form = AddComment()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'title': 'Add Comment',
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'if_checklist': pk,
                'form': form,
            }
            return render(request, 'add_comment.html', context)
        else:
            form = AddComment()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'title': 'Add Comment',
                'if_checklist': pk,
                'form': form,
            }
            return render(request, 'add_comment.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Add Comment'
        }
        return render(request, 'add_comment.html', context)


@login_required
def reject(request, id_project, id_requirement):
    email = Account.objects.get(username=request.user.username)
    context = {
        'Name': Project.objects.get(id=id_project).project_name,
        'project': Project.objects.get(id=id_project),
        'Req': ReqsProject.objects.get(id=id_requirement),
        'title': 'Reject',
        'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
    }
    if (Project.objects.get(id=id_project).klient == email) or (Project.objects.get(id=id_project).Pentester == email):
        if request.method == 'POST':
            form_tmp = ReqsProject.objects.get(id=id_requirement)
            form_tmp.status = 0
            form_tmp.save()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'title': 'Reject',
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'if_post': 0,
            }
            return render(request, 'reject.html', context)
        else:
            return render(request, 'reject.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Reject'
        }
        return render(request, 'reject.html', context)


@login_required
def restore(request, id_project, id_requirement):
    email = Account.objects.get(username=request.user.username)
    context = {
        'Name': Project.objects.get(id=id_project).project_name,
        'project': Project.objects.get(id=id_project),
        'Req': ReqsProject.objects.get(id=id_requirement),
        'title': 'Reject',
        'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
    }
    if (Project.objects.get(id=id_project).klient == email) or (Project.objects.get(id=id_project).Pentester == email):
        if request.method == 'POST':
            form_tmp = ReqsProject.objects.get(id=id_requirement)
            form_tmp.status = 1
            form_tmp.save()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'title': 'Reject',
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'if_post': 0,
            }
            return render(request, 'restore.html', context)
        else:
            return render(request, 'restore.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Reject'
        }
        return render(request, 'restore.html', context)


@login_required
def about(request):
    context = {
        'Obiekty': Chapter.objects.all(),
        'title': 'About'
    }
    return render(request, 'about.html', context)


@login_required
def subsection(request, pk):
    context = {
        'Obiekty': Subsection.objects.all().filter(chapter_nr_id=pk),
        'Name': Chapter.objects.get(id=pk).chapter_title,
        'title': 'Subsection'
    }
    return render(request, 'subsection.html', context)


@login_required
def tests(request, pk):
    context = {
        'Obiekty': Requirement.objects.all().filter(subsection_nr_id=pk).order_by('pk'),
        'Name': Subsection.objects.get(id=pk).subsection_name,
        'title': 'Tests'
    }
    return render(request, 'tests.html', context)
