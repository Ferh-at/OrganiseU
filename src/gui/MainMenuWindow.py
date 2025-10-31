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
        # Header
        self.tasks_label = customtkinter.CTkLabel(
            master=self,
            text=f"Welcome, {self.username}",
            text_color="white",
            font=("Montserrat", 20, "bold"),
            fg_color="#1A7FD2",
        )
        self.tasks_label.place(relx=0.5, rely=0.10, anchor="center")

        # Today Overview box
        total, completed, pending = self.task_manager.count_tasks(self.username)
        self.overview_frame = customtkinter.CTkFrame(self, fg_color="#134E96")
        self.overview_frame.place(relx=0.5, rely=0.24, anchor="center")

        self.overview_title = customtkinter.CTkLabel(
            self.overview_frame,
            text="Today Overview",
            text_color="white",
            font=("Montserrat", 16, "bold"),
        )
        self.overview_title.place(relx=0.5, rely=0.2, anchor="center")

        self.overview_stats = customtkinter.CTkLabel(
            self.overview_frame,
            text=f"Tasks: {completed}/{total} completed  •  Pending: {pending}",
            text_color="white",
            font=("Montserrat", 14),
        )
        self.overview_stats.place(relx=0.5, rely=0.6, anchor="center")

        # Live clock (top-right)
        self.clock_label = customtkinter.CTkLabel(
            master=self,
            text="",
            text_color="white",
            font=("Montserrat", 14),
            fg_color="#1A7FD2",
        )
        self.clock_label.place(relx=0.93, rely=0.06, anchor="center")
        self._tick_clock()

        # Quick Actions
        self.add_task_btn = customtkinter.CTkButton(
            master=self,
            text="Add Task",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            text_color="black",
            width=160,
            height=40,
            command=self.on_add_task,
        )
        self.add_task_btn.place(relx=0.25, rely=0.75, anchor="center")

        self.view_tasks_btn = customtkinter.CTkButton(
            master=self,
            text="Task Manager",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            text_color="black",
            width=160,
            height=40,
            command=self.on_open_task_manager,
        )
        self.view_tasks_btn.place(relx=0.5, rely=0.75, anchor="center")

        self.habits_btn = customtkinter.CTkButton(
            master=self,
            text="Habit Tracker",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            text_color="black",
            width=160,
            height=40,
            command=self.on_open_habits,
        )
        self.habits_btn.place(relx=0.75, rely=0.75, anchor="center")

        # Placeholder for future: timer and analytics
        self.timer_btn = customtkinter.CTkButton(
            master=self,
            text="Task Timer",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            text_color="black",
            width=160,
            height=36,
            command=self.on_open_timer,
        )
        self.timer_btn.place(relx=0.35, rely=0.86, anchor="center")

        self.analytics_btn = customtkinter.CTkButton(
            master=self,
            text="Analytics",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            text_color="black",
            width=160,
            height=36,
            command=self.on_open_analytics,
        )
        self.analytics_btn.place(relx=0.65, rely=0.86, anchor="center")

        # Refresh tasks preview dropdown (kept minimal)
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
        self.tasks_dropdown.place(relx=0.5, rely=0.42, anchor="center")

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

    # ========= Actions =========
    def on_add_task(self):
        # Lightweight add-task dialog using a transient frame
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Add Task")
        dialog.geometry("360x220")
        dialog.attributes("-topmost", True)

        title_entry = customtkinter.CTkEntry(
            dialog, placeholder_text="Task title", width=300
        )
        title_entry.place(relx=0.5, rely=0.25, anchor="center")

        desc_entry = customtkinter.CTkEntry(
            dialog, placeholder_text="Description (optional)", width=300
        )
        desc_entry.place(relx=0.5, rely=0.45, anchor="center")

        feedback = customtkinter.CTkLabel(dialog, text="", text_color="red")
        feedback.place(relx=0.5, rely=0.65, anchor="center")

        def submit():
            title = title_entry.get().strip()
            description = desc_entry.get().strip() or None
            if not title:
                feedback.configure(text="Title is required")
                return
            try:
                self.task_manager.add_task(self.username, title, description)
                # refresh overview and dropdown
                self._refresh_overview()
                self._refresh_dropdown()
                dialog.destroy()
            except Exception as e:
                feedback.configure(text=str(e))

        submit_btn = customtkinter.CTkButton(
            dialog,
            text="Add",
            fg_color="#5EE2F1",
            hover_color="#3CC1D4",
            text_color="black",
            width=140,
            command=submit,
        )
        submit_btn.place(relx=0.5, rely=0.85, anchor="center")

    def on_open_task_manager(self):
        # Placeholder: open full Task Manager window
        pass

    def on_open_habits(self):
        # Placeholder: open Habit Tracker window
        pass

    def on_open_timer(self):
        # Placeholder: open Task Timer UI
        pass

    def on_open_analytics(self):
        # Placeholder: open Analytics UI
        pass

    # ===== Helpers =====
    def _refresh_overview(self):
        total, completed, pending = self.task_manager.count_tasks(self.username)
        self.overview_stats.configure(
            text=f"Tasks: {completed}/{total} completed  •  Pending: {pending}"
        )

    def _refresh_dropdown(self):
        titles = [title for _id, title in self.task_manager.get_tasks(self.username)]
        if not titles:
            titles = ["No tasks yet"]
        self.tasks_dropdown.configure(values=titles)

    def _tick_clock(self):
        import datetime as _dt

        now = _dt.datetime.now().strftime("%a %d %b, %H:%M:%S")
        self.clock_label.configure(text=now)
        self.after(1000, self._tick_clock)
