"""Identifiants de titre 3DS des jeux visés.

Sources : clockwork/runtime/src/frontend/games.h (KNOWN_DUMPS), zakuro/COMPATIBILITY.md,
Yo-kai-Watch-2-Archipelago (installation/installer.py : mods/<00040000001B2900>/).
Les adresses mémoire NE sont PAS ici : elles diffèrent par jeu ET par région (chaque région est
un code.bin différent, voir games.h) et restent à établir sur le PC du joueur.
"""
TITLES = {
    0x00040000001B2900: "Yo-kai Watch 2 : Spectres Psychiques (EUR)",
    0x00040000001D6800: "Yo-kai Watch 3 (EUR)",
    0x00040000001CEC00: "Yo-kai Watch Blasters : Peloton du Chat Rouge (EUR)",
    0x00040000001CF000: "Yo-kai Watch Blasters : Escadron du Chien Blanc (EUR)",
    # USA, pour comparaison (versions les plus testées par Clockwork)
    0x00040000001B2700: "Yo-kai Watch 2 : Psychic Specters (USA)",
    0x00040000001D6700: "Yo-kai Watch 3 (USA)",
    0x00040000001CEB00: "Yo-kai Watch Blasters : Red Cat Corps (USA)",
    0x00040000001CEF00: "Yo-kai Watch Blasters : White Dog Squad (USA)",
}


def update_title(title_id: int) -> int:
    """Titre de la mise à jour d'un jeu (0004000E...), ex. Blasters 2.0 = Moon Rabbit Crew."""
    return (title_id & 0x0000_0000_FFFF_FFFF) | 0x0004_000E_0000_0000
