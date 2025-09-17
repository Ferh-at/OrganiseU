import customtkinter
from PIL import Image
from core.Auth import Auth, UserExistsError, InvalidCredentialsError, WeakPasswordError

class LoginWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.auth = Auth()

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

        self.UsernameEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Enter a username",
            width=300,
            height=45,
            corner_radius=20,
            fg_color="#BEF8FF",  # light blue background
            border_color="#5EE2F1",  # darker blue outline
            border_width=2,
            text_color="black",
            placeholder_text_color="gray50"
        )
        self.UsernameEntry.place(relx=0.5, rely=0.4, anchor="center")

        # --- PasswordEntry Entry ---
        self.PasswordEntry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Enter a password",
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
            command=self.AttemptRegistration
        )
        self.RegisterButton.place(relx=0.5, rely=0.7, anchor="center")

        self.FeedbackLabel = customtkinter.CTkLabel(
            master=self,
            text="",
            text_color="red",
            font=("Montserrat", 16),
        )
        self.FeedbackLabel.place(relx=0.5, rely=0.3, anchor="center")

    def AttemptLogin(self):
        username = self.UsernameEntry.get().strip()
        password = self.PasswordEntry.get().strip()

        try:
            if self.auth.LoginUser(username, password):
                self.FeedbackLabel.configure(text="Login Successful", text_color="green")
                # transition to the main window with tasks, habits etc. here
        except InvalidCredentialsError:
            self.FeedbackLabel.configure(text="Invalid username or password", text_color="red")
        except Exception as e:
            self.FeedbackLabel.configure(text=f"Unexpected error, {str(e)}", text_color="red")

    def AttemptRegistration(self):
        #! OR GO DIRECTLY TO ANOTHER SCREEN
        username = self.UsernameEntry.get().strip()
        password = self.PasswordEntry.get().strip()

        try:
            if self.auth.RegisterUser(username, password):
                self.FeedbackLabel.configure(text="Registration Successful", text_color="green")
                #! TRANSITION TO ONBOARDING PROCESS
        except UserExistsError:
            self.FeedbackLabel.configure(text="Username is already taken!", text_color="red")
        except WeakPasswordError:
            self.FeedbackLabel.configure(text="Password must be between 8-15 alphanumeric characters and include a symbol!", text_color="red")
        except Exception:
            self.FeedbackLabel.configure(text="Unexpected error, {str(Exception)}", text_color="red")


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


        