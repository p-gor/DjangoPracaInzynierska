from django.db import models
from users.models import Account


# Create your models here.


class Chapter(models.Model):
    chapter_title = models.CharField(max_length=256, default=None)

    def __str__(self):
        return self.chapter_title


class Subsection(models.Model):
    chapter_nr = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    subsection_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.subsection_name


class Requirement(models.Model):
    subsection_nr = models.ForeignKey(Subsection, on_delete=models.CASCADE)
    requirement_name = models.CharField(max_length=256, default=None)
    nist = models.CharField(max_length=10, blank=True, null=True, default=None)
    cwe = models.CharField(max_length=10, blank=True, null=True, default=None)
    lvl1 = models.BooleanField(default=True)
    lvl2 = models.BooleanField(default=True)
    lvl3 = models.BooleanField(default=True)
    white_box = models.BooleanField(default=True)
    black_box = models.BooleanField(default=True)
    gray_box = models.BooleanField(default=True)
    dostep_do_dokumentacji = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - wymagany dostęp do dokumentacji
    dostep_do_kodu = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - wymagany dostęp do kodu
    dostep_do_mechanizmow_kryptograficznych = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - wymagany dostęp do mechanizmów kryptograficznych
    dostep_do_dziennika_zdarzen = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - wymagany dostęp do dziennika zdarzeń
    tworzenie_kont = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - umożliwienie tworzenia kont oraz logowania
    mfa = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - sprawdzane w przypadku wdrożenia mfa
    csp = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - sprawdzane w przypadku wdrożenia csp
    wprowadzanie_danych = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - sprawdzane w przypadku umożliwienia wprowadzania danych
    dzialanie_na_plikach = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - sprawdzane w przypadku umożliwienia działania na plikach
    wykorzystywany_mechanizm_zarzadzania_sesja = models.IntegerField(default=0)
    # 0 - nie dotyczy
    # 1 - Cookies
    # 2 - Token
    wykorzystywany_kod = models.BooleanField(default=False)
    # 0 - nie dotyczy
    # 1 - sprawdzane w przypadku wykorzystywania niezarządzanego kodu
    wykorzystywane_uslugi_sieciowe = models.IntegerField(default=0)
    # 0 - nie dotyczy
    # 1 - SOAP
    # 2 - REST
    # 3 - GraphQL lub inne

    def __str__(self):
        return self.requirement_name


class Project(models.Model):
    project_name = models.CharField(max_length=256, default=None)
    date_made = models.DateTimeField(verbose_name="data utworzenia", auto_now_add=True)
    klient = models.ForeignKey(Account, blank=True, null=True, default=None, on_delete=models.CASCADE,
                               db_column='email', related_name='+')
    Pentester = models.ForeignKey(Account, blank=True, null=True, default=None, on_delete=models.CASCADE,
                                  db_column='username', related_name='+')
    requirements = models.ManyToManyField(Requirement, through='ReqsProject')
    Okresl_poziom_bezpieczenstwa = models.IntegerField(default=None)
    # 0 - L1
    # 1 - L2
    # 2 - L3
    Okresl_metode_testowania = models.IntegerField(default=None)
    # 0 - white box
    # 1 - black box
    # 2 - gray box
    Okresl_dostep_do_dokumentacji = models.BooleanField(default=False)
    # 0 - brak dostępu do dokumentacji
    # 1 - udzielony dostęp do dokumentacji
    Okresl_dostep_do_kodu_zrodlowego = models.BooleanField(default=False)
    # 0 - brak dostępu do kodu
    # 1 - umożliwiony dostęp do kodu
    Okresl_dostep_do_mechanizmow_kryptograficznych = models.BooleanField(default=False)
    # 0 - brak dostępu do mechanizmów kryptograficznych
    # 1 - udzielony dostęp do mechanizmów kryptograficznych
    Okresl_dostep_do_dziennika_zdarzen = models.BooleanField(default=False)
    # 0 - brak dostępu do dziennika zdarzeń
    # 1 - udzielony dostęp do dziennika zdarzeń
    Okresl_mozliwosc_tworzenia_kont = models.BooleanField(default=False)
    # 0 - brak możliwości tworzenia kont
    # 1 - aplikacja zapewnie możliwośc tworzenia kont
    Okresl_zaimplementowanie_mfa = models.BooleanField(default=False)
    # 0 - brak zaimplementowania mfa
    # 1 - zaimplementowane mfa
    Okresl_zaimplementowanie_csp = models.BooleanField(default=False)
    # 0 - brak zaimplementowania csp
    # 1 - zaimplementowane csp
    Okresl_mozliwosc_wprowadzania_danych = models.BooleanField(default=False)
    # 0 - aplikacja nie umożliwia wprowadzania danych
    # 1 - aplikacja umożliwia wprowadzanie danych
    Okresl_mozliwosc_dzialania_na_plikach = models.BooleanField(default=False)
    # 0 - aplikacja nie umozliwia pobierania/wgrywania plików
    # 1 - aplikacja umożliwia wgrywanie/pobieranie plików
    Okresl_wykorzystywany_mechanizm_zarzadzania_sesja = models.IntegerField(default=0)
    # 0 - nie wykorzystywany jest mechanizm zarządzania sesją
    # 1 - Cookies
    # 2 - Token
    Okresl_wykorzystywany_kod = models.BooleanField(default=False)
    # 0 - zarządzany
    # 1 - niezarządzany
    Okresl_wykorzystywane_uslugi_sieciowe = models.IntegerField(default=0)
    # 0 - nie są wykorzystywane usługi sieciowe
    # 1 - SOAP
    # 2 - REST
    # 3 - GraphQL lub inne

    def __str__(self):
        return self.project_name

    class Meta:
        unique_together = [['project_name', 'klient']]


class ReqsProject(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    # 0 - Odrzucony
    # 1 - Przyjęty
    comment = models.CharField(max_length=256, default=None, blank=True)

    class Meta:
        unique_together = [['project', 'requirement']]

