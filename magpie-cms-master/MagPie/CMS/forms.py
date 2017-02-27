"""This module is created to built the forms"""
__author__ = 'Richa Sharma <richa@weboniselab.com>'

from django import forms


class ChangePasswordForm(forms.Form):
    """ The class is to create change password form"""

    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'old_password',
                'data-required': 'true',
                'data-describedby': 'old_password-description',
                'data-description': 'old_password',
                'placeholder': 'Old Password',
            }),
        required=True
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'new_password',
                'data-required': 'true',
                'data-describedby': 'new_password-description',
                'data-description': 'new_password',
                'placeholder': 'New Password',
                'data-pattern': '.{8,15}'
            }),
        max_length=15,
        min_length=8,
        required=True
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                'id': 'confirm_password',
                'class': 'form-control',
                'data-required': 'true',
                'data-describedby': 'confirm_password-description',
                'data-description': 'confirm_password',
                'placeholder': 'Confirm Password',
                'data-conditional': "confirm",
                'data-pattern': '.{8,15}'
            }),
        required=True
    )


class LoginForm(forms.Form):

    """ The class is to create login form"""
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'id': 'email',
                'data-required': 'true',
                'data-describedby': 'email-description',
                'data-description': 'email',
                'data-pattern': r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|'
                                r'(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'
                                r'(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            }),
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'id': 'password',
                'data-required': 'true',
                'data-describedby': 'password-description',
                'data-description': 'password',
            }),
        required=True
    )

TEXT_COLOR = (('#000000', 'Black'), ('#FFFFFF', 'White'))


class AddThemeForm(forms.Form):
    """ The class is to create add theme form"""
    theme_color = forms.CharField(
        label='Primary Color',
        widget=forms.HiddenInput(
            attrs={
                'id': 'themeColor',
                'data-required': 'true',
                'data-describedby': 'themeColor-description',
                'data-description': 'themeColor',
                'value': '#02a9d8'
            }),
        required=True
    )

    font_color = forms.ChoiceField(
        label='Text Color',
        widget=forms.RadioSelect(),
        choices=TEXT_COLOR,
        initial='#FFFFFF'
    )

    logo = forms.FileField(
        label="Upload Logo *",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'logo',
                'data-required': 'true',
                'data-describedby': 'logo-description',
                'data-description': 'logo',
                'data-conditional': "file_extn"
            }),
        required=True
    )
    splash_screen = forms.FileField(
        label="Upload Splash Screen *",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'splash_screen',
                'data-required': 'true',
                'data-describedby': 'splash_screen-description',
                'data-description': 'splash_screen',
                'data-conditional': "file_extn"
            }),
        required=True
    )
    fav_icon = forms.FileField(
        label="Upload Fav Icon",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'fav_icon',
                'data-describedby': 'fav_icon-description',
                'data-description': 'fav_icon',
                'data-conditional': "file_extn_ico"
            }),
        required=False
    )
    app_icon = forms.FileField(
        label="Upload App Logo *",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'app_icon',
                'data-required': 'true',
                'data-describedby': 'app_icon-description',
                'data-description': 'app_icon',
                'data-conditional': "file_extn"
            }),
        required=True
    )


class EditThemeForm(forms.Form):
    """ The class is to create edit theme form"""
    theme_color = forms.CharField(
        label='Primary Color',
        widget=forms.HiddenInput(
            attrs={
                'id': 'themeColor',
                'data-required': 'true',
                'data-describedby': 'themeColor-description',
                'data-description': 'themeColor',
                'value': '#02a9d8'
            }),
        required=True
    )

    font_color = forms.ChoiceField(
        label='Text Color',
        widget=forms.RadioSelect(),
        choices=TEXT_COLOR,
        initial='#FFFFFF'
    )

    logo = forms.FileField(
        label="Upload Logo *",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'logo',
                'data-required': 'true',
                'data-describedby': 'logo-description',
                'data-description': 'logo',
                'data-conditional': "file_extn"
            }),
        required=False
    )
    splash_screen = forms.FileField(
        label="Upload Splash Screen *",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'splash_screen',
                'data-required': 'true',
                'data-describedby': 'splash_screen-description',
                'data-description': 'splash_screen',
                'data-conditional': "file_extn"
            }),
        required=False
    )
    fav_icon = forms.FileField(
        label="Upload Fav Icon",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'fav_icon',
                'data-describedby': 'fav_icon-description',
                'data-description': 'fav_icon',
                'data-conditional': "file_extn_ico"
            }),
        required=False
    )
    app_icon = forms.FileField(
        label="Upload App Logo *",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control inpUpload',
                'id': 'app_icon',
                'data-required': 'true',
                'data-describedby': 'app_icon-description',
                'data-description': 'app_icon',
                'data-conditional': "file_extn"
            }),
        required=False
    )


