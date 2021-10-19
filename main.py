#!/usr/bin/env python3

import curses
from random import randint
from time import sleep


class Snake:
    def __init__(self, stdscr, size=10, speed=0.3, initial_size=4, highscores=[]):
        self.valid_inputs = {curses.KEY_UP: (
            0, -1), curses.KEY_DOWN: (0, 1), curses.KEY_RIGHT: (1, 1), curses.KEY_LEFT: (1, -1)}
        self.__target = '🍎'
        self.__initial_size = initial_size
        self.__board_size = size
        self.__speed = speed
        self.highscores = highscores
        self.__board = [
            ['  ']*self.__board_size for _ in range(self.__board_size)]
        self.__body_coords = [[0, i] for i in range(self.__initial_size)]
        self._add_target()
        self.__direction = [0, 1]
        self.stdscr = stdscr
        # the first element signifies whether it's an x or y translation 0: y 1: x
        # the second element signifies direction 1: right -1: left
        self.__score = 0
        self.alive = True

    def start(self):
        while(self.alive):
            key = self.stdscr.getch()
            if(key in self.valid_inputs): self.set_direction(key)
            self.move()

    def wipe(self):
        self.stdscr.nodelay(1)
        self.__board = [
            ['  ']*self.__board_size for _ in range(self.__board_size)]
        self.__body_coords = [[0, i] for i in range(self.__initial_size)]
        self._add_target()
        self.__direction = [0, 1]
        self.__score = 0
        self.alive = True

    def move(self):
        new_head = self.__body_coords[0][:]
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
            self._clear_board()
            if(list(self._apple_coords) in self.__body_coords):
                self._level_up()
        self.redraw()

    def redraw(self):
        if(not self.alive):
            self.stdscr.erase()
        top_border = '-'+'-—'*self.__board_size
        self.stdscr.addstr(0, 1, top_border)
        self.stdscr.addstr(self.__board_size+1, 1, top_border)
        for i in range(self.__board_size):
            side_border = '| '
            self.stdscr.addstr(i+1, 2, ''.join(self.__board[i]))
            self.stdscr.addstr(i+1, 0, side_border)
            if(i == 2 and self.alive):
                side_border += '\tScore: ' + str(self.__score)
            self.stdscr.addstr(i+1, self.__board_size*2+2, side_border)
            self.stdscr.refresh()
        sleep(self.__speed)

    def end(self):
        self.highscores.append(self.__score)
        self.highscores = sorted(list(set(self.highscores)), reverse=True)[:3]
        self.__board = [
            ['  ']*self.__board_size for _ in range(self.__board_size)]
        self.__board[3][3] = 'You lose'
        self.__board[4][3] = 'Score = '+str(self.__score)
        for i, x in enumerate(self.highscores):
            self.__board[i+5][3] = f'{i+1}: {x}'
        self.__board[9][2] = 'Play again? y/n'
        self.redraw()
        self.stdscr.nodelay(0)
        key = self.stdscr.getch()
        if(key == 121): self.wipe()
        else: exit()

    def set_direction(self, key):
        idx = self.valid_inputs[key]
        if(idx[0] == self.__direction[0] and idx[1] == -self.__direction[1]):
            return
        self.__direction[0] = idx[0]
        self.__direction[1] = idx[1]

    def _add_target(self):
        free_spaces = self._generate_free_coords()
        self._apple_coords = free_spaces[randint(0, len(free_spaces)-1)]
        self.__board[self._apple_coords[0]
                     ][self._apple_coords[1]] = self.__target

    def _clear_board(self):
        for i in range(self.__board_size):
            for x in range(len(self.__board[i])):
                if(self.__board[i][x] != self.__target):
                    self.__board[i][x] = '  '
        for j in self.__body_coords:
            if(self.__body_coords.index(j) == 0):
                self.__board[j[0]][j[1]] = '█ '
                continue
            self.__board[j[0]][j[1]] = 'O '

    def _generate_free_coords(self):
        return [(i, x) for i in range(self.__board_size)
                for x in range(len(self.__board[i])) if([i, x] not in self.__body_coords)]

    def _level_up(self):
        new_tail = self.__body_coords[-1][:]
        new_tail[self.__direction[0]] -= self.__direction[1]
        self.__body_coords.append(new_tail)
        self._add_target()
        self.__score += 1

    def _update_state(self):
        head = self.__body_coords[0]
        tail = self.__body_coords[1:]
        self.alive = head not in tail
        if(not self.alive): self.end()

def main(stdscr):
    stdscr.timeout(0)
    curses.curs_set(0)
    stdscr.refresh()
    snake = Snake(stdscr, size=12, speed=0.15)
    snake.start()

if(__name__ == '__main__'):
    curses.wrapper(main)
