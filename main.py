#!/usr/bin/env python3

from copy import deepcopy
import curses
from random import randint
from time import sleep


class Snake:
    def __init__(self, size=10, speed=0.3, initial_size=4):
        self.valid_inputs = {curses.KEY_UP: (
            0, -1), curses.KEY_DOWN: (0, 1), curses.KEY_RIGHT: (1, 1), curses.KEY_LEFT: (1, -1)}
        self.__board_size = size
        self.__board = [['  ']*size for _ in range(size)]
        self.__body_coords = [[0, i] for i in range(initial_size)]
        free_spaces = self._generate_free_coords()
        self._apple_coords = free_spaces[randint(0, len(free_spaces)-1)]
        self.__board[self._apple_coords[0]][self._apple_coords[1]] = '🍎'
        self.__direction = [0, 1]
        # the first element signifies whether it's an x or y translation 0: y 1: x
        # the second element signifies direction 1: right -1: left
        self.__speed = speed
        self.__score = 0
        self.alive = True

    def _generate_free_coords(self):
        return [(i, x) for i in range(self.__board_size)
                for x in range(len(self.__board[i])) if([i, x] not in self.__body_coords)]

    def _update_state(self):
        head = self.__body_coords[0]
        tail = self.__body_coords[1:]
        self.alive = head not in tail

    def set__direction(self, key):
        idx = self.valid_inputs[key]
        if(idx[0] == self.__direction[0] and idx[1] == -self.__direction[1]):
            return
        self.__direction[0] = idx[0]
        self.__direction[1] = idx[1]

    def _clear__board(self):
        for i in range(self.__board_size):
            for x in range(len(self.__board[i])):
                if(self.__board[i][x] != '🍎'):
                    self.__board[i][x] = '  '
        for j in self.__body_coords:
            if(self.__body_coords.index(j) == 0):
                self.__board[j[0]][j[1]] = '█ '
                continue
            self.__board[j[0]][j[1]] = 'O '

    def _level_up(self):
        new_tail = deepcopy(self.__body_coords)[-1]
        new_tail[self.__direction[0]] -= self.__direction[1]
        self.__body_coords.append(new_tail)
        free_spaces = self._generate_free_coords()
        self._apple_coords = free_spaces[randint(0, len(free_spaces)-1)]
        self.__board[self._apple_coords[0]][self._apple_coords[1]] = '🍎'
        self.__score += 1

    def move(self):
        new_head = deepcopy(self.__body_coords)[0]
        new_head[self.__direction[0]] += self.__direction[1]
        self.__body_coords.insert(0, new_head)
        self._update_state()
        if(self.alive):
            self.__body_coords.pop()
            if(self.__body_coords[0][self.__direction[0]] < 0):
                self.__body_coords[0][self.__direction[0]
                                      ] = self.__board_size-1
            elif(self.__body_coords[0][self.__direction[0]] > self.__board_size-1):
                self.__body_coords[0][self.__direction[0]] = 0
            self._clear__board()
            if(list(self._apple_coords) in self.__body_coords):
                self._level_up()

    def redraw(self, stdscr):
        if(not self.alive):
            stdscr.erase()
        top_border = '-'+'-—'*self.__board_size
        stdscr.addstr(0, 1, top_border)
        stdscr.addstr(self.__board_size+1, 1, top_border)
        for i in range(self.__board_size):
            side_border = '| '
            stdscr.addstr(i+1, 2, ''.join(self.__board[i]))
            stdscr.addstr(i+1, 0, side_border)
            if(i == 2 and self.alive):
                side_border += '\tScore: ' + str(self.__score)
            stdscr.addstr(i+1, self.__board_size*2+2, side_border)
            stdscr.refresh()
        sleep(self.__speed)

    def end(self):
        self.__board = [
            ['  ']*self.__board_size for _ in range(self.__board_size)]
        self.__board[3][3] = 'You lose'
        self.__board[4][3] = 'Score = '+str(self.__score)


def main(stdscr):
    stdscr.timeout(0)
    curses.curs_set(0)
    stdscr.refresh()
    snake = Snake(size=12, speed=0.23)
    while True:
        key = stdscr.getch()
        if(key in snake.valid_inputs):
            snake.set__direction(key)
        if(not snake.alive):
            snake.end()
        else:
            snake.move()
        snake.redraw(stdscr)


if(__name__ == '__main__'):
    curses.wrapper(main)
