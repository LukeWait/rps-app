# -*- coding: utf-8 -*-
"""
Project: Rock Paper Scissors LAN App
Description: Allows users to connect to other users over a local area network to play
             Rock Paper Scissors and communicate via text messages.
Version: 2.1.0
Author: Luke Wait
Date: October 8, 2023
License: MIT License

Dependencies (requirements.txt):
packaging==23.2
customtkinter==5.2.1
CTkMessagebox==2.5
CTkListbox==0.10
CTkToolTip==0.8
Pillow==10.1.0
gTTS==2.4.0
playsound==1.2.2

GitHub Repository: https://github.com/LukeWait/rps-app
"""

import socket
import threading
import hashlib
import os
import re
import pkg_resources
import platform
import customtkinter as ctk
from CTkMessagebox import *
from CTkListbox import *
from CTkToolTip import *
from tkinter import *
from PIL import Image
from gtts import gTTS
from playsound import playsound

base_path = pkg_resources.resource_filename(__name__, "")


class Gui(ctk.CTk):
    """Represents the graphical user interface.

    Utilizes the customtkinter library (ctk) for appearance settings and interactions.

    Attributes:
        images_path (str): Path to the directory containing images used in the GUI.
        audio_path (str): Path to the directory containing audio resources.
        images_avatar (dict): Dictionary of avatar images for user selection.
        newuser_avatar_buttons (dict): Dictionary of avatar selection buttons.
        bg_label (ctk.CTkLabel): Label for the background image.
        audio_on (bool): Flag indicating whether audio is enabled.
        tts_on (bool): Flag indicating whether text-to-speech is enabled.

    Methods:
        __init__(): Initializes the Gui object, sets up the main window, loads images, and creates frames.
        load_images(): Loads images used in the GUI from specified directories.
        load_fonts(): Loads fonts used in the GUI from specified directories.
        create_login_frame(): Creates and configures the login frame where users can log in.
        create_newuser_frame(): Creates and configures the new user registration frame.
        create_profile_frame(): Creates and configures the user profile frame.
        create_main_frame(): Creates and configures the main game frame.
        show_login_screen(): Displays the login frame, making it visible to the user.
        show_newuser_screen(): Displays the new user registration frame. Users can create a new account.
        show_main_screen(): Displays the user profile frame showing user information and options.
        show_main_frame(): Displays the main game frame containing game controls and chat functionality.
        update_status_textbox(msg): Updates the status textbox with the provided message.
        update_main_textbox(msg, type): Updates the main game textbox with the provided message.
        update_lobby_state(state): Updates the state of the lobby frame and its components.
        update_game_state(state): Updates the state of the game frame and its components.
        update_lobby_slider_value(value): Updates the displayed value of the lobby host slider.
        ascii_results(player, opponent): Generates an ASCII art representation of the game result.
        text_to_speech(msg): Converts text to speech and plays the audio.
        play_audio(sound): Plays an audio file with the specified sound.
    """

    def __init__(self):
        """Initializes the Gui object, sets up the main window, loads images, and creates frames.

        Configures various settings and elements for the game interface.
        """
        super().__init__()
        
        # customtkinter appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure window
        self.title("Rock Paper Scissors LAN App")
        self.geometry("900x600")
        self.resizable(False, False)

        # Configure grid layout (1x2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Define paths to various resource directories
        self.images_path = os.path.join(base_path, "../assets/images")
        self.fonts_path = os.path.join(base_path, "../assets/fonts")
        self.audio_path = os.path.join(base_path, "../assets/audio")

        # Load images and fonts
        self.load_images()
        self.load_fonts()

        # Dictionary of avatar images
        self.images_avatar = {
            "catdog": self.avatar_catdog,
            "penguin": self.avatar_penguin,
            "monkey": self.avatar_monkey,
            "turtle": self.avatar_turtle,
            "snake": self.avatar_snake,
            "sloth": self.avatar_sloth,
            "chick": self.avatar_chick,
            "whale": self.avatar_whale,
        }

        # Dictionary of avatar selection buttons
        self.newuser_avatar_buttons = {}

        # Set background image
        self.bg_label = ctk.CTkLabel(self, image=self.image_bg, text="")
        self.bg_label.grid(row=0, column=0, rowspan=2)

        # Audio settings
        self.audio_on = True
        self.tts_on = False

        # Create and show frames
        self.create_login_frame()
        self.create_newuser_frame()
        self.create_profile_frame()
        self.create_main_frame()
        self.show_login_screen()


    def load_images(self):
        """Loads images used in the GUI from specified directories.
        """
        try:
            # Images and icons used in GUI
            self.image_bg = ctk.CTkImage(Image.open(os.path.join(self.images_path, "bg-gradient.jpg")), size=(900, 600))
            self.image_rps_login = ctk.CTkImage(Image.open(os.path.join(self.images_path, "rps-pixel.png")), size=(250, 114))
            self.image_rps_profile = ctk.CTkImage(Image.open(os.path.join(self.images_path, "rps-pixel.png")), size=(110, 50))
            self.icon_image = ctk.CTkImage(Image.open(os.path.join(self.images_path, "image-icon.png")), size=(60, 60))
            self.icon_back = ctk.CTkImage(Image.open(os.path.join(self.images_path, "back.png")), size=(20, 20))
            self.icon_add_user = ctk.CTkImage(Image.open(os.path.join(self.images_path, "add-user.png")), size=(20, 20))
            self.icon_chat = ctk.CTkImage(Image.open(os.path.join(self.images_path, "chat.png")), size=(20, 20))
            self.icon_connected = ctk.CTkImage(Image.open(os.path.join(self.images_path, "connect-yes.png")), size=(50, 50))
            self.icon_disconnected = ctk.CTkImage(Image.open(os.path.join(self.images_path, "connect-no.png")), size=(50, 50))
            
            # Avatars referenced by images_avatar dictionary
            self.avatar_catdog = ctk.CTkImage(Image.open(os.path.join(self.images_path, "catdog.png")), size=(60, 60))
            self.avatar_chick = ctk.CTkImage(Image.open(os.path.join(self.images_path, "chick.png")), size=(60, 60))
            self.avatar_monkey = ctk.CTkImage(Image.open(os.path.join(self.images_path, "monkey.png")), size=(60, 60))
            self.avatar_penguin = ctk.CTkImage(Image.open(os.path.join(self.images_path, "penguin.png")), size=(60, 60))
            self.avatar_sloth = ctk.CTkImage(Image.open(os.path.join(self.images_path, "sloth.png")), size=(60, 60))
            self.avatar_snake = ctk.CTkImage(Image.open(os.path.join(self.images_path, "snake.png")), size=(60, 60))
            self.avatar_turtle = ctk.CTkImage(Image.open(os.path.join(self.images_path, "turtle.png")), size=(60, 60))
            self.avatar_whale = ctk.CTkImage(Image.open(os.path.join(self.images_path, "whale.png")), size=(60, 60))

            # CTkMessagebox icons
            self.icon_info = os.path.join(self.images_path, "info.png")
            self.icon_cancel = os.path.join(self.images_path, "cancel.png")
            self.icon_check = os.path.join(self.images_path, "check.png")
            self.icon_question = os.path.join(self.images_path, "question.png")
            self.icon_warning = os.path.join(self.images_path, "warning.png")

        except Exception as e:
            print(f"Error:\n{str(e)}")
    
    def load_fonts(self):
        """Loads fonts used in the GUI from specified directories.
        """
        try:
            ctk.FontManager.load_font(os.path.join(self.fonts_path, "HARLOWSI.TTF"))
            
        except Exception as e:
            print(f"Error:\n{str(e)}")
    
    def create_login_frame(self):
        """Creates and configures the login frame.

        Users can enter username and password to load user data and enter the main screen.
        """
        # Configure login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=0)
        self.login_frame.grid_rowconfigure(4, weight=1)

        # Configure login frame widgets
        self.login_label = ctk.CTkLabel(self.login_frame, text="", image=self.image_rps_login)
        self.login_label.grid(row=0, column=0, padx=25, pady=(150, 15))
        self.login_username = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=200)
        self.login_username.grid(row=1, column=0, padx=50, pady=(15, 15))
        self.login_password = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="Password", width=200)
        self.login_password.grid(row=2, column=0, padx=50, pady=(0, 15))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", width=200)
        self.login_button.grid(row=3, column=0, padx=50, pady=(15, 15))
        self.login_newuser_button = ctk.CTkButton(self.login_frame, corner_radius=0, height=40, border_spacing=10,
                                                       text="Add New User", fg_color="transparent",
                                                       text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.icon_add_user, anchor="center")
        self.login_newuser_button.grid(row=4, column=0, pady=(15, 30), sticky="ews")
    
    def create_newuser_frame(self):
        """Creates and configures the newuser frame.

        Users can choose an avatar and set their username and password here.
        """
        # Configure newuser frame
        self.newuser_frame = ctk.CTkFrame(self, corner_radius=0)
        self.newuser_frame.grid_rowconfigure(6, weight=1)

        # Configure newuser frame widgets
        self.newuser_label = ctk.CTkLabel(self.newuser_frame, text="Choose your warrior:",
                                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.newuser_label.grid(row=0, column=0, columnspan=2, padx=30, pady=(30, 15))
        self.newuser_username = ctk.CTkEntry(self.newuser_frame, width=200, placeholder_text="Username")
        self.newuser_username.grid(row=7, column=0, columnspan=2, padx=50, pady=(0, 15))
        self.newuser_password = ctk.CTkEntry(self.newuser_frame, width=200, show="*", placeholder_text="Password")
        self.newuser_password.grid(row=8, column=0, columnspan=2, padx=50, pady=(0, 15))
        self.newuser_password2 = ctk.CTkEntry(self.newuser_frame, width=200, show="*", placeholder_text="Repeat password")
        self.newuser_password2.grid(row=9, column=0, columnspan=2, padx=50, pady=(0, 15))
        self.newuser_back_button = ctk.CTkButton(self.newuser_frame, height=30, border_spacing=0, text="",
                                                   fg_color="transparent", hover_color=("gray70", "gray30"),
                                                   image=self.icon_back, width=30)
        self.newuser_back_button.grid(row=10, column=0, padx=(50, 0), pady=(15, 30), sticky="w")
        self.newuser_save_button = ctk.CTkButton(self.newuser_frame, text="Save New User", width=130)
        self.newuser_save_button.grid(row=10, column=0, columnspan=2, padx=(0, 50), pady=(15, 30), sticky="e")

        # Enumerate through the images_avatar dictionary to create newuser_avatar_buttons
        for i, (avatar_name, avatar_image) in enumerate(self.images_avatar.items()):
            self.avatar_buttons = ctk.CTkButton(master=self.newuser_frame, border_spacing=0, text="", width=80, 
                                                   fg_color="transparent", image=avatar_image, border_width=0,
                                                   hover_color=("gray70", "gray30"))
            self.avatar_buttons.grid(row=(i % 4) + 1, column=i // 4, padx=25, pady=(0, 15), sticky="ew")
            # Save to the newuser_avatar_buttons dictionary
            self.newuser_avatar_buttons[avatar_name] = self.avatar_buttons

    def create_profile_frame(self):
        """Creates and configures the user profile frame.

        This frame displays user information and options in the main screen.
        """
        # Configure profile frame
        self.profile_frame = ctk.CTkFrame(self, corner_radius=0)
        self.profile_frame.grid_columnconfigure(1, weight=1)

        # Configure profile frame widgets
        self.profile_button = ctk.CTkButton(self.profile_frame, text="", fg_color="transparent", image=self.icon_image,
                                                      font=ctk.CTkFont(family="Harlow Solid Italic", size=36, weight="bold"), 
                                                      width=50, border_spacing=0, hover_color=("gray70", "gray30"))
        self.profile_button.grid(row=0, column=0, padx=(15, 0), pady=15)
        self.profile_button_tooltip = CTkToolTip(self.profile_button, delay=0.5, message="Profile options")
        self.profile_winloss_label = ctk.CTkLabel(self.profile_frame, text="", font=ctk.CTkFont(family="Harlow Solid Italic", size=18))
        self.profile_winloss_label.grid(row=0, column=1, padx=5, pady=0)
        self.profile_rps_label = ctk.CTkLabel(self.profile_frame, text="", image=self.image_rps_profile)
        self.profile_rps_label.grid(row=0, column=2, padx=(0, 20), pady=15, sticky="e")

    def create_main_frame(self):
        """Creates and configures the main frame.

        This frame includes three inner frames: the game frame, the lobby frame, and the status frame.

        The game frame displays game and chat functionality.
        The lobby frame is a tabbed frame that facilitates network connections and application settings.
        The status frame displays the current state of connectivity.
        """
        # Determine the console text size based on the operating system
        if platform.system() == "Windows":
            text_size = 11
        else:
            text_size = 10
      
        # Configure the main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, width=600)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Configure the game frame
        self.game_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=300)
        self.game_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")
        self.game_frame.grid_rowconfigure(1, weight=1)
        self.game_frame.grid_columnconfigure(0, weight=1)

        # Configure the game frame widgets
        self.game_rps_button = ctk.CTkSegmentedButton(self.game_frame, state="disabled")
        self.game_rps_button.grid(row=0, column=0, columnspan=2, padx=(15, 7.5), pady=(10, 15), sticky="ew")
        self.game_rps_button.configure(values=["Rock", "Paper", "Scissors"])
        self.game_textbox = ctk.CTkTextbox(self.game_frame, state="disabled", width=277.5, fg_color="gray8",
                                           font=ctk.CTkFont(family="Consolas", size=text_size), wrap=WORD)
        self.game_textbox.grid(row=1, column=0, columnspan=2, padx=(15, 7.5), pady=0, sticky="nsew")
        self.game_chatbox = ctk.CTkEntry(self.game_frame, placeholder_text="Chat here...", state="disabled")
        self.game_chatbox.grid(row=2, column=0, padx=(15, 0), pady=15, sticky="ew")
        self.game_chat_button = ctk.CTkButton(self.game_frame, height=30, border_spacing=0, text="",
                                                   fg_color="transparent", hover_color=("gray70", "gray30"),
                                                   image=self.icon_chat, width=30, state="disabled")
        self.game_chat_button.grid(row=2, column=1, padx=(0, 7.5), pady=15, sticky="e")
        self.game_chat_button_tooltip = CTkToolTip(self.game_chat_button, delay=0.5, message="Send chat text")
        self.game_textbox.tag_config("local_chat", justify="right", background="#4000FF", relief=RAISED, borderwidth=2, 
                                     lmargin1=30, lmargin2=30, rmargin=8, spacing1=6, spacing3=6)
        self.game_textbox.tag_config("peer_chat", justify="left", background="gray25", relief=RAISED, borderwidth=2, 
                                     lmargin1=8, lmargin2=8,rmargin=30, spacing1=6, spacing3=6)
        self.game_textbox.tag_config("system_chat", justify="center", spacing1=1, spacing3=1)

        # Configure the tabbed lobby frame
        self.lobby_frame = ctk.CTkTabview(self.main_frame, width=277.5)
        self.lobby_frame.grid(row=0, column=1, padx=(7.5, 15), pady=0, sticky="nsew")
        self.lobby_frame.add("Join")
        self.lobby_frame.add("Host")
        self.lobby_frame.add("Settings")
        self.lobby_frame.tab("Join").grid_columnconfigure((0, 1), weight=1, uniform="tabcolumns")
        self.lobby_frame.tab("Join").grid_rowconfigure(0, weight=1)
        self.lobby_frame.tab("Host").grid_columnconfigure((0, 1), weight=1, uniform="tabcolumns")
        self.lobby_frame.tab("Host").grid_rowconfigure(4, weight=1)
        self.lobby_frame.tab("Settings").grid_columnconfigure((0, 1), weight=1, uniform="tabcolumns")
        self.lobby_frame.tab("Settings").grid_rowconfigure(4, weight=1)

        # Configure the join tab widgets
        self.lobby_join_listbox = CTkListbox(self.lobby_frame.tab("Join"), font=("Consolas", text_size), fg_color="gray8", justify="center")
        self.lobby_join_listbox.grid(row=0, column=0, columnspan=2, padx=15, pady=(5, 0), sticky="new")
        self.lobby_join_search_button = ctk.CTkButton(self.lobby_frame.tab("Join"), text="Search", width=80)
        self.lobby_join_search_button.grid(row=1, column=0, padx=15, pady=(20, 15), sticky="e")
        self.lobby_join_button = ctk.CTkButton(self.lobby_frame.tab("Join"), text="Join", state="disabled", width=80)
        self.lobby_join_button.grid(row=1, column=1, padx=15, pady=(20, 15), sticky="w")

        # Configure the host tab widgets
        self.lobby_host_ip_label = ctk.CTkLabel(self.lobby_frame.tab("Host"), text="Local IP")
        self.lobby_host_ip_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 0))
        self.lobby_host_ip_label2 = ctk.CTkLabel(self.lobby_frame.tab("Host"), text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.lobby_host_ip_label2.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 15))
        self.lobby_host_rounds_label = ctk.CTkLabel(self.lobby_frame.tab("Host"), text="Rounds to play")
        self.lobby_host_rounds_label.grid(row=2, column=0, columnspan=2, padx=15, pady=(15, 5))
        self.lobby_host_slider = ctk.CTkSlider(self.lobby_frame.tab("Host"), from_=1, to=5, number_of_steps=4, 
                                               command=self.update_lobby_slider_value)
        self.lobby_host_slider.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")
        self.lobby_host_slider_tooltip = CTkToolTip(self.lobby_host_slider, message="3")
        self.lobby_host_refresh_button = ctk.CTkButton(self.lobby_frame.tab("Host"), text="Refresh", width=80)
        self.lobby_host_refresh_button.grid(row=4, column=0, padx=15, pady=(20, 15), sticky="se")
        self.lobby_host_button = ctk.CTkButton(self.lobby_frame.tab("Host"), text="Host", width=80)
        self.lobby_host_button.grid(row=4, column=1, padx=15, pady=(20, 15), sticky="sw")

        # Configure the settings tab widgets
        self.lobby_settings_server_label = ctk.CTkLabel(self.lobby_frame.tab("Settings"), text="Server Port:")
        self.lobby_settings_server_label.grid(row=0, column=0, padx=7.5, pady=(20, 7.5), sticky="e")
        self.lobby_settings_serverport = ctk.CTkEntry(self.lobby_frame.tab("Settings"), placeholder_text="51515", width=80)
        self.lobby_settings_serverport.grid(row=0, column=1, padx=7.5, pady=(20, 7.5), sticky="w")
        self.lobby_settings_broad_label = ctk.CTkLabel(self.lobby_frame.tab("Settings"), text="Broadcast Port:")
        self.lobby_settings_broad_label.grid(row=1, column=0, padx=7.5, pady=7.5, sticky="e")
        self.lobby_settings_broadport = ctk.CTkEntry(self.lobby_frame.tab("Settings"), placeholder_text="12121", width=80)
        self.lobby_settings_broadport.grid(row=1, column=1, padx=7.5, pady=7.5, sticky="w")
        self.lobby_settings_audio_label = ctk.CTkLabel(self.lobby_frame.tab("Settings"), text="Audio:")
        self.lobby_settings_audio_label.grid(row=2, column=0, padx=7.5, pady=7.5, sticky="e")
        self.lobby_settings_audio_switch = ctk.CTkSwitch(self.lobby_frame.tab("Settings"), text="")
        self.lobby_settings_audio_switch.grid(row=2, column=1, padx=7.5, pady=7.5, sticky="w")
        self.lobby_settings_audio_switch.select()
        self.lobby_settings_tts_label = ctk.CTkLabel(self.lobby_frame.tab("Settings"), text="Text to Speech:")
        self.lobby_settings_tts_label.grid(row=3, column=0, padx=7.5, pady=7.5, sticky="e")
        self.lobby_settings_tts_switch = ctk.CTkSwitch(self.lobby_frame.tab("Settings"), text="")
        self.lobby_settings_tts_switch.grid(row=3, column=1, padx=7.5, pady=7.5, sticky="w")
        self.lobby_settings_default_button = ctk.CTkButton(self.lobby_frame.tab("Settings"), text="Default", width=80)
        self.lobby_settings_default_button.grid(row=4, column=0, padx=15, pady=(7.5, 15), sticky="se")
        self.lobby_settings_save_button = ctk.CTkButton(self.lobby_frame.tab("Settings"), text="Save", width=80)
        self.lobby_settings_save_button.grid(row=4, column=1, padx=15, pady=(7.5, 15), sticky="sw")

        # Configure the status frame
        self.status_frame = ctk.CTkFrame(self.main_frame, width=277.5)
        self.status_frame.grid(row=1, column=1, padx=(7.5, 15), pady=15, sticky="nsew")
        self.status_frame.grid_rowconfigure(0, weight=1)
        self.status_frame.grid_columnconfigure(0, weight=1)

        # Configure the status frame widgets
        self.status_connection_label = ctk.CTkLabel(self.status_frame, text="Connection Status", font=ctk.CTkFont(size=20, weight="bold"))
        self.status_connection_label.grid(row=0, column=0, columnspan=2, padx=0, pady=15)
        self.status_textbox = ctk.CTkTextbox(self.status_frame, height=80, state="disabled", width=165, fg_color="gray8",
                                             font=ctk.CTkFont(family="Consolas", size=text_size))
        self.status_textbox.grid(row=1, column=0, padx=(15, 0), pady=0, sticky="w")
        self.status_connection_button = ctk.CTkButton(self.status_frame, text="", fg_color="transparent", image=self.icon_disconnected, 
                                                         border_spacing=6, width=50, hover_color=("gray70", "gray30"),
                                                         state="disabled")
        self.status_connection_button.grid(row=1, column=1, padx=15, pady=0)
        self.status_connection_button_tooltip = CTkToolTip(self.status_connection_button, delay=0.5, message="Disconnect")
        self.status_progressbar = ctk.CTkProgressBar(self.status_frame, height=12)
        self.status_progressbar.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        self.status_progressbar.configure(mode="indeterminate")

    def show_login_screen(self):
        """Displays the login frame.
        """
        self.newuser_frame.grid_forget()
        self.profile_frame.grid_forget()
        self.main_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.login_button.focus_set()
        self.login_username.delete(0, END)
        self.login_username.configure(placeholder_text="Username")
        self.login_password.delete(0, END)
        self.login_password.configure(placeholder_text="Password")

    def show_newuser_screen(self):
        """Displays the newuser frame.
        """
        self.login_frame.grid_forget()
        self.main_frame.grid_forget()
        self.newuser_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.newuser_save_button.focus_set()
        self.newuser_username.delete(0, END)
        self.newuser_username.configure(placeholder_text="Username")
        self.newuser_password.delete(0, END)
        self.newuser_password.configure(placeholder_text="Password")
        self.newuser_password2.delete(0, END)
        self.newuser_password2.configure(placeholder_text="Repeat password")

    def show_main_screen(self):
        """Displays the user profile and main frames.
        """
        self.login_frame.grid_forget()
        self.newuser_frame.grid_forget()
        self.profile_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid(row=1, column=0, sticky="ns")
        self.lobby_join_search_button.focus_set()

    def update_status_textbox(self, msg):
        """Updates the status textbox with the provided message.

        This textbox is used for displaying the network connection status.
        
        Args:
            msg (str): The message to display in the status textbox.
        """
        self.status_textbox.configure(state="normal")
        self.status_textbox.delete("0.0", END)
        self.status_textbox.insert("0.0", msg)
        self.status_textbox.configure(state="disabled")

    def update_main_textbox(self, msg, type):
        """Updates the main game textbox with the provided message.

        This textbox is used for displaying chat messages and game related information.

        Args:
            msg (str): The message to display in the game textbox.
            type (str): The type of message (e.g., "local_chat", "peer_chat", "system_chat").
        """
        if type == "system_chat":
            self.game_textbox.configure(state="normal")
            self.game_textbox.insert(END, msg, type)
            self.game_textbox.insert(END, "\n")
            self.game_textbox.see(END)
            self.game_textbox.configure(state="disabled")
        elif type == "local_chat" or type == "peer_chat":
            self.game_textbox.configure(state="normal")
            self.game_textbox.insert(END, msg + "\n", type)
            self.game_textbox.insert(END, "\n")
            self.game_textbox.see(END)
            self.game_textbox.configure(state="disabled")
            self.game_chatbox.delete(0, END)
            
            # Start text-to-speech and audio in separate threads
            if self.tts_on:
                tts = threading.Thread(target=lambda: self.text_to_speech(msg))
                tts.start()

            txt_audio = {"local_chat": "txt-send.mp3", "peer_chat": "txt-receive.mp3"}    
            if self.audio_on:
                audio = threading.Thread(target=lambda: self.play_audio(txt_audio[type]))
                audio.start()

    def update_lobby_state(self, state):
        """Updates the state of the lobby frame and its components.

        Args:
            state (str): The state to set ("normal" or "disabled").
        """
        if state == "normal":
            self.status_connection_button.configure(image=self.icon_disconnected, state="disabled")
            self.status_progressbar.stop()
            self.lobby_frame.configure(state="normal")
            self.lobby_join_search_button.configure(state="normal")
            self.lobby_host_button.configure(state="normal")
            self.lobby_host_refresh_button.configure(state="normal")
            self.lobby_host_slider.configure(state="normal")
        elif state == "disabled":
            self.status_connection_button.configure(image=self.icon_connected, state="normal")
            self.status_progressbar.start()
            self.lobby_frame.configure(state="disabled")
            self.lobby_join_button.configure(state="disabled")
            self.lobby_join_search_button.configure(state="disabled")
            if self.lobby_join_listbox.size() > 0:
                self.lobby_join_listbox.delete(0, END)
            self.lobby_host_button.configure(state="disabled")
            self.lobby_host_refresh_button.configure(state="disabled")
            self.lobby_host_slider.configure(state="disabled")

    def update_game_state(self, state):
        """Updates the state of the game frame and its components.

        Args:
            state (str): The state to set ("normal" or "disabled").
        """
        if state == "normal":
            self.game_rps_button.configure(state="normal")
            self.game_rps_button.set("unselect")
            self.game_chat_button.configure(state="normal")
            self.game_chatbox.configure(state="normal")
        elif state == "disabled":
            self.game_rps_button.configure(state="disabled")
            self.game_rps_button.set("unselect")
            self.game_chat_button.configure(state="disabled")
            self.game_chatbox.configure(state="disabled")

    def update_lobby_slider_value(self, value):
        """Updates the displayed tooltip value of the lobby host slider.

        Args:
            value (int): The value to display on the slider.
        """
        self.lobby_host_slider_tooltip.configure(message=int(value))

    def ascii_results(self, player, opponent):
        """Generates an ASCII art representation of the game result.

        Args:
            player (str): The player's choice ("Rock", "Paper", or "Scissors").
            opponent (str): The opponent's choice ("Rock", "Paper", or "Scissors").

        Returns:
            str: The ASCII art representation of the game result.
        """
        rock_scissors =     f"    _______       \ //         _______    \n" \
                            f"---/   ____)       v/ S.  ____(____   \---\n" \
                            f"      (_____)            (______          \n" \
                            f"      (_____)           (__________       \n" \
                            f"      (____)                  (____)      \n" \
                            f"---.__(___)                    (___)__.---\n" \
                            f"                --YOU WIN--               \n"
        
        rock_paper =        f"    _______       \ //         _______    \n" \
                            f"---/   ____)       v/ S.  ____(____   \---\n" \
                            f"      (_____)            (______          \n" \
                            f"      (_____)           (_______          \n" \
                            f"      (____)             (_______         \n" \
                            f"---.__(___)                (__________.---\n" \
                            f"               --YOU LOSE--               \n"
        
        rock_rock =         f"    _______       \ //         _______    \n" \
                            f"---/   ____)       v/ S.      (____   \---\n" \
                            f"      (_____)                (_____)      \n" \
                            f"      (_____)                (_____)      \n" \
                            f"      (____)                  (____)      \n" \
                            f"---.__(___)                    (___)__.---\n" \
                            f"                  --TIE--                 \n"
        
        paper_rock =        f"    _______       \ //         _______    \n" \
                            f"---/   ____)____   v/ S.      (____   \---\n" \
                            f"          ______)            (_____)      \n" \
                            f"          _______)           (_____)      \n" \
                            f"         _______)             (____)      \n" \
                            f"---.__________)                (___)__.---\n" \
                            f"                --YOU WIN--               \n"
        
        paper_scissors =    f"    _______       \ //         _______    \n" \
                            f"---/   ____)____   v/ S.  ____(____   \---\n" \
                            f"          ______)        (______          \n" \
                            f"          _______)      (__________       \n" \
                            f"         _______)             (____)      \n" \
                            f"---.__________)                (___)__.---\n" \
                            f"               --YOU LOSE--               \n"

        paper_paper =       f"    _______       \ //         _______    \n" \
                            f"---/   ____)____   v/ S.  ____(____   \---\n" \
                            f"          ______)        (______          \n" \
                            f"          _______)      (_______          \n" \
                            f"         _______)        (_______         \n" \
                            f"---.__________)            (__________.---\n" \
                            f"                  --TIE--                 \n"
        
        scissors_paper =    f"    _______       \ //         _______    \n" \
                            f"---/   ____)____   v/ S.  ____(____   \---\n" \
                            f"          ______)        (______          \n" \
                            f"       __________)      (_______          \n" \
                            f"      (____)             (_______         \n" \
                            f"---.__(___)                (__________.---\n" \
                            f"                --YOU WIN--               \n"

        scissors_rock =     f"    _______       \ //         _______    \n" \
                            f"---/   ____)____   v/ S.      (____   \---\n" \
                            f"          ______)            (_____)      \n" \
                            f"       __________)           (_____)      \n" \
                            f"      (____)                  (____)      \n" \
                            f"---.__(___)                    (___)__.---\n" \
                            f"               --YOU LOSE--               \n"

        scissors_scissors = f"    _______       \ //         _______    \n" \
                            f"---/   ____)____   v/ S.  ____(____   \---\n" \
                            f"          ______)        (______          \n" \
                            f"       __________)      (__________       \n" \
                            f"      (____)                  (____)      \n" \
                            f"---.__(___)                    (___)__.---\n" \
                            f"                  --TIE--                 \n"

        # Dictionary references ASCII art based on outcome
        outcomes = {
            ("Rock", "Scissors"): rock_scissors,
            ("Rock", "Paper"): rock_paper,
            ("Rock", "Rock"): rock_rock,
            ("Paper", "Rock"): paper_rock,
            ("Paper", "Scissors"): paper_scissors,
            ("Paper", "Paper"): paper_paper,
            ("Scissors", "Paper"): scissors_paper,
            ("Scissors", "Rock"): scissors_rock,
            ("Scissors", "Scissors"): scissors_scissors
        }

        return outcomes.get((player, opponent))

    def text_to_speech(self, msg):
        """Converts text to speech and plays the audio file.

        Args:
            msg (str): The text message to convert to speech and play.
        """
        myobj = gTTS(text=msg, lang="en", slow=False)
        audio_file = os.path.join(self.audio_path, "chat-to-speech.mp3")
        if os.path.exists(audio_file):
            os.remove(audio_file)
        myobj.save(audio_file)
        playsound(audio_file)

    def play_audio(self, sound):
        """Plays an audio file with the specified sound.

        Args:
            sound (str): The name of the audio file to play.
        """
        audio_file = os.path.join(self.audio_path, sound)
        playsound(audio_file)


