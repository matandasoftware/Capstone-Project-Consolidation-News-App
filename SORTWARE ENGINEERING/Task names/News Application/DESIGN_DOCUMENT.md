# NEWS APPLICATION - DESIGN DOCUMENT

## 1. PROJECT OVERVIEW
A Django-based news publishing platform where journalists publish articles, editors approve them, and readers subscribe to content. The system includes role-based access control, email notifications, social media integration, and a RESTful API.

---

## 2. FUNCTIONAL REQUIREMENTS

### FR1: User Management
- FR1.1: System shall support three user roles: Reader, Editor, Journalist
- FR1.2: Users shall be assigned to groups based on their role
- FR1.3: Each user role shall have specific permissions assigned to their group
- FR1.4: Custom user model shall contain role-specific fields
- FR1.5: Mutually exclusive role fields (Journalist fields = None for Readers, Reader fields = None for Journalists)

### FR2: Article Management
- FR2.1: Journalists shall create, view, update, and delete articles
- FR2.2: Articles shall have an approval status (approved/pending)
- FR2.3: Editors shall review and approve articles for publishing
- FR2.4: Editors shall view, update, and delete articles
- FR2.5: Readers shall only view approved articles

### FR3: Newsletter Management
- FR3.1: Journalists shall create, view, update, and delete newsletters
- FR3.2: Editors shall view, update, and delete newsletters
- FR3.3: Readers shall only view newsletters

### FR4: Publisher Management
- FR4.1: Publishers shall have multiple editors associated
- FR4.2: Publishers shall have multiple journalists associated
- FR4.3: Articles shall be linked to publishers through journalists/editors

### FR5: Subscription System
- FR5.1: Readers shall subscribe to publishers
- FR5.2: Readers shall subscribe to individual journalists
- FR5.3: Subscriptions shall determine content delivery

### FR6: Article Approval Workflow
- FR6.1: When article is approved, system shall send email to all subscribers
- FR6.2: Subscribers include users subscribed to the publisher
- FR6.3: Subscribers include users subscribed to the journalist
- FR6.4: When article is approved, system shall post to X (Twitter) account

### FR7: RESTful API
- FR7.1: API shall retrieve articles for subscribed publishers
- FR7.2: API shall retrieve articles for subscribed journalists
- FR7.3: API shall authenticate third-party clients
- FR7.4: API shall serialize data to JSON/XML formats
- FR7.5: API shall return only articles relevant to client's subscriptions

---

## 3. NON-FUNCTIONAL REQUIREMENTS

### NFR1: Code Quality
- NFR1.1: Code shall follow PEP 8 style guide
- NFR1.2: Code shall be well-commented and readable
- NFR1.3: Code shall use descriptive variable names
- NFR1.4: Code shall be modular with functions for specific tasks

### NFR2: Security
- NFR2.1: Access control shall be enforced for all views
- NFR2.2: User input shall be validated (defensive coding)
- NFR2.3: Exception handling shall be implemented throughout
- NFR2.4: Passwords shall be hashed and secure

### NFR3: Performance
- NFR3.1: Database queries shall be optimized
- NFR3.2: Code shall be written efficiently
- NFR3.3: API responses shall be fast

### NFR4: Testing
- NFR4.1: Automated unit tests shall be written for API
- NFR4.2: Tests shall verify correct article retrieval based on subscriptions
- NFR4.3: Tests shall use Django's testing framework

### NFR5: Maintainability
- NFR5.1: Database schema shall be normalized
- NFR5.2: Code shall be maintainable and extensible
- NFR5.3: Clear separation of concerns

---

## 4. DATABASE DESIGN (NORMALIZED)

### Table 1: CustomUser (extends AbstractUser)
**Purpose:** Store all user information with role-specific fields
**Fields:**
- id (PK, Auto)
- username (Unique, String, max_length=150)
- email (Unique, Email)
- password (Hashed, String)
- first_name (String, max_length=150)
- last_name (String, max_length=150)
- role (Choice Field: 'READER', 'EDITOR', 'JOURNALIST')
- is_active (Boolean, default=True)
- is_staff (Boolean, default=False)
- date_joined (DateTime, auto_now_add=True)
- subscribed_publishers (ManyToMany to Publisher, null=True, blank=True) [For READER only]
- subscribed_journalists (ManyToMany to CustomUser, null=True, blank=True) [For READER only]

