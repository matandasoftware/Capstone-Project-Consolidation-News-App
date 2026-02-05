# EXPLANATION: news_app/models.py

## What This File Is
The models.py file defines the database structure for the news application. It contains Python classes that represent database tables and their relationships.

## Why This File Is Important
Models are the single, definitive source of truth about your data. They contain the essential fields and behaviors of the data you're storing. Django automatically creates database tables from these models, and provides an API to interact with the database without writing SQL.

## File Structure Overview
This file contains 4 main models:
1. CustomUser - Extended user model with roles and subscriptions
2. Publisher - News organizations
3. Article - News articles with approval workflow
4. Newsletter - Newsletter publications

---

## Detailed Code Breakdown

### Import Section
```python
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify
from django.core.exceptions import ValidationError
```

**What each import does:**
- `models` - Core Django models module, provides all field types and model base class
- `AbstractUser` - Django's built-in user model that we extend to add custom fields
- `Group, Permission` - Django's permission system for role-based access control
- `slugify` - Converts text to URL-friendly format (e.g., "My Article" becomes "my-article")
- `ValidationError` - Used to raise validation errors when data is invalid

---

## Model 1: CustomUser

### Purpose
Extends Django's default user model to support three distinct roles (Reader, Editor, Journalist) with role-specific fields and automatic group assignment.

### Class Definition
```python
class CustomUser(AbstractUser):
```
**What this does:** Creates a new user model that inherits all standard Django user fields (username, email, password, etc.) and adds custom functionality.

### Role Choices
```python
ROLE_CHOICES = [
    ('READER', 'Reader'),
    ('EDITOR', 'Editor'),
    ('JOURNALIST', 'Journalist'),
]
```
**What this does:** Defines the three allowed user roles. The first value (e.g., 'READER') is stored in the database, the second (e.g., 'Reader') is shown in forms.

### Role Field
```python
role = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default='READER',
    help_text='User role determines permissions and available fields'
)
```
**What this does:**
- `CharField` - Stores text up to 20 characters
- `choices=ROLE_CHOICES` - Restricts input to only the three defined roles
- `default='READER'` - New users are readers by default
- `help_text` - Shows explanation in admin interface

### Subscription Fields (Reader Only)
```python
subscribed_publishers = models.ManyToManyField(
    'Publisher',
    blank=True,
    related_name='subscribers',
    help_text='Publishers this reader is subscribed to'
)
```
**What this does:**
- `ManyToManyField` - A reader can subscribe to many publishers, and a publisher can have many subscribers
- `'Publisher'` - References the Publisher model (defined later in this file)
- `blank=True` - Field is optional, not required
- `related_name='subscribers'` - Allows reverse access: publisher.subscribers.all() gets all subscribers

```python
subscribed_journalists = models.ManyToManyField(
    'self',
    blank=True,
    symmetrical=False,
    limit_choices_to={'role': 'JOURNALIST'},
    related_name='journalist_subscribers',
    help_text='Journalists this reader is subscribed to'
)
```
**What this does:**
- `'self'` - References the same model (CustomUser subscribing to other CustomUsers)
- `symmetrical=False` - If User A subscribes to User B, B doesn't automatically subscribe to A
- `limit_choices_to={'role': 'JOURNALIST'}` - Only journalists can be subscribed to
- `related_name='journalist_subscribers'` - Access subscribers via journalist.journalist_subscribers.all()

### Save Method Override
```python
def save(self, *args, **kwargs):
    is_new = self.pk is None
    super().save(*args, **kwargs)
    
    if is_new or 'role' in kwargs.get('update_fields', []):
        self._assign_to_group()
```
**What this does:**
- `is_new = self.pk is None` - Checks if this is a new user (no primary key yet)
- `super().save(*args, **kwargs)` - Calls the parent class save method to actually save to database
- `if is_new or 'role' in kwargs...` - Assigns to group if new user or role changed
- `self._assign_to_group()` - Calls our custom method to handle group assignment

### Group Assignment Method
```python
def _assign_to_group(self):
    self.groups.clear()
    
    if self.role == 'READER':
        group, created = Group.objects.get_or_create(name='readers_group')
    elif self.role == 'EDITOR':
        group, created = Group.objects.get_or_create(name='editors_group')
    elif self.role == 'JOURNALIST':
        group, created = Group.objects.get_or_create(name='journalists_group')
    else:
        return
    
    self.groups.add(group)
```
**What this does:**
- `self.groups.clear()` - Removes user from all current groups
- `Group.objects.get_or_create(name='...')` - Gets existing group or creates it if it doesn't exist
- `self.groups.add(group)` - Adds user to the appropriate group

**Why this matters:** Django's permission system uses groups. By assigning users to groups, we can control what they can do in the system.

