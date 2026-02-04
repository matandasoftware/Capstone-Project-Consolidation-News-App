from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news_app.models import Article, Newsletter, Publisher


class Command(BaseCommand):
    '''
    Custom management command to create user groups and assign permissions.
    Run with: python manage.py setup_groups
    
    Creates three groups with appropriate permissions:
    - readers_group: Can view articles and newsletters
    - editors_group: Can view, update, delete, and approve articles/newsletters
    - journalists_group: Can create, view, update, delete articles/newsletters
    '''
    help = 'Create user groups and assign permissions based on roles'
    
    def handle(self, *args, **kwargs):
        '''
        Main command handler.
        Creates groups and assigns permissions for each role.
        '''
        # Create Readers Group
        readers_group, created = Group.objects.get_or_create(name='readers_group')
        if created:
            self.stdout.write(self.style.SUCCESS('Created readers_group'))
        else:
            self.stdout.write('readers_group already exists')
        
        # Clear existing permissions and assign new ones
        readers_group.permissions.clear()
        
        # Assign view permissions for Article
        article_ct = ContentType.objects.get_for_model(Article)
        view_article = Permission.objects.get(
            codename='view_article',
            content_type=article_ct
        )
        readers_group.permissions.add(view_article)
        
        # Assign view permissions for Newsletter
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)
        view_newsletter = Permission.objects.get(
            codename='view_newsletter',
            content_type=newsletter_ct
        )
        readers_group.permissions.add(view_newsletter)
        
        self.stdout.write(self.style.SUCCESS(
            'Assigned permissions to readers_group: view_article, view_newsletter'
        ))
        
        # Create Editors Group
        editors_group, created = Group.objects.get_or_create(name='editors_group')
        if created:
            self.stdout.write(self.style.SUCCESS('Created editors_group'))
        else:
            self.stdout.write('editors_group already exists')
        
        # Clear existing permissions and assign new ones
        editors_group.permissions.clear()
        
        # Assign permissions for Article (view, change, delete, approve)
        article_ct = ContentType.objects.get_for_model(Article)
        view_article = Permission.objects.get(codename='view_article', content_type=article_ct)
        change_article = Permission.objects.get(codename='change_article', content_type=article_ct)
        delete_article = Permission.objects.get(codename='delete_article', content_type=article_ct)
        approve_article = Permission.objects.get(codename='approve_article', content_type=article_ct)
        
        editors_group.permissions.add(view_article, change_article, delete_article, approve_article)
        
        # Assign permissions for Newsletter (view, change, delete)
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)
        view_newsletter = Permission.objects.get(codename='view_newsletter', content_type=newsletter_ct)
        change_newsletter = Permission.objects.get(codename='change_newsletter', content_type=newsletter_ct)
        delete_newsletter = Permission.objects.get(codename='delete_newsletter', content_type=newsletter_ct)
        
        editors_group.permissions.add(view_newsletter, change_newsletter, delete_newsletter)
        
        self.stdout.write(self.style.SUCCESS(
            'Assigned permissions to editors_group: view/change/delete articles and newsletters, approve articles'
        ))
        
        # Create Journalists Group
        journalists_group, created = Group.objects.get_or_create(name='journalists_group')
        if created:
            self.stdout.write(self.style.SUCCESS('Created journalists_group'))
        else:
            self.stdout.write('journalists_group already exists')
        
        # Clear existing permissions and assign new ones
        journalists_group.permissions.clear()
        
        # Assign full CRUD permissions for Article (except approve)
        article_ct = ContentType.objects.get_for_model(Article)
        add_article = Permission.objects.get(codename='add_article', content_type=article_ct)
        view_article = Permission.objects.get(codename='view_article', content_type=article_ct)
        change_article = Permission.objects.get(codename='change_article', content_type=article_ct)
        delete_article = Permission.objects.get(codename='delete_article', content_type=article_ct)
        
        journalists_group.permissions.add(add_article, view_article, change_article, delete_article)
        
        # Assign full CRUD permissions for Newsletter
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)
        add_newsletter = Permission.objects.get(codename='add_newsletter', content_type=newsletter_ct)
        view_newsletter = Permission.objects.get(codename='view_newsletter', content_type=newsletter_ct)
        change_newsletter = Permission.objects.get(codename='change_newsletter', content_type=newsletter_ct)
        delete_newsletter = Permission.objects.get(codename='delete_newsletter', content_type=newsletter_ct)
        
        journalists_group.permissions.add(add_newsletter, view_newsletter, change_newsletter, delete_newsletter)
        
        # Assign permissions for Publisher (add)
        publisher_ct = ContentType.objects.get_for_model(Publisher)
        add_publisher = Permission.objects.get(codename='add_publisher', content_type=publisher_ct)
        journalists_group.permissions.add(add_publisher)
        
        self.stdout.write(self.style.SUCCESS(
            'Assigned permissions to journalists_group: full CRUD on articles and newsletters (except approval), add publishers'
        ))
        
        self.stdout.write(self.style.SUCCESS('\nAll groups created and permissions assigned successfully!'))