**Normalization:** 3NF - No transitive dependencies, all non-key attributes depend on primary key

### Table 2: Publisher
**Purpose:** Represent publishing organizations
**Fields:**
- id (PK, Auto)
- name (String, max_length=200, unique=True)
- description (Text, blank=True)
- website (URL, blank=True)
- created_at (DateTime, auto_now_add=True)
- updated_at (DateTime, auto_now=True)

**Normalization:** 3NF - Simple entity with no complex dependencies

### Table 3: PublisherEditor
**Purpose:** Many-to-Many relationship between Publishers and Editors
**Fields:**
- id (PK, Auto)
- publisher_id (FK to Publisher)
- editor_id (FK to CustomUser, limited to role='EDITOR')
- assigned_date (DateTime, auto_now_add=True)

**Normalization:** Junction table for M:N relationship

### Table 4: PublisherJournalist
**Purpose:** Many-to-Many relationship between Publishers and Journalists
**Fields:**
- id (PK, Auto)
- publisher_id (FK to Publisher)
- journalist_id (FK to CustomUser, limited to role='JOURNALIST')
- assigned_date (DateTime, auto_now_add=True)

**Normalization:** Junction table for M:N relationship

### Table 5: Article
**Purpose:** Store news articles
**Fields:**
- id (PK, Auto)
- title (String, max_length=300)
- slug (SlugField, unique=True)
- content (Text)
- summary (Text, max_length=500)
- author (FK to CustomUser, limited to role='JOURNALIST')
- publisher (FK to Publisher, null=True, blank=True)
- is_approved (Boolean, default=False)
- is_independent (Boolean, default=False) [True if no publisher]
- approved_by (FK to CustomUser, limited to role='EDITOR', null=True, blank=True)
- approved_at (DateTime, null=True, blank=True)
- created_at (DateTime, auto_now_add=True)
- updated_at (DateTime, auto_now=True)
- published_at (DateTime, null=True, blank=True)

**Normalization:** 3NF - All fields depend on primary key, no redundancy

### Table 6: Newsletter
**Purpose:** Store newsletters
**Fields:**
- id (PK, Auto)
- title (String, max_length=300)
- slug (SlugField, unique=True)
- content (Text)
- author (FK to CustomUser, limited to role='JOURNALIST')
- publisher (FK to Publisher, null=True, blank=True)
- is_independent (Boolean, default=False)
- created_at (DateTime, auto_now_add=True)
- updated_at (DateTime, auto_now=True)
- published_at (DateTime, null=True, blank=True)

**Normalization:** 3NF - All fields depend on primary key, no redundancy

---

## 5. USER ROLES & PERMISSIONS

### Role: READER
**Django Group:** readers_group
**Permissions:**
- view_article
- view_newsletter
**Custom Fields:**
- subscribed_publishers (ManyToMany to Publisher)
- subscribed_journalists (ManyToMany to CustomUser)
**Capabilities:**
- View approved articles
- View newsletters
- Subscribe to publishers
- Subscribe to journalists
- Access personal dashboard

### Role: EDITOR
**Django Group:** editors_group
**Permissions:**
- view_article
- change_article (update)
- delete_article
- view_newsletter
- change_newsletter (update)
- delete_newsletter
- approve_article (custom permission)
**Custom Fields:** None specific
**Capabilities:**
- Review pending articles
- Approve articles for publication
- Update articles
- Delete articles
- View/Update/Delete newsletters
- Manage publisher content

### Role: JOURNALIST
**Django Group:** journalists_group
**Permissions:**
- add_article (create)
- view_article
- change_article (update)
- delete_article
- add_newsletter (create)
- view_newsletter
- change_newsletter (update)
- delete_newsletter
**Custom Fields:** None (articles and newsletters linked via ForeignKey)
**Capabilities:**
- Create articles (independent or for publisher)
- Update own articles
- Delete own articles
- Create newsletters
- Update own newsletters
- Delete own newsletters
- View all articles

---

## 6. APPLICATION WORKFLOW

