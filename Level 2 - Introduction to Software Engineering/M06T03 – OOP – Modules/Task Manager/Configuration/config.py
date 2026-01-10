"""Configuration settings for the Task Manager application."""

# Admin user credentials
ADMIN_USERNAME = "admin"

# Menu configurations
ADMIN_MENU = [
    ("r", "register user"),
    ("a", "add task"),
    ("va", "view all tasks"),
    ("vm", "view my tasks"),
    ("vc", "view completed tasks"),
    ("del", "delete a task"),
    ("ds", "display statistics"),
    ("gr", "generate reports"),
    ("e", "exit")
]

USER_MENU = [
    ("a", "add task"),
    ("va", "view all tasks"),
    ("vm", "view my tasks"),
    ("e", "exit")
]
