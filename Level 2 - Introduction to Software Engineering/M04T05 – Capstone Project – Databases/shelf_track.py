"""shelf_track.py - Bookstore Inventory Management System
A comprehensive bookstore database management system that allows clerks to:
- Add new books to the database
- Update book information (quantity, title, authorID)
- Delete books from the database
- Search for specific books
- View details of all books with author information
This program follows PEP 8 standards and implements proper error handling,
data validation, and modular design patterns.
"""
import sqlite3
from contextlib import contextmanager
from typing import Optional
# Database Configuration
DATABASE_NAME = 'ebookstore.db'
# DATABASE CONNECTION MANAGEMENT
@contextmanager
def get_database_connection():
    """Context manager for database connections.
    Ensures proper connection handling and automatic cleanup.
    Prevents database locks and resource leaks.
    Yields:
        sqlite3.Connection: Active database connection
    Raises:
        sqlite3.Error: If database connection fails
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        yield conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()
def initialize_database():
    """Initialize the database with required tables and populate with initial data.
    Creates:
        - author table with id (PK), name, country
        - book table with id (PK), title, authorID (FK), qty
    Populates tables with initial dataset if empty.
    """
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            # Create author table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS AUTHOR (
                    ID INTEGER PRIMARY KEY,
                    NAME TEXT NOT NULL,
                    COUNTRY TEXT NOT NULL
                )
            ''')
            # Create book table with foreign key constraint
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS BOOK (
                    ID INTEGER PRIMARY KEY,
                    TITLE TEXT NOT NULL,
                    AUTHORID INTEGER NOT NULL,
                    QTY INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (AUTHORID) REFERENCES AUTHOR(ID)
                )
            ''')
            # Check if tables are empty and populate with initial data
            cursor.execute('SELECT COUNT(*) FROM AUTHOR')
            if cursor.fetchone()[0] == 0:
                # Populate author table
                authors_data = [
                    (1290, 'Charles Dickens', 'England'),
                    (8937, 'J.K. Rowling', 'England'),
                    (2356, 'C.S. Lewis', 'Ireland'),
                    (6380, 'J.R.R. Tolkien', 'South Africa'),
                    (5620, 'Lewis Carroll', 'England')
                ]
                cursor.executemany(
                    'INSERT INTO AUTHOR (ID, NAME, COUNTRY) VALUES (?, ?, ?)',
                    authors_data
                )
            cursor.execute('SELECT COUNT(*) FROM BOOK')
            if cursor.fetchone()[0] == 0:
                # Populate book table
                books_data = [
                    (3001, 'A Tale of Two Cities', 1290, 30),
                    (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                    (1290, 'The Lion, the Witch and the Wardrobe', 2356, 25),
                    (8937, 'The Lord of the Rings', 6380, 37),
                    (3003, "Alice's Adventures in Wonderland", 5620, 12)
                ]
                cursor.executemany(
                    'INSERT INTO BOOK (ID, TITLE, AUTHORID, QTY) VALUES (?, ?, ?, ?)',
                    books_data
                )
            conn.commit()
            print("Database initialized successfully.\n")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise
# INPUT VALIDATION
def validate_integer_input(prompt: str, min_value: Optional[int] = None,
                          max_value: Optional[int] = None) -> int:
    """Validate and return integer input from user.
    Args:
        prompt: Message to display to user
        min_value: Minimum acceptable value (optional)
        max_value: Maximum acceptable value (optional)
    Returns:
        int: Validated integer input
    """
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
def validate_non_empty_string(prompt: str) -> str:
    """Validate and return non-empty string input from user.
    Args:
        prompt: Message to display to user
    Returns:
        str: Non-empty string input
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")
def validate_positive_integer(prompt: str) -> int:
    """Validate and return positive integer input.
    Args:
        prompt: Message to display to user
    Returns:
        int: Positive integer
    """
    return validate_integer_input(prompt, min_value=1)
def validate_four_digit_id(prompt: str) -> int:
    """Validate and return a four-digit integer ID.
    Args:
        prompt: Message to display to user
    Returns:
        int: Four-digit integer (1000-9999)
    """
    return validate_integer_input(prompt, min_value=1000, max_value=9999)