### Workflow 1: Article Publication Process
1. Journalist creates article (status: is_approved=False)
2. Article saved to database with author and optional publisher
3. Editor views pending articles list
4. Editor reviews article content
5. Editor approves article (is_approved=True, approved_by=editor, approved_at=now)
6. System triggers post-approval actions:
   a. Collect all subscribers (publisher subscribers + journalist subscribers)
   b. Send email notification to all subscribers with article details
   c. Post article to X (Twitter) using API
7. Article now visible to all readers

### Workflow 2: Reader Subscription Flow
1. Reader browses publishers
2. Reader clicks "Subscribe to Publisher"
3. Publisher added to reader's subscribed_publishers
4. Reader browses journalists
5. Reader clicks "Subscribe to Journalist"
6. Journalist added to reader's subscribed_journalists
7. Reader receives notifications when subscribed entities publish approved articles

### Workflow 3: API Client Access
1. Third-party client authenticates (token/session)
2. Client requests articles via API endpoint
3. System identifies client's subscriptions
4. System filters articles:
   - Articles from subscribed publishers (is_approved=True)
   - Articles from subscribed journalists (is_approved=True)
5. System serializes articles to JSON/XML
6. System returns filtered articles to client

---

## 7. ACCESS CONTROL MATRIX

| User Role  | Create Article | View Article | Update Article | Delete Article | Approve Article | View Newsletter | Update Newsletter | Delete Newsletter | Subscribe | Access API |
|------------|----------------|--------------|----------------|----------------|-----------------|-----------------|-------------------|-------------------|-----------|-----------|
| Reader     | ❌             | ✅ (Approved)| ❌             | ❌             | ❌              | ✅              | ❌                | ❌                | ✅        | ✅        |
| Editor     | ❌             | ✅ (All)     | ✅             | ✅             | ✅              | ✅              | ✅                | ✅                | ❌        | ✅        |
| Journalist | ✅             | ✅ (All)     | ✅ (Own)       | ✅ (Own)       | ❌              | ✅              | ✅ (Own)          | ✅ (Own)          | ❌        | ✅        |

---

## 8. UI/UX PLANNING

### Page 1: Homepage (/)
**Accessible to:** All users (including anonymous)
**Purpose:** Landing page with featured articles
**Elements:**
- Navigation bar (Login/Register buttons if not authenticated)
- Featured approved articles (card layout)
- Search bar for articles
- Filter by publisher/journalist
- Footer with links

### Page 2: Login Page (/login)
**Accessible to:** Anonymous users
**Purpose:** User authentication
**Elements:**
- Username/Email field
- Password field
- "Remember Me" checkbox
- Login button
- Link to registration page
- Error messages display

### Page 3: Registration Page (/register)
**Accessible to:** Anonymous users
**Purpose:** New user registration
**Elements:**
- Username field
- Email field
- Password field
- Confirm password field
- Role selection (Reader/Journalist - Editors assigned by admin)
- Register button
- Link to login page
- Validation error messages

### Page 4: Reader Dashboard (/reader/dashboard)
**Accessible to:** Authenticated READER role
**Purpose:** Personalized content feed
**Elements:**
- Navigation bar (Logout button)
- "My Subscriptions" section (publishers and journalists)
- "Latest Articles" from subscribed sources
- "Browse Publishers" button
- "Browse Journalists" button
- Search functionality

### Page 5: Browse Publishers (/publishers)
**Accessible to:** Authenticated READER role
**Purpose:** Discover and subscribe to publishers
**Elements:**
- List/Grid of all publishers
- Publisher name, description, article count
- "Subscribe" button (toggles to "Unsubscribe")
- Search/Filter functionality

### Page 6: Browse Journalists (/journalists)
**Accessible to:** Authenticated READER role
**Purpose:** Discover and subscribe to journalists
**Elements:**
- List/Grid of all journalists
- Journalist name, bio, article count
- "Subscribe" button (toggles to "Unsubscribe")
- Search/Filter functionality

### Page 7: Article Detail (/article/<slug>)
**Accessible to:** All authenticated users
**Purpose:** View full article content
**Elements:**
- Article title
- Author name and publisher (if applicable)
- Publication date
- Article content (formatted)
- Related articles section
- Share buttons

