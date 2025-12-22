from django import forms
from .models import Review
from .models import Track

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "rhyme_imagery", "structure_rhythm", "style_execution",
            "individuality", "atmosphere_vibe", "trend_relevance", "title", "text",
        )
        labels = {
            "rhyme_imagery":    "Rymy / Obrazy",
            "structure_rhythm": "Struktura / Rytmika",
            "style_execution":  "Styl / Realizacja",
            "individuality":    "Indywidualność / Charyzma",
            "atmosphere_vibe":  "Atmosfera / Wajb",
            "trend_relevance":  "Trend / Aktualność",
            "title":            "Tytuł recenzji",
            "text":             "Treść (opcjonalnie)",
        }
        widgets = {
            "rhyme_imagery":    forms.NumberInput(attrs={"type":"range","min":0,"max":10,"step":1,"class":"form-range rating-slider","data-target":"ri"}),
            "structure_rhythm": forms.NumberInput(attrs={"type":"range","min":0,"max":10,"step":1,"class":"form-range rating-slider","data-target":"sr"}),
            "style_execution":  forms.NumberInput(attrs={"type":"range","min":0,"max":10,"step":1,"class":"form-range rating-slider","data-target":"se"}),
            "individuality":    forms.NumberInput(attrs={"type":"range","min":0,"max":10,"step":1,"class":"form-range rating-slider","data-target":"ind"}),
            "atmosphere_vibe":  forms.NumberInput(attrs={"type":"range","min":0,"max":10,"step":1,"class":"form-range rating-slider","data-target":"av"}),
            "trend_relevance":  forms.NumberInput(attrs={"type":"range","min":0,"max":10,"step":1,"class":"form-range rating-slider","data-target":"tr"}),
            "title": forms.TextInput(attrs={"class": "form-control form-control-lg insony-title-input", "placeholder": "Tytuł recenzji", "maxlength": "120", "autocomplete": "off"}),
            "text": forms.Textarea(attrs={"class": "form-control insony-textarea", "rows": 7, "placeholder": "Podziel się wrażeniami…", "maxlength": "8500"}),
        }

class TrackEditForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ["title", "artist", "genre", "authored_date", "duration", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Tytuł utworu"
            }),
            "artist": forms.Select(attrs={"class": "form-select"}),
            "genre": forms.Select(attrs={"class": "form-select"}), 
            "authored_date": forms.DateInput(attrs={
                "type": "date", "class": "form-control"
            }),
            "duration": forms.TimeInput(attrs={
                "type": "time", "class": "form-control", "step": 1  
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 3, "placeholder": "Opis (opcjonalnie)"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "genre" in self.fields:
            self.fields["genre"].required = False