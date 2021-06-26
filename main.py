#!/usr/bin/env python3

from copy import deepcopy
import curses
from random import randint
from time import sleep


class Snake:
    def __init__(self, size=10, speed=0.3, initial_size=4):
        self.valid_inputs = {curses.KEY_UP: (
            0, -1), curses.KEY_DOWN: (0, 1), curses.KEY_RIGHT: (1, 1), curses.KEY_LEFT: (1, -1)}
        self._board_size = size
        self._board = [['  ']*size for _ in range(size)]
        self._apple_coords = [
            randint(0, self._board_size-1), randint(0, self._board_size-1)]
        self._board[self._apple_coords[0]
                    ][self._apple_coords[1]] = '🍎'
        self._body_coords = [[0, i] for i in range(initial_size)]
        self._direction = [0, 1]
        self._speed = speed
        self._initial_size = initial_size
        self._score = 0
        self.alive = True

    def _update_state(self):
        head = self._body_coords[0]
        tail = self._body_coords[1:]
        self.alive = head not in tail

    def set_direction(self, key):
        idx = self.valid_inputs[key]
        if(idx[0] == self._direction[0] and idx[1] == -self._direction[1]):
            return
        self._direction[0] = idx[0]
        self._direction[1] = idx[1]

    def _clear_board(self):
        for i in range(self._board_size):
            for x in range(len(self._board[i])):
                if(self._board[i][x] != '🍎'):
                    self._board[i][x] = '  '
        for j in self._body_coords:
            if(self._body_coords.index(j) == 0):
                self._board[j[0]][j[1]] = '█ '
                continue
            self._board[j[0]][j[1]] = 'O '

    def _level_up(self):
        new_tail = deepcopy(self._body_coords)[-1]
        new_tail[self._direction[0]] -= self._direction[1]
        self._body_coords.append(new_tail)
        free_spaces = [(i, x) for i in range(self._board_size)
                       for x in range(len(self._board[i])) if(self._board[i][x] == '  ')]
        self._apple_coords = free_spaces[randint(0, len(free_spaces)-1)]
        self._board[self._apple_coords[0]][self._apple_coords[1]] = '🍎'
        self._score += 1

    def move(self):
        new_head = deepcopy(self._body_coords)[0]
        new_head[self._direction[0]] += self._direction[1]
        self._body_coords.insert(0, new_head)
        self._update_state()
        if(self.alive):
            self._body_coords.pop()
            if(self._body_coords[0][self._direction[0]] < 0):
                self._body_coords[0][self._direction[0]] = self._board_size-1
            elif(self._body_coords[0][self._direction[0]] > self._board_size-1):
                self._body_coords[0][self._direction[0]] = 0
            self._clear_board()
            if(list(self._apple_coords) in self._body_coords):
                self._level_up()

    def redraw(self, stdscr):
        if(not self.alive):
            stdscr.erase()
        top_border = '-'+'-—'*self._board_size
        stdscr.addstr(0, 1, top_border)
        stdscr.addstr(self._board_size+1, 1, top_border)
        for i in range(self._board_size):
            side_border = '| '
            stdscr.addstr(i+1, 2, ''.join(self._board[i]))
            stdscr.addstr(i+1, 0, side_border)
            if(i == 2 and self.alive):
                side_border += '\tScore: ' + str(self._score)
            stdscr.addstr(i+1, self._board_size*2+2, side_border)
            stdscr.refresh()
        sleep(self._speed)

    def end(self):
        self._board = [
            ['  ']*self._board_size for _ in range(self._board_size)]
        self._board[self._board_size//4][self._board_size//4] = 'You lose'
        self._board[self._board_size//4+1][self._board_size //
                                           4] = 'Score = '+str(self._score)


def main(stdscr):
    stdscr.timeout(0)
    curses.curs_set(0)
    stdscr.refresh()
    snake = Snake(size=12, speed=0.23)
    while True:
        key = stdscr.getch()
        if(key in snake.valid_inputs):
            snake.set_direction(key)
        if(not snake.alive):
            snake.end()
        else:
            snake.move()
        snake.redraw(stdscr)


if(__name__ == '__main__'):
    curses.wrapper(main)
