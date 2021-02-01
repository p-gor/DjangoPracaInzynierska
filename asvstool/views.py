from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Chapter, Subsection, Requirement, Project, ReqsProject
from users.models import Account
from .forms import AddProject, AddComment
from django.contrib.auth.decorators import login_required
import csv


# Create your views here.

def home(request):
    return render(request, 'home.html')


@login_required
def project(request):
    typ_konta = Account.objects.get(username=request.user.username).type_account
    wymagania = ReqsProject.objects.all().filter(project=request.POST.get('id'))
    if typ_konta == 0:
        if request.method == "POST":
            obiekt = Project.objects.get(id=request.POST.get('id'))
            obiekt.delete()
    else:
        if request.method == "POST":
            if wymagania:
                response = HttpResponse(content_type='text/csv')
                writer = csv.writer(response)
                writer.writerow(['Chapter', 'Subsection', 'Requirement', 'Level 1', 'Level 2', 'Level 3',
                                 'NIST', 'CWE', 'Status', 'Comment'])
                count = ReqsProject.objects.all().filter(project=request.POST.get('id')).count()
                index = ReqsProject.objects.all().filter(project=request.POST.get('id')).first().id
                for i in range(count):
                    req = (wymagania.get(
                               id=index + i).requirement.subsection_nr.chapter_nr.chapter_title,
                           wymagania.get(
                               id=index + i).requirement.subsection_nr.subsection_name,
                           wymagania.get(
                               id=index + i).requirement.requirement_name,
                           wymagania.get(
                               id=index + i).requirement.lvl1,
                           wymagania.get(
                               id=index + i).requirement.lvl2,
                           wymagania.get(
                               id=index + i).requirement.lvl3,
                           wymagania.get(
                               id=index + i).requirement.nist,
                           wymagania.get(
                               id=index + i).requirement.cwe,
                           wymagania.get(id=index + i).status,
                           wymagania.get(id=index + i).comment)
                    writer.writerow(req)
                response['Content-Disposition'] = 'attachment; filename="Checklist.csv"'
                return response
            else:
                return redirect('tool-details', request.POST.get('id'))
    context_klient = {
        'Obiekty': Project.objects.all().filter(Klient=request.user).order_by('date_made').reverse(),
        'title': 'Projekty',
    }
    context_pentester = {
        'Obiekty': Project.objects.all().filter(Pentester=request.user).order_by('date_made').reverse(),
        'title': 'Projekty'
    }
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
                form_tmp.Klient = request.user
                Obiekty = Project.objects.all()
                for obiekt in Obiekty:
                    if (form_tmp.Klient == obiekt.Klient) and (form_tmp.project_name == obiekt.project_name):
                        form = AddProject()
                        context = {
                            'info': 'Projekt o podanej nazwie został już utworzony! Prosze podac inną nazwę projektu',
                            'title': 'Nowy Projekt',
                            'form': form
                        }
                        return render(request, 'add_project.html', context)
                form_tmp.save()
                return redirect('tool-project')
        else:
            form = AddProject()
        return render(request, 'add_project.html', {'title': 'Nowy Projekt', 'form': form})
    else:
        return redirect('tool-project')


