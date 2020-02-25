from constants import Spell_Names

from threading import Timer, Lock
from functools import total_ordering
from datetime import datetime, timedelta

class SummonerTimers(object):
    def __init__(self):
        self.timers = []
        self.lock = Lock()
        self.start_time = None
        self.message = []
    
    def add_timer(self, lane, spell, cd):
        if cd <= 0 or self.start_time is None:
            return

        self.lock.acquire()
        try:
            for timer in self.timers:
                if timer.lane == lane and timer.spell == spell:
                    return

            timer = SummonerTimer(lane, spell, datetime.now() + timedelta(seconds=cd), self.remove_timer)

            self.timers.append(timer)
            self.update_message()
        finally:
            self.lock.release()
    
    def remove_timer(self, timer):
        self.lock.acquire()
        try:
            self.timers.remove(timer)
            self.update_message()
        finally:
            self.lock.release()

    def reset_lane_timers(self, lane):
        self.lock.acquire()
        try:
            timers_to_remove = []
            for timer in self.timers:
                if timer.lane == lane:
                    timers_to_remove.append(timer)

            for timer in timers_to_remove:
                timer.stop_early()
                self.timers.remove(timer)
            
            self.update_message()
        finally:
            self.lock.release()
    
    def remove_all_timers(self):
        self.lock.acquire()
        try:
            for timer in self.timers:
                timer.stop_early()
            self.timers = []
            self.update_message()
        finally:
            self.lock.release()

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_message(self):
        return self.message.copy()

    def update_message(self):
        self.timers.sort()
        self.message = []

        last_lane = None

        if len(self.timers) != 0:
            self.message.append('----------')

        for timer in self.timers:
            same_as_last = False
            if timer.lane != last_lane:
                message_line = f'[{timer.lane.name}] '
            else:
                message_line = self.message[-1]
                same_as_last = True
            

            delta = int((timer.expiration_time - self.start_time).total_seconds())
            time_string = f'{delta // 60}:{"{:02d}".format(delta % 60)}'
            message_line += f'{Spell_Names[timer.spell]} {time_string} '

            last_lane = timer.lane

            if not same_as_last:
                self.message.append(message_line)
            else:
                self.message[-1] = message_line

@total_ordering
class SummonerTimer(object):
    def __init__(self, lane, spell, expiration_time, remove_func):
        self.lane = lane
        self.spell = spell
        self.expiration_time = expiration_time

        self.timer = Timer((expiration_time - datetime.now()).total_seconds(), remove_func, args=[self])
        self.timer.start()
    
    def stop_early(self):
        self.timer.cancel()

    def __eq__(self, other):
        return False

    def __lt__(self, other):
        if self.lane.value < other.lane.value:
            return True 
        elif self.lane.value > other.lane.value:
            return False
        
        if self.spell.value < other.spell.value:
            return True
        elif self.spell.value > other.spell.value:
            return False

        return False