### Validation Method
```python
def clean(self):
    super().clean()
    
    if self.role != 'READER':
        if self.subscribed_publishers.exists() or self.subscribed_journalists.exists():
            raise ValidationError(
                'Only users with READER role can have subscriptions.'
            )
```
**What this does:**
- `clean()` - Called before saving to validate data
- Checks if non-readers have subscriptions (which shouldn't happen)
- Raises error if rule is violated

### String Representation
```python
def __str__(self):
    return f"{self.username} ({self.get_role_display()})"
```
**What this does:** Returns human-readable string when user is printed (e.g., "john_doe (Reader)")
- `get_role_display()` - Django method that returns the display value from ROLE_CHOICES

### Meta Class
```python
class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'
    ordering = ['-date_joined']
```
**What this does:**
- `verbose_name` - How model appears in admin (singular)
- `verbose_name_plural` - How model appears in admin (plural)
- `ordering = ['-date_joined']` - Default sort: newest users first (minus sign means descending)

---

## Model 2: Publisher

### Purpose
Represents news publishing organizations that employ editors and journalists.

### Basic Fields
```python
name = models.CharField(
    max_length=200,
    unique=True,
    help_text='Publisher name (must be unique)'
)
```
**What this does:**
- `unique=True` - No two publishers can have the same name
- Stores text up to 200 characters

```python
description = models.TextField(
    blank=True,
    help_text='Description of the publisher'
)
```
**What this does:**
- `TextField` - Unlimited text length (for long descriptions)
- `blank=True` - Optional field

```python
website = models.URLField(
    blank=True,
    help_text='Publisher website URL'
)
```
**What this does:**
- `URLField` - Validates that input is a valid URL format
- Optional field

### Staff Relationships
```python
editors = models.ManyToManyField(
    CustomUser,
    limit_choices_to={'role': 'EDITOR'},
    related_name='publisher_editors',
    blank=True,
    help_text='Editors associated with this publisher'
)
```
**What this does:**
- Publishers can have multiple editors
- Only users with EDITOR role can be selected
- `related_name='publisher_editors'` - Access via user.publisher_editors.all()

```python
journalists = models.ManyToManyField(
    CustomUser,
    limit_choices_to={'role': 'JOURNALIST'},
    related_name='publisher_journalists',
    blank=True,
    help_text='Journalists associated with this publisher'
)
```
**What this does:**
- Publishers can have multiple journalists
- Only users with JOURNALIST role can be selected

### Timestamp Fields
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```
**What this does:**
- `auto_now_add=True` - Automatically set when record is created, never changes
- `auto_now=True` - Automatically updated every time record is saved

---

## Model 3: Article

### Purpose
Represents news articles with an approval workflow. Articles can be independent or associated with a publisher.

### Title and Slug
```python
title = models.CharField(
    max_length=300,
    help_text='Article title'
)

slug = models.SlugField(
    max_length=350,
    unique=True,
    blank=True,
    help_text='URL-friendly version of title'
)
```
**What this does:**
- `title` - Article headline
- `slug` - URL-safe version (e.g., "breaking-news-today" instead of "Breaking News Today!")
- `unique=True` - Each article must have unique slug
- `blank=True` - Auto-generated if not provided

### Content Fields
```python
content = models.TextField(
    help_text='Full article content'
)

summary = models.TextField(
    max_length=500,
    help_text='Brief summary of the article'
)
```
**What this does:**
- `content` - Main article text (unlimited length)
- `summary` - Short preview (max 500 characters)

### Author Relationship
```python
author = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE,
    limit_choices_to={'role': 'JOURNALIST'},
    related_name='articles',
    help_text='Journalist who wrote this article'
)
```
**What this does:**
- `ForeignKey` - Each article has ONE author (but a journalist can have many articles)
- `on_delete=models.CASCADE` - If journalist is deleted, their articles are also deleted
- `limit_choices_to` - Only journalists can be authors
- `related_name='articles'` - Access via journalist.articles.all()

### Publisher Relationship
```python
publisher = models.ForeignKey(
    Publisher,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='articles',
    help_text='Publisher (leave blank for independent articles)'
)
```
**What this does:**
- Optional relationship (independent journalists don't need publishers)
- `on_delete=models.SET_NULL` - If publisher is deleted, article's publisher field becomes NULL (article isn't deleted)
- `null=True, blank=True` - Field can be empty in database and forms

### Approval Fields
```python
is_approved = models.BooleanField(
    default=False,
    help_text='Whether article has been approved by an editor'
)

is_independent = models.BooleanField(
    default=False,
    help_text='True if article is not associated with a publisher'
)

approved_by = models.ForeignKey(
    CustomUser,
    on_delete=models.SET_NULL,
    limit_choices_to={'role': 'EDITOR'},
    null=True,
    blank=True,
    related_name='approved_articles',
    help_text='Editor who approved this article'
)

