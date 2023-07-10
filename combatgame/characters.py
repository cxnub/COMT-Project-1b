"""Classes implementation for player characters with their attributes."""

from __future__ import annotations
import random
import os
from typing import TYPE_CHECKING

from combatgame.skills import Skills, BaseSkill, SkillEffects
from combatgame.utils.utils import csv_to_dict
from combatgame.resources.ascii_art import ascii_arts

if TYPE_CHECKING:
    from combatgame.enemies import EnemyCharacter

# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

# get job_classes_attributes.csv file path
job_class_attributes_path = f"{this_file_dir}/data/job_class_attributes.csv"

# convert job_classes_attributes.csv file to python dictionary
job_class_attributes = csv_to_dict(job_class_attributes_path, "job")


class BaseCharacter:
    """Represents a character.

    Attributes
    ----------
    name : str
        The name of the character.
    health_points : int
        The health points of the character.
    attack_points : int
        The attack points of the character.
    defense_points : int
        The defense points of the character.
    speed_points : int
        The speed points of the character.
    magic_points : int
        The magic points of the character.
    luck : int
        The luck attribute of the character.
    skills : list[Skill]
        The skills of the character.
    active_effects : dict
        Dictionary of active effects on character.
    character_image : str
        The path to the character's image.
    ascii_art : List
        The ASCII Art for the job class.
    starting_column_position : int
        The starting column position in combat screen.

    Notes
    -----
    `starting_col_pos` will only be set in combat screen.
     """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, name: str, job_class: str = None):
        """Initializes a character instance.

         Parameters
         ----------
         name : str
            The name of the character.
         job_class : str
            The job class of the character.
         """

        # initialize attributes
        self.name = name
        self.health_points = 0
        self.attack_points = 0
        self.defense_points = 0
        self.speed_points = 0
        self.magic_points = 0
        self.job_class = ""

        # how lucky the character is (max - 100)
        self.luck = 0

        # character's job class skills
        self.skills = []

        # active effects from using skills
        self.active_effects = []

        # character's image
        self.character_image = ""

        # ASCII Art of the job class
        self.ascii_art = []

        # starting column position in combat screen
        # note: this value will only be set when in combat screen
        self.starting_column_position = 0

        if job_class:
            self._assign_job_class_attributes(job_class)

    def _assign_job_class_attributes(self, job_class_name: str) -> None:
        """Assign job class attributes from job_classes_attributes.csv.

        Parameters
        ----------
        job_class_name : str
            The name of the job class.
        """

        attr = job_class_attributes[job_class_name]
        self.job_class = job_class_name
        self.max_health_points: int = int(attr["HP"])
        self.max_defense_points: int = int(attr["DP"])
        self.attack_points: int = int(attr["AP"])
        self.speed_points: int = int(attr["SP"])
        self.magic_points: int = int(attr["MP"])
        self.luck: int = int(attr["Luck"])
        self.ascii_art = ascii_arts[job_class_name]

        self.health_points: int = self.max_health_points
        self.defense_points: int = self.max_defense_points

    def restore_stats(self):
        """Restore the statistics of the character back to its default values."""

        self._assign_job_class_attributes(self.job_class)

    def get_active_effect(self, effect: SkillEffects):
        """Get the effect object that matches the effect given.

        Parameters
        ----------
        effect : SkillEffects
            The effect class to look for.

        Returns
        -------
        SkillEffects : The effect object if effect is in self.active_effects, None otherwise.
        """

        # checks if there is an active_effects attribute
        if hasattr(self, "active_effects"):
            return next((item for item in self.active_effects if isinstance(item, effect)), None)

        return None

    def basic_attack(self, target: BaseCharacter) -> str:
        """Deals basic attack to target.

        Parameters
        ----------
        target : BaseCharacter
            The target of the basic attack.

        Returns
        -------
        log : str
            The log of using basic attack.
        """

        total_damage = 0
        log = ""

        # reduce speed points by 1
        self.speed_points -= 1

        # checks if target has invincible effect and assigns effect to the return value
        if effect := target.get_active_effect(SkillEffects.Invincible):

            # the log to return
            log = f"{self.name}'s attack was REJECTED due to {target.name}'s" + \
                f" {effect.belongs_to}."

            # reduce the use count of the effect
            effect.use_count -= 1

            # remove effect if its used up
            if effect.use_count <= 0:
                target.active_effects.remove(effect)

            return log

        # checks if target has reflective shield effect and assigns effect to the return value
        if effect := target.get_active_effect(SkillEffects.ReflectiveShield):
            log = effect.take_effect(self, self.attack_points)

            # reduce the use count of the effect
            effect.use_count -= 1

            # remove effect if its used up
            if effect.use_count == 0:
                target.active_effects.remove(effect)

            return log

        # calculates chances of critical hit based on job class's luck
        # critical hits ignores target's defense points and reduces their HP
        # by the amount of attacker's AP
        critical_hit = (random.randint(1, 100)) <= self.luck

        # critical hits ignores target's defense points and reduces their HP
        # by double the amount of attacker's AP
        if critical_hit:
            total_damage = 2 * self.attack_points
            log = f"{self.name} lands a CRITICAL hit and dealt {total_damage}HP on {target.name}!"

        else:
            # if target's defense points is more than atttackers's AP no damage
            # is dealt
            total_damage = max(self.attack_points - target.defense_points, 0)
            log = f"{self.name} attacked {target.name}, dealing {total_damage}HP."

            if total_damage == 0:
                log = f"{self.name} tried attacking {target.name} but cant get through its defense!"

        # deducts target's health points by total_damage
        target.health_points -= total_damage

        # deducts target's defense points by 1
        target.defense_points -= 1

        return log

    def heal(self) -> None:
        """Heal method.
        raises health points by 1 to 10.

        Returns
        -------
        log : str
            The log for using heal.
        """
        # reduce speed points by 1
        self.speed_points -= 1

        # health points increase
        hp_increase = random.randint(1, 10)

        # raise speed points by 1 to 10
        self.health_points += hp_increase

        return f"{self.name} used heal and gained {hp_increase}HP."

    def check_skill_cost(self, skill: BaseSkill):
        """Check if the character has enough points to use the skill.

        Parameters
        ----------
        skill : BaseSkill
            The skill instance.

        Returns
        -------
        bool : True if character has enough points to use the skill, False otherwise.
        log : str
            The log for checking skill cost.
        """

        # not enough speed points
        if self.speed_points < skill.speed_points_cost:
            log = f"Not enough speed points. You need {skill.speed_points_cost} but only " \
                f"have {self.speed_points}."

            return False, log

        # not enough magic points
        if self.magic_points < skill.magic_points_cost:
            log = f"Not enough magic points. You need {skill.magic_points_cost} but only " \
                f"have {self.magic_points}."

            return False, log

        return True, ""

    def use_skill(self, skill_index: int, target: "EnemyCharacter" = None):
        """Use a skill.

        Parameters
        ----------
        skill_index : int
            The index of the skill to use in the skills list.

        target : EnemyCharacter
            The target to use the skill on. Defaults to None.

        Returns
        -------

        """

        # check if skill_index is valid
        if skill_index >= len(self.skills):
            print(f"skill_index ({skill_index}) out of range")
            return None

        # get skill object
        skill: BaseSkill = self.skills[skill_index]

        # check if character have enough points to use the skill
        is_available, log = self.check_skill_cost(skill)

        # handle skill not available
        if not is_available:
            return is_available, log

        # process the skill

        # deduct points
        self.speed_points -= skill.speed_points_cost
        self.magic_points -= skill.magic_points_cost

        # use skill if target is given
        if target:
            return skill.use(self, target)

        if skill.require_target:
            print("Skill requires a target argument.")
            return None

        return skill.use(self)

    def is_alive(self):
        """Checks if hp is > 0

        Returns
        -------
        bool : True if character is alive, False otherwise.

        """
        return self.health_points > 0


