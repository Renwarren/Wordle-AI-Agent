import pygame
from utility import *
from random import choice
from constants import * 
from solver import solver

pygame.init()
pygame.font.init()
pygame.display.set_caption("WORDLE SOLVER")

#----------------------------

DICT = slice_word(load_dict("words.txt"))
GUESSES = []
FEEDBACK = []
INDEX = 0
GAME_OVER = False
ANSWER = choice(slice_word(load_dict('words.txt')))
UNGUESSED = ALPHABET
INPUT = choice(slice_word(load_dict('words.txt')))

FONT = pygame.font.SysFont("free sans bold", SQ_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", SQ_SIZE//2)

agent = solver(INPUT,DICT)
#----------------------------
def draw_unguessed_letters():
    letters = FONT_SMALL.render(UNGUESSED,False,GREY)
    surface = letters.get_rect(center = (WIDTH//2,TOP_MARGIN//2))
    screen.blit(letters,surface)

def determine_unguessed_letters(guesses):
    guessed_letters = ''.join(guesses)
    unguessed_letters = ""
    for letter in ALPHABET:
        if letter not in guessed_letters:
            unguessed_letters = unguessed_letters + letter
    return unguessed_letters    

def determine_color(guess,position):
    letter = guess[position]
    if letter == ANSWER[position]:
        return GREEN
    elif letter in ANSWER:
        #We have to check for a specific occurence.
        #for example if ANSWER = JELLO, and we enter LLLLL, we expect GRAY-GRAY-GREEN-GREEN-GREY 
        n_target = ANSWER.count(letter)
        n_correct = 0
        n_occurence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= position:
                    n_occurence +=1
                if letter == ANSWER[i]:
                    n_correct +=1
        if n_target - n_correct - n_occurence >=0:
            return YELLOW
    return GREY

def draw_squares(y_begin,x_begin,sq_sz,GAME_OVER):
    y = y_begin +10
    for i in range(NUMBER_OF_GUESSES):
        x = x_begin
        for j in range(5):
            #square
            square = pygame.Rect(x,y,sq_sz,sq_sz)
            pygame.draw.rect(screen,GREY,square,width=2,border_radius=5)

            #letters that have been guessed
            if i < len(GUESSES):
                color = determine_color(GUESSES[i],j)
                pygame.draw.rect(screen,color,square,border_radius=5)
                letter = FONT.render(GUESSES[i][j], False,BLACK)
                surface = letter.get_rect(center = (x+sq_sz//2,y+sq_sz//2))
                screen.blit(letter,surface)

            #user text input(next guess)
            if i == len(GUESSES) and j < len(agent.guess):
                letter = FONT.render(agent.guess[j],False,GREY)
                surface = letter.get_rect(center = (x+sq_sz//2,y+sq_sz//2))
                screen.blit(letter,surface)

            x += sq_sz + MARGIN
        y += sq_sz + MARGIN

    #SHOW the correct answer if you lose
    if len(GUESSES) ==6 and GUESSES[5] != ANSWER:
        GAME_OVER = True
        letters = FONT.render(ANSWER,False,CERISE)
        surface = letters.get_rect(center = (WIDTH//2, HEIGHT - BOTTOM_MARGIN//2 - MARGIN))
        screen.blit(letters,surface)
    #CONGRATS USER
    elif GAME_OVER == True and len(GUESSES) <=6:
        letters = FONT.render("CONGRATS",False,CERISE)
        surface = letters.get_rect(center = (WIDTH//2, HEIGHT - BOTTOM_MARGIN//2 - MARGIN))
        screen.blit(letters,surface)

#create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#animation loop
ANIMATING = True
while ANIMATING:

    #background
    screen.fill("white")
    draw_unguessed_letters()
    draw_squares(TOP_MARGIN,SIDE_MARGIN,SQ_SIZE,GAME_OVER)
    

    #update the screen
    pygame.display.flip()

    #track user interactions
    for event in pygame.event.get():

        #closing the window
        if event.type == pygame.QUIT:
            ANIMATING = False
        #press some keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ANIMATING = False
            
            #return key to submit a guess
            elif event.key == pygame.K_RETURN:
                GUESSES.append(agent.guess)
                for j in range (5):
                    color = determine_color(GUESSES[INDEX],j)
                    FEEDBACK.append(color)
                INDEX +=1
                UNGUESSED = determine_unguessed_letters(GUESSES)
                if agent.guess == ANSWER:
                    GAME_OVER = True
                    agent.guess = ""
                    break
                else:
                    GAME_OVER = False
                print("Word to find:",ANSWER)
                vector = agent.get_frequency()
                agent.remove_words(FEEDBACK,vector)
                print(agent.guess_list)
                agent.choose_word()
                print('AI Guess is:',agent.guess)
                FEEDBACK = []

            
