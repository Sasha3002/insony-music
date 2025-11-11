from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
        }),
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
        }),
    )
    accept_terms = forms.BooleanField(
        label="Akceptuję regulamin Insony",
        required=True,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
        })
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Єдиний стиль для інпутів
        text_inputs = ("username", "email", "password1", "password2")
        for name in text_inputs:
            field = self.fields[name]
            # існуючі attrs + клас
            attrs = field.widget.attrs
            attrs["class"] = (attrs.get("class", "") + " form-control").strip()

        # Плейсхолдери + зручності
        self.fields["username"].widget.attrs.update({
            "placeholder": "Twoja nazwa użytkownika",
            "autofocus": "autofocus",
            "autocomplete": "username",
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "name@example.com",
            "autocomplete": "email",
            "inputmode": "email",
        })
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Min. 8 znaków (litery i cyfry)",
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Powtórz hasło",
        })

        # Приховуємо підказки під полями
        self.fields["username"].help_text = ""
        # ці 2 поля оголошені у формі, тож help_text теж ховаємо напряму
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    # --- Валідації ---

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            raise ValidationError("Email jest wymagany.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Konto z takim adresem e-mail już istnieje.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Hasła nie są takie same.")

        if p1:
            try:
                password_validation.validate_password(
                    p1,
                    user=User(username=cleaned.get("username"), email=cleaned.get("email"))
                )
            except ValidationError as e:
                self.add_error("password1", e)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip()
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False  # Aktywacja przez email
        if commit:
            user.save()
        return user
