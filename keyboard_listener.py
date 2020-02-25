from constants import Lanes, Spells, DEFAULT_INPUT_DELAY, Cooldowns

from pynput import keyboard
from threading import Lock
import time
from pynput.keyboard import Key, KeyCode, Listener
from threading import Lock
import time

class KeyboardListener(object):
    def __init__(self, callback, summoner_timers, spells_per_lane):
        self.callback = callback
        self.mappings = {
            '<shift>+z': 
                lambda: summoner_timers.add_timer(
                    Lanes.TOP, 
                    spells_per_lane[Lanes.TOP][0],
                    Cooldowns[spells_per_lane[Lanes.TOP][0]] - DEFAULT_INPUT_DELAY), 
            '<shift>+x': 
                lambda: summoner_timers.add_timer(
                    Lanes.JUNG, 
                    spells_per_lane[Lanes.JUNG][0], 
                    Cooldowns[spells_per_lane[Lanes.JUNG][0]] - DEFAULT_INPUT_DELAY),
            '<shift>+c': 
                lambda: summoner_timers.add_timer(
                    Lanes.MID, 
                    spells_per_lane[Lanes.MID][0], 
                    Cooldowns[spells_per_lane[Lanes.MID][0]] - DEFAULT_INPUT_DELAY),
            '<shift>+v': 
                lambda: summoner_timers.add_timer(
                    Lanes.BOT, 
                    spells_per_lane[Lanes.BOT][0], 
                    Cooldowns[spells_per_lane[Lanes.BOT][0]] - DEFAULT_INPUT_DELAY),
            '<shift>+b': 
                lambda: summoner_timers.add_timer(
                    Lanes.SUPP, 
                    spells_per_lane[Lanes.SUPP][0], 
                    Cooldowns[spells_per_lane[Lanes.SUPP][0]] - DEFAULT_INPUT_DELAY),
            '<alt>+z': 
                lambda: summoner_timers.add_timer(
                    Lanes.TOP, 
                    spells_per_lane[Lanes.TOP][1], 
                    Cooldowns[spells_per_lane[Lanes.TOP][1]] - DEFAULT_INPUT_DELAY), 
            '<alt>+x': 
                lambda: summoner_timers.add_timer(
                    Lanes.JUNG, 
                    spells_per_lane[Lanes.JUNG][1], 
                    Cooldowns[spells_per_lane[Lanes.JUNG][1]] - DEFAULT_INPUT_DELAY),
            '<alt>+c': 
                lambda: summoner_timers.add_timer(
                    Lanes.MID, 
                    spells_per_lane[Lanes.MID][1], 
                    Cooldowns[spells_per_lane[Lanes.MID][1]] - DEFAULT_INPUT_DELAY),
            '<alt>+v': 
                lambda: summoner_timers.add_timer(
                    Lanes.BOT, 
                    spells_per_lane[Lanes.BOT][1], 
                    Cooldowns[spells_per_lane[Lanes.BOT][1]] - DEFAULT_INPUT_DELAY),
            '<alt>+b': 
                lambda: summoner_timers.add_timer(
                    Lanes.SUPP, 
                    spells_per_lane[Lanes.SUPP][1], 
                    Cooldowns[spells_per_lane[Lanes.SUPP][1]] - DEFAULT_INPUT_DELAY),
            '=+\\': self.callback
        }

        self.listener = keyboard.GlobalHotKeys(self.mappings)
        self.listener.start()
    
    def pause(self):
        self.listener.stop()
    
    def unpause(self):
        self.listener = keyboard.GlobalHotKeys(self.mappings)
        self.listener.start()

    def stop(self):
        self.listener.stop()
        self.listener.join()
