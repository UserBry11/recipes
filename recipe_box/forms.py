from django import forms
from recipe_box.models import Author


class AddRecipe(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthor(forms.ModelForm):
    # Instead of defining everything at toplevel
    # We can use to have django do it all for us
    # So we just define one thing with class
    class Meta:
        model = Author  # Base of Author
        fields = ['name', 'bio']
