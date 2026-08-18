"""Główny plik uruchamiający grę tekstową.

uruchamiać za pomocą tego pliku autorem jest Kacper Kliber
"""

import random

from rich.live import Live
from rich.prompt import Prompt

from ui import stworz_widok
import zmienne as stan_gry
import baza_danych_sceny_fabularne as baza_danych


def czekaj_na_enter(tekst_promp="Wciśnij Enter, aby kontynuować..."):
    """Pokazuje widok Live i czeka na Enter na dole pełnego ekranu."""
    koniec_gry = False

    if stan_gry.psychika <= 0:
        stan_gry.tekst_fabuly += "\n\nGAME OVER! Janusz Cię wykończył."
        tekst_promp = "Wciśnij Enter, aby zakończyć grę..."
        koniec_gry = True

    elif stan_gry.kieszonkowe <= 0:
        stan_gry.tekst_fabuly += "\n\nGAME OVER! Nie masz kasy."
        tekst_promp = "Wciśnij Enter, aby zakończyć grę..."
        koniec_gry = True

    elif stan_gry.zaczerwienienie_janusza >= 100:
        stan_gry.tekst_fabuly += "\n\nGAME OVER! wyleciałeś z roboty."
        tekst_promp = "Wciśnij Enter, aby zakończyć grę..."
        koniec_gry = True

    elif (
        stan_gry.kieszonkowe >= 100
        and stan_gry.zaczerwienienie_janusza <= 10
        and stan_gry.psychika >= 80
    ):
        stan_gry.tekst_fabuly += (
            "\n\nWIN! Masz dobre statystyki i wygrałeś z Januszem!"
        )
        tekst_promp = "Wciśnij Enter, aby zakończyć grę..."
        koniec_gry = True

    with Live(stworz_widok(), refresh_per_second=4, screen=True) as live:
        live.console.input(f"\n[cyan]{tekst_promp}[/cyan]")

    if koniec_gry:
        raise SystemExit


def dodaj_zmiany(*zmiany):
    """Dopisuje czytelne podsumowanie wpływu decyzji na statystyki."""
    stan_gry.tekst_fabuly += "\nZmiana statystyk: " + ", ".join(zmiany)


def sklep():
    """Funkcja obsługująca zakupy po ciężkim dniu pracy."""
    while True:
        # przygotowanie napisów w zależności od tego czy gracz coś kupił

        status_multisport = "Już masz Multisport! -> -10% Psychiki codziennie" if stan_gry.multisport else "Jeszcze nie masz Multisportu. (50zł) -> +10% psychiki codziennie"

        stan_gry.tekst_fabuly = (
            "--- Sklep ---\n"
            "1. Energy Drink (10 zł) -> +15% Psychiki\n"
            "2. Melisa dla Janusza (15 zł) -> -20% Wkurwu Janusza\n"
            f"3. {status_multisport}\n"
            "4. Wyjdź ze sklepu"
        )
        czekaj_na_enter("Wciśnij Enter, aby wybrać zakupy...")

        zakup = Prompt.ask(
            "\nCo kupujesz?",
            choices=[ "3", "Energy Drink", "1", "Melisa", "2", "multisport", "3", "Wyjdź", "4"],
            default="4",
        )

        if zakup in ["4", "Wyjdź"]:
            stan_gry.tekst_fabuly = "--- Sklep ---\nWychodzisz ze sklepu."
            czekaj_na_enter()
            return

        elif zakup in ["1", "Energy Drink"]:
            if stan_gry.kieszonkowe >= 10:
                stan_gry.kieszonkowe -= 10
                stan_gry.psychika = min(100, stan_gry.psychika + 15)
                stan_gry.tekst_fabuly = "--- Sklep ---\nKupiłeś Energy Drink! Psychika skacze w górę."
                dodaj_zmiany("-10 zł", "+15% psychiki")
            else:
                stan_gry.tekst_fabuly = "--- Sklep ---\nBrak kasy! Janusz płaci za mało."
        elif zakup in ["2", "Melisa"]:
            if stan_gry.kieszonkowe >= 15:
                stan_gry.kieszonkowe -= 15
                stan_gry.zaczerwienienie_janusza = max(
                    0, stan_gry.zaczerwienienie_janusza - 20
                )
                stan_gry.tekst_fabuly = "--- Sklep ---\nPoczęstowałeś Janusza melisą. Trochę ochłonął!"
                dodaj_zmiany("-15 zł", "-20% wkurwu Janusza")
            else:
                stan_gry.tekst_fabuly = "--- Sklep ---\nBrak kasy na melisę!"
        elif zakup in ["3", "multisport"]:
            if stan_gry.multisport:
                stan_gry.tekst_fabuly = "--- Sklep ---\nJuż masz Multisport!"
            elif stan_gry.kieszonkowe >= 50:
                stan_gry.kieszonkowe -= 50
                stan_gry.multisport = True
                stan_gry.tekst_fabuly = "--- Sklep ---\nKupiłeś Multisport! Psychika wzrasta codziennie."
                dodaj_zmiany("-50 zł", "Multisport aktywny")
            else:
                stan_gry.tekst_fabuly = "--- Sklep ---\nBrak kasy na Multisport!"

        czekaj_na_enter("Wciśnij Enter, aby wrócić do sklepu...")