### Page 8: Journalist Dashboard (/journalist/dashboard)
**Accessible to:** Authenticated JOURNALIST role
**Purpose:** Manage articles and newsletters
**Elements:**
- Navigation bar (Logout button)
- "My Articles" section (tabs: All, Pending Approval, Approved)
- "Create New Article" button
- "My Newsletters" section
- "Create New Newsletter" button
- Article/Newsletter management (Edit/Delete buttons)

### Page 9: Create/Edit Article (/journalist/article/create or /journalist/article/<id>/edit)
**Accessible to:** Authenticated JOURNALIST role
**Purpose:** Create or edit article
**Elements:**
- Title field (with character counter)
- Slug field (auto-generated from title, editable)
- Summary textarea
- Content editor (rich text editor)
- Publisher dropdown (optional - for independent articles)
- "Is Independent" checkbox
- Save as Draft button
- Submit for Approval button
- Cancel button
- Validation messages

### Page 10: Editor Dashboard (/editor/dashboard)
**Accessible to:** Authenticated EDITOR role
**Purpose:** Review and approve articles
**Elements:**
- Navigation bar (Logout button)
- "Pending Articles" section (count badge)
- List of pending articles with:
  * Title
  * Author name
  * Publisher
  * Submission date
  * "Review" button
- "All Articles" section
- Search/Filter functionality

### Page 11: Article Review (/editor/article/<id>/review)
**Accessible to:** Authenticated EDITOR role
**Purpose:** Review and approve/reject article
**Elements:**
- Article preview (full display)
- Author information
- Publisher information
- Submission date
- "Approve" button (green, prominent)
- "Edit" button
- "Delete" button (with confirmation)
- "Back to Dashboard" button
- Approval confirmation modal

---

## 9. API ENDPOINTS DESIGN

### Base URL: /api/v1/

### Endpoint 1: GET /api/v1/articles/
**Purpose:** Retrieve all approved articles for authenticated client based on subscriptions
**Authentication:** Required (Token or Session)
**Method:** GET
**Query Parameters:**
- format (optional): json or xml (default: json)
- page (optional): pagination
- page_size (optional): items per page
**Response:**
- Status 200: List of articles (JSON/XML)
- Status 401: Unauthorized
**Filters Applied:**
- Only approved articles (is_approved=True)
- Only from subscribed publishers OR subscribed journalists

### Endpoint 2: GET /api/v1/articles/<id>/
**Purpose:** Retrieve single article details
**Authentication:** Required
**Method:** GET
**Response:**
- Status 200: Article details
- Status 404: Article not found
- Status 403: Not subscribed to publisher/journalist

### Endpoint 3: GET /api/v1/publishers/
**Purpose:** Retrieve list of publishers
**Authentication:** Required
**Method:** GET
**Response:**
- Status 200: List of publishers

### Endpoint 4: GET /api/v1/journalists/
**Purpose:** Retrieve list of journalists
**Authentication:** Required
**Method:** GET
**Response:**
- Status 200: List of journalists

### Endpoint 5: POST /api/v1/subscribe/publisher/<id>/
**Purpose:** Subscribe to a publisher
**Authentication:** Required (READER role)
**Method:** POST
**Response:**
- Status 200: Subscription successful
- Status 400: Already subscribed

### Endpoint 6: POST /api/v1/subscribe/journalist/<id>/
**Purpose:** Subscribe to a journalist
**Authentication:** Required (READER role)
**Method:** POST
**Response:**
- Status 200: Subscription successful
- Status 400: Already subscribed

---

## 10. EMAIL NOTIFICATION DESIGN

### Trigger: Article Approval
**Sender:** noreply@newsapp.com
**Recipients:** All users subscribed to article's publisher OR article's journalist author
**Subject:** New Article Published: {article_title}
**Body Template:**
```
Hello {reader_name},

A new article has been published by {journalist_name} {from_publisher}.

Title: {article_title}
Summary: {article_summary}

Read the full article here: {article_url}

---
You received this email because you are subscribed to {publisher_or_journalist_name}.
To unsubscribe, visit: {unsubscribe_url}
```

---

## 11. X (TWITTER) INTEGRATION DESIGN

### Trigger: Article Approval
**Method:** POST request to X API using Python requests module
**API Endpoint:** https://api.twitter.com/2/tweets
**Authentication:** Bearer Token (OAuth 2.0)
**Post Content:**
```
📰 New Article Published!

{article_title}

{article_summary}

Read more: {article_url}

#{publisher_hashtag} #News
```
**Error Handling:** Log errors but don't block article approval if posting fails

