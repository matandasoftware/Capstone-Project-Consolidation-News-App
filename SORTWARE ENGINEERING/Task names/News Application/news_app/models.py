from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Supports three roles: READER, EDITOR, JOURNALIST.
    Each role has specific fields and permissions.
    """
    ROLE_CHOICES = [
        ('READER', 'Reader'),
        ('EDITOR', 'Editor'),
        ('JOURNALIST', 'Journalist'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='READER',
        help_text='User role determines permissions and available fields'
    )
    
    # Fields for READER role only
    subscribed_publishers = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='subscribers',
        help_text='Publishers this reader is subscribed to'
    )
    
    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        limit_choices_to={'role': 'JOURNALIST'},
        related_name='journalist_subscribers',
        help_text='Journalists this reader is subscribed to'
    )
    
    def save(self, *args, **kwargs):
        """
        Override save to assign user to appropriate group based on role.
        Also ensures role-specific fields are cleared for other roles.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Assign user to appropriate group based on role
        if is_new or 'role' in kwargs.get('update_fields', []):
            self._assign_to_group()
    
    def _assign_to_group(self):
        """
        Assign user to the appropriate Django group based on their role.
        Removes user from all other role groups.
        """
        # Remove from all role groups first
        self.groups.clear()
        
        # Assign to appropriate group
        if self.role == 'READER':
            group, created = Group.objects.get_or_create(name='readers_group')
        elif self.role == 'EDITOR':
            group, created = Group.objects.get_or_create(name='editors_group')
        elif self.role == 'JOURNALIST':
            group, created = Group.objects.get_or_create(name='journalists_group')
        else:
            return
        
        self.groups.add(group)
    
    def clean(self):
        """
        Validate that READER-specific fields are only used for readers.
        """
        super().clean()
        
        # Only validate subscriptions if user already exists (has been saved to database)
        # New users don't have an ID yet, so can't access many-to-many relationships
        if self.pk and self.role != 'READER':
            if self.subscribed_publishers.exists() or self.subscribed_journalists.exists():
                raise ValidationError(
                    'Only users with READER role can have subscriptions.'
                )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']


class Publisher(models.Model):
    """
    Represents a news publishing organization.
    Publishers have editors and journalists who create content.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Publisher name (must be unique)'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Description of the publisher'
    )
    
    website = models.URLField(
        blank=True,
        help_text='Publisher website URL'
    )
    
    editors = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'role': 'EDITOR'},
        related_name='publisher_editors',
        blank=True,
        help_text='Editors associated with this publisher'
    )
    
    journalists = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'role': 'JOURNALIST'},
        related_name='publisher_journalists',
        blank=True,
        help_text='Journalists associated with this publisher'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'
        ordering = ['name']


class Article(models.Model):
    """
    Represents a news article.
    Articles can be independent or linked to a publisher.
    Requires editor approval before being visible to readers.
    """
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
    
    content = models.TextField(
        help_text='Full article content'
    )
    
    summary = models.TextField(
        max_length=1500,
        help_text='Brief summary of the article'
    )
    
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'JOURNALIST'},
        related_name='articles',
        help_text='Journalist who wrote this article'
    )
    
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        help_text='Publisher (leave blank for independent articles)'
    )
    
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Publication date/time'
    )
    
    def save(self, *args, **kwargs):
        """
        Auto-generate slug from title if not provided.
        Set is_independent flag based on publisher.
        """
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Set is_independent flag
        self.is_independent = self.publisher is None
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        approval_status = "✓ Approved" if self.is_approved else "⏳ Pending"
        return f"{self.title} - {approval_status}"
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']
        permissions = [
            ('approve_article', 'Can approve articles for publication'),
        ]


class Newsletter(models.Model):
    """
    Represents a newsletter publication.
    Can be independent or linked to a publisher.
    """
    title = models.CharField(
        max_length=300,
        help_text='Newsletter title'
    )
    
    slug = models.SlugField(
        max_length=350,
        unique=True,
        blank=True,
        help_text='URL-friendly version of title'
    )
    
    content = models.TextField(
        help_text='Newsletter content'
    )
    
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'JOURNALIST'},
        related_name='newsletters',
        help_text='Journalist who created this newsletter'
    )
    
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newsletters',
        help_text='Publisher (leave blank for independent newsletters)'
    )
    
    is_independent = models.BooleanField(
        default=False,
        help_text='True if newsletter is not associated with a publisher'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Publication date/time'
    )
    
    def save(self, *args, **kwargs):
        """
        Auto-generate slug from title if not provided.
        Set is_independent flag based on publisher.
        """
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Newsletter.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Set is_independent flag
        self.is_independent = self.publisher is None
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
        ordering = ['-created_at']
