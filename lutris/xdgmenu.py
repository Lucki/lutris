"""Get games available from the XDG menu"""
import xdg.Menu
import locale

IGNORED_ENTRIES = ["lutris", "mame", "dosbox", "steam"]

locale._strxfrm = locale.strxfrm


def strxfrm(s):
    """Monkey patch to address an encoding bug in pyxdg (fixed in current trunk)"""
    return locale._strxfrm(s.encode('utf-8'))
locale.strxfrm = strxfrm


def get_xdg_games():
    """Return list of games stored in the XDG menu."""
    cache = xdg.Menu.parse()
    game_menu = [entry
                 for entry in cache.getEntries() if str(entry) == "Games"][0]
    xdg_games = []
    for game in game_menu.getEntries():
        if not isinstance(game, xdg.Menu.MenuEntry):
            continue
        entry_name = str(game)[:-(len(".desktop"))]
        if entry_name in IGNORED_ENTRIES:
            continue
        desktop_entry = game.DesktopEntry
        game_name = unicode(desktop_entry)
        exe = desktop_entry.getExec()
        xdg_games.append((game_name, exe))
    return xdg_games
