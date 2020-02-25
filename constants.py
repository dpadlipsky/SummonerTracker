from enum import Enum, auto

DEFAULT_INPUT_DELAY = 10

class Lanes(Enum):
    TOP = auto()
    JUNG = auto()
    MID = auto()
    BOT = auto()
    SUPP = auto()

class Spells(Enum):
    F = auto()
    T = auto()
    H = auto()
    C = auto()
    G = auto()
    B = auto()
    E = auto()
    I = auto()

Cooldowns = {
    Spells.F : 300,
    Spells.T : 360,
    Spells.H : 240,
    Spells.C : 240,
    Spells.G : 180,
    Spells.B : 180,
    Spells.E : 210,
    Spells.I : 180
}

Spell_Names = {
    Spells.F : 'flash',
    Spells.T : 'tp',
    Spells.H : 'heal',
    Spells.C : 'cleanse',
    Spells.G : 'ghost',
    Spells.B : 'barrier',
    Spells.E : 'exhaust',
    Spells.I : 'ignite'
}
