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
            bg_image_pil = Image.open("assets/BackgroundEntryWindow.png")
            original_width, original_height = bg_image_pil.size
            self.bg_image = customtkinter.CTkImage(light_image=bg_image_pil, size=(original_width, original_height))
            
            self.background_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
            self.background_label.grid(row=0, column=0, sticky="nsew") 
            self.background_label.lower() 
        except FileNotFoundError:
            print("Warning: assets/Background.jpg not found. Using solid color.")
            self.configure(fg_color="#D2951A") 
            self.bg_image = None 
        except Exception as e: 
            print(f"Error loading background image: {e}")
            self.configure(fg_color="#D2951A")
            self.bg_image = None

        begin_journey_pil = Image.open("assets/BeginYourJourneyButton.png")
        
        btn_img_width, btn_img_height = begin_journey_pil.size
        self.BeginYourJourneyButtonImage = customtkinter.CTkImage(
            light_image=begin_journey_pil, 
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
        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        if self.bg_image: 
            if event.width > 0 and event.height > 0:
                self.bg_image.configure(size=(event.width, event.height))

    def on_begin_journey_click(self):
        print("Begin Your Journey button clicked!")

class EntryWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            bg_image_pil = Image.open("assets/BackgroundEntryWindow.png")
            original_width, original_height = bg_image_pil.size
            self.bg_image = customtkinter.CTkImage(light_image=bg_image_pil, size=(original_width, original_height))
            
            self.background_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
            self.background_label.grid(row=0, column=0, sticky="nsew")  

        except FileNotFoundError:
            print("Warning: assets/Background.jpg not found. Using solid color.")
            self.configure(fg_color="#D2951A") 
            self.bg_image = None 
        except Exception as e: 
            print(f"Error loading background image: {e}")
            self.configure(fg_color="#D2951A")
            self.bg_image = None
        

        begin_journey_pil = Image.open("assets/BeginYourJourneyButton.png")
        
        btn_img_width, btn_img_height = begin_journey_pil.size
        self.BeginYourJourneyButtonImage = customtkinter.CTkImage(
            light_image=begin_journey_pil, 
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
        
        self.BeginYourJourneyButton.place(relx=0.5, rely=0.5, anchor="center")

