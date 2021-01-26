from django import forms
from .models import Project, ReqsProject, Requirement
from users.models import Account

poziom = (
    (0, "Pierwszy poziom bezpieczeństwa"),
    (1, "Drugi poziom bezpieczeństwa"),
    (2, "Trzeci poziom bezpieczeństwa"),
)

metoda = (
    (0, "White box"),
    (1, "Black box"),
    (2, "Gray box"),
)

dokumentacja = (
    (0, "Brak dostępu do dokumentacji"),
    (1, "Udzielony dostęp do dokumentacji"),
)

kod_zrodlowy = (
    (0, "Brak dostępu do kodu"),
    (1, "Udzielony dostęp do kodu"),
)

mechanizmy_kryptograficzne = (
    (0, "Brak dostępu do mechanizmów kryptograficznych"),
    (1, "Udzielony dostęp do mechanizmów kryptograficznych"),
)

dziennik_zdarzen = (
    (0, "Brak dostępu do dziennika zdarzeń"),
    (1, "Udzielony dostęp do dziennika zdarzeń"),
)

konta_logowanie = (
    (0, "Brak możliwości tworzenia kont oraz logowania"),
    (1, "Dostępna mozliwość tworzenia kont oraz logowania"),
)

uwierzytelnianie_mfa = (
    (0, "Brak możliwości uwierzytelniania wielopoziomowego"),
    (1, "Dostępna mozliwość uwierzytelniania wielopoziomowego"),
)

uwierzytelnianie_csp = (
    (0, "Brak wdrożenia uwierzytelniania z wykorzystaniem csp"),
    (1, "Wdrożona możliwość uwierzytelniania z wykorzystaniem csp"),
)

wprowadzanie_danych_do_aplikacji = (
    (0, "Brak możliwości wprowadzania danych"),
    (1, "Zaimplementowana możliwość wprowadzania danych"),
)

pobieranie_wgrywanie_plikow = (
    (0, "Brak możliwości pobierania/wgrywania plików"),
    (1, "Zaimplementowana możliwość pobierania/wgrywania plików"),
)

mechanizm_zarzadzania_sesja = (
    (0, "Brak wykorzystywania mechanizmu zarządzania sesją"),
    (1, "Zaimplementowany mechanizm HTTP Cookies"),
    (2, "Zaimplementowany mechanizm w postaci przekazywania Tokena"),
)

kod_aplikacji = (
    (0, "Wykorzystywany kod zarządzany"),
    (1, "Wykorzystywany kod niezarządzany"),
)

uslugi_sieciowe = (
    (0, "Brak wykorzystywania usług sieciowych"),
    (1, "Wykorzystywane usługi sieciowe oparte o technologię SOAP"),
    (2, "Wykorzystywane usługi sieciowe oparte o technologię REST"),
    (3, "Wykorzystywane usługi sieciowe oparte o technologię GraphQL lub inną"),
)


class AddProject(forms.ModelForm):
    project_name = forms.CharField(max_length=256, required=True,
                               widget=forms.TextInput(attrs={'class': 'pr', 'title': 'Project name'}))
    Pentester = forms.ModelChoiceField(queryset=Account.objects.all().filter(type_account=1, is_admin=False))
    Okresl_poziom_bezpieczenstwa = forms.ChoiceField(choices=poziom)
    Okresl_metode_testowania = forms.ChoiceField(choices=metoda)
    Okresl_dostep_do_dokumentacji = forms.ChoiceField(choices=dokumentacja)
    Okresl_dostep_do_kodu_zrodlowego = forms.ChoiceField(choices=kod_zrodlowy)
    Okresl_dostep_do_mechanizmow_kryptograficznych = forms.ChoiceField(choices=mechanizmy_kryptograficzne)
    Okresl_dostep_do_dziennika_zdarzen = forms.ChoiceField(choices=dziennik_zdarzen)
    Okresl_mozliwosc_tworzenia_kont = forms.ChoiceField(choices=konta_logowanie)
    Okresl_zaimplementowanie_mfa = forms.ChoiceField(choices=uwierzytelnianie_mfa)
    Okresl_zaimplementowanie_csp = forms.ChoiceField(choices=uwierzytelnianie_csp)
    Okresl_mozliwosc_wprowadzania_danych = forms.ChoiceField(choices=wprowadzanie_danych_do_aplikacji)
    Okresl_mozliwosc_dzialania_na_plikach = forms.ChoiceField(choices=pobieranie_wgrywanie_plikow)
    Okresl_wykorzystywany_mechanizm_zarzadzania_sesja = forms.ChoiceField(choices=mechanizm_zarzadzania_sesja)
    Okresl_wykorzystywany_kod = forms.ChoiceField(choices=kod_aplikacji)
    Okresl_wykorzystywane_uslugi_sieciowe = forms.ChoiceField(choices=uslugi_sieciowe)

    class Meta:
        model = Project
        fields = ('project_name', 'Pentester', 'Okresl_poziom_bezpieczenstwa', 'Okresl_metode_testowania',
                  'Okresl_dostep_do_dokumentacji', 'Okresl_dostep_do_kodu_zrodlowego',
                  'Okresl_dostep_do_mechanizmow_kryptograficznych', 'Okresl_dostep_do_dziennika_zdarzen',
                  'Okresl_mozliwosc_tworzenia_kont', 'Okresl_zaimplementowanie_mfa', 'Okresl_zaimplementowanie_csp',
                  'Okresl_mozliwosc_wprowadzania_danych', 'Okresl_mozliwosc_dzialania_na_plikach',
                  'Okresl_wykorzystywany_mechanizm_zarzadzania_sesja', 'Okresl_wykorzystywany_kod',
                  'Okresl_wykorzystywane_uslugi_sieciowe')

        exclude = ('klient', 'requirements')


class AddComment(forms.ModelForm):
    comment = forms.CharField(max_length=256, required=False,
                              widget=forms.TextInput(attrs={'class': 'special', 'title': 'Comment'}))

    class Meta:
        model = ReqsProject

        fields = ('comment',)

        exclude = ('project', 'requirement', 'status')
