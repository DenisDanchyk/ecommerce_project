from django import forms


class SearchForm(forms.Form):
    search_field = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Пошук...', 'maxlength': 30}))
