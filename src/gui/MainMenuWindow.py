import customtkinter
from PIL import Image
from core.TaskManager import TaskManager


class MainMenu(customtkinter.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.parent = parent
        self.username = username
        self.task_manager = TaskManager()

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
            self.configure(fg_color="#1A7FD2")
            self.BGImage = None
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.configure(fg_color="#1A7FD2")
            self.BGImage = None
        # tasks dropdown (OptionMenu)
        self.tasks_label = customtkinter.CTkLabel(
            master=self,
            text="Your Tasks",
            text_color="white",
            font=("Montserrat", 18),
            fg_color="#1A7FD2",
        )
        self.tasks_label.place(relx=0.5, rely=0.2, anchor="center")

        task_titles = [
            title for _id, title in self.task_manager.get_tasks(self.username)
        ]
        if not task_titles:
            task_titles = ["No tasks yet"]

        self.tasks_dropdown = customtkinter.CTkOptionMenu(
            master=self,
            values=task_titles,
            fg_color="#5EE2F1",
            button_color="#3CC1D4",
            text_color="black",
        )
        self.tasks_dropdown.place(relx=0.5, rely=0.27, anchor="center")

    def FadeOut(self, step=0.05):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha = max(0, alpha - step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeOut, step)
        else:
            self.destroy()
            # login = MainMenu(self.parent)
            # login.grid(row=0, column=0, sticky="nsew")
            # login.FadeIn()

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
            self.after(3, self.SlideOut, x + 15)
        else:
            self.destroy()
            # login = LoginWindow(self.parent)
            # login.place(x=750, y=0)
            # login.SlideIn()

    def SlideIn(self, x=750):
        if x >= 0:
            self.place(x=x, y=0)
            self.parent.update()
            self.after(3, self.SlideIn, x - 15)
