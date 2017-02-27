"""This module is created to built the forms"""
__author__ = 'Richa Sharma <richa@weboniselab.com>'

from django import forms
from WebApp.models import PersonalInformation, InsuranceClaim
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    """ The class is to create Login form"""
    email = forms.CharField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                'class': 'inpData',
                'placeholder': _('Email'),
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
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'inpData',
                'placeholder': _('Password'),
                'id': 'password',
                'data-required': 'true',
                'data-describedby': 'password-description',
                'data-description': 'password',
            }),
        required=True
    )

class PersonalInformationForm(forms.Form):
    """ The class is to create personal document form"""

    def __init__(self, *args, **kwargs):
        super(PersonalInformationForm, self).__init__(*args, **kwargs)

    forename = forms.CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'first_name',
                'placeholder': _('John'),
                'data-required': 'true',
                'data-describedby': 'first_name-description',
                'data-description': 'first_name',
                'data-pattern': r"^[a-zA-Z'. ]+$"
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter first name')
        }
    )
    surname = forms.CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'last_name',
                'placeholder': _('Doe'),
                'data-required': 'true',
                'data-describedby': 'last_name-description',
                'data-description': 'last_name',
                'data-pattern': r"^[a-zA-Z'. ]+$"
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter last name')
        }
    )
    addressLine1 = forms.CharField(
        label=_("Address line 1"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'address_line1',
                'class': 'inpData',
                'placeholder': _('1234 Commercial Dr.'),
                'data-required': 'true',
                'data-describedby': 'address_line1-description',
                'data-description': 'address_line1',
                'data-conditional': "check_spaces",
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter address line 1')
        }
    )
    addressLine2 = forms.CharField(
        label=_("Address line 2 (Optional)"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'address_line2',
                'class': 'inpData',
                'placeholder': _('Apartment 45'),
                'data-describedby': 'address_line2-description',
                'data-description': 'address_line2',
                'data-conditional': "check_spaces",
            }
        ),
        required=False
    )
    addressLine3 = forms.CharField(
        label=_("Address line 3 (Optional)"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'address_line3',
                'class': 'inpData',
                'placeholder': _('Main City, PM'),
                'data-describedby': 'address_line3-description',
                'data-description': 'address_line3',
                'data-conditional': "check_spaces",
            }
        ),
        required=False
    )
    city = forms.CharField(
        label=_("City"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'city',
                'class': 'inpData',
                'placeholder': _('Main City'),
                'data-required': 'true',
                'data-describedby': 'city-description',
                'data-description': 'city',
                'data-conditional': "check_spaces",
                'data-pattern': r"^[a-zA-Z ]+$"
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter city')
        }
    )
    country = forms.CharField(
        label=_("Country"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'country',
                'class': 'inpData',
                'placeholder': _('PM'),
                'data-required': 'true',
                'data-describedby': 'country-description',
                'data-description': 'country',
                'data-conditional': "check_spaces",
                'data-pattern': r"^[a-zA-Z ]+$"
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter country')
        }
    )
    postcode = forms.CharField(
        label=_("Postcode"),
        widget=forms.TextInput(
            attrs={
                'id': 'zipcode',
                'class': 'inpData',
                'placeholder': _('44223'),
                'data-required': 'true',
                'data-describedby': 'zipcode-description',
                'data-description': 'zipcode',
                'data-pattern': r"^[0-9a-zA-Z ]+$"
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter postcode')
        }
    )
    mobile = forms.CharField(
        label=_("Phone Number"),
        widget=forms.TextInput(
            attrs={
                'id': 'phone_number',
                'class': 'inpData',
                'placeholder': _('1 343 222 2222'),
                'data-required': 'true',
                'data-describedby': 'phone_number-description',
                'data-description': 'phone_number',
                'data-pattern': r"^[+]{0,1}[0-9\(\)\-]{6,14}$"
            }
        ),
        required=True,
        max_length=20,
        min_length=1,
        error_messages={
            'required': _('Please enter phone number'),
            'max_length': _('Please enter valid phone number'),
            'min_length': _('Please enter valid phone number')
        }
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
                'class': 'inpData',
                'placeholder': _('email@mydomain.com'),
                'data-required': 'true',
                'data-describedby': 'email-description',
                'data-description': 'email',
                'data-pattern': r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|'
                                r'(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'
                                r'(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter email id')
        }
    )


METHOD_OF_CONTACT = (('email', _('Email'),), ('phone_number', _('Phone'),))

