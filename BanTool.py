from nicegui import ui
import json

plats = []
name = ''
id = None
reason = ''
games = []
table_container = None

def set_plat(p):
    if {'platformID': id, 'platform': p} in plats:
        return
    plats.append({'platformID': id, 'platform': p})

def set_name(n):
    global name
    name = n

def set_id(i):
    global id
    id = int(i)

def set_reason(r):
    global reason
    reason = r

def set_game(g):
    if {'game': g} in games:
        return
    games.append({'game': g})

with open("globalBans.json", "r") as f:
    globalBans = json.load(f)

def save():
    with open("globalBans.json", "w") as f:
        json.dump(globalBans, f, indent=4)


def build_table():
    table_container.clear()

    with table_container:
        with ui.grid(columns=6).classes('w-full'):
            ui.label("Name")
            ui.label("Reason")
            ui.label("Platforms")
            ui.label("IDs")
            ui.label("Games")
            ui.label("")

            for ban in globalBans["bans"]:
                platforms = ", ".join(p["platform"] for p in ban["platforms"])
                ids = ", ".join(str(p["platformID"]) for p in ban["platforms"])
                games_list = ", ".join(g["game"] for g in ban["games"])
                ui.label(ban["username"])
                ui.label(ban["reason"])
                ui.label(platforms)
                ui.label(ids)
                ui.label(games_list)
                ui.button(
                    "UNANNIHILATE",
                    color="transparent",
                    on_click=lambda b=ban: unban(b)
                )

def unban(ban):
    globalBans["bans"].remove(ban)
    build_table()

def ban():
    global plats
    global games
    newBan = {
        'username': name,
        'reason': reason,
        'games': games,
        'platforms': plats
    }
    if (name == '' or reason == '' or games == [] or plats == []):
        ui.notify('error banning, something is empty!')
        return
    globalBans["bans"].append(newBan)

    plats = []
    games = []
    ui.notify("User has been ANNIHILATED")
    build_table()

def root():
    ui.add_head_html("""
    <style>
    /* Global hacker green background and text */
    body {
        background-color: #000000;
        color: #00ff00;
        font-family: monospace;
    }

    /* Labels and general text */
    div, span, label {
        color: #00ff00 !important;
    }

    /* Make all buttons green with black text and square */
    .q-btn {
        color: black !important;               /* black text */
        border: 1px solid #00ff00 !important;  /* optional green border */
        border-radius: 0 !important;           /* square corners */
    }

    /* Inputs */
    .q-field__control {
        background-color: black !important;
        border: 1px solid #00ff00 !important;
    }

    .q-field__native {
        color: #00ff00 !important;
    }

    .q-field__label {
        color: #00ff00 !important;
    }

    /* Tables */
    .q-table {
        color: #00ff00 !important;
    }
    .transparent-dropdown .q-field__inner {
        background-color: transparent !important;
    }
    .transparent-dropdown .q-menu {
        background-color: rgba(255, 255, 255, 0.5) !important; /* Semi-transparent panel */
        backdrop-filter: blur(5px); /* Optional: Adds a nice blur effect */
        box-shadow: none !important; /* Removes shadow */
    }
    </style> 
    """)

    ui.label('FUSION ANNIHILATE HACKER TOOL').classes('text-5xl mt-4 mb-2')

    name_input = ui.input("username", on_change=lambda e: set_name(e.value))
    reason_input = ui.input("reason", on_change=lambda e: set_reason(e.value))

    with ui.dropdown_button('Preset Reasons', auto_close=True, color="transparent"):
        ui.button('Alting', on_click=lambda e: reason_input.set_value("alting"), color="black")
        ui.button('Crashing Public Lobbies', on_click=lambda e: reason_input.set_value("Crashing Public Lobbies"), color="black")
        ui.button('NSFW Behavior', on_click=lambda e: reason_input.set_value("NSFW Behavior"),
                  color="black")
        ui.button('NSFW Media', on_click=lambda e: reason_input.set_value("NSFW Media"),
                  color="black")
        ui.button('Malicious Client Use', on_click=lambda e: reason_input.set_value("Malicious Client Use"), color="black")



    id_input = ui.input("id", on_change=lambda e: set_id(e.value))

    with ui.button_group():
        ui.button("Steam", on_click=lambda: set_plat("Steam"), color='transparent')
        ui.button("Epic", on_click=lambda: set_plat("Epic"), color='transparent')

    with ui.button_group():
        ui.button("BONELAB", on_click=lambda: set_game("BONELAB"), color='transparent')
        ui.button("BONEWORKS", on_click=lambda: set_game("BONEWORKS"), color='transparent')

    ui.button("ANNIHILATE", on_click=ban, color='transparent')
    ui.button("Save", on_click=save, color='transparent')
    global table_container
    table_container = ui.column()

    build_table()

ui.run(root())