class Network:
    """Manages network-related functionality.

    Attributes:
        gui (Gui): Reference to the shared Gui instance.
        local_ip (str): Local IP address.
        server_port (int): Default server port.
        broadcast_port (int): Port for broadcasting.
        broadcast_address (str): Broadcast address for server discovery.

    Methods:
        get_local_ip(): Retrieves the local IP address and calculates the broadcast address.
        discover_servers(): Discovers available servers on the network.
    """

    def __init__(self, gui):
        """Initializes the Network instance.
        
        Args:
            gui (Gui): Reference to the shared Gui instance.
        """
        self.gui = gui
        self.local_ip = None
        self.broadcast_address = None
        self.server_port = 51515
        self.broadcast_port = 12121

    def get_local_ip(self):
        """Retrieves the local IP address and calculates the broadcast address.
        """    
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80)) # Connect to a remote server
            self.local_ip = sock.getsockname()[0]
            ip_parts = self.local_ip.split('.')
            ip_parts[3] = '255' # Calculate the broadcast address
            self.broadcast_address = '.'.join(ip_parts)
            
        except Exception as e:
            CTkMessagebox(title="IP Retrieval Failed", message=f"An error occurred:\n{str(e)}", 
                            icon=self.gui.icon_cancel, master=self.gui, sound=True)
            self.local_ip = "No IP Found"
            self.broadcast_address = None

        finally:
            sock.close()
            
    def discover_servers(self):
        """Discovers available servers on the network.

        Returns:
            list: List of available servers with their details.
                Each entry is a tuple (server_ip, server_port, username, total_rounds).
        """
        available_servers = []

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            udp_socket.sendto(b"LOOKUP", (self.broadcast_address, self.broadcast_port))
            udp_socket.settimeout(5)

            while True:
                try:
                    data, addr = udp_socket.recvfrom(1024)
                    data_values = data.decode('utf-8').split(',')
                    if len(data_values) == 3:
                        server_port, username, total_rounds = data_values
                        available_servers.append((addr[0], server_port, username, total_rounds))
                        
                except socket.timeout:
                    break  # Timeout reached, stop receiving

        except Exception as e:
            CTkMessagebox(title="Server Lookup Failed", message=f"Error:\n{str(e)}", 
                            icon=self.gui.icon_cancel, master=self.gui, sound=True)
        
        finally:
            udp_socket.close()
            return available_servers


