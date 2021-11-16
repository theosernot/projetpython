#!/usr/bin/python3

# Copyright (c) 2017-2019 Samuel Thibault <samuel.thibault@ens-lyon.org>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Samuel Thibault ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import sys
import pygame
import select
import socket
import select
import socket
s = socket . socket ( socket . AF_INET6 , socket . SOCK_STREAM , 0)
s. setsockopt ( socket . SOL_SOCKET , socket . SO_REUSEADDR , 1)
s. bind (("", 9000) )
s. listen (1)
l = []
m = []
o = 0
j = []
dict = {}
dict2 = {}
dict3 = {}

map = [ [ ' ', ' ', ' ', ' ', 'V', ' ', ' ', ' ', ' ', ' ' ],
        [ ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ' ],
        [ ' ', 'X', ' ', ' ', ' ', 'S', ' ', ' ', 'X', ' ' ],
        [ ' ', 'X', ' ', 'X', ' ', 'X', 'X', ' ', 'X', 'M' ],
        [ 'W', 'X', ' ', 'X', 'A', 'X', 'X', ' ', 'X', ' ' ],
        [ ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X', ' ' ],
        [ ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ' ],
        [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ] ]

width = len(map[0])
height = len(map)

# This is the sprites size
unit = 64
grass = (0x00, 0x90, 0x00)
rock = (0x90, 0x90, 0x90)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode( (unit * width, unit * height) )

# Load resources
woman = pygame.image.load("image/woman.png")
woman_ghost = woman.copy()
woman_ghost.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
woman_coords = [ 0, 0 ]
man = pygame.image.load("image/man.png")
man_ghost = man.copy()
man_ghost.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
man_coords = [ 0, 0 ]

snake = pygame.image.load("image/snake.png")
snake_ghost = snake.copy()
snake_ghost.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
snake_coords = [ 0, 0 ]

stone = pygame.image.load("image/stone.png")
stone_coords = [ 0, 0 ]

apple = pygame.image.load("image/apple.png")
apple_coords = [ 0, 0 ]

meat = pygame.image.load("image/jambom.png")
meat_coords = [ 0, 0 ] 

woman_move = [ 0, 0 ]
man_move = [ 0, 0 ]
snake_move = [ 0, 0 ]
woman_newmove = [ 0, 0 ]

# Initialize positions
def init():
    def find(coords, c):
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == c:
                    coords[0] = x
                    coords[1] = y
                    return
        raise Exception('oops')

    find(woman_coords, 'W')
    find(man_coords, 'M')
    find(snake_coords, 'S')
    find(apple_coords, 'A')
    find(meat_coords, 'V')

init()


while True:
    c,b,n = select.select(l+[s],[],[])
    for i in c:
        if i == s:
            sc , a = s.accept()
            print("Nouveau joueur :", a)
            l.append(sc)
            m.append(sc.getpeername())
            o+=1
            ip=str(m[o-1][0])
            port=str(m[o-1][1])
            new = ("User " + "<" + ip + ">" + ":" + "<" + port + ">" + " connected\n")
            dict2[str(port)] = sc
            for k in l:
                if k != sc:
                    k.send(new.encode("utf-8"))
        
    e = pygame.event.wait()

    # Check for exit
    if e.type == pygame.QUIT:
        sys.exit()

    elif e.type == pygame.KEYDOWN:

    # Check for wowoman movements
        if e.key == pygame.K_z:
            woman_move = [ 0, -1 ]
            pass
        elif e.key == pygame.K_s:
            woman_move = [ 0, 1 ]
            pass
        elif e.key == pygame.K_q:
            woman_move = [ -1, 0 ]
            pass
        elif e.key == pygame.K_d:
            woman_move = [ 1, 0 ]
            pass

    # Check for man movements
        elif e.key == pygame.K_UP:
            man_move = [ 0, -1 ]
            pass
        elif e.key == pygame.K_DOWN:
            man_move = [ 0, 1 ]
            pass
        elif e.key == pygame.K_LEFT:
            man_move = [ -1, 0 ]
            pass
        elif e.key == pygame.K_RIGHT:
            man_move = [ 1, 0 ]
            pass

    # Check for serpent movements
        elif e.key == pygame.K_o:
            snake_move = [ 0, -1 ]
            pass
        elif e.key == pygame.K_l:
            snake_move = [ 0, 1 ]
            pass
        elif e.key == pygame.K_k:
            snake_move = [ -1, 0 ]
            pass
        elif e.key == pygame.K_m:
            snake_move = [ 1, 0 ]
            pass

    #else:
    #    print(e)

    def move(coords, move):
        return [ coords[0] + move[0], coords[1] + move[1] ]

    # Compute moves
    woman_newcoords = move(woman_coords, woman_move)
    man_newcoords = move(man_coords, man_move)
    snake_newcoords = move(snake_coords, snake_move)

    # But bound to window
    def bound(newcoords, coords, move):
        if newcoords[0] < 0 or newcoords[0] >= width or newcoords[1] < 0 or newcoords[1] >= height:
            # out of bounds
            newcoords[0] = coords[0]
            newcoords[1] = coords[1]
            move[0] = 0
            move[1] = 0

    bound(woman_newcoords, woman_coords, woman_move)
    bound(man_newcoords, man_coords, man_move)
    bound(snake_newcoords, snake_coords, snake_move)

    def collide(newcoords, coords, move):
        if map[newcoords[1]][newcoords[0]] == 'X':
            # Stone
            newcoords[0] = coords[0]
            newcoords[1] = coords[1]
            move[0] = 0
            move[1] = 0

    # Prevent collisions with stones
    collide(woman_newcoords, woman_coords, woman_move)
    collide(man_newcoords, man_coords, man_move)
    collide(snake_newcoords, snake_coords, snake_move)

    # Prevent collisions between players
    if woman_newcoords == man_newcoords:
        woman_newcoords = woman_coords
        woman_move = [ 0, 0 ]
        man_newcoords = man_coords
        man_move = [ 0, 0 ]

    # Make everybody move when everybody chose her/his direction
    if woman_move != [ 0, 0 ] and man_move != [ 0, 0 ] and snake_move != [ 0, 0]:
        woman_coords = woman_newcoords
        man_coords = man_newcoords
        snake_coords = snake_newcoords
        woman_move = [ 0, 0 ]
        man_move = [ 0, 0 ]
        snake_move = [ 0, 0 ]

    #print("woman at %u,%u to %u,%u" % (woman_coords[0], woman_coords[1], woman_newcoords[0], woman_newcoords[1]))
    #print("man at %u,%u to %u,%u" % (man_coords[0], man_coords[1], man_newcoords[0], man_newcoords[1]))
    #print("snake at %u,%u to %u,%u" % (snake_coords[0], snake_coords[1], snake_newcoords[0], snake_newcoords[1]))

    # Display everything
    screen.fill(grass)

    def blit(item, coords):
        screen.blit(item, (unit * coords[0], unit * coords[1]))

    # Display stones
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 'X':
                blit(stone, (x, y))

    # Display moving items
    blit(apple, apple_coords)
    blit(meat, meat_coords)

    blit(woman_ghost, woman_newcoords)
    blit(woman, woman_coords)
    blit(man_ghost, man_newcoords)
    blit(man, man_coords)

    blit(snake_ghost, snake_newcoords)
    blit(snake, snake_coords)

    # Show new state
    pygame.display.flip()

    if woman_coords == apple_coords:
        print("woman won!\n")
        sys.exit()
    elif man_coords == apple_coords:
        print("man won!\n")
        sys.exit()

    if woman_coords == snake_coords:
        print("woman lost!\n")
        sys.exit()

    elif man_coords == snake_coords:
        print("man lost!\n")
        sys.exit()

    if woman_coords == meat_coords:
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_z:
                woman_move = [ 0, -2 ]
                pass
            elif e.key == pygame.K_s:
                woman_move = [ 0, 2 ]
                pass
            elif e.key == pygame.K_q:
                woman_move = [ -2, 0 ]
                pass
            elif e.key == pygame.K_d:
                woman_move = [ 2, 0 ]
                pass
    bound(woman_newcoords, woman_coords, woman_move)
    collide(woman_newcoords, woman_coords, woman_move)
    if woman_newcoords == man_newcoords:
        woman_newcoords = woman_coords
        woman_move = [ 0, 0 ]
        man_newcoords = man_coords
        man_move = [ 0, 0 ]
    blit(woman_ghost, woman_newcoords)           
           
