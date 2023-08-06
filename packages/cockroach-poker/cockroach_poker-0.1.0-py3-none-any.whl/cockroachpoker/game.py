from itertools import repeat, cycle
from functools import reduce
from enum import Enum
from random import shuffle, choice

class Suit:
    BAT = 'BAT'
    RAT = 'RAT'
    TOAD = 'TOAD'
    SPIDER = 'SPIDER'
    STINKBUG = 'STINKBUG'
    SCORPION = 'SCORPION'
    FLY = 'FLY'
    COCKROACH = 'COCKROACH'

    values = (BAT, RAT, TOAD, SPIDER, STINKBUG, SCORPION, FLY, COCKROACH)

class Action:
    PLAY = 'PLAY'
    CALL_OR_PASS = 'CALL_OR_PASS'
    CALL = 'CALL'
    PASS = 'PASS'

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tabled = {}

    def __repr__(self):
        return 'Player(name={}, tabled={}, hand={})'.format(
                self.name, self.tabled, self.hand)

    def __eq__(self, other):
        return self.name == other.name and \
                self.hand == other.hand and \
                self.tabled == other.tabled

    def deal(self, card):
        self.hand.append(card)

class Game:
    def __init__(self):
        self.players = {}
        self.next = None
        self.from_players = []
        self.to_player = None
        self.card = None
        self.claim = None

    def join(self, name):
        self.players[name] = Player(name)

    def deal(self):
        deck=reduce(
                lambda a, x: a + x,
                (list(repeat(suit, 8)) for suit in Suit.values))
        shuffle(deck)
        hand_size = int(len(deck) / len(self.players))
        for c, p in zip(deck, cycle((p for n, p in self.players.items()))):
            p.deal(c)
        self.next = (choice(list(self.players.keys())), Action.PLAY)

    def table(self):
        played = {}
        if self.from_players:
            played['from'] = self.from_players
        if self.to_player:
            played['to'] = self.to_player
        if self.claim:
            played['claim'] = self.claim
        next = {}
        if self.next:
            next['player'] = self.next[0]
            next['action'] = self.next[1]
        return {
                'tabled': {p.name: p.tabled for n, p in self.players.items()},
                'played': played,
                'next': next
                }

    def next_player(self):
        return self.next 

    def play(self, from_player, to_player, card, claim):
        # TODO: check from_player was next
        # TODO: chack play is next action
        print('removing', card, 'from', sorted(self.players[from_player].hand))
        self.players[from_player].hand.remove(card)
        self.from_players.append(from_player)
        self.next = (to_player, Action.CALL_OR_PASS)
        self.to_player = to_player
        self.claim = claim
        self.card = card

    def call(self, agree):
        # TODO: check from_player was next
        # TODO: chack call is next action
        if (agree and self.claim == self.card) or \
                (not agree and self.claim != self.card):
            self.next = (self.from_players[-1], Action.PLAY)
            n = self.players[self.from_players[-1]].tabled.get(self.card, 0)
            self.players[self.from_players[-1]].tabled[self.card] = n + 1
            self.card = None
            self.claim = None
            self.from_players =[] 
            self.to_player = None
            return True
        else:
            self.next = (self.to_player, Action.PLAY)
            n = self.players[self.to_player].tabled.get(self.card, 0)
            self.players[self.to_player].tabled[self.card] = n + 1
            self.card = None
            self.claim = None
            self.from_players = []
            self.to_player = None
            return False

    def will_pass(self):
        self.next = (self.to_player, Action.PASS)
        return (self.card,
            set(self.players.keys()) -
            set(self.from_players) -
            set([self.to_player]))

    def pass_on(self, from_player, to_player, card, claim):
        # TODO: check from and card
        self.claim = claim
        self.from_players.append(from_player)
        self.to_player = to_player
        if len(self.from_players) < len(self.players) - 1:
            self.next = (to_player, Action.CALL_OR_PASS)
        else:
            self.next = (to_player, Action.CALL)

    def check_loser(self):
        for n, p in self.players.items():
            for s, c in p.tabled.items():
                if c == 4:
                    return n
        return None
