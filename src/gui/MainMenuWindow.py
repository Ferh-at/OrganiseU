import customtkinter
from PIL import Image
from core.TaskManager import TaskManager
from gui.TaskManagerWindow import TaskManagerWindow
from gui.HabitTrackerWindow import HabitTrackerWindow
from gui.FocusTimerWindow import FocusTimerWindow
from gui.AnalyticsWindow import AnalyticsWindow
from gui.QuickNotesWindow import QuickNotesWindow
from gui.DailyGoalsWindow import DailyGoalsWindow
from gui.CalendarWindow import CalendarWindow
from gui.SettingsWindow import SettingsWindow


class MainMenu(customtkinter.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.parent = parent
        self.username = username
        self.TaskManager = TaskManager()

        # Color palette - consistent throughout
        self.Colors = {
            "Primary": "#2E86AB",  # Main blue
            "Secondary": "#06A77D",  # Green accent
            "Accent": "#F18F01",  # Orange accent
            "Dark": "#1B263B",  # Dark background
            "Light": "#E8F4F8",  # Light background
            "Text": "#FFFFFF",  # White text
            "TextDark": "#1B263B",  # Dark text
            "Success": "#06A77D",  # Success green
            "Warning": "#F18F01",  # Warning orange
            "Hover": "#A23B72",  # Hover purple
        }

        try:
            BackgroundImagePIL = Image.open("assets/BackgroundNormal.png")
            OriginalWidth, OriginalHeight = BackgroundImagePIL.size
            self.BGImage = customtkinter.CTkImage(
                light_image=BackgroundImagePIL, size=(OriginalWidth, OriginalHeight)
            )
            self.BackgroundLabel = customtkinter.CTkLabel(
                self, image=self.BGImage, text=""
            )
            self.BackgroundLabel.grid(row=0, column=0, sticky="nsew")
        except FileNotFoundError:
            print("Warning: assets/BackgroundNormal.png not found. Using solid color.")
            self.configure(fg_color=self.Colors["Dark"])
            self.BGImage = None
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.configure(fg_color=self.Colors["Dark"])
            self.BGImage = None

        self._CreateHeader()
        self._CreateOverviewSection()
        self._CreateQuickActions()
        self._CreateProductivityTools()

        # Configure grid weights for responsive layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _CreateHeader(self):
        # Header section with welcome message and clock
        HeaderFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        HeaderFrame.place(relx=0, rely=0, relwidth=1.0, relheight=0.12)

        # Welcome label
        self.WelcomeLabel = customtkinter.CTkLabel(
            HeaderFrame,
            text=f"Welcome back, {self.username}! 👋",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
            fg_color=self.Colors["Primary"],
            corner_radius=12,
            height=50,
        )
        self.WelcomeLabel.place(relx=0.02, rely=0.5, anchor="w")

        # Live clock
        self.ClockLabel = customtkinter.CTkLabel(
            HeaderFrame,
            text="",
            text_color=self.Colors["Text"],
            font=("Montserrat", 14),
            fg_color=self.Colors["Dark"],
            corner_radius=8,
            height=35,
            width=180,
        )
        self.ClockLabel.place(relx=0.98, rely=0.5, anchor="e")
        self._TickClock()

    def _CreateOverviewSection(self):
        # Overview section with stats and quick task access
        OverviewFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=15
        )
        OverviewFrame.place(
            relx=0.5, rely=0.17, anchor="center", relwidth=0.95, relheight=0.20
        )

        # Title
        OverviewTitle = customtkinter.CTkLabel(
            OverviewFrame,
            text="📊 Today's Overview",
            text_color=self.Colors["Text"],
            font=("Montserrat", 16, "bold"),
        )
        OverviewTitle.place(relx=0.5, rely=0.3, anchor="center")

        # Stats display
        Total, Completed, Pending = self.TaskManager.CountTasks(self.username)
        CompletionRate = int((Completed / Total * 100) if Total > 0 else 0)

        self.OverviewStats = customtkinter.CTkLabel(
            OverviewFrame,
            text=f"✅ {Completed}/{Total} Completed  •  ⏳ {Pending} Pending  •  📈 {CompletionRate}%",
            text_color=self.Colors["Text"],
            font=("Montserrat", 12),
        )
        self.OverviewStats.place(relx=0.5, rely=0.55, anchor="center")

        # Quick task dropdown
        TaskTitles = [
            Title
            for _id, Title, _status, _desc in self.TaskManager.GetTasks(self.username)
        ]
        if not TaskTitles:
            TaskTitles = ["No tasks yet - click 'Add Task' to get started!"]

        self.TasksDropdown = customtkinter.CTkOptionMenu(
            OverviewFrame,
            values=TaskTitles,
            fg_color=self.Colors["Secondary"],
            button_color=self.Colors["Accent"],
            button_hover_color=self.Colors["Warning"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11),
            width=350,
            height=30,
        )
        self.TasksDropdown.place(relx=0.5, rely=0.82, anchor="center")

    def _CreateQuickActions(self):
        # Quick actions section - primary task management
        # Button container frame
        ActionsFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=12
        )
        ActionsFrame.place(relx=0.02, rely=0.40, relwidth=0.96, relheight=0.12)

        # Label right above the box
        ActionsLabel = customtkinter.CTkLabel(
            self,
            text="⚡ Quick Actions",
            text_color=self.Colors["Text"],
            font=("Montserrat", 15, "bold"),
            fg_color="transparent",
        )
        ActionsLabel.place(relx=0.02, rely=0.37, anchor="w")

        # Add Task button
        self.AddTaskBtn = customtkinter.CTkButton(
            ActionsFrame,
            text="➕ Add Task",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=165,
            height=42,
            corner_radius=10,
            command=self.OnAddTask,
        )
        self.AddTaskBtn.grid(row=0, column=0, padx=10, pady=8)

        # Task Manager button
        self.ViewTasksBtn = customtkinter.CTkButton(
            ActionsFrame,
            text="📋 Task Manager",
            fg_color=self.Colors["Accent"],
            hover_color=self.Colors["Warning"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=165,
            height=42,
            corner_radius=10,
            command=self.OnOpenTaskManager,
        )
        self.ViewTasksBtn.grid(row=0, column=1, padx=10, pady=8)

        # Habit Tracker button
        self.HabitsBtn = customtkinter.CTkButton(
            ActionsFrame,
            text="🎯 Habit Tracker",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=165,
            height=42,
            corner_radius=10,
            command=self.OnOpenHabits,
        )
        self.HabitsBtn.grid(row=0, column=2, padx=10, pady=8)

        # Analytics button
        self.AnalyticsBtn = customtkinter.CTkButton(
            ActionsFrame,
            text="📊 Analytics",
            fg_color=self.Colors["Dark"],
            hover_color=self.Colors["Primary"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=165,
            height=42,
            corner_radius=10,
            command=self.OnOpenAnalytics,
        )
        self.AnalyticsBtn.grid(row=0, column=3, padx=10, pady=8)

    def _CreateProductivityTools(self):
        # Productivity tools section
        # Tools button container
        ToolsFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=12
        )
        ToolsFrame.place(relx=0.02, rely=0.55, relwidth=0.96, relheight=0.20)

        # Label right above the box
        ToolsLabel = customtkinter.CTkLabel(
            self,
            text="🛠️ Productivity Tools",
            text_color=self.Colors["Text"],
            font=("Montserrat", 15, "bold"),
            fg_color="transparent",
        )
        ToolsLabel.place(relx=0.02, rely=0.52, anchor="w")

        # Timer button
        self.TimerBtn = customtkinter.CTkButton(
            ToolsFrame,
            text="⏱️ Focus Timer\n(Pomodoro)",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=135,
            height=65,
            corner_radius=10,
            command=self.OnOpenTimer,
        )
        self.TimerBtn.grid(row=0, column=0, padx=8, pady=8)

        # Notes button
        self.NotesBtn = customtkinter.CTkButton(
            ToolsFrame,
            text="📝 Quick Notes",
            fg_color=self.Colors["Accent"],
            hover_color=self.Colors["Warning"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=135,
            height=65,
            corner_radius=10,
            command=self.OnOpenNotes,
        )
        self.NotesBtn.grid(row=0, column=1, padx=8, pady=8)

        # Goals button
        self.GoalsBtn = customtkinter.CTkButton(
            ToolsFrame,
            text="🎯 Daily Goals",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=135,
            height=65,
            corner_radius=10,
            command=self.OnOpenGoals,
        )
        self.GoalsBtn.grid(row=0, column=2, padx=8, pady=8)

        # Calendar button
        self.CalendarBtn = customtkinter.CTkButton(
            ToolsFrame,
            text="📅 Calendar",
            fg_color=self.Colors["Accent"],
            hover_color=self.Colors["Warning"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=135,
            height=65,
            corner_radius=10,
            command=self.OnOpenCalendar,
        )
        self.CalendarBtn.grid(row=0, column=3, padx=8, pady=8)

        # Settings button
        self.SettingsBtn = customtkinter.CTkButton(
            ToolsFrame,
            text="⚙️ Settings",
            fg_color=self.Colors["Dark"],
            hover_color=self.Colors["Primary"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=135,
            height=65,
            corner_radius=10,
            command=self.OnOpenSettings,
        )
        self.SettingsBtn.grid(row=0, column=4, padx=8, pady=8)

    # ========= Animation Methods =========
    def FadeOut(self, Step=0.05):
        Alpha = self.parent.attributes("-alpha")
        if Alpha > 0:
            Alpha = max(0, Alpha - Step)
            self.parent.attributes("-alpha", Alpha)
            self.after(20, self.FadeOut, Step)
        else:
            self.destroy()

    def FadeIn(self, Step=0.05):
        Alpha = self.parent.attributes("-alpha")
        if Alpha < 1:
            Alpha = min(1, Alpha + Step)
            self.parent.attributes("-alpha", Alpha)
            self.after(20, self.FadeIn, Step)

    def SlideOut(self, X=0):
        if X <= 750:
            self.place(x=-X, y=0)
            self.parent.update()
            self.after(3, self.SlideOut, X + 15)
        else:
            self.destroy()

    def SlideIn(self, X=750):
        if X >= 0:
            self.place(x=X, y=0)
            self.parent.update()
            self.after(3, self.SlideIn, X - 15)

    # ========= Action Handlers =========
    def OnAddTask(self):
        Dialog = customtkinter.CTkToplevel(self)
        Dialog.title("Add New Task")
        Dialog.geometry("450x550")
        Dialog.attributes("-topmost", True)
        Dialog.configure(fg_color=self.Colors["Light"])

        # Scrollable content
        ContentFrame = customtkinter.CTkScrollableFrame(
            Dialog, fg_color=self.Colors["Light"]
        )
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        TitleLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Task Title *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        TitleLabel.pack(pady=(5, 5))

        TitleEntry = customtkinter.CTkEntry(
            ContentFrame,
            placeholder_text="Enter task title...",
            width=380,
            height=35,
            fg_color="white",
            text_color=self.Colors["TextDark"],
            border_color=self.Colors["Primary"],
            border_width=2,
            corner_radius=8,
        )
        TitleEntry.pack(pady=5)

        DescLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Description (Optional)",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        DescLabel.pack(pady=(10, 5))

        DescEntry = customtkinter.CTkEntry(
            ContentFrame,
            placeholder_text="Add a description...",
            width=380,
            height=35,
            fg_color="white",
            text_color=self.Colors["TextDark"],
            border_color=self.Colors["Primary"],
            border_width=2,
            corner_radius=8,
        )
        DescEntry.pack(pady=5)

        # Subtasks section
        SubtasksLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Subtasks (Optional)",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        SubtasksLabel.pack(pady=(15, 5))

        # Container for subtask entries
        SubtaskEntries = []

        SubtasksFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=8
        )
        SubtasksFrame.pack(fill="x", pady=5)

        def AddSubtaskEntry():
            EntryFrame = customtkinter.CTkFrame(SubtasksFrame, fg_color="white")
            EntryFrame.pack(fill="x", padx=10, pady=5)

            SubtaskEntry = customtkinter.CTkEntry(
                EntryFrame,
                placeholder_text="Subtask title...",
                width=320,
                height=30,
                fg_color=self.Colors["Light"],
                text_color=self.Colors["TextDark"],
                border_color=self.Colors["Secondary"],
                border_width=1,
            )
            SubtaskEntry.pack(side="left", padx=5)
            SubtaskEntries.append(SubtaskEntry)

            RemoveBtn = customtkinter.CTkButton(
                EntryFrame,
                text="✕",
                fg_color=self.Colors["Accent"],
                hover_color="#D97706",
                width=30,
                height=30,
                command=lambda: (
                    EntryFrame.destroy(),
                    SubtaskEntries.remove(SubtaskEntry),
                ),
            )
            RemoveBtn.pack(side="left")

        AddSubtaskBtn = customtkinter.CTkButton(
            ContentFrame,
            text="➕ Add Subtask",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=150,
            height=30,
            command=AddSubtaskEntry,
        )
        AddSubtaskBtn.pack(pady=10)

        Feedback = customtkinter.CTkLabel(
            ContentFrame, text="", text_color="red", font=("Montserrat", 11)
        )
        Feedback.pack(pady=10)

        def Submit():
            Title = TitleEntry.get().strip()
            Description = DescEntry.get().strip() or None
            if not Title:
                Feedback.configure(text="⚠️ Title is required", text_color="red")
                return

            # Collect subtasks
            Subtasks = [
                entry.get().strip() for entry in SubtaskEntries if entry.get().strip()
            ]

            try:
                self.TaskManager.AddTask(self.username, Title, Description, Subtasks)
                self._RefreshOverview()
                self._RefreshDropdown()
                Dialog.destroy()
            except Exception as e:
                Feedback.configure(text=f"❌ Error: {str(e)}", text_color="red")

        # Bottom buttons frame
        ButtonFrame = customtkinter.CTkFrame(Dialog, fg_color=self.Colors["Light"])
        ButtonFrame.pack(fill="x", pady=(0, 20))

        SubmitBtn = customtkinter.CTkButton(
            ButtonFrame,
            text="✓ Add Task",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            width=140,
            height=35,
            corner_radius=8,
            command=Submit,
        )
        SubmitBtn.pack(pady=10)

    def OnOpenTaskManager(self):
        TaskManagerWindow(self, self.username)

    def OnOpenHabits(self):
        HabitTrackerWindow(self, self.username)

    def OnOpenTimer(self):
        FocusTimerWindow(self, self.username)

    def OnOpenAnalytics(self):
        AnalyticsWindow(self, self.username)

    def OnOpenNotes(self):
        QuickNotesWindow(self, self.username)

    def OnOpenGoals(self):
        DailyGoalsWindow(self, self.username)

    def OnOpenCalendar(self):
        CalendarWindow(self, self.username)

    def OnOpenSettings(self):
        SettingsWindow(self, self.username)

    # ========= Helper Methods =========
    def _RefreshOverview(self):
        Total, Completed, Pending = self.TaskManager.CountTasks(self.username)
        CompletionRate = int((Completed / Total * 100) if Total > 0 else 0)
        self.OverviewStats.configure(
            text=f"✅ {Completed}/{Total} Completed  •  ⏳ {Pending} Pending  •  📈 {CompletionRate}%"
        )

    def _RefreshDropdown(self):
        Titles = [
            Title
            for _id, Title, _status, _desc in self.TaskManager.GetTasks(self.username)
        ]
        if not Titles:
            Titles = ["No tasks yet - click 'Add Task' to get started!"]
        self.TasksDropdown.configure(values=Titles)

    def _TickClock(self):
        import datetime as _dt

        Now = _dt.datetime.now().strftime("%a %d %b, %H:%M:%S")
        self.ClockLabel.configure(text=Now)
        self.after(1000, self._TickClock)