approved_at = models.DateTimeField(
    null=True,
    blank=True,
    help_text='When the article was approved'
)
```
**What this does:**
- `is_approved` - Boolean flag: False until editor approves
- `is_independent` - Auto-set based on whether publisher exists
- `approved_by` - Tracks which editor approved it
- `approved_at` - Timestamp of approval

### Timestamp Fields
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
published_at = models.DateTimeField(
    null=True,
    blank=True,
    help_text='Publication date/time'
)
```
**What this does:**
- `created_at` - When article was first created
- `updated_at` - Last edit time
- `published_at` - When article goes live (can be scheduled for future)

### Save Method Override
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
        original_slug = self.slug
        counter = 1
        while Article.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
    
    self.is_independent = self.publisher is None
    
    super().save(*args, **kwargs)
```
**What this does:**
1. **Slug Generation:**
   - If no slug provided, create one from title
   - Check if slug already exists
   - If exists, add number suffix (e.g., "my-article-1", "my-article-2")
   - Keep incrementing until unique slug found

2. **Independent Flag:**
   - Automatically set `is_independent` to True if no publisher

3. **Save to Database:**
   - Call parent save method to write to database

### String Representation
```python
def __str__(self):
    approval_status = "✓ Approved" if self.is_approved else "⏳ Pending"
    return f"{self.title} - {approval_status}"
```
**What this does:** Shows title with visual indicator of approval status

### Meta Class
```python
class Meta:
    verbose_name = 'Article'
    verbose_name_plural = 'Articles'
    ordering = ['-created_at']
    permissions = [
        ('approve_article', 'Can approve articles for publication'),
    ]
```
**What this does:**
- `ordering = ['-created_at']` - Newest articles first
- `permissions` - Adds custom permission "approve_article" (assigned to editors group)

---

## Model 4: Newsletter

### Purpose
Represents newsletter publications. Simpler than articles (no approval workflow).

### Fields (Similar to Article)
```python
title = models.CharField(max_length=300, help_text='Newsletter title')
slug = models.SlugField(max_length=350, unique=True, blank=True, help_text='URL-friendly version of title')
content = models.TextField(help_text='Newsletter content')
author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'JOURNALIST'}, related_name='newsletters', help_text='Journalist who created this newsletter')
publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='newsletters', help_text='Publisher (leave blank for independent newsletters)')
is_independent = models.BooleanField(default=False, help_text='True if newsletter is not associated with a publisher')
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
published_at = models.DateTimeField(null=True, blank=True, help_text='Publication date/time')
```

**Key Differences from Article:**
- No `is_approved` field (newsletters don't need approval)
- No `approved_by` or `approved_at` fields
- No `summary` field (newsletters are self-contained)

### Save Method
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
        original_slug = self.slug
        counter = 1
        while Newsletter.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
    
    self.is_independent = self.publisher is None
    
    super().save(*args, **kwargs)
```
**What this does:** Same slug generation logic as Article model

---

## How Models Connect Together

### User → Article
- Journalist creates articles (author field)
- Editor approves articles (approved_by field)
- Reader subscribes to journalists to see their articles

### User → Publisher
- Reader subscribes to publishers
- Editors and journalists are associated with publishers

### Publisher → Article
- Articles can be published by a publisher (optional)
- If no publisher, article is independent

### Subscription System
- Reader.subscribed_publishers → Publisher.subscribers
- Reader.subscribed_journalists → Journalist.journalist_subscribers

---

## Database Schema Summary

**CustomUser Table:**
- id, username, email, password, role
- subscribed_publishers (ManyToMany via junction table)
- subscribed_journalists (ManyToMany via junction table)

**Publisher Table:**
- id, name, description, website
- editors (ManyToMany via junction table)
- journalists (ManyToMany via junction table)

**Article Table:**
- id, title, slug, content, summary
- author_id (ForeignKey to CustomUser)
- publisher_id (ForeignKey to Publisher, nullable)
- is_approved, is_independent
- approved_by_id (ForeignKey to CustomUser, nullable)
- approved_at, created_at, updated_at, published_at

**Newsletter Table:**
- id, title, slug, content
- author_id (ForeignKey to CustomUser)
- publisher_id (ForeignKey to Publisher, nullable)
- is_independent
- created_at, updated_at, published_at

---

## Key Takeaways

1. **CustomUser** extends Django's user system with roles and subscriptions
2. **Group Assignment** happens automatically when users are created/updated
3. **Publisher** connects editors and journalists to organizations
4. **Article** has approval workflow (editors approve journalist's work)
5. **Newsletter** is simpler (no approval needed)
6. **Slugs** are auto-generated for SEO-friendly URLs
7. **Timestamps** track creation and update times automatically
8. **Relationships** use ForeignKey (one-to-many) and ManyToManyField (many-to-many)
9. **Validation** ensures data integrity (e.g., only readers can subscribe)
10. **Custom Permission** "approve_article" will be assigned to editors group
