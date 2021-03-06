"""Represents the machine that picks numbers"""

import random

from . import utils
from . import loggable
from .settings import SETTINGS as S


class Ball(object):
    """A ball representing a number in the game"""

    def __init__(self, number):
        """Initialise the ball"""
        self.number = number
        #
        # Get the name for this ball (eg B1, I20)
        number_lookup = S['card-numbers']
        for letter, col in zip('BINGO', sorted(number_lookup.keys())):
            numbers = number_lookup[col]
            if number in numbers:
                self.letter = letter
                self.col = col
                break
        else:
            raise ValueError('Could not locate details for {0}'.format(number))
        #
        self.full_name = '{0}{1}'.format(self.letter, self.number)


class BallMachine(utils.Drawable, loggable.Loggable):
    """A machine to pick balls at random"""

    def __init__(self, name, state):
        """Initialise the machine"""
        self.addLogger()
        self.name = name
        self.state = state
        #
        self.all_balls = [Ball(n) for n in S['machine-balls']]
        self.balls = []
        self.current_ball = None
        self.interval = self.initial_interval = S['machine-interval'] * 1000
        self.running = False
        #
        self.ui = self.create_ui()
        self.reset_machine()

    def create_ui(self):
        """Create the UI components"""
        components = utils.DrawableGroup()
        #
        self.current_ball_ui = utils.getLabel(
            'machine-ball',
            S['machine-ball-position'],
            '0'
        )
        components.append(self.current_ball_ui)
        #
        return components

    def start_machine(self):
        """Start the machine"""
        self.running = True
        self.state.add_generator('ball-machine', self.pick_balls())

    def stop_machine(self):
        """Stop the machine"""
        self.running = False

    def reset_machine(self):
        """Reset the machine"""
        self.running = False
        self.balls = list(self.all_balls)
        random.shuffle(self.balls)
        self.interval = self.initial_interval

    def pick_balls(self):
        """Pick the balls"""
        for ball in self.balls:
            self.set_current_ball(ball)
            #
            # Wait for next ball
            yield self.interval
            #
            # Wait until we are running
            if not self.running:
                yield 0

    def set_current_ball(self, ball):
        """Set the current ball"""
        self.log.info('Current ball is {0}'.format(ball))
        #
        self.current_ball = ball
        self.current_ball_ui.set_text(ball.full_name)

    def draw(self, surface):
        """Draw the machine"""
        self.ui.draw(surface)