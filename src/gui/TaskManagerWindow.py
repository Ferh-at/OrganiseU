import customtkinter
from core.TaskManager import TaskManager


class TaskManagerWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.TaskManager = TaskManager()

        # Window configuration
        self.title("Task Manager")
        self.geometry("900x700")
        self.attributes("-topmost", True)

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

        self.configure(fg_color=self.Colors["Light"])

        self._CreateUI()
        self._LoadTasks()

    def _CreateUI(self):
        # Header
        HeaderFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x", padx=0, pady=0)

        Title = customtkinter.CTkLabel(
            HeaderFrame,
            text="📋 Task Manager",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Task list frame
        self.TaskListFrame = customtkinter.CTkScrollableFrame(
            self, fg_color="white", corner_radius=10
        )
        self.TaskListFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # Button frame
        ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.Colors["Light"])
        ButtonFrame.pack(fill="x", padx=20, pady=(0, 20))

        AddBtn = customtkinter.CTkButton(
            ButtonFrame,
            text="➕ Add New Task",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self._AddTask,
        )
        AddBtn.pack(side="left", padx=5)

        RefreshBtn = customtkinter.CTkButton(
            ButtonFrame,
            text="🔄 Refresh",
            fg_color=self.Colors["Primary"],
            hover_color=self.Colors["Dark"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self._LoadTasks,
        )
        RefreshBtn.pack(side="left", padx=5)

        CloseBtn = customtkinter.CTkButton(
            ButtonFrame,
            text="✕ Close",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self.destroy,
        )
        CloseBtn.pack(side="right", padx=5)

    def _LoadTasks(self):
        # Clear existing tasks
        for widget in self.TaskListFrame.winfo_children():
            widget.destroy()

        # Load tasks from database
        Tasks = self.TaskManager.GetTasks(self.username)

        if not Tasks:
            NoTasksLabel = customtkinter.CTkLabel(
                self.TaskListFrame,
                text="No tasks found. Click 'Add New Task' to create one!",
                text_color=self.Colors["TextDark"],
                font=("Montserrat", 14),
            )
            NoTasksLabel.pack(pady=50)
            return

        # Display each task with subtasks
        for TaskID, TaskTitle, TaskStatus, TaskDesc in Tasks:
            self._CreateTaskCard(TaskID, TaskTitle, TaskStatus, TaskDesc)

    def _CreateTaskCard(self, TaskID, TaskTitle, TaskStatus, TaskDesc):
        # Get subtasks for this task
        Subtasks = self.TaskManager.GetSubtasks(TaskID)

        # Main task card
        TaskCard = customtkinter.CTkFrame(
            self.TaskListFrame,
            fg_color=self.Colors["Primary"]
            if TaskStatus == "pending"
            else self.Colors["Success"],
            corner_radius=10,
        )
        TaskCard.pack(fill="x", padx=10, pady=10)

        # Task header frame
        TaskHeaderFrame = customtkinter.CTkFrame(TaskCard, fg_color="transparent")
        TaskHeaderFrame.pack(fill="x", padx=10, pady=10)

        # Task status icon and title
        StatusIcon = "✓" if TaskStatus == "completed" else "○"
        TaskLabel = customtkinter.CTkLabel(
            TaskHeaderFrame,
            text=f"{StatusIcon} {TaskTitle}",
            text_color=self.Colors["Text"],
            font=("Montserrat", 15, "bold"),
            anchor="w",
        )
        TaskLabel.pack(side="left", padx=5, fill="x", expand=True)

        # Task buttons
        if TaskStatus == "pending":
            CompleteTaskBtn = customtkinter.CTkButton(
                TaskHeaderFrame,
                text="✓ Complete",
                fg_color=self.Colors["Success"],
                hover_color="#048A5E",
                text_color=self.Colors["Text"],
                font=("Montserrat", 10, "bold"),
                width=90,
                height=30,
                command=lambda: self._CompleteTask(TaskID),
            )
            CompleteTaskBtn.pack(side="right", padx=5)

        DeleteBtn = customtkinter.CTkButton(
            TaskHeaderFrame,
            text="🗑️ Delete",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 10, "bold"),
            width=80,
            height=30,
            command=lambda: self._DeleteTask(TaskID),
        )
        DeleteBtn.pack(side="right", padx=5)

        # Description if exists
        if TaskDesc:
            DescLabel = customtkinter.CTkLabel(
                TaskCard,
                text=f"📝 {TaskDesc}",
                text_color=self.Colors["Text"],
                font=("Montserrat", 11),
                anchor="w",
            )
            DescLabel.pack(anchor="w", padx=15, pady=(0, 5))

        # Subtasks section
        if Subtasks:
            SubtasksFrame = customtkinter.CTkFrame(
                TaskCard, fg_color=self.Colors["Dark"], corner_radius=8
            )
            SubtasksFrame.pack(fill="x", padx=15, pady=(5, 10))

            for SubtaskID, SubtaskTitle, SubtaskStatus in Subtasks:
                self._CreateSubtaskItem(
                    SubtasksFrame, SubtaskID, SubtaskTitle, SubtaskStatus, TaskStatus
                )

    def _CreateSubtaskItem(
        self, parent, SubtaskID, SubtaskTitle, SubtaskStatus, ParentTaskStatus
    ):
        SubtaskFrame = customtkinter.CTkFrame(parent, fg_color="transparent")
        SubtaskFrame.pack(fill="x", padx=10, pady=5)

        # Subtask checkbox or icon
        StatusIcon = "✓" if SubtaskStatus == "completed" else "☐"

        SubtaskLabel = customtkinter.CTkLabel(
            SubtaskFrame,
            text=f"  {StatusIcon} {SubtaskTitle}",
            text_color=self.Colors["Text"],
            font=("Montserrat", 12),
            anchor="w",
        )
        SubtaskLabel.pack(side="left", padx=5, fill="x", expand=True)

        # Only show complete button if subtask is pending and parent task is pending
        if SubtaskStatus == "pending" and ParentTaskStatus == "pending":
            CompleteBtn = customtkinter.CTkButton(
                SubtaskFrame,
                text="✓",
                fg_color=self.Colors["Success"],
                hover_color="#048A5E",
                text_color=self.Colors["Text"],
                width=30,
                height=25,
                command=lambda: self._CompleteSubtask(SubtaskID),
            )
            CompleteBtn.pack(side="right", padx=5)

    def _AddTask(self):
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
            ContentFrame, placeholder_text="Enter task title...", width=380, height=35
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
            ContentFrame, placeholder_text="Add a description...", width=380, height=35
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
                self._LoadTasks()
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
            command=Submit,
        )
        SubmitBtn.pack(pady=10)

    def _DeleteTask(self, TaskID):
        # Confirm deletion
        ConfirmDialog = customtkinter.CTkToplevel(self)
        ConfirmDialog.title("Confirm Delete")
        ConfirmDialog.geometry("350x150")
        ConfirmDialog.attributes("-topmost", True)
        ConfirmDialog.configure(fg_color=self.Colors["Light"])

        MsgLabel = customtkinter.CTkLabel(
            ConfirmDialog,
            text="Are you sure you want to delete this task?\nAll subtasks will also be deleted.",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12),
            justify="center",
        )
        MsgLabel.pack(pady=20)

        BtnFrame = customtkinter.CTkFrame(ConfirmDialog, fg_color=self.Colors["Light"])
        BtnFrame.pack(pady=10)

        def ConfirmDelete():
            self.TaskManager.DeleteTask(TaskID)
            self._LoadTasks()
            ConfirmDialog.destroy()

        YesBtn = customtkinter.CTkButton(
            BtnFrame,
            text="Yes, Delete",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            width=120,
            command=ConfirmDelete,
        )
        YesBtn.pack(side="left", padx=10)

        NoBtn = customtkinter.CTkButton(
            BtnFrame,
            text="Cancel",
            fg_color=self.Colors["Dark"],
            hover_color=self.Colors["Primary"],
            text_color=self.Colors["Text"],
            width=120,
            command=ConfirmDialog.destroy,
        )
        NoBtn.pack(side="left", padx=10)

    def _CompleteTask(self, TaskID):
        self.TaskManager.CompleteTask(TaskID)
        self._LoadTasks()

    def _CompleteSubtask(self, SubtaskID):
        self.TaskManager.CompleteSubtask(SubtaskID)
        self._LoadTasks()
