import customtkinter
from PIL import Image
from core.Auth import Auth
from gui.MainMenuWindow import MainMenu


class RegistrationWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.Auth = Auth()

        try:
            BackgroundImagePIL = Image.open("assets/BackgroundNormal.png")
            original_width, original_height = BackgroundImagePIL.size
            self.BGImage = customtkinter.CTkImage(
                light_image=BackgroundImagePIL, size=(original_width, original_height)
            )

            self.BackgroundLabel = customtkinter.CTkLabel(
                self, image=self.BGImage, text=""
            )
            self.BackgroundLabel.grid(row=0, column=0, sticky="nsew")

        except FileNotFoundError:
            print("Warning: assets/Background.jpg not found. Using solid color.")
            self.configure(fg_color="#D2951A")
            self.BGImage = None
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.configure(fg_color="#D2951A")
            self.BGImage = None

        self.UsernameEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Enter a username",
            width=300,
            height=45,
            fg_color="#BEF8FF",
            border_color="#5EE2F1",
            border_width=2,
            text_color="black",
            placeholder_text_color="gray50",
        )
        self.UsernameEntry.place(relx=0.5, rely=0.15, anchor="center")

        self.PasswordEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Enter a password",
            width=300,
            height=45,
            fg_color="#BEF8FF",
            border_color="#5EE2F1",
            border_width=2,
            text_color="black",
            placeholder_text_color="gray50",
            show="*",
        )
        self.PasswordEntry.place(relx=0.5, rely=0.23, anchor="center")

        self.ConfirmPasswordEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Confirm password",
            width=300,
            height=45,
            fg_color="#BEF8FF",
            border_color="#5EE2F1",
            border_width=2,
            text_color="black",
            placeholder_text_color="gray50",
            show="*",
        )
        self.ConfirmPasswordEntry.place(relx=0.5, rely=0.31, anchor="center")

        self.ConcentrationLabel = customtkinter.CTkLabel(
            self, text="Average Concentration", text_color="black", fg_color="#BEF8FF"
        )
        self.ConcentrationLabel.place(relx=0.3, rely=0.42, anchor="e")

        self.ConcentrationSlider = customtkinter.CTkSlider(
            self,
            from_=1,
            to=10,
            number_of_steps=9,
            width=200,
            fg_color="#BEF8FF",
            progress_color="#5EE2F1",
            button_color="#3CC1D4",
            button_hover_color="#2BA0B4",
        )
        self.ConcentrationSlider.set(5)
        self.ConcentrationSlider.place(relx=0.35, rely=0.42, anchor="w")

        self.DisciplineLabel = customtkinter.CTkLabel(
            self, text="Average Discipline", text_color="black", fg_color="#BEF8FF"
        )
        self.DisciplineLabel.place(relx=0.3, rely=0.50, anchor="e")

        self.DisciplineSlider = customtkinter.CTkSlider(
            self,
            from_=1,
            to=10,
            number_of_steps=9,
            width=200,
            fg_color="#BEF8FF",
            progress_color="#5EE2F1",
            button_color="#3CC1D4",
            button_hover_color="#2BA0B4",
        )
        self.DisciplineSlider.set(5)
        self.DisciplineSlider.place(relx=0.35, rely=0.50, anchor="w")

        self.MotivationLabel = customtkinter.CTkLabel(
            self, text="Average Motivation", text_color="black", fg_color="#BEF8FF"
        )
        self.MotivationLabel.place(relx=0.3, rely=0.58, anchor="e")

        self.MotivationSlider = customtkinter.CTkSlider(
            self,
            from_=1,
            to=10,
            number_of_steps=9,
            width=200,
            fg_color="#BEF8FF",
            progress_color="#5EE2F1",
            button_color="#3CC1D4",
            button_hover_color="#2BA0B4",
        )
        self.MotivationSlider.set(5)
        self.MotivationSlider.place(relx=0.35, rely=0.58, anchor="w")

        self.EnergyLabel = customtkinter.CTkLabel(
            self, text="Average Energy Levels", text_color="black", fg_color="#BEF8FF"
        )
        self.EnergyLabel.place(relx=0.3, rely=0.66, anchor="e")

        self.EnergySlider = customtkinter.CTkSlider(
            self,
            from_=1,
            to=10,
            number_of_steps=9,
            width=200,
            fg_color="#BEF8FF",
            progress_color="#5EE2F1",
            button_color="#3CC1D4",
            button_hover_color="#2BA0B4",
        )
        self.EnergySlider.set(5)
        self.EnergySlider.place(relx=0.35, rely=0.66, anchor="w")

        self.RegisterButton = customtkinter.CTkButton(
            master=self,
            text="Register",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            width=200,
            height=40,
            command=self.AttemptRegister,
        )
        self.RegisterButton.place(relx=0.5, rely=0.8, anchor="center")

        # ============ Feedback Label ============
        self.FeedbackLabel = customtkinter.CTkLabel(self, text="", text_color="red")
        self.FeedbackLabel.place(relx=0.5, rely=0.87, anchor="center")

    def AttemptRegister(self):
        Username = self.UsernameEntry.get().strip()
        Password = self.PasswordEntry.get().strip()
        PasswordConf = self.ConfirmPasswordEntry.get().strip()

        if Password != PasswordConf:
            self.FeedbackLabel.configure(
                text="Passwords do not match", text_color="red"
            )
            return

        Concentration = int(self.ConcentrationSlider.get())
        Discipline = int(self.DisciplineSlider.get())
        Motivation = int(self.MotivationSlider.get())
        Energy = int(self.EnergySlider.get())

        try:
            self.Auth.RegisterUser(
                Username, Password, Concentration, Discipline, Motivation, Energy
            )
        except Exception as e:
            self.FeedbackLabel.configure(
                text=f"An error has occured, {e}", text_color="red"
            )
            return

        self.FeedbackLabel.configure(text="Registration successful", text_color="green")
        self.registered_username = Username
        self.after(1500, self.FadeOut)

    def FadeOut(self, step=0.05):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha = max(0, alpha - step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeOut, step)
        else:
            # Obtain username saved earlier to avoid accessing destroyed widgets
            username = getattr(self, "registered_username", "")
            self.destroy()
            login = MainMenu(self.parent, username)
            login.grid(row=0, column=0, sticky="nsew")
            login.FadeIn()

    def FadeIn(self, step=0.1):
        alpha = self.parent.attributes("-alpha")
        if alpha < 1:
            alpha = min(1, alpha + step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeIn, step)

    def SlideOut(self, x=0):
        if x <= 750:
            self.place(x=-x, y=0)
            self.parent.update()
            self.after(3, self.SlideOut, x + 15)
        else:
            self.destroy()
            # Use stored username if available
            username = getattr(self, "registered_username", "")
            login = MainMenu(self.parent, username)
            login.place(x=750, y=0)
            login.SlideIn()

    def SlideIn(self, x=750):
        if x >= 0:
            self.place(x=x, y=0)
            self.parent.update()
            self.after(3, self.SlideIn, x - 15)
