"""Classes implemenetation for skills"""

import os
import random
from typing import TYPE_CHECKING

from combatgame.utils.utils import csv_to_dict

# import only for type hinting
if TYPE_CHECKING:
    from combatgame.characters import BaseCharacter
    from combatgame.enemies import EnemyCharacter


# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

# skill_attributes.csv file path
skill_attributes_path = f"{this_file_dir}/data/skill_attributes.csv"

# convert skill_attributes.csv to python dictionary
skill_attributes = csv_to_dict(skill_attributes_path, "skill")


class BaseSkill:
    """Represents a skill.

    Attributes
    ----------
    name : str
        The name of the skill.

    description : str
        The description of the skill.

    magic_points_cost : int
        The amount of magic points cost to use this skill.

    speed_points_cost : int
        The amount of speed points cost to use this skill.

    require_target : bool
        True if skill affects an enemy, False otherwise.

    message_displays : list of str
        A list of message displays when skill is used.

    belongs_to : str
        The character the skill belongs to.
    """

    name: str = ""
    description: str = ""
    magic_points_cost: int = 0
    speed_points_cost: int = 0
    require_target: bool = False
    message_displays: list[str] = []
    belongs_to: str = ""

    def __init__(self, skill_class_name: str):
        """Initialize a skill instance.

        Parameters
        ----------
        skill_class_name : str
            The name of the class of the skill.
        """
        self._assign_skill_attributes(skill_class_name)

    def _assign_skill_attributes(self, skill_class_name: str):
        """Assign skill attributes from skill_attributes.csv.

        Parameters
        ----------
        skill_class_name : str
            The name of the class of the skill.
        """
        attr = skill_attributes[skill_class_name]
        self.name: str = str(attr["name"])
        self.magic_points_cost: int = int(attr["mp_cost"])
        self.speed_points_cost: int = int(attr["sp_cost"])
        require_target_attr = str(attr["require_target"]).lower()
        self.require_target: bool = require_target_attr == "yes"
        self.belongs_to: str = str(attr["belongs_to"])

    def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
        """Use the skill."""
        raise NotImplementedError(
            "Subclasses must implement the use method")

class SkillEffects:
    """A container class for storing skill effects data classes.

    This class serves as a container for all the skill effects in the game.
    It provides a centralized location to access and manage the different skills effects.
    """

    class Invincible:
        """Data class for invincible effect.
        
        Attributes
        ----------
        name : str
            The name of the effect.
        description : str
            The description of the effect.
        use_count : int
            The amount of uses allowed.
        belongs_to : BaseSkill
            The skill the effect belong to.
        """
        def __init__(self):
            self.name = "Invincible"
            self.description = "Blocks any incoming attacks."
            self.use_count = 1
            self.belongs_to = "Illusionary Aura"

        def __str__(self):
            return self.name

    class ReflectiveShield:
        """Data class for reflective shield effect."""
        def __init__(self):
            self.name = "Reflective Shield"
            self.description = "Reflects any incoming attacks back to the enemies."
            self.use_count = 1
            self.belongs_to = "Reflective Shield"

        def take_effect(self, attacker: "BaseCharacter", damage: int):
            """Use the effect.
            
            Parameters
            ----------
            attacker : BaseCharacter
                The attacker that tried to attack.
            damage : int
                The damage the attacker intended to deal.

            Returns
            -------
            log : str
                The battle log.
            """

            # if damage more than attacker's defense points,
            # deal remaining damage to attacker's health points
            defense_points_damage = min(damage, attacker.defense_points)
            health_points_damage = max(0, damage - attacker.defense_points)

            # deals the damage
            attacker.defense_points -= defense_points_damage
            attacker.health_points -= health_points_damage

            log = f"{attacker.name}'s attack was met with a defensive shield, " \
                "causing the damage to reflect back to themselves. " \
                f"(-{defense_points_damage}DP and -{health_points_damage}HP)"

            return log


        def __str__(self):
            return self.name