class InsuranceClaimForm(forms.Form):
    """ The class is to create insurance claim form"""

    def __init__(self, *args, **kwargs):
        super(InsuranceClaimForm, self).__init__(*args, **kwargs)
        claim_choices = self.get_claim_choices()
        self.fields['claim_types'].choices = claim_choices

    @classmethod
    def get_claim_choices(cls):
        """Returns the claim choices"""
        insurance_claim_obj = InsuranceClaim()
        claim_types = insurance_claim_obj.file_operations('claim_type')
        return [claim_choice for claim_type
                in claim_types for claim_choice
                in claim_type.items()]

    claim_types = forms.ChoiceField(
        label=_("What type of claim would you like to file?"),
        widget=forms.Select(
            attrs={
                'id': 'id_claim_types',
                'class': 'inpData',
                'placeholder': _('Select Claim Type'),
                'data-required': 'true',
                'data-describedby': 'id_claim_types-description',
                'data-description': 'id_claim_types',
                'data-conditional': "check_more_info_read",
            },
        ),
        required=True,
        error_messages={
            'required': _('Please Select Claim type')
        }
    )
    save_personal_info = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'id': "savePersonalInfo"
            }
        ),
        initial="0"
    )
    claim_description = forms.CharField(
        label=_("Claim Description"),
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'inpData',
                'placeholder': _('Enter claim description'),
            }
        ),
        required=False,
    )
    attach_file = forms.ImageField(
        label=_("Please attach a proof of purchase"),
        widget=forms.FileInput(
            attrs={
                'id': 'attach_file',
                'class': 'inpData inpUpload',
            }),
        required=False
    )
    addressLine1 = forms.CharField(
        label=_("Please verify your address line 1 *"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'id_address_line1',
                'class': 'inpData',
                'placeholder': _('1234 Commercial Dr.'),
                'data-required': 'true',
                'data-describedby': 'id_address_line1-description',
                'data-description': 'id_address_line1',
                'data-conditional': "check_spaces",
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter address line 1')
        }
    )
    addressLine2 = forms.CharField(
        label=_("Verify address line 2"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'id_address_line2',
                'class': 'inpData',
                'placeholder': _('Apartment 45'),
            }
        ),
        required=False
    )
    addressLine3 = forms.CharField(
        label=_("Verify address line 3"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'id_address_line3',
                'class': 'inpData',
                'placeholder': _('Main City, PM'),
            }
        ),
        required=False
    )
    city = forms.CharField(
        label=_("Verify city *"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'id_city',
                'class': 'inpData',
                'placeholder': _('Main City'),
                'data-required': 'true',
                'data-describedby': 'id_city-description',
                'data-description': 'id_city',
                'data-conditional': "check_spaces",
                'data-pattern': r"^[a-zA-Z ]+$"
            }
        ),
        required=False
    )
    country = forms.CharField(
        label=_("Verify country *"),
        widget=forms.TextInput(
            attrs={
                'rows': 3,
                'id': 'id_country',
                'class': 'inpData',
                'placeholder': _('PM'),
                'data-required': 'true',
                'data-describedby': 'country-description',
                'data-description': 'country',
                'data-conditional': "check_spaces",
                'data-pattern': r"^[a-zA-Z ]+$"
            }
        ),
        required=False
    )
    postcode = forms.CharField(
        label=_("Verify Postcode *"),
        widget=forms.TextInput(
            attrs={
                'id': 'id_zipcode',
                'class': 'inpData',
                'placeholder': _('44223'),
                'data-required': 'true',
                'data-pattern': r"^[0-9a-zA-Z ]+$",
                'data-describedby': 'id_zipcode-description',
                'data-description': 'id_zipcode',
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter postcode')
        }
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
                'class': 'inpData',
                'placeholder': _('email@mydomain.com'),
                'data-required': 'true',
                'data-describedby': 'email-description',
                'data-description': 'email',
                'data-pattern': r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|'
                                r'(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'
                                r'(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter valid email id')
        }
    )


LOST_CARD_CHOICES = (('lost', _('Lost')), ('stolen', _('Stolen')))

