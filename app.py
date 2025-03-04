import os
import sys
from random import randint, choice

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.spinner import Spinner, SpinnerOption

import pygame


def resource_path(relative_path: str) -> str:

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, str(relative_path))


pygame.mixer.init()

roulette = pygame.mixer.Sound(resource_path("resources/wheel.mp3"))
selected = pygame.mixer.Sound(resource_path("resources/selected.mp3"))
button_sound = pygame.mixer.Sound(resource_path("resources/button.mp3"))

roulette.set_volume(0.5)
selected.set_volume(0.5)


class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_name = resource_path("resources/font.ttf")
        self.color = (0, 0, 0)
        self.font_size = 40
        self.background_color = (0.9, 0.5, 0.5)
        self.halign = "center"


class ValorantRandomizer(App):
    def build(self):
        Window.set_icon(resource_path("resources/logo.png"))
        Window.clearcolor = (1, 0.27, 0.33)

        self.agents = [
            "Brimstone", "Viper", "Omen", "Killjoy", "Cypher",
            "Sova", "Sage", "Phoenix", "Jett", "Reyna",
            "Raze", "Breach", "Skye", "Yoru", "Astra",
            "KAY/O", "Chamber", "Neon", "Fade", "Harbor",
            "Deadlock", "Gekko", "Iso", "Clove"
        ]

        self.remove = [
            "Astra", "Chamber", "Fade", "Harbor", "Iso",
            "Killjoy", "Raze", "Skye"
        ]

        for i in self.remove:
            if i in self.agents:
                self.agents.remove(i)

        self.primary_weapons = [
            "Stinger",
            "Spectre",
            "Bucky",
            "Judge",
            "Bulldog",
            "Guardian",
            "Phantom",
            "Vandal",
            "Marshal",
            "Outalw",
            "Operator",
            "Ares",
            "Odin"
        ]

        self.secondary_weapons = [
            "Classic",
            "Shorty",
            "Frenzy",
            "Ghost",
            "Sheriff"
        ]

        self.shields = [
            "Bouclier léger",
            "Bouclier lourd",
            "Bouclier régénératif"
        ]

        self.layout = BoxLayout(
            orientation='vertical',
            padding=100,
            spacing=50
        )

        self.label = Label(
            text="Abonnez-vous à Gild56 !",
            font_size=100,
            font_name=resource_path("resources/font.ttf"),
            color=(0, 0, 0),
            halign="center"
        )
        self.layout.add_widget(self.label)

        self.spinner = Spinner(
            text="Choisis l'objet !",
            values=(
                "Agents",
                "Armes principales",
                "Armes secondaires",
                "Boucliers"
            ),
            size_hint=(None, None),
            size=(500, 100),
            font_size=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=resource_path("resources/font.ttf"),
            color=(0, 0, 0),
            background_color=(1, 0.27, 0.33),
            halign="center",
            option_cls=CustomSpinnerOption
        )
        self.layout.add_widget(self.spinner)

        def on_spinner_select(spinner, value):
            self.selected_option = value
            self.button.disabled = False
            button_sound.play()
        self.spinner.bind(text=on_spinner_select)

        def on_spinner_open(spinner):
            button_sound.play()
        self.spinner.bind(on_release=on_spinner_open)

        self.button = Button(
            text="Tourner la roulette !",
            font_size=80,
            color=(0, 0, 0),
            on_press=self.start_selection,
            font_name=resource_path("resources/font.ttf"),
            background_color=(1, 0.27, 0.33),
            halign="center",
            disabled=True
        )
        self.layout.add_widget(self.button)

        return self.layout

    def start_selection(self, instance):
        self.time_intervals = (
            [0.03] * 20 +
            [0.04] * 13 +
            [0.045] * 5 +
            [0.05] * 3 +
            [0.065] * 3 +
            [0.078] * 2 +
            [0.1] * 2 +
            [0.2] * 1 +
            [0.5] * 1 +
            [1] * 1
        )

        self.index = 0
        self.selection_event = Clock.schedule_once(
            self.update_text, self.time_intervals[self.index])
        self.button.text = "Attendez..."

    def update_text(self, dt):
        roulette.play()
        if self.index < len(self.time_intervals) - 1:
            self.button.disabled = True
            self.spinner.disabled = True
            if self.selected_option == "Agents":
                self.label.text = choice(self.agents)
            elif self.selected_option == "Armes principales":
                self.label.text = choice(self.primary_weapons)
            elif self.selected_option == "Boucliers":
                self.label.text = choice(self.shields)
            else:
                self.label.text = choice(self.secondary_weapons)
            self.index += 1
            Clock.schedule_once(
                self.update_text, self.time_intervals[self.index])
        else:
            if randint(0, 3) == 0:
                if self.selected_option == "Agents":
                    self.label.text = choice(self.agents)
                elif self.selected_option == "Armes principales":
                    self.label.text = choice(self.primary_weapons)
                elif self.selected_option == "Boucliers":
                    self.label.text = choice(self.shields)
                else:
                    self.label.text = choice(self.secondary_weapons)
            self.button.disabled = False
            self.spinner.disabled = False
            selected.play()
            self.button.text = "Tourner la roulette !"


if __name__ == "__main__":
    ValorantRandomizer().run()
