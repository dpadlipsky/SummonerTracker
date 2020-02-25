from constants import Lanes, Spells, Cooldowns, Spell_Names
from summoner_timer import SummonerTimers
from file_handler import FileModifiedHandler
from keyboard_listener import KeyboardListener

import time

from tailer import tail
from datetime import datetime, timedelta
from pynput import keyboard

FULL_PATH = "C:\\Riot Games\\League of Legends\\MyNotes.txt"
DIRECTORY_PATH = "C:\\Riot Games\\League of Legends"
FILE_NAME = "MyNotes.txt"

summoner_timers = SummonerTimers()
controller = keyboard.Controller()

def custom_type(controller, string, delay):
    for character in string:
        controller.press(character)
        controller.release(character)
        time.sleep(delay)

def type_line(controller, string, delay):
    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)
    time.sleep(delay)
    custom_type(controller, string, delay)
    time.sleep(delay)
    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)

def execute():
    global listener
    print("Executing")
    listener.pause()
    time.sleep(.0001)
    for line in summoner_timers.get_message():
        type_line(controller, line, .000001)
    listener.unpause()

valid_1 = ['START', 'RESET', 'SUM', 'SET']
valid_roles = ['TOP', 'JUNG', 'MID', 'BOT', 'SUPP']
valid_spells = ['F', 'T', 'H', 'C', 'G', 'I', 'E', 'B']

spells_per_lane = {
    Lanes.TOP: (Spells.F, Spells.T),
    Lanes.JUNG: (Spells.F, Spells.C),
    Lanes.MID: (Spells.F, Spells.I),
    Lanes.BOT: (Spells.F, Spells.H),
    Lanes.SUPP: (Spells.F, Spells.I),
}

def callback():
    try:
        line = tail(open(FULL_PATH), lines=1)[-2]
        line = line.upper().split()
        
        if len(line) <= 0:
            return

        if not line[0] in valid_1:
            return
        
        if line[0] == 'START':
            start_time = datetime.now() - timedelta(seconds=int(line[1]))
            summoner_timers.set_start_time(start_time)
            summoner_timers.remove_all_timers()

        elif line[0] == 'RESET':
            if line[1] not in valid_roles:
                return
            
            lane = Lanes[line[1]]
            summoner_timers.reset_lane_timers(lane)

        elif line[0] == 'SET':
            if line[1] not in valid_roles or line[2] not in valid_spells:
                return

            lane = Lanes[line[1]]
            spell = Spells[line[2]]
            diff = int(line[3])
            cd = Cooldowns[spell] - diff
            summoner_timers.add_timer(lane, spell, cd)

        elif line[0] == 'SUM':
            if line[1] not in valid_roles or line[2] not in valid_spells or line[3] not in valid_spells:
                return

            lane = Lanes[line[1]]
            spell1 = Spells[line[2]]
            spell2 = Spells[line[3]]
            spells_per_lane[lane] = (spell1, spell2)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    global listener
    file_handler = FileModifiedHandler(DIRECTORY_PATH, FILE_NAME, callback)
    listener = KeyboardListener(execute, summoner_timers, spells_per_lane)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        file_handler.stop()
        listener.stop()
