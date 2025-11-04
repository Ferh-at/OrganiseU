import customtkinter
import datetime
from tkcalendar import DateEntry


class AddHabitWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username, habit_manager, on_success_callback=None):
        super().__init__(parent)

        self.username = username
        self.HabitManager = habit_manager
        self.OnSuccessCallback = on_success_callback

        # Color palette
        self.Colors = {
            "Primary": "#2E86AB",
            "Secondary": "#06A77D",
            "Accent": "#F18F01",
            "Dark": "#1B263B",
            "Light": "#E8F4F8",
            "Text": "#FFFFFF",
            "TextDark": "#1B263B",
            "Success": "#06A77D",
        }

        # Window configuration
        self.title("Add New Habit")
        self.geometry("500x700")
        self.attributes("-topmost", True)
        self.configure(fg_color=self.Colors["Light"])

        # Get user's discipline for preview
        stats = self.HabitManager._GetUserStats(username)
        self.UserDiscipline = stats["discipline"]

        self._CreateUI()

    def _CreateUI(self):
        # Scrollable content
        ContentFrame = customtkinter.CTkScrollableFrame(
            self, fg_color=self.Colors["Light"]
        )
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # Habit Name
        NameLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Habit Name *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        NameLabel.pack(pady=(5, 5))

        self.NameEntry = customtkinter.CTkEntry(
            ContentFrame,
            placeholder_text="Enter habit name...",
            width=420,
            height=35,
            fg_color="white",
            text_color=self.Colors["TextDark"],
            border_color=self.Colors["Primary"],
            border_width=2,
            corner_radius=8,
        )
        self.NameEntry.pack(pady=5)

        # Habit Type: Positive/Negative
        TypeLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Habit Type *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        TypeLabel.pack(pady=(15, 5))

        self.HabitTypeVar = customtkinter.StringVar(value="positive")
        TypeFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=8
        )
        TypeFrame.pack(fill="x", pady=5)

        PositiveRadio = customtkinter.CTkRadioButton(
            TypeFrame,
            text="✅ Positive (e.g., drink water, exercise)",
            variable=self.HabitTypeVar,
            value="positive",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 11),
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
        )
        PositiveRadio.pack(anchor="w", padx=15, pady=8)

        NegativeRadio = customtkinter.CTkRadioButton(
            TypeFrame,
            text="❌ Negative (e.g., phone usage, junk food)",
            variable=self.HabitTypeVar,
            value="negative",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 11),
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
        )
        NegativeRadio.pack(anchor="w", padx=15, pady=8)

        # Goal Type: Increase/Decrease
        GoalLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Your Goal *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        GoalLabel.pack(pady=(15, 5))

        self.GoalTypeVar = customtkinter.StringVar(value="increase")
        GoalFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=8
        )
        GoalFrame.pack(fill="x", pady=5)

        IncreaseRadio = customtkinter.CTkRadioButton(
            GoalFrame,
            text="📈 Increase (do it more often)",
            variable=self.GoalTypeVar,
            value="increase",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 11),
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            command=self._UpdatePreview,
        )
        IncreaseRadio.pack(anchor="w", padx=15, pady=8)

        DecreaseRadio = customtkinter.CTkRadioButton(
            GoalFrame,
            text="📉 Decrease (do it less often)",
            variable=self.GoalTypeVar,
            value="decrease",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 11),
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            command=self._UpdatePreview,
        )
        DecreaseRadio.pack(anchor="w", padx=15, pady=8)

        # Current Count
        CurrentLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Current Daily Count *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        CurrentLabel.pack(pady=(15, 5))

        CurrentSubLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="How many times per day do you currently do this?",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 9),
        )
        CurrentSubLabel.pack(pady=(0, 5))

        self.CurrentEntry = customtkinter.CTkEntry(
            ContentFrame,
            placeholder_text="e.g., 15",
            width=420,
            height=35,
            fg_color="white",
            text_color=self.Colors["TextDark"],
            border_color=self.Colors["Primary"],
            border_width=2,
            corner_radius=8,
        )
        self.CurrentEntry.pack(pady=5)
        self.CurrentEntry.bind("<KeyRelease>", lambda e: self._UpdatePreview())

        # Target Count
        TargetLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Target Goal *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        TargetLabel.pack(pady=(15, 5))

        TargetSubLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="What's your final goal?",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 9),
        )
        TargetSubLabel.pack(pady=(0, 5))

        self.TargetEntry = customtkinter.CTkEntry(
            ContentFrame,
            placeholder_text="e.g., 5",
            width=420,
            height=35,
            fg_color="white",
            text_color=self.Colors["TextDark"],
            border_color=self.Colors["Primary"],
            border_width=2,
            corner_radius=8,
        )
        self.TargetEntry.pack(pady=5)
        self.TargetEntry.bind("<KeyRelease>", lambda e: self._UpdatePreview())

        # Target Date
        DateLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Target Date *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        DateLabel.pack(pady=(15, 5))

        DateSubLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="When do you want to reach your goal?",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 9),
        )
        DateSubLabel.pack(pady=(0, 5))

        # Date picker frame
        DateFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=8
        )
        DateFrame.pack(fill="x", pady=5)

        self.DatePicker = DateEntry(
            DateFrame,
            width=40,
            background=self.Colors["Primary"],
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            mindate=datetime.date.today() + datetime.timedelta(days=1),
        )
        self.DatePicker.pack(padx=15, pady=10)
        self.DatePicker.bind("<<DateEntrySelected>>", lambda e: self._UpdatePreview())

        # Preview Label
        PreviewFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color=self.Colors["Primary"], corner_radius=10
        )
        PreviewFrame.pack(fill="x", pady=(20, 10))

        PreviewTitle = customtkinter.CTkLabel(
            PreviewFrame,
            text="📊 Preview",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
        )
        PreviewTitle.pack(pady=(10, 5))

        self.PreviewLabel = customtkinter.CTkLabel(
            PreviewFrame,
            text="Enter values above to see preview",
            text_color=self.Colors["Text"],
            font=("Montserrat", 12),
            wraplength=380,
        )
        self.PreviewLabel.pack(pady=(5, 15))

        # Feedback label
        self.Feedback = customtkinter.CTkLabel(
            ContentFrame, text="", text_color="red", font=("Montserrat", 11)
        )
        self.Feedback.pack(pady=10)

        # Bottom buttons frame
        ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.Colors["Light"])
        ButtonFrame.pack(fill="x", pady=(0, 20))

        SubmitBtn = customtkinter.CTkButton(
            ButtonFrame,
            text="✓ Add Habit",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            width=140,
            height=35,
            corner_radius=8,
            command=self._Submit,
        )
        SubmitBtn.pack(pady=10)

    def _UpdatePreview(self):
        """Update the preview label when values change"""
        try:
            baseline = int(self.CurrentEntry.get())
            target = int(self.TargetEntry.get())
            target_date = self.DatePicker.get_date()

            preview_text = self.HabitManager.CalculatePreview(
                baseline, target, target_date, self.UserDiscipline
            )
            self.PreviewLabel.configure(text=preview_text)
        except ValueError:
            self.PreviewLabel.configure(text="Enter valid numbers to see preview")
        except Exception as e:
            self.PreviewLabel.configure(text=f"Error: {str(e)}")

    def _Submit(self):
        """Handle habit submission"""
        # Validate inputs
        habit_name = self.NameEntry.get().strip()
        if not habit_name:
            self.Feedback.configure(text="⚠️ Habit name is required", text_color="red")
            return

        try:
            baseline_count = int(self.CurrentEntry.get())
            target_count = int(self.TargetEntry.get())
        except ValueError:
            self.Feedback.configure(
                text="⚠️ Current and target counts must be numbers", text_color="red"
            )
            return

        if baseline_count < 0 or target_count < 0:
            self.Feedback.configure(
                text="⚠️ Counts must be positive numbers", text_color="red"
            )
            return

        # Validate goal type matches the direction
        goal_type = self.GoalTypeVar.get()
        if goal_type == "increase" and target_count <= baseline_count:
            self.Feedback.configure(
                text="⚠️ Target must be higher than current for 'increase' goal",
                text_color="red",
            )
            return
        elif goal_type == "decrease" and target_count >= baseline_count:
            self.Feedback.configure(
                text="⚠️ Target must be lower than current for 'decrease' goal",
                text_color="red",
            )
            return

        target_date = self.DatePicker.get_date()
        if target_date <= datetime.date.today():
            self.Feedback.configure(
                text="⚠️ Target date must be in the future", text_color="red"
            )
            return

        # Get habit type
        is_positive = 1 if self.HabitTypeVar.get() == "positive" else 0

        try:
            self.HabitManager.AddHabit(
                self.username,
                habit_name,
                is_positive,
                goal_type,
                baseline_count,
                target_count,
                target_date.isoformat(),
            )

            if self.OnSuccessCallback:
                self.OnSuccessCallback()

            self.destroy()
        except Exception as e:
            self.Feedback.configure(text=f"❌ Error: {str(e)}", text_color="red")
