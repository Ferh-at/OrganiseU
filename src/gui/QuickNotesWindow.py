import customtkinter


class QuickNotesWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username

        # Window configuration
        self.title("Quick Notes")
        self.geometry("700x600")
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
            text="📝 Quick Notes",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Toolbar
        ToolbarFrame = customtkinter.CTkFrame(self, fg_color=self.Colors["Light"])
        ToolbarFrame.pack(fill="x", padx=20, pady=(20, 10))

        SaveBtn = customtkinter.CTkButton(
            ToolbarFrame,
            text="💾 Save",
            fg_color=self.Colors["Secondary"],
            hover_color="#048A5E",
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=100,
            height=35,
            command=self._SaveNote,
        )
        SaveBtn.pack(side="left", padx=5)

        ClearBtn = customtkinter.CTkButton(
            ToolbarFrame,
            text="🗑️ Clear",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=100,
            height=35,
            command=self._ClearNote,
        )
        ClearBtn.pack(side="left", padx=5)

        # Notes text area
        self.NotesTextbox = customtkinter.CTkTextbox(
            self,
            fg_color="white",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 13),
            corner_radius=10,
            wrap="word",
        )
        self.NotesTextbox.pack(fill="both", expand=True, padx=20, pady=10)

        # Insert placeholder text
        self.NotesTextbox.insert("1.0", "Start typing your notes here...\n\n")

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

    def _SaveNote(self):
        Content = self.NotesTextbox.get("1.0", "end-1c")
        # Placeholder for save functionality
        print(f"Saving note: {Content[:50]}...")

    def _ClearNote(self):
        self.NotesTextbox.delete("1.0", "end")
