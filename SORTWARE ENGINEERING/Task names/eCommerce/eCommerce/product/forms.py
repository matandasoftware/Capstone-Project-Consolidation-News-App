from django import forms
from .models import Store, Product, Category, Review


class StoreForm(forms.ModelForm):
    """Form for creating and editing stores."""
    
    class Meta:
        model = Store
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Store Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Store Description'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'name': 'Store Name',
            'description': 'Description',
            'is_active': 'Active',
        }


class ProductForm(forms.ModelForm):
    """Form for creating and editing products."""
    
    class Meta:
        model = Product
        fields = ['name', 'store', 'category', 'description', 'price', 'stock', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Name'
            }),
            'store': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Product Description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
                'step': '1'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        """Filter stores to show only vendor's stores."""
        super().__init__(*args, **kwargs)
        if user:
            self.fields['store'].queryset = Store.objects.filter(vendor=user)
        
        # Ensure stock field accepts 0
        self.fields['stock'].required = True
        self.fields['stock'].min_value = 0
        
        # Add helpful text for category field
        if not Category.objects.exists():
            self.fields['category'].help_text = 'No categories available. Please create a category first.'
    
    def clean_store(self):
        """Validate store field."""
        store = self.cleaned_data.get('store')
        if not store:
            raise forms.ValidationError("Please select a store. If you don't have any stores, create one first.")
        return store
    
    def clean_category(self):
        """Validate category field."""
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Please select a category. If no categories exist, create one first.")
        return category
    
    def clean_stock(self):
        """Validate stock field - explicitly allow 0"""
        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise forms.ValidationError("Stock quantity is required.")
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories."""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category Description'
            }),
        }

class ReviewForm(forms.ModelForm):
    """Form for creating and editing reviews."""
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this product...'
            }),
        }
        labels = {
            'rating': 'Rating',
            'comment': 'Your Review',
        }