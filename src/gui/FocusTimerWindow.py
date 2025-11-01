import customtkinter


class FocusTimerWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.TimerRunning = False
        self.TimeRemaining = 25 * 60  # 25 minutes in seconds

        # Window configuration
        self.title("Focus Timer")
        self.geometry("500x600")
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
            text="⏱️ Focus Timer",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Main content
        ContentFrame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=10)
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # Pomodoro info
        InfoLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Pomodoro Technique: 25 minutes of focused work",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 14),
        )
        InfoLabel.pack(pady=20)

        # Timer display
        TimerFrame = customtkinter.CTkFrame(
            ContentFrame,
            fg_color=self.Colors["Primary"],
            corner_radius=100,
            width=300,
            height=300,
        )
        TimerFrame.pack(pady=30)
        TimerFrame.pack_propagate(False)

        self.TimerLabel = customtkinter.CTkLabel(
            TimerFrame,
            text="25:00",
            text_color=self.Colors["Text"],
            font=("Montserrat", 72, "bold"),
        )
        self.TimerLabel.place(relx=0.5, rely=0.5, anchor="center")

        # Control buttons
        ControlFrame = customtkinter.CTkFrame(ContentFrame, fg_color="white")
        ControlFrame.pack(pady=20)

        self.StartBtn = customtkinter.CTkButton(
            ControlFrame,
            text="▶ Start",
            fg_color=self.Colors["Secondary"],
            hover_color="#048A5E",
            text_color=self.Colors["Text"],
            font=("Montserrat", 16, "bold"),
            width=140,
            height=50,
            command=self._StartTimer,
        )
        self.StartBtn.pack(side="left", padx=10)

        self.PauseBtn = customtkinter.CTkButton(
            ControlFrame,
            text="⏸ Pause",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 16, "bold"),
            width=140,
            height=50,
            command=self._PauseTimer,
            state="disabled",
        )
        self.PauseBtn.pack(side="left", padx=10)

        ResetBtn = customtkinter.CTkButton(
            ControlFrame,
            text="↻ Reset",
            fg_color=self.Colors["Dark"],
            hover_color=self.Colors["Primary"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 16, "bold"),
            width=140,
            height=50,
            command=self._ResetTimer,
        )
        ResetBtn.pack(side="left", padx=10)

        # Preset times
        PresetFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color=self.Colors["Light"], corner_radius=10
        )
        PresetFrame.pack(fill="x", padx=20, pady=20)

        PresetLabel = customtkinter.CTkLabel(
            PresetFrame,
            text="Quick Presets:",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12, "bold"),
        )
        PresetLabel.pack(pady=(10, 5))

        PresetBtnFrame = customtkinter.CTkFrame(
            PresetFrame, fg_color=self.Colors["Light"]
        )
        PresetBtnFrame.pack(pady=(0, 10))

        for minutes, label in [
            (5, "5 min"),
            (15, "15 min"),
            (25, "25 min"),
            (45, "45 min"),
        ]:
            btn = customtkinter.CTkButton(
                PresetBtnFrame,
                text=label,
                fg_color=self.Colors["Primary"],
                hover_color=self.Colors["Dark"],
                width=80,
                height=30,
                command=lambda m=minutes: self._SetTimer(m),
            )
            btn.pack(side="left", padx=5)

        # Close button
        CloseBtn = customtkinter.CTkButton(
            self,
            text="✕ Close",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self.destroy,
        )
        CloseBtn.pack(pady=(0, 20))

    def _SetTimer(self, minutes):
        if not self.TimerRunning:
            self.TimeRemaining = minutes * 60
            self._UpdateTimerDisplay()

    def _UpdateTimerDisplay(self):
        Minutes = self.TimeRemaining // 60
        Seconds = self.TimeRemaining % 60
        self.TimerLabel.configure(text=f"{Minutes:02d}:{Seconds:02d}")

    def _StartTimer(self):
        self.TimerRunning = True
        self.StartBtn.configure(state="disabled")
        self.PauseBtn.configure(state="normal")
        self._Tick()

    def _Tick(self):
        if self.TimerRunning and self.TimeRemaining > 0:
            self.TimeRemaining -= 1
            self._UpdateTimerDisplay()
            self.after(1000, self._Tick)
        elif self.TimeRemaining == 0:
            self.TimerRunning = False
            self.StartBtn.configure(state="normal")
            self.PauseBtn.configure(state="disabled")
            self.TimerLabel.configure(text="Done! 🎉")

    def _PauseTimer(self):
        self.TimerRunning = False
        self.StartBtn.configure(state="normal")
        self.PauseBtn.configure(state="disabled")

    def _ResetTimer(self):
        self.TimerRunning = False
        self.TimeRemaining = 25 * 60
        self._UpdateTimerDisplay()
        self.StartBtn.configure(state="normal")
        self.PauseBtn.configure(state="disabled")
