import pygame



pygame.mixer.init()
sound_files = [ "test.wav"                              # 0
                    , "metro_interior_01.wav"               # 1
                    , "metro_interior_02.wav"               # 2
                    , "train_station_hall_1.wav"            # 3
                    # sound efects
                    , "hbo_you_litle_stinker.wav"           # 4
                    , "metro_derpating_exterior_01.wav"     # 5
                    , "metro_derpating_exterior_02.wav"     # 6
                    , "metro_interior_01.wav"               # 7
                    , "metro_interior_02.wav"               # 8
                    , "metro_pass_by_01.wav"                # 9
                    , "metro_pull_in_exterior_01.wav"       # 10
                    , "metro_ride_departing_interior_01.wav"# 11
                    , "metro_ride_stopping_interior_01.wav" # 12
                    , "metro_train_crossing_01.wav"         # 13
                    , "thank_you_sir_may_i_have_another.wav"# 14
                    , "gun_shoot_metal.wav"]                # 15

def stationMusic( efect ):
    pygame.mixer.music.load("assets/" + str(sound_files[efect]))
    pygame.mixer.music.play()

def efectSound(  efect ):
    sound = pygame.mixer.Sound("assets/" + str(sound_files[efect]))
    sound.play()




