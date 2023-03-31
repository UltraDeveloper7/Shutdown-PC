import pyttsx3
import speech_recognition as sr
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import E, EW, W, messagebox
from PIL import Image, ImageTk

# Initialize speech recognition and text-to-speech engine
speech_recognizer = sr.Recognizer()
speaker = pyttsx3.init()

def TakeCommands():
    # Open physical microphone of your computer
    with sr.Microphone() as source_mic:
        print('Listening/Waiting.....')
        speech_recognizer.pause_threshold = 0.5
        # reducing noise from the environment
        speech_recognizer.adjust_for_ambient_noise(source_mic)
        # Store audio to audio variable
        audio_store = speech_recognizer.listen(source_mic)
        try:
            print("Recognizing...")
            # Recognize audio using google api
            Question = speech_recognizer.recognize_google(audio_store)
            print(f"You answered: {Question}")
            # Return audio as text
            return Question.lower()
        except Exception as e:
            print(e)
            print("Say that again Mister")
            # Return 'None' if there are errors while you are speaking!
            return "none"

def Speak(audio_store):
    speaker.say(audio_store)
    speaker.runAndWait()


def system_call(action):
    confirm_message = f"Are you sure you want to {action} the computer immediately?"
    user_confirmation = messagebox.askyesno(
        "Confirmation", confirm_message)
    
    if user_confirmation:
        Speak(f"OK. I will {action} the computer immediately!")
        try:
            if action == "shutdown":
                os.system("shutdown /s /t 0")
            elif action == "restart":
                os.system("shutdown /r /t 0")
            else:
                os.system("shutdown.exe /h")
        except Exception as e:
            print(e)
            Speak("There was an error executing the command.")
    else:
        Speak("Alright then")

def voice_commands():
    options = {
        "shutdown": "shutdown",
        "shut down": "shutdown",
        "restart": "restart",
        "hibernate": "hibernate"
    }
    Speak("Do you want to shutdown, restart, or hibernate your computer?")
    command = TakeCommands()
    action = options.get(command, None)
    if action is not None:
        system_call(action)
    elif "neither" in command:
        Speak("Thank you Mister, I won't shut down or restart the computer.")
    else:
        Speak("Sorry, I didn't understand. Please try again.")

class GUI:
    def __init__(self):
        
        self.root = ctk.CTk()
        self.width, self.height = 720, 330
        self.root.geometry(f"{self.width}x{self.height}+400+300")
        self.root.resizable(False,False)
        self.root.title('Shut Down Windows')

        # Adding labels to GUI
        img_path = os.path.join('D:/Python/Shut Down PC', 'windows-11.png')
        
        # Load and convert the image to a PhotoImage
        pil_image = Image.open(img_path)
        self.image_widget = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(100, 100))
        self.label_widget = ctk.CTkLabel(self.root, text = '', image = self.image_widget,)
        self.label_widget.place(relx=0.25, rely=0.2, anchor=tk.W)
        
        self.label1 = ctk.CTkLabel(self.root,
                                   text="\n Windows 11\n",
                                   font=("Arial Bold", 40), text_color="#357EC7")
        self.label1.grid(row=1, column=1, sticky="nsew",columnspan=1)

        # Adding buttons to GUI
        self.shutdown_btn = ctk.CTkButton(self.root,
                                          text="Shutdown",
                                          font=("Arial", 12),
                                          command=lambda: system_call("shutdown"))
        self.shutdown_btn.grid(row=3, column=0, sticky="nsw", padx=30, pady=10)

        self.restart_btn = ctk.CTkButton(self.root,
                                         text="Restart",
                                         font=("Arial", 12),
                                         command=lambda: system_call("restart"))
        self.restart_btn.grid(row=3, column=1, sticky="nsw", padx=10, pady=10)

        self.hibernate_btn = ctk.CTkButton(self.root,
                                           text="Hibernate",
                                           font=("Arial", 12),
                                           command=lambda: system_call("hibernate"))
        self.hibernate_btn.grid(row=3, column=2, sticky="nsw", padx=30, pady=10)
        
        # Adding an optionmenu box for user-choice
        self.label2 = ctk.CTkLabel(self.root,
                                  text="  What do you want the computer to do:   ",
                                  font=("Arial Bold", 14))
        self.label2.grid(row=6, column=0, sticky="nsew",  columnspan=1)
        
        self.optionmenu_var = ctk.StringVar(value = " ")
        self.combobox = ctk.CTkOptionMenu(self.root, values = ["shutdown","restart","hibernate"],
                                          command=self.user_choice, fg_color="#4F4F4F", button_color= "#4F4F4F", variable=self.optionmenu_var)
        self.combobox.grid(row=6, column=1, sticky="nsew", pady=10)
        
        # Adding voice command button to GUI
        self.voice_command_btn = ctk.CTkButton(self.root,
                                               text="Voice Commands",
                                               font=("Arial", 12),
                                               command=self.voice_commands)
        self.voice_command_btn.grid(row=7, column=1, sticky="nsew", padx=30, pady=8)

        # Adding appearance option menu to GUI
        self.label_mode = ctk.CTkLabel(master=self.root,
                                       text="   Appearance Mode:",
                                       font=("Arial", 12))
        self.label_mode.grid(row=10, column=0, sticky = W)

        self.optionmenu_1 = ctk.CTkOptionMenu(master=self.root,
                                              values=["Dark", "Light", "System"],
                                              font=("Arial", 12), fg_color="#4F4F4F", button_color="#4F4F4F",
                                              command=self.change_appearance_mode)
        self.optionmenu_1.set("System")
        self.optionmenu_1.grid(row=10, column=0, sticky = "ne")


        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def user_choice(self, choice):
        system_call(choice)

    def voice_commands(self):
        voice_commands()

    def on_closing(self):
        #Speak("Goodbye Mister")
        self.root.destroy()

    #def enter_pressed(self, event):
        #choice = self.textbox.get().lower()
        #self.keyboard_choice(choice)

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        

if __name__ == '__main__':
    voice_assistant_gui = GUI()