ALLOWED_CLAIM_CHOICES = ((False, 'Self Assistance'), (True, 'Allows Reordering of Cards'))


class AddInstituteForm(forms.Form):
    """ The class is to create add institution form"""
    name_en = forms.CharField(
        label="Institution Name (In English)",
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'name_en',
                'placeholder': "Institution Name (In English)",
                'data-required': 'true',
                'data-describedby': 'name_en-description',
                'data-description': 'name_en',
                'data-pattern': r"^[a-zA-Z0-9\(\)'. -]+$"
            }
        ),
        required=True,
        error_messages={
            'required': 'Please enter institution name in English'
        }
    )
    name_es = forms.CharField(
        label="Institution Name (In Spanish)",
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'name_es',
                'placeholder': "Institution Name (In Spanish)",
            }
        ),
        required=False,
    )
    name_zh = forms.CharField(
        label="Institution Name (In Chinese)",
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'name_zh',
                'placeholder': "Institution Name (In Chinese)",
            }
        ),
        required=False,
    )
    allow_reorder_cards = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                'data-required': 'true',
                'data-describedby': 'allow_reorder_cards-description',
                'data-description': 'allow_reorder_cards',
            }
        ),
        choices=ALLOWED_CLAIM_CHOICES,
        initial=True,
        required=True,
        error_messages={
            'required': 'Please select at least one'
        }
    )
    contact_no = forms.CharField(
        label="Contact Number",
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'contact_no',
                'placeholder': "Contact Number",
                'data-describedby': 'contact_no-description',
                'data-description': 'contact_no',
                'data-required': 'true',
                'data-pattern': r"^[+]{0,1}[0-9\(\)\-\, \/]+$"
            }
        ),
        required=True,
        error_messages={
            'required': 'Please enter contact number',
            'max_length': 'Please enter valid contact number'
        }
    )
    email = forms.EmailField(
        label="Contact Email",
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
                'class': 'inpData',
                'placeholder': "Contact Email",
                'data-describedby': 'email-description',
                'data-description': 'email',
                'data-pattern': r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|'
                                r'(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'
                                r'(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            }
        ),
        required=False,
        error_messages={
            'required': 'Please enter contact email'
        }
    )
    postal_address = forms.CharField(
        label="Postal Address ",
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'inpData',
                'id': 'postal_address',
                'placeholder': 'Postal Address',
                'data-describedby': 'postal_address-description',
                'data-description': 'postal_address',
                }
        ),
        required=False,
        error_messages={
            'required':'Please enter postal address'
        }
    )
    instructional_text = forms.CharField(
        label="Instructional Text",
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'inpData',
                'id': 'instructional_text',
                'placeholder': 'Instructional Text',
                'data-describedby': 'instructional_text-description',
                'data-description': 'instructional_text',
                }
        ),
        required=False,
        error_messages={
            'required': 'Please enter instructional text'
        }
    )
    region = forms.CharField(
        label="Region / Country",
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'region',
                'placeholder': "Region / Country",
                'data-required': 'true',
                'data-describedby': 'region-description',
                'data-description': 'region',
                'data-pattern': r"^[a-zA-Z\(\) .]+$"
            }
        ),
        required=True,
        error_messages={
            'required': 'Please enter region / country'
        }
    )

    def clean(self):
        cleaned_data = super(AddInstituteForm, self).clean()
        allow_reorder_cards = cleaned_data.get("allow_reorder_cards")

        if allow_reorder_cards == 'False':
            cleaned_data['allow_reorder_cards'] = ''

        # Always return the full collection of cleaned data.
        return cleaned_data


class ChangeVersionForm(forms.Form):
    """ The class is to create change version form"""

    minimum_version = forms.CharField(
        label="Minimum Version",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'minimum_version',
                'data-required': 'true',
                'data-describedby': 'minimum_version-description',
                'data-description': 'minimum_version',
                'placeholder': 'Minimum Version',
            }),
        required=True
    )

    latest_version = forms.CharField(
        label="Latest Version",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'latest_version',
                'data-required': 'true',
                'data-describedby': 'latest_version-description',
                'data-description': 'latest_version',
                'placeholder': 'Latest Version'
            }),
        required=True
    )