class Tank(BaseCharacter):
    """Represents a Tanker player character.

     Attributes
     ----------
     name : str
        Player character's name.

    """

    def __init__(self, name: str):

        # get job class type
        job_class = self.__class__.__name__

        # initialize attributes of BaseCharacter class
        super().__init__(name, job_class)

        # initialize skills to job class
        self.skills = [Skills.WhiskerGuard(), Skills.ClawSwipe()]

    def __str__(self):
        return "Tank"

    def __repr__(self):
        return f"{self.__class__.__name__}(\'{self.name}\')"


class MirrorMage(BaseCharacter):
    """Represents a MirrorMage player character.

     Attributes
     ----------
     name : str
        Player character's name.

    """

    def __init__(self, name: str):

        # get job class type
        job_class = self.__class__.__name__

        # initialize attributes of BaseCharacter class
        super().__init__(name, job_class)

        # initialize skills to job class
        self.skills = [Skills.IllusionaryAura(), Skills.ReflectiveShield()]

    def __str__(self):
        return "Mirror Mage"

    def __repr__(self):
        return f"{self.__class__.__name__}(\'{self.name}\')"


class Healer(BaseCharacter):
    """Represents a Healer player character.

     Attributes
     ----------
     name : str
        Player character's name.

    """

    def __init__(self, name: str):

        # get job class type
        job_class = self.__class__.__name__

        # initialize attributes of BaseCharacter class
        super().__init__(name, job_class)

        # initialize skills to job class
        self.skills = [Skills.HealingPurr(), Skills.LuckyCharm()]

    def __str__(self):
        return "Healer"

    def __repr__(self):
        return f"{self.__class__.__name__}(\'{self.name}\')"


class Assassin(BaseCharacter):
    """Represents an Assassin player character.

     Attributes
     ----------
     name : str
        Player character's name.

    """

    def __init__(self, name: str):

        # get job class type
        job_class = self.__class__.__name__

        # initialize attributes of BaseCharacter class
        super().__init__(name, job_class)

        # initialize skills to job class
        self.skills = [Skills.PurrfectStrike(), Skills.CripplingStrike()]

    def __str__(self):
        return "Assassin"

    def __repr__(self):
        return f"{self.__class__.__name__}(\'{self.name}\')"