---

## 12. SIGNAL IMPLEMENTATION DESIGN (OPTION 1)

### Signal: post_save on Article model
**When:** Article.is_approved changes from False to True
**Actions:**
1. Collect all subscribers:
   - Get all readers subscribed to article.publisher
   - Get all readers subscribed to article.author
   - Combine and deduplicate
2. Send email to each subscriber (async task recommended)
3. Post to X API using requests module
4. Log success/failure

**Implementation File:** signals.py in app directory
**Registration:** apps.py ready() method

---

## 13. TECHNOLOGY STACK

### Backend:
- Django 4.x or 5.x
- Django REST Framework (for API)
- Python 3.10+

### Database:
- SQLite (development)
- PostgreSQL (production - recommended)

### Authentication:
- Django built-in authentication
- Django REST Framework Token Authentication (for API)

### Email:
- Django email backend
- SMTP configuration

### External APIs:
- X (Twitter) API v2
- Python requests module

### Testing:
- Django TestCase
- Django REST Framework APITestCase

---

## 14. PROJECT STRUCTURE

```
ACADEMICS/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── DESIGN_DOCUMENT.md
├── news_project/              # Main project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── news_app/                  # Main application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── signals.py
    ├── permissions.py
    ├── urls.py
    ├── forms.py
    ├── tests.py
    ├── migrations/
    │   └── __init__.py
    ├── templates/
    │   └── news_app/
    │       ├── base.html
    │       ├── home.html
    │       ├── login.html
    │       ├── register.html
    │       ├── reader_dashboard.html
    │       ├── journalist_dashboard.html
    │       ├── editor_dashboard.html
    │       ├── article_detail.html
    │       ├── article_form.html
    │       ├── article_review.html
    │       ├── publishers_list.html
    │       └── journalists_list.html
    └── static/
        └── news_app/
            ├── css/
            │   └── styles.css
            └── js/
                └── scripts.js
```

---

## 15. SECURITY CONSIDERATIONS

### Authentication & Authorization:
- All views protected with login_required decorator
- Permission checks using @permission_required decorator
- Role-based access control using Django groups
- Custom permission checks in views

### Input Validation:
- Django forms for all user input
- CSRF protection on all forms
- XSS prevention through template escaping
- SQL injection prevention through ORM

### Data Protection:
- Password hashing (Django default PBKDF2)
- Email verification recommended
- Secure session management
- HTTPS enforcement in production

---

## 16. TESTING STRATEGY

### Unit Tests (API):
1. Test article retrieval for reader with publisher subscription
2. Test article retrieval for reader with journalist subscription
3. Test article retrieval with no subscriptions (empty result)
4. Test article retrieval for unauthenticated user (401)
5. Test article filtering (only approved articles returned)
6. Test serializer output format
7. Test pagination
8. Test XML format response

### Integration Tests:
1. Test full article approval workflow
2. Test email sending on approval
3. Test subscription flow

---

## 17. IMPLEMENTATION PHASES

### Phase 1: Setup & Models
- Create Django project and app
- Create custom user model
- Create Publisher, Article, Newsletter models
- Setup admin interface
- Run migrations

### Phase 2: Authentication & Groups
- Create user groups (readers_group, editors_group, journalists_group)
- Assign permissions to groups
- Create registration and login views
- Create role-based dashboards

### Phase 3: Article Management
- Create journalist article CRUD views
- Create article list/detail views
- Implement access control

### Phase 4: Editor Approval System
- Create editor dashboard
- Create article review view
- Implement approval logic
- Add email notification
- Add X posting

### Phase 5: Subscription System
- Create publisher/journalist browse views
- Implement subscription functionality
- Update reader dashboard with subscribed content

### Phase 6: RESTful API
- Install Django REST Framework
- Create serializers
- Create API views
- Configure API URLs
- Implement authentication

### Phase 7: Testing
- Write automated tests for API
- Test subscription-based filtering
- Test permissions

### Phase 8: Refinement
- Code review (PEP 8)
- Add comments
- Optimize queries
- Error handling
- Final testing

---

END OF DESIGN DOCUMENT