# AUTHOR OPERATIONS
def add_author():
    """Add a new author to the database.
    Prompts user for author ID, name, and country.
    Validates that author ID is exactly 4 digits.
    Uses parameterized queries to prevent SQL injection.
    """
    print("\n--- ADD NEW AUTHOR ---")
    try:
        author_id = validate_four_digit_id("Enter author ID (4 digits): ")
        name = validate_non_empty_string("Enter author name: ")
        country = validate_non_empty_string("Enter author country: ")
        with get_database_connection() as conn:
            cursor = conn.cursor()
            # Check if author ID already exists
            cursor.execute('SELECT ID FROM AUTHOR WHERE ID = ?', (author_id,))
            if cursor.fetchone():
                print(f"Error: Author with ID {author_id} already exists.")
                return
            # Insert new author
            cursor.execute('''
                INSERT INTO AUTHOR (ID, NAME, COUNTRY)
                VALUES (?, ?, ?)
            ''', (author_id, name, country))
            conn.commit()
            print(f"\nAuthor '{name}' added successfully!")
    except sqlite3.Error as e:
        print(f"Database error while adding author: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
# BOOK OPERATIONS
def add_book():
    """Add a new book to the database.
    Prompts user for book ID, title, author ID, and quantity.
    Validates author existence before insertion.
    Offers option to add new author if not found.
    Uses parameterized queries to prevent SQL injection.
    """
    print("\n--- ADD NEW BOOK ---")
    try:
        book_id = validate_four_digit_id("Enter book ID (4 digits): ")
        title = validate_non_empty_string("Enter book title: ")
        author_id = validate_four_digit_id("Enter author ID (4 digits): ")
        qty = validate_integer_input("Enter quantity: ", min_value=0)
        with get_database_connection() as conn:
            cursor = conn.cursor()
            
            # Check if book ID already exists first
            cursor.execute('SELECT ID FROM BOOK WHERE ID = ?', (book_id,))
            if cursor.fetchone():
                print(f"\nError: Book with ID {book_id} already exists.")
                print("Operation cancelled. Please use a different book ID.")
                return
            
            # Verify author exists
            cursor.execute('SELECT NAME, COUNTRY FROM AUTHOR WHERE ID = ?', (author_id,))
            author_data = cursor.fetchone()
            
            if author_data:
                # Author exists - show confirmation and continue
                author_name, author_country = author_data
                print(f"\nAuthor found: {author_name} ({author_country})")
                print(f"Proceeding to add book '{title}' by this author...")
            else:
                # New author detected - ask for confirmation before continuing
                print(f"\n⚠️  NEW AUTHOR DETECTED!")
                print(f"Author ID {author_id} does not exist in the database.")
                print(f"\nYou are attempting to add:")
                print(f"  Book: '{title}'")
                print(f"  Author ID: {author_id} (NEW)")
                
                response = input("\nDo you want to add this new author and continue? (yes/no): ").strip().lower()
                
                if response != 'yes':
                    print("\nOperation cancelled. Book not added.")
                    print("Tip: You can add the author first using Menu Option 6, then add the book.")
                    return
                
                # User confirmed - get author details
                print("\n--- NEW AUTHOR DETAILS ---")
                author_name = validate_non_empty_string("Enter author name: ")
                author_country = validate_non_empty_string("Enter author country: ")
                
                # Insert new author
                cursor.execute('''
                    INSERT INTO AUTHOR (ID, NAME, COUNTRY)
                    VALUES (?, ?, ?)
                ''', (author_id, author_name, author_country))
                print(f"✓ Author '{author_name}' added successfully!")
                print(f"✓ Now adding book '{title}'...")
            
            # Insert new book
            cursor.execute('''
                INSERT INTO BOOK (ID, TITLE, AUTHORID, QTY)
                VALUES (?, ?, ?, ?)
            ''', (book_id, title, author_id, qty))
            
            conn.commit()
            
            # Final success message
            print(f"\n{'='*50}")
            print(f"✓ SUCCESS! Book added to inventory:")
            print(f"  ID: {book_id}")
            print(f"  Title: {title}")
            print(f"  Author: {author_name} ({author_country})")
            print(f"  Quantity: {qty}")
            print(f"{'='*50}")
            
    except sqlite3.Error as e:
        print(f"\n✗ Database error while adding book: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
def update_book():
    """Update book information in the database.
    Allows updating quantity (default), title, or author information.
    Displays current book and author details before update.
    Uses INNER JOIN to show complete book information.
    """
    print("\n--- UPDATE BOOK ---")
    try:
        book_id = validate_four_digit_id("Enter book ID to update (4 digits): ")
        with get_database_connection() as conn:
            cursor = conn.cursor()
            # Retrieve current book and author information using INNER JOIN
            cursor.execute('''
                SELECT B.ID, B.TITLE, B.AUTHORID, B.QTY, A.NAME, A.COUNTRY
                FROM BOOK B
                INNER JOIN AUTHOR A ON B.AUTHORID = A.ID
                WHERE B.ID = ?
            ''', (book_id,))
            book_data = cursor.fetchone()
            if not book_data:
                print(f"Error: Book with ID {book_id} not found.")
                return
            # Display current book information
            book_id, title, author_id, qty, author_name, author_country = book_data
            print("\nCurrent Book Information:")
            print("-" * 50)
            print(f"ID: {book_id}")
            print(f"Title: {title}")
            print(f"Author ID: {author_id}")
            print(f"Author Name: {author_name}")
            print(f"Author Country: {author_country}")
            print(f"Quantity: {qty}")
            print("-" * 50)
            # Update menu
            print("\nWhat would you like to update?")
            print("1. Quantity (default)")
            print("2. Title")
            print("3. Author ID")
            print("4. Author Name and Country")
            choice = validate_integer_input("Enter choice (1-4): ", min_value=1, max_value=4)
            if choice == 1:
                new_qty = validate_integer_input("Enter new quantity: ", min_value=0)
                cursor.execute('UPDATE BOOK SET QTY = ? WHERE ID = ?', (new_qty, book_id))
                print(f"\nQuantity updated to {new_qty}.")
            elif choice == 2:
                new_title = validate_non_empty_string("Enter new title: ")
                cursor.execute('UPDATE BOOK SET TITLE = ? WHERE ID = ?', (new_title, book_id))
                print(f"\nTitle updated to '{new_title}'.")
            elif choice == 3:
                new_author_id = validate_four_digit_id("Enter new author ID (4 digits): ")
                # Verify new author exists
                cursor.execute('SELECT ID FROM AUTHOR WHERE ID = ?', (new_author_id,))
                if not cursor.fetchone():
                    print(f"\nNew author detected (ID {new_author_id} not in database).")
                    print("Please provide author details:")
                    author_name = validate_non_empty_string("Enter author name: ")
                    author_country = validate_non_empty_string("Enter author country: ")
                    cursor.execute('''
                        INSERT INTO AUTHOR (ID, NAME, COUNTRY)
                        VALUES (?, ?, ?)
                    ''', (new_author_id, author_name, author_country))
                    print(f"\nAuthor '{author_name}' added successfully!")
                cursor.execute('UPDATE BOOK SET AUTHORID = ? WHERE ID = ?', (new_author_id, book_id))
                print(f"\nAuthor ID updated to {new_author_id}.")
            elif choice == 4:
                # Update author information
                new_name = validate_non_empty_string("Enter new author name: ")
                new_country = validate_non_empty_string("Enter new author country: ")
                cursor.execute('''
                    UPDATE AUTHOR SET NAME = ?, COUNTRY = ?
                    WHERE ID = ?
                ''', (new_name, new_country, author_id))
                print(f"\nAuthor information updated.")
                print(f"Name: {new_name}")
                print(f"Country: {new_country}")
            conn.commit()
            print("\nUpdate completed successfully!")
    except sqlite3.Error as e:
        print(f"Database error while updating book: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
def delete_book():
    """Delete a book from the database.
    Prompts for confirmation before deletion.
    Displays book information before deletion.
    """
    print("\n--- DELETE BOOK ---")
    try:
        book_id = validate_four_digit_id("Enter book ID to delete (4 digits): ")
        with get_database_connection() as conn:
            cursor = conn.cursor()
            # Check if book exists and display information
            cursor.execute('''
                SELECT B.TITLE, A.NAME
                FROM BOOK B
                INNER JOIN AUTHOR A ON B.AUTHORID = A.ID
                WHERE B.ID = ?
            ''', (book_id,))
            book_data = cursor.fetchone()
            if not book_data:
                print(f"Error: Book with ID {book_id} not found.")
                return
            title, author_name = book_data
            print(f"\nBook to delete:")
            print(f"ID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author_name}")
            # Confirm deletion
            confirm = input("\nAre you sure you want to delete this book? (yes/no): ").strip().lower()
            if confirm == 'yes':
                cursor.execute('DELETE FROM BOOK WHERE ID = ?', (book_id,))
                conn.commit()
                print(f"\nBook '{title}' deleted successfully!")
            else:
                print("\nDeletion cancelled.")
    except sqlite3.Error as e:
        print(f"Database error while deleting book: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
def search_books():
    """Search for books in the database.
    Supports searching by:
    - Book ID
    - Title (partial match)
    - Author name (partial match)
    Displays all matching results with author information.
    """
    print("\n--- SEARCH BOOKS ---")
    print("Search by:")
    print("1. Book ID")
    print("2. Title")
    print("3. Author Name")
    try:
        choice = validate_integer_input("Enter choice (1-3): ", min_value=1, max_value=3)
        with get_database_connection() as conn:
            cursor = conn.cursor()
            if choice == 1:
                book_id = validate_four_digit_id("Enter book ID (4 digits): ")
                cursor.execute('''
                    SELECT B.ID, B.TITLE, B.QTY, A.NAME, A.COUNTRY
                    FROM BOOK B
                    INNER JOIN AUTHOR A ON B.AUTHORID = A.ID
                    WHERE B.ID = ?
                ''', (book_id,))
            elif choice == 2:
                title_search = validate_non_empty_string("Enter title (or part of it): ")
                cursor.execute('''
                    SELECT B.ID, B.TITLE, B.QTY, A.NAME, A.COUNTRY
                    FROM BOOK B
                    INNER JOIN AUTHOR A ON B.AUTHORID = A.ID
                    WHERE B.TITLE LIKE ?
                ''', (f'%{title_search}%',))
            elif choice == 3:
                author_search = validate_non_empty_string("Enter author name (or part of it): ")
                cursor.execute('''
                    SELECT B.ID, B.TITLE, B.QTY, A.NAME, A.COUNTRY
                    FROM BOOK B
                    INNER JOIN AUTHOR A ON B.AUTHORID = A.ID
                    WHERE A.NAME LIKE ?
                ''', (f'%{author_search}%',))
            results = cursor.fetchall()
            if not results:
                print("\nNo books found matching your search criteria.")
                return
            print(f"\n{len(results)} book(s) found:")
            print("=" * 70)
            for book_id, title, qty, author_name, author_country in results:
                print(f"ID: {book_id}")
                print(f"Title: {title}")
                print(f"Author: {author_name} ({author_country})")
                print(f"Quantity: {qty}")
                print("-" * 70)
    except sqlite3.Error as e:
        print(f"Database error while searching: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
def view_all_books():
    """Display details of all books in the database.
    Uses INNER JOIN to retrieve book and author information.
    Displays results in a user-friendly format using zip() function.
    """
    print("\n--- VIEW ALL BOOKS ---")
    try:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT B.TITLE, A.NAME, A.COUNTRY
                FROM BOOK B
                INNER JOIN AUTHOR A ON B.AUTHORID = A.ID
                ORDER BY B.TITLE
            ''')
            results = cursor.fetchall()
            if not results:
                print("\nNo books found in the database.")
                return
            print(f"\nTotal books: {len(results)}\n")
            print("Details " + "-" * 63)
            # Use zip to iterate through results and display formatted output
            for title, author_name, author_country in results:
                print(f"Title: {title}")
                print(f"Author's Name: {author_name}")
                print(f"Author's Country: {author_country}")
                print("-" * 70)
    except sqlite3.Error as e:
        print(f"Database error while viewing books: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
# MENU SYSTEM
def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 40)
    print("   BOOKSTORE INVENTORY SYSTEM")
    print("=" * 40)
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. View details of all books")
    print("0. Exit")
    print("=" * 40)
def main():
    """Main program loop.
    Initializes database and presents menu options to user.
    Handles user input and directs to appropriate functions.
    Continues until user chooses to exit.
    """
    print("Welcome to Shelf Track - Bookstore Inventory Management System")
    print("=" * 70)
    try:
        # Initialize database on startup
        initialize_database()
        # Main program loop
        while True:
            display_menu()
            try:
                choice = validate_integer_input("Enter your choice: ", min_value=0, max_value=5)
                if choice == 1:
                    add_book()
                elif choice == 2:
                    update_book()
                elif choice == 3:
                    delete_book()
                elif choice == 4:
                    search_books()
                elif choice == 5:
                    view_all_books()
                elif choice == 0:
                    print("\nThank you for using Shelf Track!")
                    print("Goodbye!")
                    break
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                print("Goodbye!")
                break
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("Program will now exit.")
# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()
