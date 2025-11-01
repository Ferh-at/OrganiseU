import customtkinter
from core.TaskManager import TaskManager


class TaskManagerWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.TaskManager = TaskManager()

        # Window configuration
        self.title("Task Manager")
        self.geometry("800x600")
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
            hover_color=self.Colors["Secondary"],
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
            hover_color=self.Colors["Primary"],
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
            hover_color=self.Colors["Accent"],
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

        # Display each task
        for TaskID, TaskTitle in Tasks:
            self._CreateTaskCard(TaskID, TaskTitle)

    def _CreateTaskCard(self, TaskID, TaskTitle):
        TaskCard = customtkinter.CTkFrame(
            self.TaskListFrame, fg_color=self.Colors["Primary"], corner_radius=10
        )
        TaskCard.pack(fill="x", padx=10, pady=5)

        TaskLabel = customtkinter.CTkLabel(
            TaskCard,
            text=f"✓ {TaskTitle}",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13),
            anchor="w",
        )
        TaskLabel.pack(side="left", padx=15, pady=12, fill="x", expand=True)

        DeleteBtn = customtkinter.CTkButton(
            TaskCard,
            text="🗑️",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            width=40,
            height=30,
            command=lambda: self._DeleteTask(TaskID),
        )
        DeleteBtn.pack(side="right", padx=10, pady=8)

    def _AddTask(self):
        Dialog = customtkinter.CTkToplevel(self)
        Dialog.title("Add New Task")
        Dialog.geometry("400x250")
        Dialog.attributes("-topmost", True)
        Dialog.configure(fg_color=self.Colors["Light"])

        TitleLabel = customtkinter.CTkLabel(
            Dialog,
            text="Task Title *",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        TitleLabel.pack(pady=(20, 5))

        TitleEntry = customtkinter.CTkEntry(
            Dialog, placeholder_text="Enter task title...", width=350, height=35
        )
        TitleEntry.pack(pady=5)

        DescLabel = customtkinter.CTkLabel(
            Dialog,
            text="Description (Optional)",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        DescLabel.pack(pady=(10, 5))

        DescEntry = customtkinter.CTkEntry(
            Dialog, placeholder_text="Add a description...", width=350, height=35
        )
        DescEntry.pack(pady=5)

        def Submit():
            Title = TitleEntry.get().strip()
            Description = DescEntry.get().strip() or None
            if Title:
                self.TaskManager.AddTask(self.username, Title, Description)
                self._LoadTasks()
                Dialog.destroy()

        SubmitBtn = customtkinter.CTkButton(
            Dialog,
            text="✓ Add Task",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Secondary"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=35,
            command=Submit,
        )
        SubmitBtn.pack(pady=20)

    def _DeleteTask(self, TaskID):
        # Placeholder for delete functionality
        print(f"Delete task {TaskID}")
        self._LoadTasks()