class ReportLostCardForm(forms.Form):
    """ The class is to create report lost card form"""

    def __init__(self, *args, **kwargs):
        super(ReportLostCardForm, self).__init__(*args, **kwargs)
        self.fields['cards'].choices = self.get_all_cards()
        self.set_initials(self)

    @classmethod
    def set_initials(cls, self):
        """Set the initial values for all the fields"""
        personal_info_obj = PersonalInformation()
        personal_information = personal_info_obj.file_operations('dummy_personal_info.json')
        self.fields['address'].initial = personal_information['address']
        self.fields['zipcode'].initial = personal_information['zipcode']
        self.fields['email'].initial = personal_information['email']

    @classmethod
    def get_all_cards(cls):
        """Returns the list of all cards"""
        insurance_claim_obj = InsuranceClaim()
        card_types = insurance_claim_obj.file_operations('all_card_details')
        cards_list = card_types[0]['card_details']
        all_cards = []
        for index, card in enumerate(cards_list):
            all_cards.insert(index, (
                card.get('cardNumber'),
                card.get('cardType') + ' (****-****-****-' + card.get('cardNumber') + ')'))

        return all_cards

    cards = forms.MultipleChoiceField(
        label=_("Cards *"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    lost_stolen = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                'id': 'id_lost_stolen',
                'data-required': 'true',
                'data-describedby': 'lost_stolen-description',
                'data-description': 'lost_stolen',
            }
        ),
        choices=LOST_CARD_CHOICES,
        initial='lost',
        required=True,
        error_messages={
            'required': _('Please select at least one')
        }
    )
    date_time = forms.CharField(
        label=_('Select Date & Time *'),
        widget=forms.TextInput(
            attrs={
                'id': 'id_date_time',
                'class': 'form-control',
                'placeholder': _('Date & Time'),
                'data-date-format': 'd MM, yyyy HH:ii P',
                'data-field': 'datetime',
                'readonly': 'readonly',
                'data-required': 'true',
                'data-describedby': 'id_date_time-description',
                'data-description': 'id_date_time',
            },
        ),
        required=True,
        error_messages={
            'required': _('Please select the date and time')
        }
    )
    describe_event = forms.CharField(
        label=_("Describe The Event"),
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': _('Describe The Event'),
            }
        ),
        required=False,
    )
    address = forms.CharField(
        label=_("Verify Address *"),
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'id': 'id_address',
                'class': 'form-control',
                'data-required': 'true',
                'data-describedby': 'id_address-description',
                'data-description': 'id_address',
                'placeholder': _('Verify Address'),
                'readonly': 'readonly',
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter address')
        }
    )
    zipcode = forms.CharField(
        label=_("Verify Postcode *"),
        widget=forms.TextInput(
            attrs={
                'id': 'id_zipcode',
                'class': 'form-control',
                'placeholder': _('Verify Postcode'),
                'data-required': 'true',
                'data-describedby': 'id_zipcode-description',
                'data-description': 'id_zipcode',
                'data-pattern': r"^[0-9]+$",
                'readonly': 'readonly',
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter postcode')
        }
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
                'readonly': 'readonly',
                'class': 'inpData',
                'placeholder': _('Email'),
                'data-required': 'true',
                'data-describedby': 'email-description',
                'data-description': 'email',
                'data-pattern': r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)'
                                r'|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])'
                                r'|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter valid email id')
        }
    )


LANGUAGE_CHOICES = (('en', _('English')), ('es', _('Spanish')), ('zh-cn', _('Chinese')))

class ChangeLanguageForm(forms.Form):
    """ The class is to create and manage change language form"""
    def __init__(self, *args, **kwargs):
        super(ChangeLanguageForm, self).__init__(*args, **kwargs)

    language = forms.ChoiceField(
        label=_("Select Language *"),
        widget=forms.Select(
            attrs={
                'class': 'inpData',
                'placeholder': _('Select Language'),
                'data-validation': 'required',
                'data-validation-error-msg': _('Please select a language'),
            },
        ),
        choices=LANGUAGE_CHOICES,
        initial=_('en'),
        required=True,
        error_messages={
            'required': _('Please select a language')
        }
    )

class ActivateBundleServicesForm(forms.Form):
    """ The class is to create Login form"""
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
                'class': 'inpData',
                'placeholder': _('johndoe@doecorp.com'),
                'data-required': 'true',
                'data-describedby': 'email-description',
                'data-description': 'email',
                'data-pattern': r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|'
                                r'(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'
                                r'(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter email id')
        }
    )

class ActivatePinForm(forms.Form):
    """ The class is to create Activate Pin form"""
    pin = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'inpData',
                'id': 'pin',
                'placeholder': _('Please input your 8 digit PIN'),
                'data-required': 'true',
                'data-describedby': 'pin-description',
                'data-description': 'pin',
                'data-pattern': r"^[A-Za-z0-9_]{8}$"
            }
        ),
        required=True,
        error_messages={
            'required': _('Please enter the PIN')
        }
    )