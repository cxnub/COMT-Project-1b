"""CATastrophe Chronicles: The Wildcat Cafe

This is the main script for CATastrophe Chronicles: The Wildcat Cafe.
It is the entry point for running the game.

Author: Koh Cheng Xi
Date: 

Usage:
    python main.py
"""
from functools import partial

from combatgame.ui import Ui
from combatgame.scenes import Scenes
from combatgame.characters import Tank, MirrorMage, Healer, Assassin
from combatgame.skills import Skills, BaseSkill

def main():
    """Main game flow."""

    scenes = Scenes()
    settings = SettingsMenu()

    while True:
        start_menu_dict = {
            "Start": partial(scenes.run_scenes, settings.flash),
            "Help": HelpMenu.main,
            "Settings": settings.display_settings
        }

        Ui.Animation.display_welcome_screen()

        start_menu = Ui.Menu("CATastrophe Chronicles", start_menu_dict)
        selected = start_menu.select_option(print_line_by_line=True)

        if callable(selected):
            selected()
        else:
            print("Not callable")

class HelpMenu:
    """Container class for help menu."""

    @staticmethod
    def main():
        """Main HelpMenu function for displaying main help menu."""

        # create dictionary for main help menu
        help_menu_dict = {
            "Job Classes": HelpMenu.job_classes,
            "Skills": HelpMenu.skills,
            "Back": main
        }

        Ui.clear_terminal()

        # display main help menu
        menu = Ui.Menu("Help Menu", help_menu_dict)
        selected_option = menu.select_option()
        selected_option()

    @staticmethod
    def job_classes():
        """Function for displaying job classes help."""

        Ui.clear_terminal()

        tank = Tank("Tank")
        mirrormage = MirrorMage("MirrorMage")
        healer = Healer("Healer")
        assassin = Assassin("Assassin")

        seperator = " " * 10

        def page_one():
            # display page one

            Ui.clear_terminal()
            Ui.print_box("Page 1 - Tank and MirrorMage")

            # print ascii art and combat stats
            seperator_column_position = Ui.display_ascii_art(tank, mirrormage, sep=seperator)
            Ui.display_combat_stats(
                tank, mirrormage, seperator_column_position[0],
                sep=seperator, include_effects=False, include_skills=True
                )

            print()
            Ui.print_box("Page 1 - Tank and MirrorMage")

            input("\nPress enter to go back...")

        def page_two():
            # display page two

            Ui.clear_terminal()
            Ui.print_box("Page 2 - Healer and Assassin")

            # print ascii art and combat stats
            seperator_column_position = Ui.display_ascii_art(healer, assassin, sep=seperator)
            Ui.display_combat_stats(
                healer, assassin, seperator_column_position[0],
                sep=seperator, include_effects=False, include_skills=True
                )

            print()
            Ui.print_box("Page 2 - Healer and Assassin")

            input("\nPress enter to go back...")

        # craete dictionary for menu
        job_classes_dict = {
            "Page 1": page_one,
            "Page 2": page_two,
            "Back": HelpMenu.main
        }

        while True:
            # display the menu
            job_classes_menu = Ui.Menu("Job Class Help", job_classes_dict)
            selected_option = job_classes_menu.select_option()

            # run the selected option
            selected_option()

            Ui.clear_terminal()

    @staticmethod
    def skills():
        """Function for displaying skills info."""

        # store all skills in a list
        skills = [
            Skills.WhiskerGuard(), Skills.ClawSwipe(),
            Skills.IllusionaryAura(), Skills.ReflectiveShield(),
            Skills.HealingPurr(), Skills.LuckyCharm(),
            Skills.PurrfectStrike(), Skills.CripplingStrike()
            ]

        def display_skill_info(skill: BaseSkill):
            # function to display skill info
            print(f"Name: {skill.name}")
            print(f"Belongs to: {skill.belongs_to}")
            print(f"Description: {skill.description}")
            print("Cost:")
            print(f"{skill.speed_points_cost} Speed Points")
            print(f"{skill.magic_points_cost} Magic Points")
            input("\nPress enter to go back...")

        # create dictionary for menu with every skill in skills
        skills_menu_dict = {
            skill.name: partial(display_skill_info, skill) for skill in skills
        }
        # include the back option
        skills_menu_dict["Back"] = HelpMenu.main


        while True:
            # display the menu
            skills_menu = Ui.Menu("Skill Help", skills_menu_dict)
            selected_option = skills_menu.select_option()

            # run the selected option
            selected_option()
            Ui.clear_terminal()

class SettingsMenu:
    """Class implementation for settings menu."""

    def __init__(self):
        self.flash = True

    def display_settings(self):
        """Displays the settings menu."""

        def toggle_flash():
            self.flash = not self.flash

        while True:
            settings_menu_dict = {
                f"Flashes ({'On' if self.flash else 'Off'})": toggle_flash,
                "Back": main
            }

            # display settings menu
            settings_menu = Ui.Menu("Settings", settings_menu_dict)
            selected_option = settings_menu.select_option()

            selected_option()
            Ui.clear_terminal()


if __name__ == "__main__":
    main()
