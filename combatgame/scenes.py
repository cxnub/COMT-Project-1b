"""Module to store scenes"""
import time
from typing import List
from functools import partial

from combatgame.ui import Ui
from combatgame.game_manager import GameManager
from combatgame.characters import BaseCharacter, Tank, MirrorMage, Healer, Assassin
from combatgame.enemies import EnemyCharacter
from combatgame.resources import lore


class Scenes:
    """This class stores all the scenes as functions.
    
    Attributes
    ----------
    selected_characters : list
        The characters player have selected to play.
    show_lore : bool
        Whether to display lore or skip it
    """

    def __init__(self):
        self.selected_characters: List[BaseCharacter] = []

    def reset(self):
        """Resets the class variables to default values."""

        self.selected_characters: List[BaseCharacter] = []

    def restore_all_character_stats(self):
        """restore stats for alive player characters"""

        for character in self.selected_characters:
            if character.is_alive():
                character.restore_stats()

    def add_points_to_all_characters(self, stat: str, amount: int):
        """Add stats points to all alive player characters
        
        Parameters
        ----------
        stat : str
            The attribute name of a stat.
        amount : int
            The amount to add.
        """

        for character in self.selected_characters:
            if character.is_alive():
                # get the current value of that stat
                current_value = getattr(character, stat, 0)

                # increase the value of that stat by `amount`
                setattr(character, stat, current_value + amount)

    def start_scene(self):
        """Start of the game flow.
        
        Returns
        -------
        game_over : bool
            True if game is over, False otherwise.
        """

        Ui.execute_lore(lore.START_GAME[0])

        # create Menu object to let player choose number of playable characters
        choice_menu = Ui.Menu("Choose Number of Playable Characters", {1: 1, 2: 2, 3: 3})
        number_of_playable_characters = choice_menu.select_option()

        Ui.execute_lore(
            lore.START_GAME[1].format(
                number_of_playable_characters=number_of_playable_characters
                )
            )

        # options dictionary for menu
        characters = {
            "Whiskerwall (Tank)": ["Whiskerwall (Tank)", Tank("Whiskerwall")],
            "Purrception (MirrorMage)": ["Purrception (MirrorMage)", MirrorMage("Purrception")],
            "Meowdicine (Healer)": ["Meowdicine (Healer)", Healer("Meowdicine")],
            "Shadowpaw (Assassin)": ["Shadowpaw (Assassin)", Assassin("Shadowpaw")]
            }

        # let user select their characters
        for i in range(1, number_of_playable_characters + 1):

            # menu for choosing characters
            choose_character_menu = Ui.Menu(
                f"Choose Your {Ui.ordinal(i)} Character",
                characters
                )

            # get the user to select an option
            selected_character = choose_character_menu.select_option()

            # stores the selected character in a list
            self.selected_characters.append(selected_character[1])

            # prevents player from choosing the same character again
            characters.pop(selected_character[0])

        return False

    def scene_one(self):
        """First scene of the game flow.
        
        Returns
        -------
        game_over : bool
            True if game is over, False otherwise.
        """

        # Create the list of EnemyCharacter objects met in the first scene
        encountered_enemies = [EnemyCharacter("Viperstrike")]

        # display lore
        Ui.execute_lore(lore.SCENE_ONE[0])

        # starts the combat
        Ui.Animation.display_combat_start(self.selected_characters, encountered_enemies)
        first_combat = GameManager(self.selected_characters, encountered_enemies)
        player_won = first_combat.start_combat()
        time.sleep(2)

        if not player_won:
            Ui.execute_lore(lore.PLAYER_LOST)
            return True

        Ui.execute_lore(lore.SCENE_ONE[1])
        return False

    def scene_two(self, flash=True):
        """First scene of the game flow.
        
        Parameters
        ----------
        flash : bool
            Whether to have flash effects for thunderstorm. Defaults to True.

        Returns
        -------
        game_over : bool
            True if game is over, False otherwise.

        Notes
        -----
        FLASH WARNING!!
        """

        Ui.execute_lore(lore.SCENE_TWO)

        def second_combat_scene():

            # enemy involved in second combat scene
            enemies = [EnemyCharacter("Doomshroud")]

            Ui.Animation.display_combat_start(self.selected_characters, enemies)

            # Create GameManager object and start combat
            second_combat = GameManager(self.selected_characters, enemies)
            player_won = second_combat.start_combat()

            if not player_won:
                return True

            Ui.execute_lore(lore.SECOND_COMBAT_WIN)
            return False

        def option_one_scene():
            # the scene if the player chose option 1

            option_one_lore = lore.SCENE_TWO_OPTION_ONE
            Ui.execute_lore(option_one_lore[0])

            # restore all character stats
            self.restore_all_character_stats()

            Ui.execute_lore(option_one_lore[1])

            player_won = second_combat_scene()

            # return game_over = True, if player lost.
            if not player_won:
                return True

            Ui.execute_lore(option_one_lore[2])
            return option_two_scene()

        def option_two_scene():
            # the scene if the player chose option 2

            Ui.execute_lore(lore.SCENE_TWO_OPTION_TWO[0])

        def option_three_scene():
            # the scene if the player chose option 3

            option_three_lore = lore.SCENE_TWO_OPTION_THREE
            Ui.execute_lore(option_three_lore[0])

            # add 10 magic points to alive player characters
            self.add_points_to_all_characters("magic_points", 10)

            Ui.Animation.display_thunderstorm(flash=flash)
            Ui.execute_lore(option_three_lore[1])

            player_won = second_combat_scene()
            if not player_won:
                # return game_over = True, if player lost.
                return True

            Ui.execute_lore(option_three_lore[2])
            return option_two_scene()

        scene_two_options_dict = {
            "The Whispering Caverns": option_one_scene,
            "The Misty Peaks": option_two_scene,
            "The Enchanted Meadows": option_three_scene
        }

        options_menu = Ui.Menu("Choose a Path", scene_two_options_dict)
        selected_option = options_menu.select_option()

        # run the selected option scene and return result
        return selected_option()

    def run_scenes(self, flash):
        """Run the scenes in order."""
        scenes_order = [self.start_scene, self.scene_one, partial(self.scene_two, flash)]
        for scene in scenes_order:
            game_over = scene()
            if game_over:
                # resets class variables
                self.reset()

                Ui.Animation.display_game_over()
                time.sleep(2)
                return
