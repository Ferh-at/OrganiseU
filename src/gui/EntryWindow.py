import customtkinter
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("OrganiseU")
        self.geometry("750x750")

        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        try:
            BackgroundImagePIL = Image.open("assets/BackgroundEntryWindow.png")
            original_width, original_height = BackgroundImagePIL.size
            self.BGImage = customtkinter.CTkImage(light_image=BackgroundImagePIL, size=(original_width, original_height))
            
            self.BackgroundLabel = customtkinter.CTkLabel(self, image=self.BGImage, text="")
            self.BackgroundLabel.grid(row=0, column=0, sticky="nsew") 
            self.BackgroundLabel.lower() 
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
            fg_color="transparent", 
            hover_color="orange",
            corner_radius=0, 
            command=self.on_begin_journey_click,
        )

        
        self.BeginYourJourneyButton.place(relx=0.5, rely=0.5, anchor="center")

        # Bind the resize event
        self.bind("<Configure>", self.OnWindowResize)

    def OnWindowResize(self, event):
        if self.BGImage: 
            if event.width > 0 and event.height > 0:
                self.BGImage.configure(size=(event.width, event.height))

    def on_begin_journey_click(self):
        print("Begin Your Journey button clicked!")

class EntryWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

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
            corner_radius=25,
        )
        
        self.BeginYourJourneyButton.place(relx=0.5, rely=0.6, anchor="center")