class Server:
    """Manages server-side network communication.

    Attributes:
        app (App): Reference to the App instance.
        gui (Gui): Reference to the Gui instance.
        network (Network): Reference to the Network instance.
        client_connected (bool): Indicates whether a client is connected.
        server_socket (socket.socket): Server socket for handling client connections.
        client_socket (socket.socket): Client socket for communication with connected client.
        udp_socket (socket.socket): UDP socket for broadcasting and listening to broadcast messages.

    Methods:
        start(): Starts the server and waits for client connections.
        stop(game_state): Stops the server and sends a disconnect message to the client.
        broadcast_listen(): Listens for broadcast messages from clients.
        stop_listen(): Sends a disconnect message to stop listening for broadcast messages.
    """

    def __init__(self, app, gui, network):
        """Initializes the Server instance.

        Args:
            app (App): Reference to the App instance.
            gui (Gui): Reference to the Gui instance.
            network (Network): Reference to the Network instance.
        """
        self.app = app
        self.gui = gui
        self.network = network
        self.client_connected = False
        self.server_socket = None
        self.client_socket = None
        self.udp_socket = None

    def start(self):
        """Starts the server and waits for client connections.

        A connection facilitates game and chat communications.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.network.local_ip, self.network.server_port))
            self.server_socket.listen(1)
            print(f"Server listening on port {self.network.server_port}")

            self.client_socket, (client_ip, _) = self.server_socket.accept()
            print(f"Accepted connection from {client_ip}")
            self.app.gui.after(0, self.app.network_connected, client_ip)
            self.client_connected = True

            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                if data.startswith(b"DISCONNECT"):
                    game_state = data[len(b"DISCONNECT"):].decode("utf-8")
                    if game_state == "mid_game":
                        self.app.gui.after(0, self.app.dropout_resolution, "player")
                    break
                
                if data.startswith(b"CHAT"):
                    msg = data[len(b"CHAT"):].decode("utf-8")
                    self.app.gui.after(0, self.app.network_chat, msg, "peer_chat")
                
                if data.startswith(b"GAME"):
                    self.app.opponent_choice = data[len(b"GAME"):].decode("utf-8")
                    if self.app.player_choice:
                        self.app.gui.after(0, self.app.determine_results)
                    else:
                        self.app.gui.after(0, self.app.network_chat, 
                                           f"{self.app.opponent_username} has chosen...\n", "system_chat")
            
            self.client_socket.close()
            self.server_socket.close()
            
        except Exception as e:
            if self.app.allow_gui_update:
                CTkMessagebox(title="Server Connection Error", message=f"Error:\n{str(e)}", 
                            icon=self.gui.icon_cancel, master=self.gui, sound=True)

        finally:
            self.client_connected = False
            if self.app.allow_gui_update:
                self.app.gui.after(0, self.app.network_disconnected)

    def stop(self, game_state):
        """Stops the server and sends a disconnect message to the client.

        Args:
            game_state (str): The game state at the time of disconnection.
        """
        if self.client_connected:
            self.client_socket.send(b"DISCONNECT" + game_state.encode("utf-8"))
        else:
            self.server_socket.close()

    def broadcast_listen(self):
        """Listens for broadcast messages from clients.

        Broadcast messages can be used for server discovery by clients.
        """
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(('', self.network.broadcast_port))

            while True:
                data, addr = self.udp_socket.recvfrom(1024)
                if data.startswith(b"LOOKUP"):
                    data_to_send = f"{self.network.server_port},{self.app.user_profile['username']},{self.app.total_rounds}"
                    self.udp_socket.sendto(data_to_send.encode("utf-8"), addr)

                if data.startswith(b"CONNECT"):
                    data_values = data[len(b"CONNECT"):].decode('utf-8').split(',')
                    if len(data_values) == 2:
                        requested_ip, username = data_values
                        if requested_ip == self.network.local_ip:
                            self.app.opponent_username = username
                            # Send an "ACK" response back to the sender
                            self.udp_socket.sendto(b"ACK", addr)
                            # Start the server and close the broadcast_thread by exiting loop
                            self.app.gui.after(0, self.app.launch_server)
                            break

                if data == b"DISCONNECT":
                    if self.app.allow_gui_update:
                        self.app.gui.after(0, self.app.network_disconnected)
                    break  # Exit the loop when "DISCONNECT" message is received
        
        except Exception as e:
            CTkMessagebox(title="Hosting Connection Error", message=f"Error:\n{str(e)}", 
                          icon=self.gui.icon_cancel, master=self.gui, sound=True)

        finally:
            self.udp_socket.close()

    def stop_listen(self):
        """Sends a disconnect message to stop listening for broadcast messages.
        """
        try:
            self.udp_socket.sendto(b"DISCONNECT", (self.network.local_ip, self.network.broadcast_port))

        except Exception as e:
            CTkMessagebox(title="Error Cancelling Hosting", message=f"Error:\n{str(e)}", 
                          icon=self.gui.icon_cancel, master=self.gui, sound=True)


class Client:
    """Manages client-side network communication.

    Attributes:
        app (App): Reference to the App instance.
        gui (Gui): Reference to the Gui instance.
        network (Network): Reference to the Network instance.
        client_socket (socket.socket): Client socket for communication with the server.
        udp_socket (socket.socket): UDP socket for requesting server connection.

    Methods:
        start(server_ip, server_port): Initiates a connection to the server.
        stop(game_state): Stops the client and sends a disconnect message to the server.
    """

    def __init__(self, app, gui, network):
        """Initializes the Client instance.

        Args:
            app (App): Reference to the App instance.
            gui (Gui): Reference to the Gui instance.
            network (Network): Reference to the Network instance.
        """
        self.app = app
        self.gui = gui
        self.network = network
        self.client_socket = None
        self.udp_socket = None

    def start(self, server_ip, server_port):
        """Sends a connection request to a server through the broadcast address and 
        after confirmation, initiates a connection to the server.

        A connection facilitates game and chat communications.

        Args:
            server_ip (str): IP address of the server to connect to.
            server_port (int): Port number of the server to connect to.
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Request a connection from the broadcast port of the server
            udp_socket.bind((self.network.local_ip, self.network.broadcast_port))
            udp_socket.sendto(b"CONNECT" + f"{server_ip},{self.app.user_profile['username']}".encode("utf-8"), 
                              (server_ip, self.network.broadcast_port)) 
            udp_socket.settimeout(5)
            response, addr = udp_socket.recvfrom(1024)
            udp_socket.close()
            
            if response.startswith(b"ACK"):
                # Establish connection to server
                self.client_socket.connect((server_ip, server_port))
                self.app.gui.after(0, self.app.network_connected, server_ip)
                
                while True:
                    data = self.client_socket.recv(1024)
                    if not data:
                        break

                    if data.startswith(b"DISCONNECT"):
                        game_state = data[len(b"DISCONNECT"):].decode("utf-8")
                        if game_state == "mid_game":
                            self.app.gui.after(0, self.app.dropout_resolution, "player")
                        break

                    if data.startswith(b"CHAT"):
                        msg = data[len(b"CHAT"):].decode("utf-8")
                        self.app.gui.after(0, self.app.network_chat, msg, "peer_chat")
                    
                    if data.startswith(b"GAME"):
                        self.app.opponent_choice = data[len(b"GAME"):].decode("utf-8")
                        if self.app.player_choice:
                            self.app.gui.after(0, self.app.determine_results)
                        else:
                            self.app.gui.after(0, self.app.network_chat, 
                                               f"{self.app.opponent_username} has chosen...\n", "system_chat")

            else:
                CTkMessagebox(title="Server Connection Error", message="Server didn't acknowledge the connection request", 
                            icon=self.gui.icon_cancel, master=self.gui, sound=True)

        except Exception as e:
            if self.app.allow_gui_update:
                CTkMessagebox(title="Server Connection Error", message=f"Error:\n{str(e)}", 
                            icon=self.gui.icon_cancel, master=self.gui, sound=True)
        
        finally:
            self.client_socket.close()
            if self.app.allow_gui_update:
                self.app.gui.after(0, self.app.network_disconnected)

    def stop(self, game_state):
        """Stops the client and sends a disconnect message to the server.

        Args:
            game_state (str): The game state at the time of disconnection.
        """
        self.client_socket.send(b"DISCONNECT" + game_state.encode("utf-8"))


class App:
    """Manages the Rock Paper Scissors application.

    Attributes:
        gui (Gui): Reference to the Gui instance.
        network (Network): Reference to the Network instance.
        server (Server): Reference to the Server instance.
        client (Client): Reference to the Client instance.
        broadcast_thread (threading.Thread): Thread for broadcasting and listening to servers.
        server_thread (threading.Thread): Thread for managing the server.
        client_thread (threading.Thread): Thread for managing the client.
        allow_gui_update (bool): Flag to allow GUI updates.
        user_data_path (str): Path to the user data file.
        selected_avatar (str): The selected avatar name.
        user_profile (dict): User profile data.
        opponent_username (str): Opponent's username.
        player_choice (str): The player's choice (Rock, Paper, Scissors).
        opponent_choice (str): The opponent's choice (Rock, Paper, Scissors).
        total_rounds (int): Total number of rounds in a game.
        current_round (int): Current round number.

    Methods:
        event_login(event=None): Handles the login event.
        event_logout(): Logs the user out.
        event_add_newuser(): Displays the new user registration form.
        event_select_avatar(name): Handles avatar selection.
        event_save_newuser(event=None): Saves a new user's registration details.
        event_profile(): Displays user profile information.
        event_rps_chosen(value): Handles the player's Rock-Paper-Scissors choice.
        event_chat(event=None): Handles chat messages.
        event_ip_select(selected_option): Handles IP selection in the lobby.
        event_join_search(): Searches for available servers to join.
        event_join(): Joins a selected server.
        event_host_refresh(): Refreshes the host settings.
        event_host(): Hosts a game.
        event_settings_default(): Resets settings to default values.
        event_settings_save(): Saves user settings.
        event_disconnect(scope=None): Handles disconnection events.
        launch_server(): Launches the server.
        network_connected(peer_ip): Handles network connection.
        network_disconnected(): Handles network disconnection.
        network_chat(msg, type): Handles network chat messages.
        determine_results(): Determines game results.
        dropout_resolution(actor): Handles dropout resolution.
        update_profile_stats(): Updates user profile statistics in the GUI.
        save_profile_stats(): Saves user profile statistics to the data file.
        on_exit(): Handles application exit.
    """

    def __init__(self):
        """Initializes the App class.

        Configures various settings and defines button commands.
        """
        # Instances of classes
        self.gui = Gui()
        self.network = Network(self.gui)
        self.server = Server(self, self.gui, self.network)
        self.client = Client(self, self.gui, self.network)

        # Relative path to user save data
        self.user_data_path = os.path.join(base_path, "../data/user_data.txt")

        # User details and game variables
        self.user_profile = None
        self.opponent_username = None
        self.player_choice = None
        self.opponent_choice = None
        self.total_rounds = None
        self.current_round = None

        # Server/client threads
        self.broadcast_thread = None
        self.server_thread = None
        self.client_thread = None

        # Selected Gui Elements
        self.selected_avatar = None

        # Gui element commands and bindings
        self.gui.login_button.configure(command=self.event_login)
        self.gui.login_newuser_button.configure(command=self.event_add_newuser)
        self.gui.newuser_back_button.configure(command=self.event_logout)
        self.gui.newuser_save_button.configure(command=self.event_save_newuser)
        self.gui.profile_button.configure(command=self.event_profile)
        self.gui.game_rps_button.configure(command=self.event_rps_chosen)
        self.gui.game_chat_button.configure(command=self.event_chat)
        self.gui.lobby_join_listbox.configure(command=self.event_ip_select)
        self.gui.lobby_join_search_button.configure(command=self.event_join_search)
        self.gui.lobby_join_button.configure(command=self.event_join)
        self.gui.lobby_host_refresh_button.configure(command=self.event_host_refresh)
        self.gui.lobby_host_button.configure(command=self.event_host)
        self.gui.lobby_settings_default_button.configure(command=self.event_settings_default)
        self.gui.lobby_settings_save_button.configure(command=self.event_settings_save)
        self.gui.status_connection_button.configure(command=self.event_disconnect)
        for avatar_name, avatar_button in self.gui.newuser_avatar_buttons.items():
            avatar_button.configure(command=lambda name=avatar_name: self.event_select_avatar(name))
        self.gui.login_username.bind("<Return>", self.event_login)
        self.gui.login_password.bind("<Return>", self.event_login)
        self.gui.newuser_username.bind("<Return>", self.event_save_newuser)
        self.gui.newuser_password.bind("<Return>", self.event_save_newuser)
        self.gui.newuser_password2.bind("<Return>", self.event_save_newuser)
        self.gui.game_chatbox.bind("<Return>", self.event_chat)

        # Enables function on exit and safely close threads
        self.gui.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.allow_gui_update = True

    def event_login(self, event=None):
        """Event handler for the "Login" button on the login screen.

        Checks username and hashed password against saved users in the user data file.
        Successful login loads the user profile and shows the main screen.

        Args:
            event (optional): Defaults to None - enables binding of enter key to button.
        """
        self.gui.login_button.focus_set()
        username = self.gui.login_username.get()
        password = hashlib.sha256(self.gui.login_password.get().encode()).hexdigest()
        user_found = False

        try:
            with open(self.user_data_path, "r") as file:
                for line in file:
                    parts = line.strip().split(", ")
                    if parts[0] == username and parts[1] == password:
                        user_found = True
                        
                        # Save logged in user data to the user_profile list
                        self.user_profile = {
                            "username": parts[0],
                            "password": parts[1],
                            "avatar": parts[2],
                            "wins": int(parts[3]),
                            "loses": int(parts[4]),
                            "ties": int(parts[5]),
                        }

                        # Show main screen
                        self.gui.show_main_screen()

                        # Get user details for display in the main screen
                        self.gui.profile_button.configure(text=f" {self.user_profile['username']} ", 
                                              image=self.gui.images_avatar.get(self.user_profile['avatar']))
                        self.update_profile_stats()
                        self.network.get_local_ip()
                        self.gui.lobby_host_ip_label2.configure(text=self.network.local_ip)

                        break

            if not user_found:
                CTkMessagebox(title="Login Failed", message="User not found", icon=self.gui.icon_warning, master=self.gui)
        except FileNotFoundError:
            CTkMessagebox(title="Login Failed", message="File not found: user_data.txt", 
                          icon=self.gui.icon_cancel, master=self.gui, sound=True)
        except Exception as e:
            CTkMessagebox(title="Login Failed", message=f"An error occurred during file access:\n{str(e)}", 
                          icon=self.gui.icon_cancel, master=self.gui, sound=True)

    def event_logout(self):
        """Event handler for the "Logout" button in the Profile Options messagebox.
        Also triggers from "Back" button in the newuser screen.

        Logs out the user, hides all frames except the login frame, and clears user-related data.
        """
        # Hide all frames except login frame
        self.gui.show_login_screen()

        # Clear user_profile list, input fields and reset placeholder text
        self.user_profile = None
        if self.selected_avatar is not None:
            self.gui.newuser_avatar_buttons.get(self.selected_avatar).configure(fg_color="transparent")
            self.selected_avatar = None

    def event_add_newuser(self):
        """Event handler for the "Add New User" button on the login screen.

        Hides the login screen and displays the newuser screen.
        """
        self.gui.show_newuser_screen()

    def event_select_avatar(self, name):
        """Event handler for the avatar image buttons on the newuser screen.

        Highlights the selected avatar image and updates the selected_avatar attribute.

        Args:
            name (str): The name of the selected avatar image.
        """
        if self.selected_avatar is not None:
            self.gui.newuser_avatar_buttons.get(self.selected_avatar).configure(fg_color="transparent")
        self.gui.newuser_avatar_buttons.get(name).configure(fg_color="#007BA7")
        self.selected_avatar = name
   
    def event_save_newuser(self, event=None):
        """Event handler for the "Save" button on the newuser screen.

        Save a new user's registration data and login the user.
        Performs input validation, checks for duplicate users, and writes the user's data to file.

        Args:
            event (optional): Defaults to None - enables binding of enter key to button.
        """
        self.gui.newuser_save_button.focus_set()
        username = self.gui.newuser_username.get()
        password = self.gui.newuser_password.get()
        password2 = self.gui.newuser_password2.get()
        
        save_valid = True
        error_msg = ""

        try:
            # Check if user already exists in user_data.txt file
            with open(self.user_data_path, "r") as file:
                for line in file:
                    parts = line.strip().split(", ")
                    if parts[0] == username and parts[1] == password:
                        error_msg += "User already exists\n"
                        save_valid = False
                        file.close()
                        break

            # Input validation checks  
            if save_valid:
                error_msg += "Invalid fields found:\n"
                if self.selected_avatar is None:
                    error_msg += "\u2022 No avatar selected\n"
                    save_valid = False
                if not username:
                    error_msg += "\u2022 Username field empty\n"
                    save_valid = False
                elif len(username) < 2 or len(username) > 14:
                    error_msg += "\u2022 Username must be 2-14 char long\n"
                    save_valid = False
                if not password:
                    error_msg += "\u2022 Password field empty\n"
                    save_valid = False
                if not password2:
                    error_msg += "\u2022 Repeat password field empty\n"
                    save_valid = False
                if password != password2:
                    error_msg += "\u2022 Passwords don't match\n"
                    save_valid = False
                if ',' in username or ',' in password or ',' in password2:
                    error_msg += "\u2022 Fields cannot contain a comma\n"
            
            # Password requirements
            if save_valid:
                if not re.match(r'^(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])(.{8,})$', password):
                    error_msg = "Password must contain:\n"
                    error_msg += "\u2022 At least 8 characters\n"
                    error_msg += "\u2022 At least one number\n"
                    error_msg += "\u2022 At least one symbol\n"
                    save_valid = False

            # Write user details to user_data.txt file and login user
            if save_valid:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                with open(self.user_data_path, "a") as file:
                    file.write(f"{username}, {hashed_password}, " \
                               f"{self.selected_avatar}, 0, 0, 0\n")
                    file.close()

                    self.gui.login_username.delete(0, END)
                    self.gui.login_password.delete(0, END)
                    self.gui.login_username.insert(0, username)
                    self.gui.login_password.insert(0, password)
                    self.event_login()
            else:
                CTkMessagebox(title="Save User Failed", message=error_msg.rstrip('\n'), icon=self.gui.icon_info, master=self.gui)

        except FileNotFoundError:
            CTkMessagebox(title="Save Data Access Failed", message="File not found: user_data.txt", 
                          icon=self.gui.icon_cancel, master=self.gui)
        except Exception as e:
            CTkMessagebox(title="Save Data Access Failed Failed", message=f"An error occurred during file access:\n {str(e)}", 
                          icon=self.gui.icon_cancel, master=self.gui)

    def event_profile(self):
        """Event hanlder for the "Profile Options" button on the main screen.

        Opens a message box displaying profile options such as logout, exit, and cancel.
        Depending on the user's choice, it triggers the corresponding event.
        """
        msg = CTkMessagebox(title="Profile Options", message=f"Rock - Paper - Scissors\n\nVersion 2.3\n2023\nLuke Wait", 
                            icon=self.gui.icon_info, option_1="Logout", option_2="Exit", option_3="Cancel", master=self.gui)
        
        if msg.get() == "Logout":
            self.event_disconnect("logout")
        elif msg.get() == "Exit":
            self.event_disconnect("exit")

    def event_rps_chosen(self, value):
        """Event handler for the "Rock-Paper-Scissors" button on the main screen.

        Upon selection it disables the RPS buttons, records the user's choice, and sends it to the opponent. 
        If both players have made their choices, it calls determine_results to calculate the round outcome.

        Args:
            value (str): The user's Rock-Paper-Scissors choice ('Rock', 'Paper', or 'Scissors').
        """
        self.gui.game_rps_button.configure(state="disabled")
        self.player_choice = value

        if self.server_thread and self.server_thread.is_alive():
            self.server.client_socket.send(b"GAME" + value.encode("utf-8"))
        elif self.client_thread and self.client_thread.is_alive():
            self.client.client_socket.send(b"GAME" + value.encode("utf-8"))

        if self.opponent_choice:
            self.determine_results()
        else:
            self.network_chat(f"Waiting for {self.opponent_username}...\n", "system_chat")

    def event_chat(self, event=None):
        """Event handler for the "Send Chat Text" button on the main screen.

        Retrieves message from the chat input, sends it to the opponent, and displays in the main game window.

        Args:
            event (optional): Defaults to None - enables binding of enter key to button.
        """
        msg = self.gui.game_chatbox.get()
        
        if msg:
            self.network_chat(msg, "local_chat")
            if self.server_thread and self.server_thread.is_alive():
                self.server.client_socket.send(b"CHAT" + msg.encode("utf-8"))
            elif self.client_thread and self.client_thread.is_alive():
                self.client.client_socket.send(b"CHAT" + msg.encode("utf-8"))

    def event_ip_select(self, selected_option):
        """Event handler for the listbox in the join tab of the lobby section.
         
        Enables the "Join" button when an option is selected.

        Args:
            selected_option: The index of the selected listbox item.
        """
        self.gui.lobby_join_button.configure(state="normal")

    def event_join_search(self):
        """Event handler for the "Search" button in the join tab of the lobby section.

        Clears the listbox, retrieves the available servers using discover_servers, 
        and populates the listbox with any responses from listening servers.
        """
        if self.gui.lobby_join_listbox.size() > 0:
            self.gui.lobby_join_listbox.delete(0, END)
            self.gui.lobby_join_button.configure(state="disabled")

        self.available_servers = self.network.discover_servers()
        if self.available_servers:
            for i, server in enumerate(self.available_servers):
                display_text = f"Username: {server[2]}\nTotal Rounds: {server[3]}\n" \
                            f"IP: {server[0]}\nPort: {server[1]}"
                self.gui.lobby_join_listbox.insert(i, display_text)
        else:
            self.gui.update_status_textbox("No servers found")

    def event_join(self):
        """Event handler for the "Join" button in the join tab of the lobby section.

        Retrieves the details of the selected server from the listbox and initiates a client thread to join the server.
        """
        self.network.get_local_ip()
        self.gui.lobby_host_ip_label2.configure(text=self.network.local_ip)

        # Get details from listbox selection
        index = self.gui.lobby_join_listbox.curselection()
        server_ip = self.available_servers[index][0]
        server_port = int(self.available_servers[index][1])
        self.opponent_username = self.available_servers[index][2]
        self.total_rounds = int(self.available_servers[index][3])

        self.client_thread = threading.Thread(target=lambda: self.client.start(server_ip, server_port))
        self.client_thread.start()

    def event_host_refresh(self):
        """Event handler for the "Refresh" button in the host tab of the lobby section.
        
        Refresh the host settings and update the IP address in the lobby.
        """
        self.network.get_local_ip()
        self.gui.lobby_host_ip_label2.configure(text=self.network.local_ip)
        self.gui.lobby_host_slider.set(3)

    def event_host(self):
        """Event handler for the "Host" button in the host tab of the lobby section.
        
        Sets the total rounds for the game based on the slider value, retrieves the local IP address, 
        starts a broadcast thread to listen for incoming connections, and updates the lobby status.
        """
        self.total_rounds = int(self.gui.lobby_host_slider.get())
        self.network.get_local_ip()
        self.gui.lobby_host_ip_label2.configure(text=self.network.local_ip)

        self.broadcast_thread = threading.Thread(target=self.server.broadcast_listen)
        self.broadcast_thread.start()

        self.gui.update_status_textbox(f"Hosting at:\n" \
                                       f"IP: {self.network.local_ip}\n" \
                                       f"Port: {self.network.server_port}")
        self.gui.update_lobby_state("disabled")

    def event_settings_default(self):
        """Event handler for the "Default" button in the settings tab of the lobby section.
        
        Resets application settings to default values.
        """
        self.gui.lobby_settings_default_button.focus_set()
        self.gui.lobby_settings_serverport.delete(0, END)
        self.gui.lobby_settings_serverport.insert(0, "51515")
        self.gui.lobby_settings_broadport.delete(0, END)
        self.gui.lobby_settings_broadport.insert(0, "12121")
        self.gui.lobby_settings_audio_switch.select()
        self.gui.lobby_settings_tts_switch.deselect()

    def event_settings_save(self):
        """Event handler for the "Save" button in the settings tab of the lobby section.
        
        Validates field inputs and saves application settings.
        """
        self.gui.lobby_settings_save_button.focus_set()
        serverport_input = self.gui.lobby_settings_serverport.get()
        broadport_input = self.gui.lobby_settings_broadport.get()

        if (serverport_input and not re.match(r'^\d{1,5}$', serverport_input)) or \
           (broadport_input and not re.match(r'^\d{1,5}$', broadport_input)):
            CTkMessagebox(title="Invalid Input", message="Port fields must be valid integers with a maximum length of 5", 
                          icon=self.gui.icon_info, master=self.gui)
            return

        if serverport_input:
            self.network.server_port = int(self.gui.lobby_settings_serverport.get())
            self.gui.lobby_settings_serverport.delete(0, END)
            self.gui.lobby_settings_serverport.configure(placeholder_text=f"{self.network.server_port}")
        if broadport_input:
            self.network.broadcast_port = int(self.gui.lobby_settings_broadport.get())
            self.gui.lobby_settings_broadport.delete(0, END)
            self.gui.lobby_settings_broadport.configure(placeholder_text=f"{self.network.broadcast_port}") 
        if self.gui.lobby_settings_audio_switch:
            self.gui.audio_on = True
        else:
            self.gui.audio_on = False
        if self.gui.lobby_settings_tts_switch:
            self.gui.tts_on = True
        else:
            self.gui.tts_on = False
        CTkMessagebox(title="Settings Saved", message="Settings successfully updated", 
                          icon=self.gui.icon_check, master=self.gui)

    def event_disconnect(self, scope=None):
        """Event handler for the "Disconnect" button in the connection status section.
        Also triggers from the "Exit" button in the Profile Options messagebox or when user exits program.
        
        Disconnect from the server or client and save profile data.
        Handles various cases, including mid-game disconnection and exiting the application.

        Args:
            scope (str): The scope of disconnection, which can be "logout" or "exit". Default is None.
        """
        if self.current_round:
            msg = CTkMessagebox(title="Disconnect From Peer", message=f"Are you sure you want to disconnect mid-game?\n\n" \
                        f"You will forfeit any incomplete rounds: {self.total_rounds - (self.current_round - 1)}", 
                        icon=self.gui.icon_question, option_1="Proceed", option_2="Cancel", master=self.gui, sound=True)
            
            if msg.get() == "Proceed":
                if self.server_thread and self.server_thread.is_alive():
                    self.server.stop("mid_game")
                elif self.client_thread and self.client_thread.is_alive():
                    self.client.stop("mid_game")
                self.dropout_resolution("quitter")
            if msg.get() == "Cancel":
                return

        else:
            if self.broadcast_thread and self.broadcast_thread.is_alive():
                self.server.stop_listen()
            elif self.server_thread and self.server_thread.is_alive():
                self.server.stop("no_game")
            elif self.client_thread and self.client_thread.is_alive():
                self.client.stop("no_game")
            
        if scope == "exit":
            if self.user_profile:
                self.save_profile_stats()
            self.gui.destroy()
        elif scope == "logout":
            self.save_profile_stats()
            self.event_logout()

    def launch_server(self):
        """Launch the game server in a separate thread.
        """
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()

    def network_connected(self, peer_ip):
        """Called when a successful network connection is established. 

        Initializes current_round and updates the UI to reflect the connection status.

        Args:
            peer_ip (str): The IP address of the connected peer.
        """
        self.current_round = 1
        self.gui.update_status_textbox(f"Connection successful\n" \
                                       f"Local IP: {self.network.local_ip}\n" \
                                       f"Peer  IP: {peer_ip}")
        self.gui.update_main_textbox(f"{self.user_profile['username']} Vs. {self.opponent_username}\n\n" \
                                     f"##########################################\n\n" \
                                     f"Round {self.current_round} / {self.total_rounds}\n" \
                                     f"**************\n", "system_chat")
        self.gui.update_game_state("normal")
        self.gui.update_lobby_state("disabled")

    def network_disconnected(self):
        """Called when the network connection is terminated. 
        
        Updates the UI to reflect the disconnection status and resets various game-related attributes.
        """
        self.gui.update_status_textbox("Connection terminated")
        if self.current_round:
            self.gui.update_main_textbox("Rounds completed\nThanks for playing\n\n##########################################\n", 
                                         "system_chat")
        self.gui.update_game_state("disabled")
        self.gui.update_lobby_state("normal")

        self.player_choice = None
        self.opponent_choice = None
        self.opponent_username = None
        self.total_rounds = None
        self.current_round = None

    def network_chat(self, msg, type):
        """Called when a chat message is sent or received over the network. 
        
        Updates the main textbox with chat messages, styled by source type.

        Args:
            msg (str): The chat message.
            type (str): The type of chat message, which can be "local_chat", "peer_chat", or "system_chat".
        """
        self.gui.update_main_textbox(msg, type)

    def determine_results(self):
        """Calculates the results of a round of Rock-Paper-Scissors.
        
        Updates the user's profile stats and the main textbox with the results.
        Determines if it is the final round and either resets the game functions for another round,
        or disconnects the client from the server as the game session is completed.
        """
        choices = {"Rock": 0, "Paper": 1, "Scissors": 2}
        result = (choices[self.player_choice] - choices[self.opponent_choice]) % 3

        if result == 0:
            self.user_profile["ties"] += 1
        elif result == 1:
            self.user_profile["wins"] += 1
        else:
            self.user_profile["loses"] += 1
        
        self.update_profile_stats()
        self.network_chat(self.gui.ascii_results(self.player_choice, self.opponent_choice), "system_chat")

        if self.current_round < self.total_rounds:
            self.current_round += 1
            self.gui.update_main_textbox(f"Round {self.current_round} / {self.total_rounds}\n" \
                                         f"**************\n", "system_chat")
            self.gui.game_rps_button.configure(state="normal")
            self.gui.game_rps_button.set("unselect")
            self.player_choice = None
            self.opponent_choice = None
        else:
            if self.server_thread and self.server_thread.is_alive():
                self.server.stop("game_complete")

    def dropout_resolution(self, actor):
        """Called when a disconnection occurs mid-game.
        
        Calculates the penalty/reward and updates the main textbox and profile stats.

        Args:
            actor (str): The actor of the dropout occurance, which can be "player" or "quitter".
        """
        rounds = self.total_rounds - (self.current_round - 1)

        if actor == "player":
            self.user_profile["wins"] += rounds
            self.gui.update_main_textbox(f"{self.opponent_username} dropped out\n You've been credited {rounds} wins!\n", 
                                         "system_chat")
            self.update_profile_stats()
        elif actor == "quitter":
            self.user_profile["loses"] += rounds
            self.gui.update_main_textbox(f"You dropped out\n You've forfeited {rounds} rounds!\n", 
                                         "system_chat")
            self.update_profile_stats()
        
    def update_profile_stats(self):
        """Update the user's profile stats on the main screen.
        """
        self.gui.profile_winloss_label.configure(text=f"Wins: {self.user_profile['wins']} / " \
                                                          f"Loses: {self.user_profile['loses']} / " \
                                                          f"Ties: {self.user_profile['ties']} ")
        
    def save_profile_stats(self):
        """Save the user's profile stats to the user data file.

        Reads the file, updates the stats, and writes them back to the file.
        """
        try:
            with open(self.user_data_path, "r") as file:
                lines = file.readlines()

            for i, line in enumerate(lines):
                parts = line.strip().split(", ")
                if parts[0] == self.user_profile["username"] and parts[1] == self.user_profile["password"]:
                    parts[3] = str(self.user_profile['wins'])
                    parts[4] = str(self.user_profile['loses'])
                    parts[5] = str(self.user_profile['ties'])
                    updated_line = ", ".join(parts) + "\n"
                    lines[i] = updated_line
                    break

            with open(self.user_data_path, "w") as file:
                file.writelines(lines)

        except FileNotFoundError:
            CTkMessagebox(title="Save Profile Failed", message="File not found: user_data.txt", 
                          icon=self.gui.icon_cancel, master=self.gui, sound=True)
        except Exception as e:
            CTkMessagebox(title="Save Profile Failed", message=f"An error occurred during file access:\n{str(e)}", 
                          icon=self.gui.icon_cancel, master=self.gui, sound=True)

    def on_exit(self):
        """Called when the program is exited.
        
        Stops any running threads and performs necessary cleanup.
        """
        self.allow_gui_update = False
        self.event_disconnect("exit")


if __name__ == "__main__":
    app = App()
    app.gui.mainloop()
