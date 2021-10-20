#!/usr/bin/env python3

import curses
from random import randint
from time import sleep

class Snake:
    def __init__(self, stdscr, size=10, speed=0.3, initial_size=4, highscores=[]):
        self.valid_inputs = {curses.KEY_UP: (
            0, -1), curses.KEY_DOWN: (0, 1), curses.KEY_RIGHT: (1, 1), curses.KEY_LEFT: (1, -1)}
        self.target = '🍎'
        self.initial_size = initial_size
        self.board_size = size
        self.speed = speed
        self.highscores = highscores
        self.stdscr = stdscr
        self.wipe()

    def start(self):
        while(self.alive):
            key = self.stdscr.getch()
            if(key in self.valid_inputs): 
                self.set_direction(key)
            self.move()

    def wipe(self):
        self.stdscr.nodelay(1)
        self.board = [
            ['  ']*self.board_size for _ in range(self.board_size)]
        self.body_coords = [[0, i] for i in range(self.initial_size)]
        # # the first element signifies whether it's an x or y translation 0: y 1: x
        # # the second element signifies direction 1: right/down -1: left/up
        self._add_target()
        self.direction = [0, 1]
        self.score = 0
        self.alive = True

    def move(self):
        new_head = self.body_coords[0][:]
        new_head[self.direction[0]] += self.direction[1]
        self.body_coords.insert(0, new_head)
        self._update_state()
        if(self.alive):
            self.body_coords.pop()
            head = self.body_coords[0][self.direction[0]]
            if(head < 0 or head > self.board_size-1):
                self.end()
            self._clear_board()
            if(list(self._apple_coords) in self.body_coords):
                self._level_up()
        self.redraw()

    def redraw(self):
        if(not self.alive): 
            self.stdscr.erase()
        top_border = '-'+'-—'*self.board_size
        self.stdscr.addstr(0, 1, top_border)
        self.stdscr.addstr(self.board_size+1, 1, top_border)
        for i in range(self.board_size):
            side_border = '| '
            self.stdscr.addstr(i+1, 2, ''.join(self.board[i]))
            self.stdscr.addstr(i+1, 0, side_border)
            if(i == 2 and self.alive):
                side_border += '\tScore: ' + str(self.score)
            self.stdscr.addstr(i+1, self.board_size*2+2, side_border)
            self.stdscr.refresh()
        sleep(self.speed)

    def end(self):
        self.highscores.append(self.score)
        self.highscores = sorted(list(set(self.highscores)), reverse=True)[:3]
        self.board = [
            ['  ']*self.board_size for _ in range(self.board_size)]
        self.board[3][3] = 'You lose'
        self.board[4][3] = 'Score = '+str(self.score)
        for i, x in enumerate(self.highscores):
            self.board[i+5][3] = f'{i+1}: {x}'
        self.board[9][2] = 'Play again? y/n'
        self.redraw()
        self.stdscr.nodelay(0)
        key = self.stdscr.getch()
        while(chr(key).lower() != 'y'):
            key = self.stdscr.getch()
            if(chr(key).lower() == 'n'):
                exit()
        self.wipe()
        self.start()

    def set_direction(self, key):
        idx = self.valid_inputs[key]
        if(idx[0] == self.direction[0] and idx[1] == -self.direction[1]):
            return
        self.direction[0] = idx[0]
        self.direction[1] = idx[1]

    def _add_target(self):
        free_spaces = self._generate_free_coords()
        self._apple_coords = free_spaces[randint(0, len(free_spaces)-1)]
        self.board[self._apple_coords[0]][self._apple_coords[1]] = self.target

    def _clear_board(self):
        for i in range(self.board_size):
            for x in range(len(self.board[i])):
                if(self.board[i][x] != self.target):
                    self.board[i][x] = '  '
        for j in range(len(self.body_coords)):
            curr = self.body_coords[j]
            if(j == 0):
                self.board[curr[0]][curr[1]] = '█ '
                continue
            self.board[curr[0]][curr[1]] = 'O '

    def _generate_free_coords(self):
        return [(i, x) for i in range(self.board_size)
                for x in range(len(self.board[i])) if([i, x] not in self.body_coords)]

    def _level_up(self):
        new_tail = self.body_coords[-1][:]
        new_tail[self.direction[0]] -= self.direction[1]
        self.body_coords.append(new_tail)
        self._add_target()
        self.score += 1

    def _update_state(self):
        head = self.body_coords[0]
        tail = self.body_coords[1:]
        self.alive = head not in tail
        if(not self.alive): 
            self.end()

def main(stdscr):
    stdscr.timeout(0)
    curses.curs_set(0)
    stdscr.refresh()
    snake = Snake(stdscr, size=12, speed=0.23)
    snake.start()

curses.wrapper(main)