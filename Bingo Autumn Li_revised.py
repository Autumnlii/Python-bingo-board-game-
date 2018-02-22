#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 18:35:37 2017

@author: Qiuying(Autumn) Li

"""
import numpy as np
from copy import deepcopy


""" Summary of the method:
    This code contains 4 methods: bingo_board, one_board, many_board, many_games
    1. bingo_board: check if a square is marked or not;
    2. one_board: simulate 9 times game on one board, return win_times;
    3. many_board: efficient way to generate random baord and marked board;
    4. many_games: generate n boards, for each board plays n*9 games, return
    board as array with max win_times
    
    Test tips: just click runing
    If time is limited, set a small number,for varibale 'num' in line 27
    I assume we can achieve more than 1 times of winning in one game（9 throws of dice)

"""

num = 100000    #record game playing times

def bingo_board(board, mark,dice_1,dice_2):
    """ bingo_board can check if a board square been marked or not
        board: randomly generated 3*3 board;
        mark: 3*3 matrix with 0, if been marked, 0 -> 1;
        dice_1, dice_2: random number from 1-6;
    
    Method description: 
        if the square is the multiple of total, mark the board, 0 -> 1 
        If the sqaure is been marked, choose another square
        If there are several multuple, choose random one

    arg: 
        total: total number of two dice
        counter: temporary 2D array, store index of squares need to be marked
        index: store random index for further marking, when several multiples
        lens: total number of possible multiple need to be marked
        
    for example: I go over the 3*3 baord at the beginning, to check the possile
    squares need to be marked, and sotre their index in the 'counter';
    if length of counter > 1, return random index and marked
    if lens == 1, mark the sqaure as where it should be 
    if lens == 0, no sqaure needed to be marked, do nothing
    
    return: mark, a matrix with marked sqaure, represented as 1
    
    raises: none know bugs
        
    """
    total = dice_1 + dice_2
    counter = [[]]
    index = 0
    for i in range(0,3):
        for j in range (0,3):
            if (board[i,j] % total == 0) and mark[i,j] == 0:
                counter.append([i,j])
            else:
                pass
    del counter[0]
    lens = len(counter)
#remark random multiples 
    if lens > 1:
        index = np.random.randint(0,lens)
        geo = counter[index]
        row = geo[0]
        col = geo[1]
        mark[row,col] = 1
   
    elif lens == 1:
        geo = counter[0]
        row = geo[0]
        col = geo[1]
        mark[row,col] = 1  
    else:
        pass
    return mark

def one_board(board,mark):
    """ one board: In one board with 9 times game, return number of win_times
        'board': the random board has been used
        'mark': a 0-1 matrix stands for marked square, 1 means makred
        def of win: any 3 continuous appearance of mark in row, col or diagnal
        1+1+1 =3, 3 stands for wining
        
    Method description:
        calculate the sum of each row, each col and diagnal of matrix:'mark'
        Store all the sums in a list: new_list
        Any 3 appears mean WIN
        Count number of 3 in the new_list, as number of win_times
    
    args: 
        col: sum of each cols of mark 
        row: sum of each rows of mark 
        sumDia: sum of diagnal of mark
    
    return: win_times, total numbers of 3 appears
    
    raises: none know bugs
        
    """
    col = [sum([row[i] for row in mark]) for i in range(0,len(mark[0]))]
    row = [sum(row) for row in mark]
    sumDia = sum(mark.diagonal())
    new_list = col + row
    new_list.append(sumDia)
    y = np.array(new_list)  #data structure transformation
    win_time = np.count_nonzero(y == 3)
    return (win_time)

def many_board():
    """many_board: generate 'num' of game boards and relative mark matrixes
    
    Method description: 
        generate 'num' of game board, and store all of them in 'boards'
        generate 'num' of mark matrix, and store all 'mark' in marks
        
    arg:
        boards: store all random baords
        marks: store all mark matrix
        
    return: boards and marks
    
    raises: none know bugs
    
    """    
    boards = []
    marks = []
    for k in range(num):
        board = np.random.randint(1, 20, (3, 3))
        mark = np.zeros((3,3))
        boards.append(board)
        marks.append(mark)
    return boards,marks

def many_games():
    """many_games: running 'num' games for each board, return max win and board
    
    Method description: 
        generate 'num' of boards and marks by calling 'many_board()'
        assume we run 'num' times of games
        each game should contain 9 throw of dices
        for each throw, we mark possible sqaures on 10000 boards 
        After 9 throws, we produced a marked matrix
        calculate number of win_times by calling 'bingo_board()', end 1st game
        we are into second game and so on...
        Running 1000 times of games, find out the max win_times and board
    
    args: 
        baord_copy: deep copy in order to reference, insert
        index: store the index of the max win_times
    
    return: 
        board_most: board with max win_times
        win_most: max win_times
        
    raises:
    time complexity! O(n^3) is too much.
    It should return a vector, but after transformation, it is still look like a matrix
    
    """

    boards,marks = many_board()
    marks_copy = deepcopy(marks)
    many_wintime = [0]*num  #record every board win time
    for k in range(num):  #for each game 
        marks = deepcopy(marks_copy) #clear marks, but keep winning times
        for i in range(9):
            dice_1 = np.random.randint(1,6)
            dice_2 = np.random.randint(1,6)
            for j in range(num):#for every board
                marks[j] = bingo_board(boards[j], marks[j],dice_1,dice_2) #update current board mark
                if i == 8:#end of this game after 9 throws
                    many_wintime[j] += one_board(boards[j],marks[j])#update this board wintime
    index = np.argmax(many_wintime)#find the most wintime index
    board_most = boards[index]
    win_most = many_wintime[index]
    #print('The most win board:\n',board_most)
    #print('The win time is:',win_most)
    return board_most, win_most

"""
test at here
"""
win_board,most_win = many_games()  
print('The most win board:\n',win_board)
print('The win time is:',most_win)

##transform a matrix to a vector list 
print('This is vector of a board: \n', np.squeeze(np.asarray(win_board)))
