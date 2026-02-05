# QUICK COMMANDS REFERENCE

## Commands to Run Now (In Order)

### 1. Make Migrations
```powershell
python manage.py makemigrations
```
**What it does:** Creates migration files for your models

### 2. Apply Migrations
```powershell
python manage.py migrate
```
**What it does:** Creates database tables from migration files

### 3. Setup Groups
```powershell
python manage.py setup_groups
```
**What it does:** Creates readers_group, editors_group, journalists_group with permissions

### 4. Create Superuser
```powershell
python manage.py createsuperuser
```
**What it does:** Creates admin account for accessing /admin/

### 5. Run Server
```powershell
python manage.py runserver
```
**What it does:** Starts development server at http://127.0.0.1:8000

---

## Testing in Admin Interface

### Access Admin
1. Go to: http://127.0.0.1:8000/admin/
2. Login with superuser credentials

### Create Test Data

#### Create a Journalist:
1. Click "Users" → "Add User"
2. Fill in username and password
3. Click "Save and continue editing"
4. Set role to "Journalist"
5. Click "Save"

#### Create an Editor:
1. Same as above but set role to "Editor"

#### Create a Reader:
1. Same as above but set role to "Reader"

#### Create a Publisher:
1. Click "Publishers" → "Add Publisher"
2. Fill in name (e.g., "The Daily News")
3. Select editors and journalists from the boxes
4. Click "Save"

#### Create an Article:
1. Click "Articles" → "Add Article"
2. Fill in title, content, summary
3. Select journalist as author
4. Optionally select publisher
5. Leave "is_approved" unchecked
6. Click "Save"

### Test the Signal System

#### Setup:
1. Make sure reader is subscribed to journalist:
   - Edit the reader user
   - Scroll to "Role & Subscriptions"
   - Add journalist to "Subscribed journalists"
   - Save

#### Approve Article:
1. Go to article in admin
2. Check the "is_approved" checkbox
3. Save

#### Check Console:
You should see output like:
```
Email sent to reader@example.com for article: My Article Title
X API token not configured. Skipping X post.
```

---

## Common Django Commands

### Shell (Python console with Django loaded)
```powershell
python manage.py shell
```

### Check for Errors
```powershell
python manage.py check
```

### Show Migrations
```powershell
python manage.py showmigrations
```

### Create Test Data (in shell)
```python
from news_app.models import CustomUser, Publisher, Article

# Create journalist
journalist = CustomUser.objects.create_user(
    username='john_journalist',
    email='john@example.com',
    password='password123',
    role='JOURNALIST'
)

# Create publisher
publisher = Publisher.objects.create(
    name='Tech News Daily',
    description='Latest technology news'
)

# Add journalist to publisher
publisher.journalists.add(journalist)

# Create article
article = Article.objects.create(
    title='Breaking Tech News',
    content='This is the full article content...',
    summary='A brief summary of the article',
    author=journalist,
    publisher=publisher
)
```

---

## Troubleshooting

### Error: "django.db.migrations.exceptions.InconsistentMigrationHistory"
**Solution:**
```powershell
python manage.py migrate --run-syncdb
```

### Error: "ERRORS: news_app.CustomUser: (auth.E003)"
**Solution:** AUTH_USER_MODEL must be set before first migration
- Check settings.py has: `AUTH_USER_MODEL = 'news_app.CustomUser'`
- Delete db.sqlite3 and migrations folder
- Run makemigrations and migrate again

### Error: "Permission matching query does not exist"
**Solution:** Run migrations before setup_groups
```powershell
python manage.py migrate
python manage.py setup_groups
```

### Can't Login to Admin
**Solution:** Create superuser again
```powershell
python manage.py createsuperuser
```

---

## File Locations Quick Reference

### Models
`news_app/models.py`

### Admin
`news_app/admin.py`

### Signals
`news_app/signals.py`

### Settings
`news_project/settings.py`

### Management Command
`news_app/management/commands/setup_groups.py`

### Explanations
- `EXPLANATION_models.md`
- `EXPLANATION_admin.md`
- `EXPLANATION_signals.md`
- `EXPLANATION_setup_groups.md`

---

## Next Phase Commands (After Current Phase)

### Create Views (Next)
- Will create view functions for all pages

### Create Forms (Next)
- Will create Django forms for user input

### Create Templates (Next)
- Will create HTML templates for UI

### Create API (Later)
- Will create REST API with serializers

### Run Tests (Later)
```powershell
python manage.py test
```

---

## Ready?

Run the 5 commands above in order, then let me know:
1. ✅ Migrations completed
2. ✅ Groups setup completed
3. ✅ Superuser created
4. ✅ Can access admin at http://127.0.0.1:8000/admin/

Once confirmed, I'll create the views, forms, templates, and URLs!
