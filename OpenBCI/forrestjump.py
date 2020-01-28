# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":

    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

    # -*- coding: utf-8 -*-
    import pygame
    import random
    import datetime
    import time
    #from pyOpenBCI import OpenBCIGanglion
    import multiprocessing as mp
    #from psychopy import event, visual
    #import filterlib as flt
    #import blink as blk

    #global mac_adress
    #mac_adress = 'd2:b4:11:81:48:ad'


    #stałe
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 300
    ROAD_HEIGHT = 270
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FPS = 25
    FORREST_POS_X = 70
    FORREST_POS_Y = ROAD_HEIGHT - 90
    LAWKA_POS_Y = ROAD_HEIGHT - 20

    pygame.init()
    gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Forrest Jump Game")
    clock = pygame.time.Clock()

    #dźwięki
    dieSound = pygame.mixer.Sound("sounds/ohno.wav")
    checkpointSound = pygame.mixer.Sound("sounds/checkPoint.wav")
    backgroundSound = pygame.mixer.music.load("sounds/sweethomeMP3.mp3")
    pygame.mixer.music.play(-1)

    #grafiki
    road1 = pygame.image.load("graphics/chodnik2.0.png")
    road2 = pygame.image.load("graphics/chodnik2.0.png")

    forrest_list = []
    forrest_list.append(pygame.image.load("graphics/forrest do gry 2.png")) #0
    forrest_list.append(pygame.image.load("graphics/Forrest do gry.png")) #1
    forrest_list.append(pygame.image.load("graphics/Forrest do gry 1.png")) #2
    forrest_list.append(pygame.image.load("graphics/forrest do gry 2.png")) #3
    run_indx = 1

    lawka_list = []
    lawka_list.append(pygame.image.load("graphics/ławka0.png")) #0
    lawka_list.append(pygame.image.load("graphics/ławka0.png")) #1
    lawka_list.append(pygame.image.load("graphics/ławka0.png")) #2
    lawka_list.append(pygame.image.load("graphics/ławka0.png")) #3
    background = pygame.image.load('graphics/park.jpg')

    road1_pos_x = 0
    road2_pos_x = 500

    speed_was_up = True
    clear_game = True
    game_on = False
    lost_game = True
    forrest_jump = False
    jump_height = 7
    points = 0

    frames_since_lawka = 0
    gen_lawka_time = 50

    #napisy
    font = pygame.font.Font('freesansbold.ttf', 18)
    points_font = pygame.font.Font('freesansbold.ttf', 12)
    startScreen = font.render('JUMP FORREST JUMP', True, BLACK, WHITE)
    startScreenRect = startScreen.get_rect()
    startScreenRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)


    #MRUGANIE
    gra_trwa = True
    while gra_trwa:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_program.set()
                    gra_trwa = False

        if blink.value == 1 and forrest_jump == False and lost_game==False::
            game_on = True
            forrest_jump = True
            blink.value = 0
        if lost_game == True and blink.value ==1:
            time.sleep(1)
            clear_game = True
            lost_game = False
            blink.value = 0


        if clear_game == True:
            FPS = 25
            lawka_pos_x = []
            curr_lawka = []
            speed = 10
            points = 0
            clear_game = False

        #ekran początek
        gameDisplay.fill(WHITE)
        gameDisplay.blit(background,(0,0))
        gameDisplay.blit(road1, (road1_pos_x, ROAD_HEIGHT))
        if game_on == False:
            gameDisplay.blit(startScreen, startScreenRect)

        #ekran przegrana
        if game_on == True and lost_game == True:
            gameDisplay.blit(startScreen, startScreenRect)
            lostScreen = font.render('LICZBA PUNKTOW: ' + str(points), True, BLACK, WHITE)
            lostScreenRect = lostScreen.get_rect()
            lostScreenRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-25)
            gameDisplay.blit(lostScreen, lostScreenRect)

        #zwiększanie prędkości gry
        if speed_was_up == False and points%5 == 0:
            checkpointSound.play()
            FPS += 5
            speed_was_up = True
        if points%5 == 1:
            speed_was_up = False

        #wyświetlanie punktów
        if game_on == True:
            pointsDisplay = points_font.render('PUNKTY: ' + str(points), True, BLACK, WHITE)
            pointsRect = pointsDisplay.get_rect()
            pointsRect.center = (SCREEN_WIDTH-100, 10)
            gameDisplay.blit(pointsDisplay, pointsRect)


        if game_on == True and forrest_jump == False and lost_game == False:
            if run_indx <= 3:
                forrest = gameDisplay.blit(forrest_list[1], (FORREST_POS_X, FORREST_POS_Y))
                run_indx += 1
            elif run_indx < 6:
                forrest = gameDisplay.blit(forrest_list[2], (FORREST_POS_X, FORREST_POS_Y))
                run_indx += 1
            else:
                forrest = gameDisplay.blit(forrest_list[2], (FORREST_POS_X, FORREST_POS_Y))
                run_indx = 1
        elif game_on == False:
            forrest = gameDisplay.blit(forrest_list[0], (FORREST_POS_X, FORREST_POS_Y))


        if game_on == True and forrest_jump == True:
            if jump_height >= -7:
                going_up = 1
                if jump_height < 0:
                    going_up = -1
                FORREST_POS_Y -= (jump_height ** 2) * 0.8 * going_up
                jump_height -= 1
            else:
                forrest_jump = False
                jump_height = 7
            forrest = gameDisplay.blit(forrest_list[0], (FORREST_POS_X, FORREST_POS_Y))


        if game_on == True:
            frames_since_lawka += 1
            road1_pos_x -= speed
            if road1_pos_x <= -SCREEN_WIDTH:
                gameDisplay.blit(road2, (road2_pos_x, ROAD_HEIGHT))
                road2_pos_x -= speed
                if road2_pos_x == 0:
                    road2_pos_x = 500
                    road1_pos_x = 0


        if frames_since_lawka == gen_lawka_time:
            gen_lawka_time = random.randint(30, 50)
            gen_lawka_img = random.randint(0, 3)
            frames_since_lawka = 0
            curr_lawka.append([gen_lawka_img, SCREEN_WIDTH])

        for i in range(len(curr_lawka)):
            if curr_lawka[i][0] == 0 or curr_lawka[i][0] == 3:
                lower = 12
            else: lower = 0
            lawka = gameDisplay.blit(lawka_list[curr_lawka[i][0]], (curr_lawka[i][1], LAWKA_POS_Y+lower))
            curr_lawka[i][1] -= speed

            if curr_lawka[i][1] == 0:
                points += 1

            if forrest.colliderect(lawka):
                speed = 0
                if lost_game == False:
                    dieSound.play()
                lost_game = True
                forrest = gameDisplay.blit(forrest_list[3], (FORREST_POS_X, FORREST_POS_Y))

                #print(str(datetime.datetime.now().time()) + " punkty: " + str(points))


        pygame.display.update()
        clock.tick(FPS)

    proc_blink_det.join()
    print('Terminated.')
