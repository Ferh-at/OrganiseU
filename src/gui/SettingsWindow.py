import customtkinter


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username

        # Window configuration
        self.title("Settings")
        self.geometry("700x650")
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

    def _CreateUI(self):
        # Header
        HeaderFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x", padx=0, pady=0)

        Title = customtkinter.CTkLabel(
            HeaderFrame,
            text="⚙️ Settings",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Main content
        ContentFrame = customtkinter.CTkScrollableFrame(
            self, fg_color=self.Colors["Light"]
        )
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # User settings
        self._CreateSection(ContentFrame, "👤 User Settings")

        UserFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=10
        )
        UserFrame.pack(fill="x", pady=10)

        UsernameLabel = customtkinter.CTkLabel(
            UserFrame,
            text=f"Username: {self.username}",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 13),
        )
        UsernameLabel.pack(anchor="w", padx=20, pady=15)

        ChangePasswordBtn = customtkinter.CTkButton(
            UserFrame,
            text="🔑 Change Password",
            fg_color=self.Colors["Primary"],
            hover_color=self.Colors["Dark"],
            text_color=self.Colors["Text"],
            height=35,
        )
        ChangePasswordBtn.pack(anchor="w", padx=20, pady=(0, 15))

        # Appearance settings
        self._CreateSection(ContentFrame, "🎨 Appearance")

        AppearanceFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=10
        )
        AppearanceFrame.pack(fill="x", pady=10)

        ThemeLabel = customtkinter.CTkLabel(
            AppearanceFrame,
            text="Theme Mode:",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 13),
        )
        ThemeLabel.pack(anchor="w", padx=20, pady=(15, 5))

        ThemeSwitch = customtkinter.CTkSwitch(
            AppearanceFrame,
            text="Dark Mode",
            fg_color=self.Colors["Primary"],
            progress_color=self.Colors["Secondary"],
        )
        ThemeSwitch.pack(anchor="w", padx=20, pady=(0, 15))

        # Notification settings
        self._CreateSection(ContentFrame, "🔔 Notifications")

        NotifFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=10
        )
        NotifFrame.pack(fill="x", pady=10)

        NotifSwitch1 = customtkinter.CTkSwitch(
            NotifFrame,
            text="Task Reminders",
            fg_color=self.Colors["Primary"],
            progress_color=self.Colors["Secondary"],
        )
        NotifSwitch1.pack(anchor="w", padx=20, pady=(15, 10))
        NotifSwitch1.select()

        NotifSwitch2 = customtkinter.CTkSwitch(
            NotifFrame,
            text="Daily Goal Notifications",
            fg_color=self.Colors["Primary"],
            progress_color=self.Colors["Secondary"],
        )
        NotifSwitch2.pack(anchor="w", padx=20, pady=(0, 10))
        NotifSwitch2.select()

        NotifSwitch3 = customtkinter.CTkSwitch(
            NotifFrame,
            text="Habit Tracking Reminders",
            fg_color=self.Colors["Primary"],
            progress_color=self.Colors["Secondary"],
        )
        NotifSwitch3.pack(anchor="w", padx=20, pady=(0, 15))

        # Data management
        self._CreateSection(ContentFrame, "💾 Data Management")

        DataFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=10
        )
        DataFrame.pack(fill="x", pady=10)

        ExportBtn = customtkinter.CTkButton(
            DataFrame,
            text="📤 Export Data",
            fg_color=self.Colors["Secondary"],
            hover_color="#048A5E",
            text_color=self.Colors["Text"],
            height=35,
        )
        ExportBtn.pack(anchor="w", padx=20, pady=(15, 10))

        ClearDataBtn = customtkinter.CTkButton(
            DataFrame,
            text="🗑️ Clear All Data",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            height=35,
        )
        ClearDataBtn.pack(anchor="w", padx=20, pady=(0, 15))

        # About section
        self._CreateSection(ContentFrame, "ℹ️ About")

        AboutFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=10
        )
        AboutFrame.pack(fill="x", pady=10)

        AboutText = customtkinter.CTkLabel(
            AboutFrame,
            text="OrganiseU v1.0\nYour Personal Productivity Companion",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 13),
            justify="center",
        )
        AboutText.pack(pady=20)

        # Close button
        CloseBtn = customtkinter.CTkButton(
            self,
            text="✕ Close",
            fg_color=self.Colors["Dark"],
            hover_color=self.Colors["Primary"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self.destroy,
        )
        CloseBtn.pack(pady=(0, 20))

    def _CreateSection(self, parent, title):
        SectionLabel = customtkinter.CTkLabel(
            parent,
            text=title,
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 16, "bold"),
            anchor="w",
        )
        SectionLabel.pack(anchor="w", padx=10, pady=(15, 5))
