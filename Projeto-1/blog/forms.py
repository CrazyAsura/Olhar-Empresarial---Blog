from django import forms
from .models import Post, Comment, User, Phone

class BaseFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.EmailInput, forms.PasswordInput, forms.DateInput, forms.Select)):
                field.widget.attrs.update({
                    'class': 'form-control' if not isinstance(field.widget, forms.Select) else 'form-select',
                    'style': 'background-color: #f8f9fa; border: 1px solid #212529; color: #212529; border-radius: 0.25rem; transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out; padding: 0.375rem 0.75rem; font-size: 1rem; line-height: 1.5; color: #212529; background-color: #f8f9fa; background-clip: padding-box; border: 1px solid #ced4da; border-radius: 0.25rem; width: 100%;',
                })

class PostForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'subtitle', 'content', 'resume', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #f8f9fa; border: 1px solid #212529; color: #212529; border-radius: 0;'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #f8f9fa; border: 1px solid #212529; color: #212529; border-radius: 0;'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: #f8f9fa; border: 1px solid #212529; color: #212529; border-radius: 0; min-height: 200px;'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: #f8f9fa; border: 1px solid #212529; color: #212529; border-radius: 0; min-height: 100px;'}),
            'category': forms.Select(attrs={'class': 'form-select', 'style': 'background-color: #f8f9fa; border: 1px solid #212529; color: #212529; border-radius: 0;'}),
        }

class CommentForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, }),
        }

class UserForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'birth_date']
        widgets = {
            'password': forms.PasswordInput(),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PhoneForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['number', 'type', 'ddd']

class LoginForm(BaseFormMixin, forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}),)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),)