class Skills:
    """A container class for storing skill classes.

    This class serves as a container for all the skills in the game.
    It provides a centralized location to access and manage the different skills.
    """

    # Tank job class skill (WhiskerGuard, ClawSwipe)
    class WhiskerGuard(BaseSkill):
        """Represents WhiskerGuard skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Increases the character's defense by a random amount with " \
                "cat-like reflexes."
            self.message_displays = [
                "With a swift movement, {character} activates Whisker Guard, shielding itself " \
                    "from harm.",
                "{character} activates Whisker Guard, increasing their own defense.",
                "By focusing their inner cat instincts, {character} empowers their defense with " \
                    "Whisker Guard, ready to withstand any attack."
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the WhiskerGuard skill.
            Increases defense point by 5 to 15 points.

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # amount of defense points to increase by
            defense_points_increase = random.randint(5, 15)

            # increase character's defense points
            character.defense_points += defense_points_increase

            # choose a random display message
            message_display = random.choice(self.message_displays)

            # returns log
            return message_display.format(character=character.name) + \
                f"\n(+{defense_points_increase} Defense Points)"

    class ClawSwipe(BaseSkill):
        """Represents ClawSwipe skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Unleash a flurry of razor-sharp claws, striking enemies and " \
                "removing their defense."
            self.message_displays = [
                "The sound of claws tearing through flesh fills the air as {character} " \
                    "delivers a devastating clawswipe, leaving {target} defenseless!",
                "A flurry of razor-sharp claws slices through the air as {character} " \
                    "executes a powerful clawswipe, removing {target}'s defenses!",
                "{target} is caught off guard as {character} launches a surprise attack " \
                    "with a ferocious clawswipe, rendering {target}'s defenses useless!"
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the ClawSwipe skill.
            Removes target defense and deals remaining damage on target's health.

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # overall effect
            battle_log = f"(removed {target.name} defense)"

            # amount of damage to deal
            damage_dealt = random.randint(25, 35)

            # deal remaining damage to target's health if damage_dealt > target's defense points
            if damage_dealt > target.defense_points:

                # calculate net damage to target's health
                net_damage = damage_dealt - target.defense_points

                # decrease target's health by net_damage
                target.health_points -= net_damage

                # update battle log
                battle_log = f"(removed {target.name} defense and dealt {net_damage}HP)"

            # remove target's defense regardless of damage dealt
            target.defense_points = 0

            # choose a random display message
            message_display = random.choice(self.message_displays)

            # return display message
            return message_display.format(character=character.name, target=target.name) + \
                "\n" + battle_log


    # MirrorMage job class skill (IllusionaryAura, ReflectiveShield)
    class IllusionaryAura(BaseSkill):
        """Represents IllusionaryAura skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Creates a mesmerizing aura that confuses enemies, causing them " \
                "to miss their attacks."
            self.message_displays = [
                "{character} casts Illusionary Aura, creating a captivating aura around " \
                    "themselves.",
                "The mesmerizing aura of {character}'s Illusionary Aura confuses the enemy, " \
                    "causing them to miss their attack!",
                "The enemy's attack goes astray as they are bewildered by the illusionary aura " \
                    "surrounding {character}."
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the MirrorImage skill.
            Creates a mesmerizing aura that confuses enemies, causing them to miss their attacks.

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # set invincible skill effect to character
            invincible = SkillEffects.Invincible()
            character.active_effects.append(invincible)

            # choose a random message display
            message_display = random.choice(self.message_displays)

            # return message display
            return message_display.format(character=character.name) + \
                f"\n({str(invincible)} Effect Activated)"

    class ReflectiveShield(BaseSkill):
        """Represents ReflectiveShield skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Creates a magical barrier that reflects a portion of the next " \
                "incoming spell back at the enemy."
            self.message_displays = [
                "A shimmering shield envelops {character}, ready to reflect incoming physical " \
                    "damage from {target}.",
                "{character} channels their magic, creating a barrier of reflection to counter " \
                    "{target}'s assault.",
                "{character}'s Reflective Shield sparkles with energy, poised to send " \
                    "{target}'s strength back at them."
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter"=None):
            """Use the ReflectiveShield skill.
            Creates a magical barrier that reflects the next incoming attack back at the enemy.

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # set reflective skill effect to active effects
            reflective_shield = SkillEffects.ReflectiveShield()
            character.active_effects.append(reflective_shield)

            # choose a random message display
            message_display = random.choice(self.message_displays)

            # return message display
            return message_display.format(character=character.name, target=target.name) + \
                "\n(reflective shield effect activated)"


    # Healer job class skill (HealingPurr, LuckyAura)
    class HealingPurr(BaseSkill):
        """Represents HealingPurr skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Restores health points and brings comfort through the power of " \
                "purrs."
            self.message_displays = [
                "{character} emits a gentle purr, enveloping themselves in healing energy.",
                "The soothing purrs of {character} resonate, restoring their health points.",
                "{character}'s healing purr fills the air, bringing comfort and replenishing " \
                "their vitality."
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the HealingPurr skill.
            Increases its health points by 5 to 15 points.

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # increase character's health points by 5 to 15 points
            health_points_increase = random.randint(5, 15)
            character.health_points += health_points_increase

            # choose a random message display
            message_display = random.choice(self.message_displays)

            # return message display
            return message_display.format(character=character.name) + \
                f"\n(+{health_points_increase} health points)"

    class LuckyCharm(BaseSkill):
        """Represents LuckyCharm skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Channel inner luck to create a protective charm, increasing its " \
                "luck and favoring positive outcomes."
            self.message_displays = [
                "The air around {character} shimmers with luck as the lucky charm takes effect.",
                "The lucky charm envelops {character}, infusing them with a heightened sense of " \
                    "favorable outcomes.",
                "With the lucky charm activated, {character} feels a surge of good luck " \
                    "coursing through their veins."
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the LuckyCharm skill.
            Increases luck by 5%

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            luck_increase = 5
            character.luck += luck_increase

            # choose a random display message
            message_display = random.choice(self.message_displays)

            # return display message
            return message_display.format(character=character.name) + f"\n(+{luck_increase}% luck)"


    # Assassin job class skill (PurrfectStrike, CripplingStrike)
    class PurrfectStrike(BaseSkill):
        """Represents PurrfectStrike skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = " Unleash a swift and precise strike, targeting the enemy's weak " \
                "spot with deadly accuracy, dealing high damage."
            self.message_displays = [
                "With lightning speed, {character} lunges at {target}, aiming for a critical hit.",
                "The sound of a fierce, focused purr fills the air as {character} delivers a " \
                    "devastating blow at {target}.",
                "{target} reels from {character}'s Purrfect Strike, unable to withstand the " \
                    "precise attack."
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the PurrfectStrike skill.
            Removes target's defense and deals additional 15 to 25 damage to target's health

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # removes target's defense
            target.defense_points = 0

            # deal damage to target's health points
            damage_dealt = random.randint(15, 25)
            target.health_points -= damage_dealt

            # choose a random display message
            message_display = random.choice(self.message_displays)

            # returns message display
            return message_display.format(character=character.name, target=target.name) + \
                f"\n(removed {target.name}'s defense and dealt {damage_dealt}HP)"

    class CripplingStrike(BaseSkill):
        """Represents CripplingStrike skill.

        Attributes
        ----------
        name : str
            The name of the skill.

        description : str
            The description of the skill.

        magic_points_cost : int
            The amount of magic points cost to use this skill.

        speed_points_cost : int
            The amount of speed points cost to use this skill.

        message_displays : list of str
            A list of message displays when skill is used.
        """

        def __init__(self):
            self.description = "Deliver a precise strike that cripples the target, slowing " \
                "their movements."
            self.message_displays = [
                "{target}'s agility is hindered by {character}'s crippling strike!",
                "With a calculated strike, {character} impairs {target}'s mobility!",
                "{character}'s crippling strike disrupts {target}'s flow, hampering their movement!"
            ]

            # initialize attributes of BaseSkill class
            super().__init__(self.__class__.__name__)

        def use(self, character: "BaseCharacter", target: "EnemyCharacter" = None):
            """Use the CripplingStrike skill.
            Reduce target's speed points by 5 to 15 points

            Parameters
            ----------
            character : BaseCharacter
                The character thats using the skill.

            Target : EnemyCharacter
                The enemy to use the skill on.

            Returns
            -------
            log : str
                The log for using this skill.
            """

            # reduce target's speed points
            speed_reduction = random.randint(5, 15)
            target.speed_points = max(0, target.speed_points - speed_reduction)

            # choose a random message display
            message_display = random.choice(self.message_displays)

            # return message display
            return message_display.format(character=character.name, target=target.name) + \
                f"\n(Reduced {target.name} speed points by {speed_reduction})"
