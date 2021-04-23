from random import randint
from numpy import argmax
import pygame
from time import sleep
import os
from pygame.locals import *


CANVAS_SIZE = (1300,1075)
BACKGROUND_COLOR = (255, 255, 255)
COLOR_ACTIVE = (151, 42, 73)
COLOR_INACTIVE = (0, 0, 0)
RECT_BOX = [950, 395, 100, 50]
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Participants:
    def __init__(self, screen):
        self.screen = screen
        self.name_participant = []
        self.participant_score = []
        self.num_of_participants = 2
        self.text = ""
        self.activity = False
        self.color = COLOR_INACTIVE
        self.rect = pygame.Rect(RECT_BOX[0], RECT_BOX[1], RECT_BOX[2], RECT_BOX[3])


    def num_participants(self):

        run_loop = True

        while run_loop:

            game_name = pygame.font.SysFont('arial', 50).render("Snakes N Ladders", True, (0,0,0))
            self.screen.blit(game_name, (150, 150, 500, 50))
            enter_count = pygame.font.SysFont('arial', 50).render("Please enter the count of participants (2-8) : ", False, (0,0,0))
            self.screen.blit(enter_count, (150, 390, 500, 50))
            pygame.display.update()
            
            rectangle = pygame.draw.rect(self.screen, self.color, RECT_BOX, 2)

            for event in pygame.event.get():

                self.color = COLOR_ACTIVE if self.activity else COLOR_INACTIVE

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rectangle.collidepoint(event.pos):
                        self.activity = True
                    else:
                        self.activity = False

                elif event.type == pygame.KEYDOWN:

                    if self.activity:

                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                                                    
                        elif event.key == pygame.K_RETURN:
                            run_loop = False
                            if self.text:
                                if 1 < int(self.text[0]) < 9:
                                    self.num_of_participants = int(self.text[0])
                                self.text = ""

                        elif (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
                            run_loop = False
                            exit()
                        
                        else:
                            self.text += event.unicode
                            
                        
                        self.text_decoration(self.text, (rectangle.x + 10, rectangle.y))

                    elif (event.key == pygame.K_ESCAPE):
                        run_loop = False
                        exit()

            pygame.display.update() 

        
    def text_decoration(self, sentence, dimensions):
        self.screen.fill(BACKGROUND_COLOR)
        sent = pygame.font.SysFont('arial', 42).render(self.text, True, self.color)
        RECT_BOX[2] = max (100, sent.get_width()+20)
        self.screen.blit(sent, dimensions)


    def game_participants(self):
        
        for current_participant in range (1, self.num_of_participants+1):

            run_loop = True

            while run_loop:

                game_name = pygame.font.SysFont('arial', 50).render("Snakes N Ladders", True, (0,0,0))
                self.screen.blit(game_name, (150, 150, 500, 50))
                enter_count = pygame.font.SysFont('arial', 50).render(f"Please enter the name of {current_participant} participant : ", False, (0,0,0))
                self.screen.blit(enter_count, (150, 390, 500, 50))
                pygame.display.update()
                
                rectangle = pygame.draw.rect(self.screen, self.color, RECT_BOX, 2)

                for event in pygame.event.get():

                    self.color = COLOR_ACTIVE if self.activity else COLOR_INACTIVE

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if rectangle.collidepoint(event.pos):
                            self.activity = True
                        else:
                            self.activity = False

                    elif event.type == pygame.KEYDOWN:

                        if self.activity:

                            if event.key == pygame.K_BACKSPACE:
                                self.text = self.text[:-1]
                                                        
                            elif event.key == pygame.K_RETURN:
                                run_loop = False
                                self.name_participant.append(self.text)
                                self.participant_score.append(1)
                                self.text = ""

                            elif (event.key == pygame.K_ESCAPE):
                                run_loop = False
                                exit()

                            else:
                                self.text += event.unicode
                            
                            self.text_decoration(self.text, (rectangle.x + 10, rectangle.y))

                        elif (event.key == pygame.K_ESCAPE):
                            run_loop = False
                            exit()

                pygame.display.update()

class Ladders:
    def __init__(self):
        pass

    @staticmethod
    def ladder_positions(position):
        if position == 2: return 19
        elif position == 11: return 31
        elif position == 27: return 47
        elif position == 39: return 41
        elif position == 45: return 66
        elif position == 50: return 52
        elif position == 57: return 62
        elif position == 60: return 80
        elif position == 70: return 88
        elif position == 76: return 96
        elif position > 100: return 0
        else: return 0

class Snakes:
    def __init__(self):
        pass

    @staticmethod
    def snake_positions(position):
        if position == 16: return 8
        elif position == 21: return 18
        elif position == 35: return 23
        elif position == 48: return 29
        elif position == 58: return 39
        elif position == 67: return 51
        elif position == 87: return 65
        elif position == 93: return 71
        elif position == 98: return 78
        elif position > 100: return 0
        else: return 0

class Dice:
    def __init__(self):
        pass

    @staticmethod
    def dice_roller():
        return randint(1,6)

class Game():

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Snake and Ladder    ---deepspraj")
        self.game_canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.game_image = self.apple_block = pygame.image.load(os.path.join(BASE_DIR, 'resources/main_face_2_600x600.jpg')).convert()
        self.game_canvas.fill(BACKGROUND_COLOR)
        self.winner = "None"
        self.last_tile = 100
        self.participants = Participants(self.game_canvas)
        self.dice_face = 0
        self.current_playing_player = 0

    def draw_board(self):
        self.game_canvas.fill(BACKGROUND_COLOR)
        self.game_canvas.blit(self.game_image, (50, 60))

    def play_game(self):
        
        end_game = False
        previous_chance_over = False

        self.game_statistics()

        while not end_game:          

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        
                        self.dice_face = Dice.dice_roller()

                        if self.dice_face <= (self.last_tile - self.participants.participant_score[self.current_playing_player]):
                            self.participants.participant_score[self.current_playing_player] += self.dice_face
                            

                            self.game_statistics()

                            assistance = Ladders.ladder_positions(self.participants.participant_score[self.current_playing_player])
                            if assistance:
                                ladder_status = pygame.font.SysFont('arial', 20).render(f'{self.participants.name_participant[self.current_playing_player]} was at {self.participants.participant_score[self.current_playing_player]} and took ladder now at {assistance}', False, COLOR_INACTIVE)
                                self.game_canvas.blit(ladder_status, (800, 500, 500, 70))
                                pygame.display.update()
                                self.participants.participant_score[self.current_playing_player] = assistance


                            assistance = Snakes.snake_positions(self.participants.participant_score[self.current_playing_player])
                            if assistance:
                                snake_status = pygame.font.SysFont('arial', 20).render(f'{self.participants.name_participant[self.current_playing_player]} was at {self.participants.participant_score[self.current_playing_player]} and snake bite now at {assistance}', False, COLOR_INACTIVE)
                                self.game_canvas.blit(snake_status, (800, 500, 500, 70))
                                pygame.display.update()
                                self.participants.participant_score[self.current_playing_player] = assistance

                    elif event.key == pygame.K_ESCAPE:
                        exit()

                    previous_chance_over = True

                for i in range (self.participants.num_of_participants):
                    if self.participants.participant_score[i] == 100:
                        end_game = True

                if previous_chance_over:

                    if self.current_playing_player < self.participants.num_of_participants-1:
                        self.current_playing_player += 1
                    elif self.current_playing_player == self.participants.num_of_participants-1:
                        self.current_playing_player = 0
                    
                    
                    previous_chance_over = False

                if end_game:
                    break   
                
    def game_statistics(self):
        self.game_canvas.fill(BACKGROUND_COLOR)
        self.draw_board()
        dice_display = pygame.font.SysFont('arial', 50).render(f"{self.participants.name_participant[self.current_playing_player]}'s dice was {self.dice_face}", False, (0,0,0))
        self.game_canvas.blit(dice_display, (800, 600, 100, 50))

        for i in range (self.participants.num_of_participants):
            score = pygame.font.SysFont('arial', 30).render(f"{self.participants.name_participant[i]} : {self.participants.participant_score[i]}", False, (0,0,0))
            self.game_canvas.blit(score, (1000, 70 +(40*i), 100, 50))

        pygame.display.flip()

    def winner_declare(self):
        self.game_canvas.fill(BACKGROUND_COLOR)
        winner_display = pygame.font.SysFont('arial', 50).render("Congratssss.....", False, (0,0,0))
        self.game_canvas.blit(winner_display, (100, 200, 100, 50))

        winner_display = pygame.font.SysFont('arial', 50).render(f"Winner is {str(self.participants.name_participant[argmax(self.participants.participant_score)])}", False, (0,0,0))
        self.game_canvas.blit(winner_display, (100, 250, 100, 50))
        pygame.display.flip()
        sleep(5)

    def game_start(self):
        self.current_playing_player = 0
        end_game = False

        self.participants.num_participants()

        self.participants.game_participants()

        self.play_game()

        self.winner_declare()
    
if __name__ == "__main__":

    game = Game()
    game.game_start()