def wydarzenia_turowe():
    """Funkcja obsługująca wydarzenia turowe, które mają miejsce codziennie."""
    if stan_gry.multisport:
        stan_gry.psychika = min(100, stan_gry.psychika + 10)
        stan_gry.tekst_fabuly += "\nMultisport: +10% psychiki codziennie."
        dodaj_zmiany("+10% psychiki (Multisport)")

def rozmowa_z_januszem():
    """Obsługuje rozmowę ewaluacyjną, czyli mały boss fight z Januszem."""
    stan_gry.tekst_fabuly += (
        "\n\n--- Biuro Janusza ---\n"
        "Janusz wzywa Cię na rozmowę ewaluacyjną. Patrzy groźnie ponad kubkiem kawy."
    )
    czekaj_na_enter()

    odpowiedz = Prompt.ask(
        "\nJanusz: 'Dlaczego raport nadal nie jest gotowy?'",
        choices=["To priorytety projektu", "1", "Dać łapówkę", "2", "To wina drukarki", "3"],
        default="To priorytety projektu",
    )

    if odpowiedz in ["To priorytety projektu", "1"]:
        stan_gry.tekst_fabuly += (
            "\nSpokojnie tłumaczysz priorytety. Janusz mruczy niezadowolony, ale odpuszcza."
        )
        stan_gry.zaczerwienienie_janusza = max(0, stan_gry.zaczerwienienie_janusza - 5)
        dodaj_zmiany("-5% wkurwu Janusza")
    elif odpowiedz in ["Dać łapówkę", "2"]:
        if stan_gry.kieszonkowe >= 20:
            stan_gry.kieszonkowe -= 20
            stan_gry.zaczerwienienie_janusza = max(0, stan_gry.zaczerwienienie_janusza - 25)
            stan_gry.tekst_fabuly += "\nKawa i pączek załatwiają sprawę. Janusz nagle robi się bardzo wyrozumiały."
            dodaj_zmiany("-20 zł", "-25% wkurwu Janusza")
        else:
            stan_gry.psychika -= 10
            stan_gry.tekst_fabuly += "\nNie masz nawet na łapówkę. Janusz kończy rozmowę długim wykładem."
            dodaj_zmiany("-10% psychiki")
    else:
        stan_gry.zaczerwienienie_janusza += 15
        stan_gry.psychika -= 5
        stan_gry.tekst_fabuly += "\nJanusz nie daje się nabrać na drukarkę. W gabinecie robi się gorąco."
        dodaj_zmiany("+15% wkurwu Janusza", "-5% psychiki")

    czekaj_na_enter()


