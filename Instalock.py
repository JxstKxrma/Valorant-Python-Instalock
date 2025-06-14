import pyautogui
import time
import keyboard
import os
import json
from pynput import keyboard as pynput_keyboard

AGENT_FILE = "agents.json"
SETTINGS_FILE = "settings.json"

default_settings = {
    "click_interval": 0.05,
    "wait_interval": 0.2,
    "start_keybind": "1",
    "lock_in_position": [0, 0]
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_agents():
    if os.path.exists(AGENT_FILE):
        with open(AGENT_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_agents(agents):
    with open(AGENT_FILE, 'w') as f:
        json.dump(agents, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    else:
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def wait_for_esc():
    """Blockiert und wartet auf Esc, ignoriert Fokus."""
    while True:
        if keyboard.is_pressed('esc'):
            time.sleep(0.3)
            break
        time.sleep(0.1)

def add_or_update_agent(agents):
    clear_screen()
    print("====== ADD AGENTS ======")
    print()
    print()
    print()
    print("Esc - Cancel and go back to the main menu")
    print()
    print()
    print()
    print("Hover your mouse over the agent and press enter.")
    pos = None
    while True:
        if keyboard.is_pressed('enter'):
            pos = pyautogui.position()
            time.sleep(0.3)  # Entprellen
            break
        if keyboard.is_pressed('esc'):
            time.sleep(0.3)
            return  # Abbrechen
        time.sleep(0.1)
    clear_screen()
    print(f"Position changed: {pos}")
    name = input("Enter a name for the agent: ").strip().lower()
    if name:
        agents[name] = {"agent_position": [pos[0], pos[1]]}
        save_agents(agents)
        print(f"Agent '{name}' Saved!")
    else:
        print("No name was given. Your agent wasn`t saved.")
    time.sleep(1)

def manage_agents(agents):
    while True:
        clear_screen()
        print("====== MANAGE AGENTS ======")
        if not agents:
            print("No agents saved.\n")
        else:
            print("Saved agents:")
            for i, name in enumerate(agents.keys(), start=1):
                print(f"{i}. {name.capitalize()}")
            print()
            print("---------------------------")
            print()
        print("1 - Create a new agent")
        print("2 - Delete agents\n")
        print()
        print("Esc - Go back to the main menu.")
        print()
        print()
        print()
        print("Choice: ", end='', flush=True)
        choice = ''
        while choice == '':
            if keyboard.is_pressed('esc'):
                time.sleep(0.3)
                return
            if keyboard.is_pressed('1'):
                choice = '1'
            elif keyboard.is_pressed('2'):
                choice = '2'
            time.sleep(0.1)
        print(choice)

        if choice == '1':
            add_or_update_agent(agents)
        elif choice == '2':
            if not agents:
                print("No agents to delete were found.")
                time.sleep(1)
                continue
            print("Which agent do you want to delete?")
            agent_names = list(agents.keys())
            for i, name in enumerate(agent_names, start=1):
                print(f"{i}. {name.capitalize()}")
            print("\nEsc - Go back to the main menu.")
            print("Agent number: ", end='', flush=True)
            del_choice = ''
            while del_choice == '':
                if keyboard.is_pressed('esc'):
                    time.sleep(0.3)
                    return
                for digit in map(str, range(1, len(agent_names) + 1)):
                    if keyboard.is_pressed(digit):
                        del_choice = digit
                time.sleep(0.1)
            print(del_choice)
            selected_agent = agent_names[int(del_choice) - 1]
            print(f"Are you sure that you want to delete '{selected_agent.capitalize()}'? (j/n)")
            confirm = ''
            while confirm not in ('j', 'n'):
                if keyboard.is_pressed('j'):
                    confirm = 'j'
                elif keyboard.is_pressed('n'):
                    confirm = 'n'
                time.sleep(0.1)
            print(confirm)
            if confirm == 'j':
                del agents[selected_agent]
                save_agents(agents)
                print(f"Agent '{selected_agent.capitalize()}' was deleted.")
                time.sleep(1)
            else:
                print("Deletion canceled")
                time.sleep(1)

def show_mouse_position():
    clear_screen()
    last_pos = None
    print("====== Show mouse position ======")
    print()
    print()
    print()
    print("Esc - Go back to the main menu.")
    print()
    print()
    print()
    print("Press Enter to set the mouse position")
    print()
    print("Mouse position:")
    print()
    while True:
        x, y = pyautogui.position()
        print(f"{x} , {y}    ", end='\r')
        if keyboard.is_pressed('enter'):
            last_pos = (x, y)
            time.sleep(0.3)
            break
        if keyboard.is_pressed('esc'):
            time.sleep(0.3)
            return
        time.sleep(0.1)

    if last_pos:
        clear_screen()
        print("====== Show mouse position ======")
        print()
        print()
        print("Esc - Go back to the main menu")
        print()
        print()
        print()
        print("Mouse position (set):")
        print()
        print(f"{last_pos[0]} , {last_pos[1]}")
        print()
        wait_for_esc()

def change_settings(settings):
    while True:
        clear_screen()
        print("====== SETTINGS ======")
        print()
        print()
        print()
        print(f"1 - Pause between the Instalock (current: {settings['click_interval']}s)")
        print(f"2 - Pause after the Instalock (current: {settings['wait_interval']}s)")
        print(f"3 - Start keybind (current: '{settings['start_keybind']}')")
        print(f"4 - Change Lock-In position (current: {tuple(settings['lock_in_position'])})")
        print()
        print("Esc - Go back to the main menu")
        print()
        print()
        print()
        print("Choice: ", end='', flush=True)
        choice = ''
        while choice == '':
            if keyboard.is_pressed('esc'):
                time.sleep(0.3)
                return
            for key in ('1','2','3','4'):
                if keyboard.is_pressed(key):
                    choice = key
            time.sleep(0.1)
        print(choice)

        if choice == '1':
            new_val = input("New pause between the Instalock in seconds: ").strip()
            try:
                settings['click_interval'] = float(new_val)
                save_settings(settings)
                print("Saved!")
            except:
                print("Invalid choice")
            time.sleep(1)

        elif choice == '2':
            new_val = input("New pause after the Instalock in seconds: ").strip()
            try:
                settings['wait_interval'] = float(new_val)
                save_settings(settings)
                print("Saved!")
            except:
                print("Invalid choice")
            time.sleep(1)

        elif choice == '3':
            new_key = input("New keybind for the start: ").strip().lower()
            if new_key:
                settings['start_keybind'] = new_key
                save_settings(settings)
                print("Gespeichert!")
            else:
                print("No changes made")
            time.sleep(1)

        elif choice == '4':
            clear_screen()
            print("Hover your mouse over the Lock-In Button and press Enter")
            keyboard.wait('enter')
            lock_in_position = pyautogui.position()
            settings["lock_in_position"] = [lock_in_position[0], lock_in_position[1]]
            save_settings(settings)
            print(f"Lock-In Position gespeichert: {lock_in_position}")
            time.sleep(1)

def instalock(agent_data, settings):
    print("Instalock is running. Press 'e' to pause/unpause, 'esc' to stop.")
    time.sleep(3)
    paused = False
    stop = False

    def on_press(key):
        nonlocal paused, stop
        try:
            if key.char and key.char.lower() == 'e':
                paused = not paused
                print("Paused." if paused else "Unpaused.")
        except AttributeError:
            if key == pynput_keyboard.Key.esc:
                stop = True

    listener = pynput_keyboard.Listener(on_press=on_press)
    listener.start()

    while not stop:
        if paused:
            time.sleep(0.1)
            continue

        pyautogui.moveTo(agent_data["agent_position"][0], agent_data["agent_position"][1], duration=0)
        pyautogui.click()
        time.sleep(settings["click_interval"])
        pyautogui.moveTo(settings["lock_in_position"][0], settings["lock_in_position"][1], duration=0)
        pyautogui.click()
        time.sleep(settings["click_interval"])
        time.sleep(settings["wait_interval"])

    listener.stop()

def menu():
    agents = load_agents()
    settings = load_settings()

    while True:
        clear_screen()
        print("====== VALORANT INSTALOCK TOOL ======")
        print()
        print()
        print()
        print("1 - Start Instalock")
        print("2 - Manage agents")
        print("3 - Show mouse position")
        print("4 - Settings")
        print()
        print()
        print()
        choice = input("Choice: ").strip().lower()

        if choice == '1':
            if not agents:
                print("No agents saved.")
                time.sleep(1)
                continue
            if settings["lock_in_position"] == [0, 0]:
                print("No Lock-In position saved.")
                time.sleep(1)
                continue
            print("Choose an agent:")
            agent_names = list(agents.keys())
            for i, name in enumerate(agent_names, start=1):
                print(f"{i}. {name.capitalize()}")
            selection = input("Agenten-Nummer: ").strip()
            if selection.isdigit() and 1 <= int(selection) <= len(agent_names):
                selected_agent = agent_names[int(selection) - 1]
                print(f"DrĆ¼cke '{settings['start_keybind']}' um zu starten.")
                while not keyboard.is_pressed(settings['start_keybind']):
                    time.sleep(0.1)
                instalock(agents[selected_agent], settings)
            else:
                print("Invalid choice.")
                time.sleep(1)

        elif choice == '2':
            manage_agents(agents)

        elif choice == '3':
            show_mouse_position()

        elif choice == '4':
            change_settings(settings)

        else:
            print("Invalid choice")
            time.sleep(1)

if __name__ == "__main__":
    menu()
