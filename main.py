from copy import deepcopy
import curses
from random import randint
from time import sleep


class Snake:
    def __init__(self):
        self.valid_inputs = {curses.KEY_UP: (
            0, -1), curses.KEY_DOWN: (0, 1), curses.KEY_RIGHT: (1, 1), curses.KEY_LEFT: (1, -1)}
        self.board = [['  ']*12 for _ in range(12)]
        self.board[randint(0, len(self.board)-1)
                   ][randint(0, len(self.board)-1)] = '🍎'
        self.body_coords = [[0, i] for i in range(4)]
        self.direction = [0, 1]
        self.score = 0

    def is_alive(self):
        head = self.body_coords[0]
        tail = self.body_coords[1:]
        return head not in tail

    def set_direction(self, key):
        idx = self.valid_inputs[key]
        if(idx[0] == self.direction[0] and idx[1] == -self.direction[1]):
            return
        self.direction[0] = idx[0]
        self.direction[1] = idx[1]

    def clear_board(self):
        for i in range(len(self.board)):
            for x in range(len(self.board[i])):
                if(self.board[i][x] != '🍎'):
                    self.board[i][x] = '  '
        for j in self.body_coords:
            if(self.body_coords.index(j) == 0):
                self.board[j[0]][j[1]] = '█ '
                continue
            self.board[j[0]][j[1]] = 'O '

    def move(self):
        new_head = deepcopy(self.body_coords)[0]
        new_head[self.direction[0]] += self.direction[1]
        self.body_coords.insert(0, new_head)
        if(not self.is_alive()):
            exit()
        self.body_coords.pop()
        if(self.body_coords[0][self.direction[0]] < 0):
            self.body_coords[0][self.direction[0]] = len(self.board)-1
        elif(self.body_coords[0][self.direction[0]] > len(self.board)-1):
            self.body_coords[0][self.direction[0]] = 0
        self.clear_board()
        if(not any('🍎' in x for x in self.board)):
            self.score += 1
            new_tail = deepcopy(self.body_coords)[-1]
            new_tail[self.direction[0]] -= self.direction[1]
            self.body_coords.append(new_tail)
            free_spaces = [(i, x) for i in range(len(self.board))
                           for x in range(len(self.board[i])) if self.board[i][x] == '  ']
            new_apple_coords = free_spaces[randint(0, len(free_spaces)-1)]
            self.board[new_apple_coords[0]][new_apple_coords[1]] = '🍎'

    def redraw(self, stdscr):
        stdscr.addstr(0, 1, '-'+'-—'*len(self.board))
        stdscr.addstr(len(self.board)+1, 1, '-'+'-—'*len(self.board))
        for i in range(len(self.board)):
            base_str = '| '+''.join(self.board[i])+'|'
            if(i == 2):
                base_str += '\tScore: '+str(self.score)
            stdscr.addstr(i+1, 0, base_str)
            stdscr.refresh()


def main(stdscr):
    stdscr.timeout(0)
    curses.curs_set(0)
    stdscr.refresh()
    snake = Snake()
    while True:
        key = stdscr.getch()
        if(key in snake.valid_inputs):
            snake.set_direction(key)
        snake.move()
        snake.redraw(stdscr)
        sleep(0.23)


if __name__ == '__main__':
    curses.wrapper(main)
