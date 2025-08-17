class Email:
    """
    A class to represent an email message.
    """

    def __init__(self, email_address, subject_line, email_content):
        """
        Initialize an Email object.

        Args:
            email_address (str): The sender's email address.
            subject_line (str): The subject of the email.
            email_content (str): The content/body of the email.
        """
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content
        self.has_been_read = False

    def mark_as_read(self):
        """
        Mark the email as read.
        """
        self.has_been_read = True


# Inbox to store Email objects
inbox = []


def populate_inbox():
    """
    Add a few sample emails to the inbox for demonstration/testing.
    """
    sample_emails = [
        ("welcome@hyperiondev.com", "Welcome to HyperionDev!", "Great work on the bootcamp!"),
        ("admin@hyperiondev.com", "Copyright © 2025 HyperionDev. All rights reserved.",
         "Please read the terms and conditions."),
        ("tutor@hyperiondev.com", "Your excellent marks!", "Congratulations on your results!")
    ]
    for address, subject, content in sample_emails:
        inbox.append(Email(address, subject, content))


def list_emails():
    """
    Show all emails in the inbox with their index for user selection.
    """
    print("\nInbox:")
    for idx, email in enumerate(inbox):
        print(f"{idx}: From {email.email_address} - {email.subject_line}")
        print(f"{idx}: {email.subject_line} ({status})")


def read_email(index):
    """
    Display full details of a selected email and update its read status.

    Args:
        index (int): The index of the email to read.
    """
    if 0 <= index < len(inbox):
        email = inbox[index]
        print(f"\nFrom: {email.email_address}")
        print(f"Subject: {email.subject_line}")
        print(f"Content: {email.email_content}\n")
        if not email.has_been_read:
            email.mark_as_read()
            print(f"Email from {email.email_address} marked as read.\n")
    else:
        print("Invalid email index. Please select a valid index from the list.\n")


def main():
    """
    Main function to run the email application.
    Provides a simple menu for user interaction.
    """
    populate_inbox()
    while True:
        print("Menu:\n1. Read an email\n2. View unread emails\n3. Quit application")
        choice = input("Enter your choice (1-3): ").strip()
        if choice not in {"1", "2", "3"}:
            print("Invalid choice. Please enter 1, 2, or 3.\n")
            continue
        if choice == "1":
            if not inbox:
                print("Inbox is empty.\n")
                continue
            list_emails()
            idx_input = input("Enter the index of the email to read: ").strip()
            if not idx_input.isdigit():
                print("Invalid input. Please enter a valid number for the email index.\n")
                continue
            idx = int(idx_input)
            if idx < 0 or idx >= len(inbox):
                print("Invalid email index. Please select a valid index from the list.\n")
                continue
            read_email(idx)
        elif choice == "2":
            print("\nUnread Emails:")
            unread_found = False
            for idx, email in enumerate(inbox):
                if not email.has_been_read:
                    print(f"{idx}: {email.subject_line}")
                    unread_found = True
            if not unread_found:
                print("No unread emails.\n")
            else:
                print()
        elif choice == "3":
            print("Goodbye!")
            break
if __name__ == "__main__":
    main()