@login_required
def details_project(request, id):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).Klient == email) or (Project.objects.get(id=id).Pentester == email):
        count = Requirement.objects.all().count()
        index = Requirement.objects.all().first().id
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'checklist': ReqsProject.objects.all().filter(project=id),
            'title': 'Lista Kontrolna'
        }
        if request.method == 'POST':
            for i in range(count):
                status = 1
                if Project.objects.get(id=id).Okresl_poziom_bezpieczenstwa == 0:
                    if (Requirement.objects.get(id=index + i).lvl3) or (
                            Requirement.objects.get(id=index + i).lvl2):
                        status = 0
                    else:
                        status = 1
                elif Project.objects.get(id=id).Okresl_poziom_bezpieczenstwa == 1:
                    if Requirement.objects.get(id=index + i).lvl3:
                        status = 0
                    else:
                        status = 1
                else:
                    if Requirement.objects.get(id=index + i).lvl3:
                        status = 1
                # Metoda testowania
                if Project.objects.get(id=id).Okresl_metode_testowania == 0 and status == 1:
                    status = 1
                elif Project.objects.get(id=id).Okresl_metode_testowania == 1 and status == 1:
                    if Requirement.objects.get(id=index + i).black_box:
                        status = 1
                    else:
                        status = 0
                elif Project.objects.get(id=id).Okresl_metode_testowania == 2 and status == 1:
                    if Requirement.objects.get(id=index + i).gray_box:
                        status = 1
                    else:
                        status = 0
                # Dostęp do dokumentacji
                if Project.objects.get(id=id).Okresl_dostep_do_dokumentacji == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).dostep_do_dokumentacji:
                        status = 0
                # Dostęp do kodu
                if Project.objects.get(id=id).Okresl_dostep_do_kodu_zrodlowego == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).dostep_do_kodu:
                        status = 0
                # Dostęp do mechanizmów kryptograficznych
                if Project.objects.get(id=id).Okresl_dostep_do_mechanizmow_kryptograficznych == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).dostep_do_mechanizmow_kryptograficznych:
                        status = 0
                # Dostęp do dziennika zdarzeń
                if Project.objects.get(id=id).Okresl_dostep_do_dziennika_zdarzen == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).dostep_do_dziennika_zdarzen:
                        status = 0
                # Możliwość tworzenia kont
                if Project.objects.get(id=id).Okresl_mozliwosc_tworzenia_kont == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).tworzenie_kont:
                        status = 0
                # Zaimplementowanie mfa
                if Project.objects.get(id=id).Okresl_zaimplementowanie_mfa == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).mfa:
                        status = 0
                # Wykorzystywanie csp
                if Project.objects.get(id=id).Okresl_zaimplementowanie_csp == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).csp:
                        status = 0
                # Możliwość wprowadzania danych
                if Project.objects.get(id=id).Okresl_mozliwosc_wprowadzania_danych == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).wprowadzanie_danych:
                        status = 0
                # Możliwość pobierania/wgrywania plików
                if Project.objects.get(id=id).Okresl_mozliwosc_dzialania_na_plikach == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).dzialanie_na_plikach:
                        status = 0
                # Mechanizm zarządzania sesją
                if Project.objects.get(id=id).Okresl_wykorzystywany_mechanizm_zarzadzania_sesja == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywany_mechanizm_zarzadzania_sesja != 0:
                        status = 0
                elif Project.objects.get(id=id).Okresl_wykorzystywany_mechanizm_zarzadzania_sesja == 1 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywany_mechanizm_zarzadzania_sesja == 2:
                        status = 0
                elif Project.objects.get(id=id).Okresl_wykorzystywany_mechanizm_zarzadzania_sesja == 2 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywany_mechanizm_zarzadzania_sesja == 1:
                        status = 0
                # Wykorzystywany kod
                if Project.objects.get(id=id).Okresl_wykorzystywany_kod == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywany_kod:
                        status = 0
                # Wykorzystywane usługi sieciowe
                if Project.objects.get(id=id).Okresl_wykorzystywane_uslugi_sieciowe == 0 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe != 0:
                        status = 0
                elif Project.objects.get(id=id).Okresl_wykorzystywane_uslugi_sieciowe == 1 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe == 2 or Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe == 3:
                        status = 0
                elif Project.objects.get(id=id).Okresl_wykorzystywane_uslugi_sieciowe == 2 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe == 1 or Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe == 3:
                        status = 0
                elif Project.objects.get(id=id).Okresl_wykorzystywane_uslugi_sieciowe == 3 and status == 1:
                    if Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe == 1 or Requirement.objects.get(id=index + i).wykorzystywane_uslugi_sieciowe == 2:
                        status = 0
                object = ReqsProject(project=Project.objects.get(id=id),
                                     requirement=Requirement.objects.get(id=index + i),
                                     status=status,
                                     comment="")
                object.save()
            return render(request, 'details_project.html', context)
        else:
            return render(request, 'details_project.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Lista Kontrolna'
        }
        return render(request, 'details_project.html', context)


@login_required
def checklist(request, id, id_state):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).Klient == email) or (Project.objects.get(id=id).Pentester == email):
        chapter = Chapter.objects.get(id=id_state).chapter_title
        Obiekty = ReqsProject.objects.all().filter(project=id).filter(status=1)
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'chapter': chapter,
            'Obiekty': Obiekty.order_by('id'),
            'checklist': ReqsProject.objects.all().filter(project=id),
            'title': 'Lista Kontrolna - szczegóły'
        }
        return render(request, 'checklist.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Lista Kontrolna - szczegóły'
        }
        return render(request, 'checklist.html', context)


@login_required
def rejectlist(request, id, id_state):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).Klient == email) or (Project.objects.get(id=id).Pentester == email):
        chapter = Chapter.objects.get(id=id_state).chapter_title
        Obiekty = ReqsProject.objects.all().filter(project=id).filter(status=0)
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'chapter': chapter,
            'Obiekty': Obiekty.order_by('id'),
            'checklist': ReqsProject.objects.all().filter(project=id),
            'title': 'Odrzucone - szczegóły'
        }
        return render(request, 'rejected.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Odrzucone - szczegóły'
        }
        return render(request, 'rejected.html', context)