def losowe_zdarzenia():
    """Losuje od zera do trzech dodatkowych zdarzeń na dany dzień."""
    liczba_zdarzen = random.randint(0, 3)

    if liczba_zdarzen == 0:
        stan_gry.tekst_fabuly += (
            "\n\nDzień mija zaskakująco spokojnie. Nawet ekspres do kawy nie protestuje."
        )
        czekaj_na_enter()
        return

    zdarzenia = random.sample(
        ["pip", "wifi", "prad", "janusz"], k=liczba_zdarzen
    )

    for zdarzenie in zdarzenia:
        if zdarzenie == "pip":
            stan_gry.tekst_fabuly += (
                "\n\nKontrola PIP pojawia się bez zapowiedzi. Janusz udaje, że wszystko od zawsze działa idealnie."
            )
            stan_gry.psychika -= 8
            stan_gry.zaczerwienienie_janusza += 10
            dodaj_zmiany("-8% psychiki", "+10% wkurwu Janusza")
            czekaj_na_enter()
        elif zdarzenie == "wifi":
            stan_gry.tekst_fabuly += (
                "\n\nPada Wi-Fi w całym biurze. Przez chwilę wszyscy patrzą na siebie bezradnie."
            )
            stan_gry.psychika -= 6
            dodaj_zmiany("-6% psychiki")
            czekaj_na_enter()
        elif zdarzenie == "prad":
            stan_gry.tekst_fabuly += (
                "\n\nGaśnie światło — awaria prądu zatrzymuje całe biuro. Janusz obwinia wszystkich naraz."
            )
            stan_gry.psychika -= 10
            stan_gry.zaczerwienienie_janusza += 12
            dodaj_zmiany("-10% psychiki", "+12% wkurwu Janusza")
            czekaj_na_enter()
        else:
            rozmowa_z_januszem()

# zmieniłem nazwę zmiennej SCENY_FABULARNE
SCENY_FABULARNE = baza_danych.SCENY_FABULARNE


def scena_fabularna(dzien):
    """Rozgrywa jedną z 28 scen przypisanych do dni od 3 do 30."""
    nazwa, pytanie, opcja_1, opcja_2, sukces, porazka = SCENY_FABULARNE[dzien - 3]
    stan_gry.tekst_fabuly += f"\n\n--- {nazwa} ---\n{pytanie}"
    czekaj_na_enter()
    wybor = Prompt.ask(
        "\nCo robisz?",
        choices=[opcja_1, "1", opcja_2, "2"],
        default=opcja_1,
    )
    if wybor in [opcja_1, "1"]:
        stan_gry.kieszonkowe += 10
        stan_gry.zaczerwienienie_janusza = max(0, stan_gry.zaczerwienienie_janusza - 5)
        stan_gry.tekst_fabuly += f"\n{sukces} Dostajesz 10 zł premii."
        dodaj_zmiany("+10 zł", "-5% wkurwu Janusza")
    else:
        stan_gry.psychika -= 8
        stan_gry.zaczerwienienie_janusza += 10
        stan_gry.tekst_fabuly += f"\n{porazka} Tracisz 8% psychiki."
        dodaj_zmiany("-8% psychiki", "+10% wkurwu Janusza")
    czekaj_na_enter()


def pokaz_zakonczenie():
    """Pokazuje podsumowanie po trzydziestym dniu pracy."""
    stan_gry.tekst_fabuly = (
        "=== KONIEC 30-DNIOWEGO MIESIĄCA ===\n"
        "Przetrwałeś miesiąc w biurze Janusza. Czas na podsumowanie."
    )
    with Live(stworz_widok(), refresh_per_second=4, screen=True) as live:
        live.console.input("\n[cyan]Wciśnij Enter, aby zakończyć grę...[/cyan]")


# --- GŁÓWNA PĘTLA GRY ---

