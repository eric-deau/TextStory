from combat import encounters
from board import world_creation
from movement import movement
from utilities import game_checks, lore
from character import character_creation, display_status
import pygame
import __init__


def game():
    pygame.mixer.init()
    victory = pygame.mixer.Sound("sound/victory.mp3")
    victory.set_volume(0.05)
    lore.slow_rolling_text_printer('board/beginning.txt')
    while True:
        world = world_creation.make_board(__init__.ROWS, __init__.COLUMNS, __init__.FLOORS)
        character = character_creation.make_character()
        achieved_goal = False
        while character['HP'] > 0 and not achieved_goal:
            display_status.display_status(character)
            movement.check_for_floor_change(character, __init__.ROWS, __init__.COLUMNS, __init__.FLOORS)
            game_checks.reset_affliction(character)
            movement.describe_current_location(world, character)
            direction = movement.get_user_move()
            valid_move = movement.validate_move(world, character, direction)
            if valid_move:
                movement.move_character(character, direction)
                boss_check = game_checks.check_for_boss(character, world)
                if boss_check:
                    boss = encounters.spawn_boss(character)
                    if boss['Name'] == "EYE OF CTHULHU":
                        cthulhu = pygame.mixer.Sound("sound/cthulhu.mp3")
                        cthulhu.set_volume(0.05)
                        lore.slow_rolling_text_printer('board/eye_of_cthulhu.txt')
                        cthulhu.play()
                    if boss['Name'] == "MIMIC":
                        mimic = pygame.mixer.Sound("sound/mimic.mp3")
                        mimic.set_volume(0.05)
                        lore.slow_rolling_text_printer('board/mimic.txt')
                        mimic.play()
                    if boss['Name'] == "ZAKUM":
                        zakum = pygame.mixer.Sound("sound/zakum.mp3")
                        zakum.set_volume(0.05)
                        lore.slow_rolling_text_printer('board/zakum.txt')
                        zakum.play()
                    encounters.engage_combat(character, boss)
                    if boss['HP'] <= 0 and boss['Name'] == "EYE OF CTHULHU":
                        pygame.mixer.pause()
                        lore.slow_rolling_text_printer('board/defeat_of_eye_of_cthulhu.txt')
                    if boss['HP'] <= 0 and boss['Name'] == "MIMIC":
                        pygame.mixer.pause()
                        lore.slow_rolling_text_printer('board/defeat_of_mimic.txt')
                    if boss['HP'] <= 0 and boss['Name'] == "ZAKUM":
                        pygame.mixer.pause()
                        lore.slow_rolling_text_printer('board/defeat_of_zakum.txt')
                elif game_checks.check_for_random_foes():
                    if encounters.decide_encounter():
                        test = pygame.mixer.Sound("sound/battle.mp3")
                        test.set_volume(0.05)
                        test.play()
                        encounters.engage_combat(current_char=character, creep=encounters.spawn_monster())
                        pygame.mixer.pause()
                        victory.play()
                    else:
                        encounters.guessing_game(current_char=character)
                else:
                    pass
                achieved_goal = game_checks.check_if_goal_attained(character, rows=__init__.ROWS,
                                                                   columns=__init__.COLUMNS, floors=__init__.FLOORS)
            else:
                print("\"That door seems to be locked\"")
        pygame.mixer.pause()
        if achieved_goal and character['HP'] > 0:
            victory_ending = pygame.mixer.Sound("sound/victory_end.mp3")
            victory_ending.set_volume(0.05)
            victory_ending.play()
            lore.slow_rolling_text_printer('utilities/victory.txt')
            game_checks.slow_print_by_line('utilities/ending.txt')
        if character['HP'] <= 0:
            lore.slow_rolling_text_printer('utilities/defeat.txt')
            defeat_ending = pygame.mixer.Sound('sound/defeat.mp3')
            defeat_ending.set_volume(0.05)
            defeat_ending.play()
            game_checks.slow_print_by_line('utilities/defeat_ascii.txt')
        user_input = input("Would you like to restart? Type Y to restart, else type anything to exit.")
        if user_input.lower() == 'y':
            pygame.mixer.pause()
            continue
        else:
            break
    lore.slow_rolling_text_printer('utilities/thank_you.txt')


def main():
    """
    Drive the program.
    """
    game()


if __name__ == "__main__":
    main()