@login_required
def rejected(request, id):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id).Klient == email) or (Project.objects.get(id=id).Pentester == email):
        context = {
            'Name': Project.objects.get(id=id).project_name,
            'project': Project.objects.get(id=id),
            'checklist': ReqsProject.objects.all().filter(project=id),
            'title': 'Odrzucone'
        }
        return render(request, 'details_rejected.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Odrzucone'
        }
        return render(request, 'details_rejected.html', context)


@login_required
def add_comment(request, id_project, id_requirement, pk):
    email = Account.objects.get(username=request.user.username)
    if (Project.objects.get(id=id_project).Klient == email) or (Project.objects.get(id=id_project).Pentester == email):
        if request.method == 'POST':
            form_tmp = ReqsProject.objects.get(id=id_requirement)
            form_tmp.comment = request.POST['comment']
            form_tmp.save()
            form = AddComment()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'title': 'Dodaj Komentarz',
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'checklist': ReqsProject.objects.all().filter(project=id_project),
                'form': form,
            }
            if pk == 0:
                return render(request, 'add_comment_checklist.html', context)
            else:
                return render(request, 'add_comment_rejected.html', context)
        else:
            form = AddComment()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'title': 'Dodaj Komentarz',
                'checklist': ReqsProject.objects.all().filter(project=id_project),
                'form': form,
            }
            if pk == 0:
                return render(request, 'add_comment_checklist.html', context)
            else:
                return render(request, 'add_comment_rejected.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Dodaj Komentarz'
        }
        if pk == 0:
            return render(request, 'add_comment_checklist.html', context)
        else:
            return render(request, 'add_comment_rejected.html', context)


@login_required
def reject(request, id_project, id_requirement):
    email = Account.objects.get(username=request.user.username)
    context = {
        'Name': Project.objects.get(id=id_project).project_name,
        'project': Project.objects.get(id=id_project),
        'Req': ReqsProject.objects.get(id=id_requirement),
        'title': 'Odrzuć',
        'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
        'checklist': ReqsProject.objects.all().filter(project=id_project),
    }
    if (Project.objects.get(id=id_project).Klient == email) or (Project.objects.get(id=id_project).Pentester == email):
        if request.method == 'POST':
            form_tmp = ReqsProject.objects.get(id=id_requirement)
            form_tmp.status = 0
            form_tmp.save()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'title': 'Odrzuć',
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'checklist': ReqsProject.objects.all().filter(project=id_project),
                'if_post': 0,
            }
            return render(request, 'reject.html', context)
        else:
            return render(request, 'reject.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Odrzuć'
        }
        return render(request, 'reject.html', context)


@login_required
def restore(request, id_project, id_requirement):
    email = Account.objects.get(username=request.user.username)
    context = {
        'Name': Project.objects.get(id=id_project).project_name,
        'project': Project.objects.get(id=id_project),
        'Req': ReqsProject.objects.get(id=id_requirement),
        'title': 'Przywróć',
        'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
        'checklist': ReqsProject.objects.all().filter(project=id_project),
    }
    if (Project.objects.get(id=id_project).Klient == email) or (Project.objects.get(id=id_project).Pentester == email):
        if request.method == 'POST':
            form_tmp = ReqsProject.objects.get(id=id_requirement)
            form_tmp.status = 1
            form_tmp.save()
            context = {
                'Name': Project.objects.get(id=id_project).project_name,
                'project': Project.objects.get(id=id_project),
                'Req': ReqsProject.objects.get(id=id_requirement),
                'title': 'Przywróć',
                'chapter': ReqsProject.objects.get(id=id_requirement).requirement.subsection_nr.chapter_nr,
                'checklist': ReqsProject.objects.all().filter(project=id_project),
                'if_post': 0,
            }
            return render(request, 'restore.html', context)
        else:
            return render(request, 'restore.html', context)
    else:
        context = {
            'info': 'Nie masz dostępu do tego projektu',
            'title': 'Przywróć'
        }
        return render(request, 'restore.html', context)


@login_required
def about(request):
    context = {
        'Obiekty': Chapter.objects.all(),
        'title': 'Rozdziały ASVS'
    }
    return render(request, 'about.html', context)


@login_required
def subsection(request, pk):
    context = {
        'Obiekty': Subsection.objects.all().filter(chapter_nr_id=pk),
        'Name': Chapter.objects.get(id=pk).chapter_title,
        'title': 'Podrozdziały ASVS'
    }
    return render(request, 'subsection.html', context)


@login_required
def tests(request, pk):
    context = {
        'Obiekty': Requirement.objects.all().filter(subsection_nr_id=pk).order_by('pk'),
        'chapter_id': Subsection.objects.get(id=pk).chapter_nr_id,
        'Name': Subsection.objects.get(id=pk).subsection_name,
        'title': 'Wymagania ASVS'
    }
    return render(request, 'tests.html', context)
