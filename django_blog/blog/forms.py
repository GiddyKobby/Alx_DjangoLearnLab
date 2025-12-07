from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post, Comment, Tag
from taggit.forms import TagWidget 

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')

class PostForm(forms.ModelForm):
    # users type tags as a comma-separated string
    tag_string = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas (e.g. django,python)',
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tag_string']  # author is set in the view
        widgets = {
            'tags': TagWidget(),
        }
    def __init__(self, *args, **kwargs):
        # if instance provided, populate tag_string with existing tags
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tag_string'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        # Save the Post instance first, then handle tags
        instance = super().save(commit=False)
        if commit:
            instance.save()
        # process tags
        tag_string = self.cleaned_data.get('tag_string', '')
        tag_names = [t.strip() for t in tag_string.split(',') if t.strip()]
        # create/get Tag objects
        new_tags = []
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name__iexact=False, defaults={'name': name})
            # ensure case-insensitive duplicates are handled
            # If you want case-insensitive uniqueness, normalize names (lowercase) instead.
            new_tags.append(tag_obj)
        # assign tags (needs saved instance)
        if commit:
            instance.tags.set(new_tags)
        else:
            # if not commit, stash the tags for caller to set later
            instance._pending_tags = new_tags
        return instance
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }