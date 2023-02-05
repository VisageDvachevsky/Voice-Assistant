import getpass
from PIL import Image
import os
import time

import Bot
import customtkinter
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)

def GetUserName():
    """
    Gets the user name.

    :returns:   The user name.
    :rtype:     { return_type_description }
    """
    Username = getpass.getuser()
    return Username

commands = {
    ("браузер", "интернет", "гугл", "запрос", "поиск"): Bot.OpenBrowser,
    ("пока", "выключись", "уходи"): Bot.AssistantOff,
    ("выключи компьютер",
    "отключи комп",
    "отключи устройство",
    "выключи устройство",
    "отключи"): Bot.ComputerOff,
    ("почта", "сообщение"): Bot.sendMail,
    ("цвет", "экранный цвет", "экран"): Bot.ColorPicker,
    ("напомни", "напоминание"): Bot.reminder,
    ("найди", "найди файл", "открой файл"): Bot.FindFile
}

email_recipient = {
    ("...", '...'): "...",
    ("...", "..."): "...",
    ("...", ".."): "...",
}
class EmailApp(customtkinter.CTk):

    def Email(self):
        email, password = "@", "@"

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        app = customtkinter.CTk()

        app.geometry("500x350")
        app.title("Visage Mail")

        frame_1 = customtkinter.CTkFrame(master=app)
        frame_1.pack(pady=20, padx=60, fill="both", expand=True)
        logo_label = customtkinter.CTkLabel(frame_1, text="Visage Email", font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.pack(pady=10, padx=10)

        entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Your Email")
        entry_1.pack(pady=25, padx=10)
        entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Your Password")
        entry_2.pack(pady=15, padx=10)

        def getValue():
            global email, password
            email, password = entry_1.get(), entry_2.get()
            app.destroy()
            print(email, password)

        button_1 = customtkinter.CTkButton(master=frame_1, text="sent", command=getValue)
        button_1.pack(pady=10, padx=10) 

        app.mainloop()

        print(email, password)
        return email, password

    




class rgbname:

    def convert_rgb_to_names(self, rgb_tuple):
        css3_db = CSS3_HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))

        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index]
