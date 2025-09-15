import customtkinter
from PIL import Image

class LoginWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        try:
            BackgroundImagePIL = Image.open("assets/BackgroundNormal.png")
            original_width, original_height = BackgroundImagePIL.size
            self.BGImage = customtkinter.CTkImage(light_image=BackgroundImagePIL, size=(original_width, original_height))
            
            self.BackgroundLabel = customtkinter.CTkLabel(self, image=self.BGImage, text="")
            self.BackgroundLabel.grid(row=0, column=0, sticky="nsew")  

        except FileNotFoundError:
            print("Warning: assets/Background.jpg not found. Using solid color.")
            self.configure(fg_color="#1A7FD2") 
            self.BGImage = None 
        except Exception as e: 
            print(f"Error loading background image: {e}")
            self.configure(fg_color="#1A7FD2")
            self.BGImage = None

        self.UsernamEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Username",
            width=300,
            height=45,
            corner_radius=20,
            fg_color="#BEF8FF",  # light blue background
            border_color="#5EE2F1",  # darker blue outline
            border_width=2,
            text_color="black",
            placeholder_text_color="gray50"
        )
        self.UsernamEntry.place(relx=0.5, rely=0.4, anchor="center")

        # --- PasswordEntry Entry ---
        self.PasswordEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="PasswordEntry",
            width=300,
            height=45,
            corner_radius=20,
            fg_color="#BEF8FF",
            border_color="#5EE2F1",
            border_width=2,
            text_color="black",
            placeholder_text_color="gray50",
            show="*"  # masks input
        )
        self.PasswordEntry.place(relx=0.5, rely=0.5, anchor="center")

        # --- Example Login Button ---
        self.LoginButton = customtkinter.CTkButton(
            master=self,
            text="Login",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            corner_radius=20,
            width=200,
            height=40,
            command=self.AttemptLogin
        )
        self.LoginButton.place(relx=0.5, rely=0.6, anchor="center")


        self.RegisterButton = customtkinter.CTkButton(
            master=self,
            text="Make an account",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            corner_radius=20,
            width=200,
            height=40,
            command=self.AttemptLogin
        )
        self.RegisterButton.place(relx=0.5, rely=0.75, anchor="center")

    def AttemptLogin(self):
        username = self. UsernamEntry.get()
        PasswordEntry = self.PasswordEntry.get()
        print(f"Username: {username}, PasswordEntry: {PasswordEntry}")

    def FadeOut(self, step=0.05):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha = max(0, alpha - step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeOut, step)
        else:
            self.destroy()
            login = LoginWindow(self.parent)
            login.grid(row=0, column=0, sticky="nsew")
            login.FadeIn()
    def FadeIn(self, step=0.05):
        alpha = self.parent.attributes("-alpha")
        if alpha < 1:
            alpha = min(1, alpha + step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeIn, step)

    def SlideOut(self, x=0):
        if x <= 750:
            self.place(x=-x, y=0)
            self.parent.update()
            self.after(5, self.SlideOut, x+15)
        else:
            self.destroy()
            login = LoginWindow(self.parent)
            login.place(x=750, y=0) 
            login.SlideIn()

    def SlideIn(self, x=750):
        if x >= 0:
            self.place(x=x, y=0)
            self.parent.update()
            self.after(5, self.SlideIn, x-15)


        