import bcrypt
import re
import datetime

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


class Auth:
    def __init__(self, DBPath: str = "src/core/UsersDatabase.db"):
        self.DBPath = DBPath
        self.MaxAttempts = 3  # lock account after 5 failed attempts
        self.LockoutMinutes = 10
        self._InitialiseDB()

    # Database initialisation
    def _InitialiseDB(self) -> None:
        """Create the necessary tables if they do not exist."""
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt BLOB NOT NULL,
                    failed_attempts INTEGER DEFAULT 0,
                    lockout_until TEXT DEFAULT NULL
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
    
    # Validation
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

    # Helper methods
    def _LogAction(self, username: str, action: str) -> None:
        "Record an event in the audit log."
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO audit_log (username, action, timestamp) VALUES (?, ?, ?)",
                (username, action, datetime.datetime.now().isoformat())
            )
            conn.commit()

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

    def _IncrementFaileds(self, username: str) -> None:
        "Increase failed login attempts, lock account if necessary."
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT failed_attempts FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()
            if result:
                failed_attempts = result[0] + 1
                if failed_attempts >= self.MaxAttempts:
                    lockout_until = datetime.datetime.now() + datetime.timedelta(
                        minutes=self.LockoutMinutes
                    )
                    cursor.execute(
                        "UPDATE users SET failed_attempts = 0, lockout_until = ? WHERE username = ?",
                        (lockout_until.isoformat(), username),
                    )
                    self._log_action(username, "Account locked")
                else:
                    cursor.execute(
                        "UPDATE users SET failed_attempts = ? WHERE username = ?",
                        (failed_attempts, username),
                    )
                conn.commit()

    def _ResetFailedAttempts(self, username: str) -> None:
        "Reset failed login attempts after a successful login."
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE username = ?",
                (username,),
            )
            conn.commit()

    # Core features
    def RegisterUser(self, username: str, password: str) -> bool:
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
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, hashed_password.decode("utf-8"), salt),
            )
            conn.commit()

        self._LogAction(username, "User registered")
        return True

    def LoginUser(self, username: str, password: str) -> bool:
        "Attempt to log in a user, with lockout and logging."
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
            self._ResetFailedAttempts(username)
            self._LogAction(username, "Successful login")
            return True
        else:
            self._IncrementFaileds(username)
            self._LogAction(username, "Failed login")
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
