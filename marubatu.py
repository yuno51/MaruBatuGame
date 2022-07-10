import numpy as np
import pygame
from pygame.locals import *
import win32gui
import time

#〇 => 1,人
#× => -1,CPU

class MaruBatu:
    def __init__(self,class_window):
        self.board = np.zeros((3,3))
        '''
        self.board[1][1] = 1 
        self.board[2][2] = -1
        self.board[1][2] = 1
        self.board[1][0] = -1
        '''        
        self.player = 1
        self.playable_list = np.full((3,3),True)
        self.window = class_window

    def game_end(self,board,player): #True => 終了
        sum3 = player*3
        if (board[0,:].sum() ==sum3 or board[1,:].sum() ==sum3 or board[2,:].sum() ==sum3 
        or board[:,0].sum() ==sum3 or board[:,1].sum() ==sum3 or board[:,2].sum() ==sum3 
        or np.diag(board).sum() ==sum3 or np.diag(np.fliplr(board)).sum() ==sum3):
            return True
        else:
            return False

    def draw(self):
        return np.all(self.board != 0)

    def strategy_human(self,board,player): #return 座標
        return self.window.mouse_event()

    def strategy_cpu(self, board, player, f):
        playable_list = np.argwhere(board == 0)
        point_list = []
        for [y,x] in playable_list:
            new_board = board.copy()
            new_board[y][x] = player
            if self.game_end(new_board, player):
                return [x,y, -3*player]
            playable_list = np.argwhere(new_board == 0)
            if len(playable_list) == 0:
                return [x,y,0]
            if f == np.argmax:
                g = np.argmin
            else:
                g = np.argmax
            
            point_list.append([x,y,self.strategy_cpu(new_board, 
            -1*player ,g)[-1]])
        point_list = np.random.permutation(np.array(point_list))
        index = f(point_list[:,2])
        return point_list[index]
  
    def set_symbol(self):
        while True:
            if self.player > 0:
                [x,y] = self.strategy_human(self.board, self.player)
            else:
                [x,y] = self.strategy_cpu(self.board, self.player, np.argmax)[:2]
                #[x,y] = self.strategy_human(self.board, self.player)
            
            if self.board[y][x] ==0:
                self.board[y][x] = self.player
                self.playable_list[y][x] = False
                break
            else:
                print("alredy exist")
        return x,y
    
    def print_data(self):
        print(self.board)
        print("{}さんの番です".format(self.player))

    def game(self):
        while True:
            self.print_data()
            x,y = self.set_symbol()
            self.window.blit(x,y, self.player)

            if self.game_end(self.board,self.player):
                break

            if self.draw():
                self.player = 0
                break
            self.player = -1 * self.player
        
        if self.player == 1:
            print("1の勝利")
        elif self.player == -1:
            print("-1の勝利")
        else:
            print("引き分け")



class Window:
    def __init__(self,pygame,screenSize):
        pygame.init()
        self.screenSize = screenSize

        wm_info = pygame.display.get_wm_info()
        handle = wm_info['window']
        win32gui.MoveWindow(handle,-10,0,1280,800,1)

        self.screen = pygame.display.set_mode(self.screenSize)                                                             
        pygame.display.set_caption("SoraProject")

        self.screen.fill((0,0,0))
        self.board_image = pygame.image.load("./board.png").convert()
        self.maru_image = pygame.image.load("./maru.png").convert()
        self.batu_image = pygame.image.load("./batu.png").convert()

        self.screen.blit(self.board_image,(0,0))
        pygame.display.update()
    
    def blit(self,x,y, player):
        position = (1+200*x, 1+200*y)
        if player == 1:
            self.screen.blit(self.maru_image, position)
        else:
            self.screen.blit(self.batu_image, position)
        pygame.display.update()
    def mouse_event(self):
        while True:
            for event in pygame.event.get():
    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()                                                       
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if 0<=y and y<=599:
                        return x//200, y//200
    


window = Window(pygame, (600,700))
game = MaruBatu(window)
game.game()        
time.sleep(1)

            