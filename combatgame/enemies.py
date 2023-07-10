"""Classes implementation for enemies with their attributes."""
import os
from functools import partial

from combatgame.characters import BaseCharacter
from combatgame.resources.ascii_art import ascii_arts
from combatgame.utils.utils import csv_to_dict


# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

# get enemy_attributes.csv file path
enemy_attributes_path = f"{this_file_dir}/data/enemy_attributes.csv"

# convert enemy_attributes.csv file to python dictionary
enemy_attributes = csv_to_dict(enemy_attributes_path, "name")

# gets all available enemy names
enemy_names = enemy_attributes.keys()

class EnemyCharacter(BaseCharacter):
    """Represents an enemy character.

    ...

    Attributes
    ----------
    name : str
           The name of the player character.

    health_points : int
    attack_points : int
    defense_points : int
    speed_points : int
    luck : int
    """

    def __init__(self, name):
        # initialize parent class attributes
        super().__init__(name)

        # deletes magic points and skills since enemies do not have these
        del self.magic_points
        del self.skills
        del self.active_effects

        # initialize attributes
        attr = enemy_attributes[name]
        self.max_health_points: int = int(attr["HP"])
        self.max_defense_points: int = int(attr["DP"])
        self.attack_points: int = int(attr["AP"])
        self.speed_points: int = int(attr["SP"])
        self.luck: int = int(attr["Luck"])
        self.ascii_art = ascii_arts[name]

        self.health_points: int = self.max_health_points
        self.defense_points: int = self.max_defense_points

    def defend(self):
        """Special method defend for enemy characters only.
        Raises defense points to max.

        Returns
        -------
        log : str
            The battle log.
        """

        self.defense_points = self.max_defense_points

        return f"{self.name} restored its defense points!"

    def select_action(self, active_player: BaseCharacter):
        """Select the best action based on a rule-based approach.
        
        Parameters
        ----------
        active_player : BaseCharacter
            The active player character.
        """

        if (active_player.health_points + active_player.defense_points) < self.attack_points:
            return partial(self.basic_attack, active_player)

        if self.health_points < (0.2 * self.max_health_points):
            return self.heal

        if self.defense_points < (0.5 * self.max_defense_points):
            return self.defend

        return partial(self.basic_attack, active_player)