dzien = 1

try:

    while True:
        stan_gry.tekst_fabuly = f"=== DZIEŃ {dzien} ==="
        wydarzenia_turowe()
        czekaj_na_enter()

        # Scena 1: Nadgodziny
        if dzien == 1:
            stan_gry.tekst_fabuly += "\nJanusz: 'Młody! Zrobisz nadgodziny w weekend?'"
            stan_gry.psychika -= 10
            dodaj_zmiany("-10% psychiki")
            czekaj_na_enter("Co o tym myślisz? (Enter)")

            wybor = Prompt.ask(
                "\nCo odpowiadasz?",
                choices=["Zaakceptuj", "1", "Wyjdź z lokalu", "2"],
                default="Zaakceptuj",
            )

            if wybor == "Zaakceptuj" or wybor == "1":
                stan_gry.tekst_fabuly += "\nZgadzasz się na nadgodziny. Dostajesz 30 zł kieszonkowego!"
                stan_gry.kieszonkowe += 30
                stan_gry.psychika -= 20
                stan_gry.zaczerwienienie_janusza -= 10
                dodaj_zmiany("+30 zł", "-20% psychiki", "-10% wkurwu Janusza")
            else:
                stan_gry.tekst_fabuly += "\nOdmawiasz i wychodzisz. Janusz się wkurzył!"
                stan_gry.zaczerwienienie_janusza += 30
                dodaj_zmiany("+30% wkurwu Janusza")

            czekaj_na_enter()

        # Scena 2: Drukarka
        elif dzien == 2:
            stan_gry.tekst_fabuly += (
                "\nNagle z pokoju obok dobiega dym!\n"
                "Janusz: 'Drukarka stuka i dymi! Naprawiaj to!'"
            )
            czekaj_na_enter("Co robisz z drukarką? (Enter)")

            wybor_drukarka = Prompt.ask(
                "\nCo robisz z drukarką?",
                choices=["Kopnij obudowę", "1", "Zrestartuj", "2", "Wgraj sterownik", "3"],
                default="Zrestartuj",
            )

            if wybor_drukarka == "Kopnij obudowę" or wybor_drukarka == "1":
                stan_gry.zaczerwienienie_janusza += 20
                stan_gry.tekst_fabuly += "\nDrukarka padła całkowicie. Janusz się gotuje!"
                dodaj_zmiany("+20% wkurwu Janusza")
            elif wybor_drukarka == "Zrestartuj" or wybor_drukarka == "2":
                stan_gry.psychika -= 5
                stan_gry.tekst_fabuly += "\nReset pomógł na chwilę, ale straciłeś nerwy."
                dodaj_zmiany("-5% psychiki")
            elif wybor_drukarka == "Wgraj sterownik" or wybor_drukarka == "3":
                stan_gry.kieszonkowe += 15
                stan_gry.zaczerwienienie_janusza -= 10
                stan_gry.tekst_fabuly += "\nDrukarka działa! Janusz daje Ci 15 zł premii."
                dodaj_zmiany("+15 zł", "-10% wkurwu Janusza")

            czekaj_na_enter()

        elif 3 <= dzien <= 30:
            scena_fabularna(dzien)

        # Dodatkowe zdarzenia po głównej scenie dnia.
        losowe_zdarzenia()

        # Po zakończeniu wyzwań dnia gracz idzie do sklepu
        sklep()

        if dzien == 30:
            pokaz_zakonczenie()
            break

        # Przejście do kolejnego dnia
        dzien += 1
except KeyboardInterrupt:
    print("\n\nEwakuacja z biura!")
    print("\nTwoje staty:")
    print(f"💰 Kasa: {stan_gry.kieszonkowe} zł")
    print(f"🧠 Psychika: {stan_gry.psychika}%")
    print(f"😡 Wkurw Janusza: {stan_gry.zaczerwienienie_janusza}%\n")
    exit()
