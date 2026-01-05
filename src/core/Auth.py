import bcrypt
import re
import datetime
import sqlite3

from utils.AuthenticationWrapper import GetDBConnection


class AuthError(Exception):
    "Base exception class for authentication errors."
    pass


class UserExistsError(AuthError):
    "Raised when trying to register with an existing username."
    pass


class InvalidCredentialsError(AuthError):
    "Raised when login credentials are invalid."
    pass


class WeakPasswordError(AuthError):
    "Raised when password does not meet strength requirements."
    pass

class AlreadyOnboardedError(AuthError):
    "Raised if onboarding is attempted for a user who has already completed it."
    pass

def HashingFunction(input_string: str) -> str:
    state = [2, 3, 5, 7, 11, 13, 17, 19]
    
    MODULUS = 2**31 - 1

    for char in input_string:
        char_code = ord(char)
        for i in range(len(state)):
            state[i] = (state[i] ^ char_code)
            state[i] = (state[i] << 3 | state[i] >> (29)) & MODULUS
            state[i] = (state[i] + state[(i - 1) % len(state)]) & MODULUS
            state[i] = (state[i] * (i + 7)) & MODULUS
    final_hash = ""
    for num in state:

        final_hash += '{:08x}'.format(num)
        
    return final_hash

class Auth:
    def __init__(self, DBPath: str = "src/core/UsersDatabase.db"):
        self.DBPath = DBPath
        self.MaxAttempts = 10  # lock account after 5 failed attempts
        self.LockoutMinutes = 1
        self._InitialiseDB()

    # Database initialisation
    def _InitialiseDB(self) -> None:
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt BLOB NOT NULL,
                    failed_attempts INTEGER DEFAULT 0,
                    lockout_until TEXT DEFAULT NULL,
    
                    concentration INTEGER DEFAULT NULL,
                    discipline INTEGER DEFAULT NULL,
                    motivation INTEGER DEFAULT NULL,
                    energy INTEGER DEFAULT NULL,
                    is_onboarded INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    action TEXT,
                    timestamp TEXT
                )
            """)
            conn.commit()
    
    def _ValidateUsername(self, username: str) -> bool:
        "Check that the username is alphanumeric and between 5–15 characters."
        return bool(re.match(r"^[A-Za-z0-9_]{5,15}$", username))

    def _ValidatePassword(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[@$!%*?&]", password):
            return False
        return True

    def _LogAction(self, username: str, action: str, conn=None) -> None:
        "Record an event in the audit log."
        close_after = False
        if conn is None:
            conn = sqlite3.connect(self.DBPath)
            close_after = True

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_log (username, action, timestamp) VALUES (?, ?, ?)",
            (username, action, datetime.datetime.now().isoformat())
        )
        conn.commit()

        if close_after:
            conn.close()

    def _IsAccountLocked(self, username: str) -> bool:
        "Check if an account is currently locked out."
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT lockout_until FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()

        if result and result[0]:
            lockout_until = datetime.datetime.fromisoformat(result[0])
            if datetime.datetime.now() < lockout_until:
                return True
        return False

    def _IncrementFaileds(self, username: str, conn=None) -> None:
        """Increase failed login attempts, lock account if necessary."""
        close_after = False
        if conn is None:
            conn = sqlite3.connect(self.DBPath)
            close_after = True

        cursor = conn.cursor()
        cursor.execute("SELECT failed_attempts FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            failed_attempts = result[0] + 1
            if failed_attempts >= self.MaxAttempts:
                lockout_until = datetime.datetime.now() + datetime.timedelta(minutes=self.LockoutMinutes)
                cursor.execute(
                    "UPDATE users SET failed_attempts = 0, lockout_until = ? WHERE username = ?",
                    (lockout_until.isoformat(), username),
                )
                self._LogAction(username, "Account locked", conn)
            else:
                cursor.execute(
                    "UPDATE users SET failed_attempts = ? WHERE username = ?",
                    (failed_attempts, username),
                )
        conn.commit()

        if close_after:
            conn.close()

    def _ResetFailedAttempts(self, username: str, conn=None) -> None:
        "Reset failed login attempts after a successful login."
        close_after = False
        if conn is None:
            conn = sqlite3.connect(self.DBPath)
            close_after = True

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE username = ?",
            (username,),
        )
        conn.commit()

        if close_after:
            conn.close()

    def RegisterUser(self, username: str, password: str, concentration, discipline, motivation, energy) -> bool:
        "Register a new user after validation and hashing."
        if not self._ValidateUsername(username):
            raise ValueError("Invalid username. Use 3–20 letters, numbers, or underscores.")

        if not self._ValidatePassword(password):
            raise WeakPasswordError("Password does not meet complexity requirements.")

        if self.UserExists(username):
            raise UserExistsError("Username already exists.")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (
                    username, password_hash, salt,
                    concentration, discipline, motivation, energy, is_onboarded
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (username, hashed_password.decode("utf-8"), salt,
                concentration, discipline, motivation, energy, 1) #? The 1 stands for IsOnboarded
            )   
            conn.commit()

        self._LogAction(username, "User registered")
        return True
    
    def SaveOnboardingData(self, username: str, data: dict) -> bool:
        """
        Save onboarding ratings (concentration, discipline, motivation, energy).
        Can only be set once per user.
        """
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_onboarded FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if not result:
                raise InvalidCredentialsError("User does not exist.")
            
            if result[0] == 1:
                raise AlreadyOnboardedError("User already completed onboarding.")

            cursor.execute("""
                UPDATE users 
                SET concentration = ?, discipline = ?, motivation = ?, energy = ?, is_onboarded = 1
                WHERE username = ?
            """, (
                data.get("Concentration"),
                data.get("Discipline"),
                data.get("Motivation"),
                data.get("Energy"),
                username
            ))
            conn.commit()

        self._LogAction(username, "Onboarding completed")
        return True 
    
    def LoginUser(self, username: str, password: str) -> bool:
        """Attempt to log in a user, with lockout and logging."""
        if not self.UserExists(username):
            raise InvalidCredentialsError("User not found.")

        if self._IsAccountLocked(username):
            raise AuthError("Account is temporarily locked due to too many failed attempts.")

        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password_hash, salt FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()

            if result is None:
                raise InvalidCredentialsError("Invalid login attempt.")

            stored_hash, stored_salt = result
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                self._ResetFailedAttempts(username, conn)
                self._LogAction(username, "Successful login", conn)
                return True
            else:
                self._IncrementFaileds(username, conn)
                self._LogAction(username, "Failed login", conn)
                raise InvalidCredentialsError("Incorrect password.")

    def UserExists(self, username: str) -> bool:
        "Check if a username is already registered."
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            return cursor.fetchone() is not None
    
    # Extensible features
    def ResetPassword(self, username: str, new_password: str) -> bool:
        "Allow password reset with validation (simplified)."
        if not self._ValidatePassword(new_password):
            raise WeakPasswordError("Password does not meet complexity requirements.")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), salt)

        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ?, salt = ?, failed_attempts = 0, lockout_until = NULL WHERE username = ?",
                (hashed_password.decode("utf-8"), salt, username),
            )
            conn.commit()

        self._LogAction(username, "Password reset")
        return True
