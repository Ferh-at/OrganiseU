import customtkinter
from gui.LoginWindow import LoginWindow
from PIL import Image

class EntryWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            BackgroundImagePIL = Image.open("assets/BackgroundEntryWindow.png")
            original_width, original_height = BackgroundImagePIL.size
            self.BGImage = customtkinter.CTkImage(light_image=BackgroundImagePIL, size=(original_width, original_height))
            
            self.BackgroundLabel = customtkinter.CTkLabel(self, image=self.BGImage, text="")
            self.BackgroundLabel.grid(row=0, column=0, sticky="nsew")  

        except FileNotFoundError:
            print("Warning: assets/Background.jpg not found. Using solid color.")
            self.configure(fg_color="#D2951A") 
            self.BGImage = None 
        except Exception as e: 
            print(f"Error loading background image: {e}")
            self.configure(fg_color="#D2951A")
            self.BGImage = None
        

        BeginButtonPIL = Image.open("assets/BeginYourJourneyButton.png")
        
        btn_img_width, btn_img_height = BeginButtonPIL.size
        self.BeginYourJourneyButtonImage = customtkinter.CTkImage(
            light_image=BeginButtonPIL, 
            size=(btn_img_width, btn_img_height) # Use original image size
        )

        self.BeginYourJourneyButton = customtkinter.CTkButton(
            master=self, 
            image=self.BeginYourJourneyButtonImage, 
            text="", 
            fg_color="#BEF8FF", 
            hover_color="#5EE2F1",

            command=self.ButtonPressed
        )
        
        self.BeginYourJourneyButton.place(relx=0.5, rely=0.6, anchor="center")
    
    def ButtonPressed(self):
        self.FadeOut()
    
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

