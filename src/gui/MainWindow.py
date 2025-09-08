import customtkinter
from PIL import Image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("OrganiseU")
        self.geometry("750x750")
        
        bg_image_pil = Image.open("assets/Background.jpg")
        # Create a CTkImage object. You might want to resize it to fit your window.
        # For simplicity, let's assume it fits or will be scaled by CTkLabel.
        self.bg_image = customtkinter.CTkImage(light_image=bg_image_pil, size=(self.winfo_width(), self.winfo_height()))

        # Create a CTkLabel to hold the background image
        if self.bg_image:
            self.background_label = customtkinter.CTkLabel(self, image=self.bg_image, text="")
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1) # Make it fill the window
            # Ensure the background label is behind other widgets
            self.background_label.lower()

        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        if self.bg_image:
            self.bg_image.configure(size=(event.width, event.height))
            self.background_label.configure(image=self.bg_image) # Re-apply the updated image


if __name__ == "__main__":
    app = App()
    app.mainloop()
