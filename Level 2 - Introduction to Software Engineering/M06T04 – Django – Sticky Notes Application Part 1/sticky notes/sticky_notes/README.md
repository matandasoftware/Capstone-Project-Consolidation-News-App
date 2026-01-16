# Sticky Notes Django Application

A simple Django application for creating, viewing, editing, and deleting sticky notes.

## Features

- Create new sticky notes with title and content
- View all sticky notes in a list
- View individual note details
- Edit existing notes
- Delete notes with confirmation

## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
   ```bash
   cd "Level 2 - Introduction to Software Engineering/M06T04 – Django – Sticky Notes Application Part 1/sticky notes/sticky_notes"
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations (if not already applied):
   ```bash
   python manage.py migrate
   ```

### Running the Application

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000/
   ```

3. You should see the Sticky Notes homepage where you can:
   - View all your notes
   - Create new notes by clicking "Create New Note"
   - Click on any note title to view its details
   - Edit or delete notes from the detail page

## Project Structure

- `manage.py` - Django management script
- `sticky_notes/` - Main project configuration
  - `settings.py` - Project settings
  - `urls.py` - URL routing configuration
- `notes/` - Notes application
  - `models.py` - StickyNote model definition
  - `views.py` - View functions for CRUD operations
  - `urls.py` - URL patterns for notes app
  - `forms.py` - Form for creating/editing notes
  - `templates/notes/` - HTML templates
  - `static/notes/` - Static files (CSS, JS)

## Usage

### Creating a Note
1. Click "Create New Note" from the homepage
2. Enter a title and content
3. Click "Save"

### Viewing Notes
- All notes are listed on the homepage
- Click on a note title to view its full details

### Editing a Note
1. Open the note detail page
2. Click "Edit"
3. Modify the title or content
4. Click "Save"

### Deleting a Note
1. Open the note detail page
2. Click "Delete"
3. Confirm the deletion

## Development

To make changes to the application:
1. Modify the models in `notes/models.py`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update views in `notes/views.py`
4. Modify templates in `notes/templates/notes/`
