"""
cześć graficzna odpowiadająca za wyświetlanie fabuły i statystyk gracza 
(biblioteka rich)
autorem jest Kacper Kliber
"""

from rich.layout import Layout
from rich.panel import Panel

import zmienne as stan_gry


def stworz_widok():
    """Funkcja tworzy widok gry z podziałem na fabułę i statystyki gracza."""
    uklad = Layout()
    uklad.split_row(
        Layout(name="lewa", ratio=3),
        Layout(name="prawa", ratio=1),
    )

    uklad["lewa"].update(
        Panel(stan_gry.tekst_fabuly, title="Fabuła", border_style="cyan")
    )

    staty_tekst = (
        f"💰 Kasa: {stan_gry.kieszonkowe} zł\n"
        f"🧠 Psychika: {stan_gry.psychika}%\n"
        f"😡 Wkurw Janusza: {stan_gry.zaczerwienienie_janusza}%"
    )

    uklad["prawa"].update(
        Panel(staty_tekst, title="Statystyki", border_style="magenta")
    )

    return uklad
