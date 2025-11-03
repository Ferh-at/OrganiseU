import customtkinter


class AddTaskWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username, task_manager, on_success_callback=None):
        super().__init__(parent)

        self.username = username
        self.TaskManager = task_manager
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
        self.title("Add New Task")
        self.geometry("450x550")
        self.attributes("-topmost", True)
        self.configure(fg_color=self.Colors["Light"])

        self._CreateUI()

    def _CreateUI(self):
        # Scrollable content
        ContentFrame = customtkinter.CTkScrollableFrame(
            self, fg_color=self.Colors["Light"]
        )
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # Task Title
        TitleLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Task Title *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        TitleLabel.pack(pady=(5, 5))

        self.TitleEntry = customtkinter.CTkEntry(
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
        self.TitleEntry.pack(pady=5)

        # Task Description
        DescLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Description (Optional)",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        DescLabel.pack(pady=(10, 5))

        self.DescEntry = customtkinter.CTkEntry(
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
        self.DescEntry.pack(pady=5)

        # Subtasks section
        SubtasksLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Subtasks (Optional)",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        SubtasksLabel.pack(pady=(15, 5))

        # Container for subtask entries
        self.SubtaskEntries = []

        self.SubtasksFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=8
        )
        self.SubtasksFrame.pack(fill="x", pady=5)

        # Add Subtask button
        AddSubtaskBtn = customtkinter.CTkButton(
            ContentFrame,
            text="➕ Add Subtask",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 11, "bold"),
            width=150,
            height=30,
            command=self._AddSubtaskEntry,
        )
        AddSubtaskBtn.pack(pady=10)

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
            text="✓ Add Task",
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

    def _AddSubtaskEntry(self):
        """Add a new subtask entry field"""
        EntryFrame = customtkinter.CTkFrame(self.SubtasksFrame, fg_color="white")
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
        self.SubtaskEntries.append(SubtaskEntry)

        RemoveBtn = customtkinter.CTkButton(
            EntryFrame,
            text="✕",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            width=30,
            height=30,
            command=lambda: self._RemoveSubtaskEntry(EntryFrame, SubtaskEntry),
        )
        RemoveBtn.pack(side="left")

    def _RemoveSubtaskEntry(self, frame, entry):
        """Remove a subtask entry field"""
        frame.destroy()
        if entry in self.SubtaskEntries:
            self.SubtaskEntries.remove(entry)

    def _Submit(self):
        Title = self.TitleEntry.get().strip()
        Description = self.DescEntry.get().strip() or None

        if not Title:
            self.Feedback.configure(text="⚠️ Title is required", text_color="red")
            return

        Subtasks = [
            entry.get().strip() for entry in self.SubtaskEntries if entry.get().strip()
        ]

        try: #! a try block is used to catch any errors that may occur, for example if the database is blocked
            self.TaskManager.AddTask(self.username, Title, Description, Subtasks)

            if self.OnSuccessCallback: # ensuring that the callback exists, good dev practice
                self.OnSuccessCallback()

            self.destroy()
        except Exception as e:
            self.Feedback.configure(text=f"❌ Error: {str(e)}", text_color="red")