"""
Every request come here, check for the particular function
and then render the response after processing
"""
from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from WebApp.forms import PersonalInformationForm, ReportLostCardForm, InsuranceClaimForm,\
    LoginForm, ChangeLanguageForm, ActivateBundleServicesForm, ActivatePinForm
from WebApp.models import PersonalInformation, InsuranceClaim
from MagPie import settings
from WebApp.utils import upload_file, check_file_size, post_details_in_api
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
import os
import WebApp.utils as webapp_utils


def login_user(request):
    """
    Login page for App
    """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            valid_data = login_form.cleaned_data
            authenticated_user = authenticate_user(request, valid_data)
            if authenticated_user:
                messages.success(request, _('You are logged in successfully!'))
                return HttpResponseRedirect('/dashboard')
            else:
                return HttpResponseRedirect('/')
        else:
            login_form = LoginForm()
            return render(request, "WebApp/index.html", {'form': login_form})
    else:
        login_form = LoginForm()
        if 'is_active' in request.session:
                return HttpResponseRedirect('/dashboard')
        request.session.flush()
        return render(request, "WebApp/index.html", {'form': login_form})


def authenticate_user(request, credentials):
    """
    Authenticating user using PIB API calls
    """
    login_details = {
        'username': credentials['email'],
        'password': credentials['password'],
        'grant_type': 'password'
    }
    response = webapp_utils.login_api(login_details)
    if response is not None and 'access_token' in response:
        request.session['is_active'] = True
        request.session['user_id'] = response['userId']
        request.session['email'] = credentials['email']

        #Getting theme for BP
        theme = webapp_utils.get_business_partner_theme(request)

        #Setting theme in Session
        request.session['theme_color'] = theme['theme_color']
        request.session['font_color'] = theme['font_color']
        request.session['logo'] = theme['logo']
        request.session['fav_icon'] = theme['fav_icon']
        return True
    else:
        messages.error(request, _("Invalid email id or password"))
        return None


def logout_user(request):
    """
    Logout user deleting users data from session
    """
    request.session.flush()
    return HttpResponseRedirect('/')


def ethos(request, language='en'):
    """
    Renders Ethos Page
    """
    return render(request, 'WebApp/ethos.html')


def dashboard(request):
    """
    After Authenticating redirect to dashboard
    """
    if 'is_active' in request.session:
        webapp_utils.get_business_partner_theme(request)
        return render(request, 'WebApp/dashboard.html')
    else:
        return HttpResponseRedirect('/')


# The view personal information page
def personal_info(request):
    """To render the personal information view page"""
    if 'is_active' in request.session:
        return render(request, "WebApp/users/personal_info.html",
                      {"personal_info": webapp_utils.get_personal_info(request)})
    else:
        return HttpResponseRedirect('/')


# The Edit personal information page
def edit_personal_info(request):
    """To render the edit personal information form"""
    if 'is_active' in request.session:
        if request.method == 'POST':
            personal_information_form = PersonalInformationForm(request.POST)
            if personal_information_form.is_valid():
                personal_information_data = personal_information_form.cleaned_data
                personal_info_obj = PersonalInformation()
                personal_info_data = {
                    'forename': personal_information_data['forename'],
                    'surname': personal_information_data['surname'],
                    'address': {
                        'addressLine1': personal_information_data['addressLine1'],
                        'addressLine2': personal_information_data['addressLine2'],
                        'addressLine3': personal_information_data['addressLine3'],
                        'city': personal_information_data['city'],
                        'country': personal_information_data['country'],
                        'postcode': personal_information_data['postcode'],
                    },
                    'mobile': personal_information_data['mobile'],
                    'email': personal_information_data['email']
                }
                personal_info_obj.save_personal_info(personal_info_data)
                messages.success(request, _("Your information has been updated with Magpie."))
                return HttpResponseRedirect('/my_account/')
            else:
                return render(request, "WebApp/users/edit_personal_info.html",
                              {"form": personal_information_form})
        else:
            personal_information_form = webapp_utils.add_initial_values(
                webapp_utils.get_personal_info(request), PersonalInformationForm())
            return render(request, "WebApp/users/edit_personal_info.html",
                          {"form": personal_information_form})
    else:
        return HttpResponseRedirect('/')


# The terms & conditions page
def terms_and_conditions(request, language='en'):
    """To render the terms and conditions page"""
    return render(request, "WebApp/terms_and_conditions.html")


# The submit an insurance claim functionality
def insurance_claim(request):
    """To render the insurance claim form page"""
    if 'is_active' in request.session:
        if request.method == 'POST':
            insurance_claim_form = InsuranceClaimForm(request.POST)
            personal_info_obj = PersonalInformation()
            personal_information = webapp_utils.get_personal_info(request)
            if insurance_claim_form.is_valid():
                insurance_claim_data = insurance_claim_form.cleaned_data

                if insurance_claim_data['save_personal_info'] == "1":
                    personal_info_data = {
                        'forename': personal_information['forename'],
                        'surname': personal_information['surname'],
                        'address': {
                            'addressLine1': request.POST['addressLine1'],
                            'addressLine2': request.POST['addressLine2'],
                            'addressLine3': request.POST['addressLine3'],
                            'city': request.POST['city'],
                            'country': request.POST['country'],
                            'postcode': request.POST['postcode'],
                            },
                        'mobile': personal_information['mobile'],
                        'email': request.POST['email']
                    }
                    personal_info_obj.save_personal_info(personal_info_data)

                if 'attach_file' in request.FILES:
                    if check_file_size(request.FILES['attach_file'], int(settings.MAX_UPLOAD_SIZE)):
                        folder_path = os.path.join(settings.MEDIA_ROOT, 'Insurance')
                        folder_path = os.path.join(folder_path,
                                                   personal_information['first_name'] + '_doc')
                        folder_path = os.path.join(folder_path, insurance_claim_data['claim_types'])
                        upload_file(request.FILES['attach_file'], folder_path)
                    else:
                        messages.error(request, _("Please add image with size less than 2MB"))
                        return HttpResponseRedirect('/insurance_claim/')
                insurance_claim_data.pop('attach_file')
                body = {
                    'type': 'email',
                    'subject': 'test insurance claim',
                    'priority': 4,
                    'status': 'open',
                    'labels': ["Spam", "Ignore"],
                    'message': {
                        "direction": "in",
                        "body": json.dumps(insurance_claim_data),
                        "to":"claims@magpieint.com",
                        "from":request.POST['email'],
                        "subject":"My email subject"},
                    "_links": {
                        "customer": {
                            "class":"customer",
                            "href":"/api/v2/customers/289072912"}}}
                api_response = post_details_in_api(json.dumps(body))
                if api_response == 201:
                    return HttpResponseRedirect('/confirmation_page/')
                else:
                    messages.error(request, _("Something went wrong !!!!"))
                    return render(request, "WebApp/users/insurance_claim.html",
                                  {"form": insurance_claim_form})
            else:
                messages.error(request, _("Something went wrong !!!!"))
                return render(request, "WebApp/users/insurance_claim.html",
                              {"form": insurance_claim_form})
        else:
            insurance_claim_form = webapp_utils.add_initial_values(
                webapp_utils.get_personal_info(request), InsuranceClaimForm())
            return render(request, "WebApp/users/insurance_claim.html",
                          {"form": insurance_claim_form})
    else:
        return HttpResponseRedirect('/')


def insurance_claim_details(request):
    """To return the insurance claim details,
     fetched from the api on the ajax call"""
    if 'is_active' in request.session:
        insurance_claim_obj = InsuranceClaim()
        insurance_details = insurance_claim_obj.file_operations('insurance_details')
        return HttpResponse(json.dumps(insurance_details[0][request.GET['id']]))
    else:
        return HttpResponseRedirect('/')


# The report lost card functionality
def report_lost_card(request):
    """To render the report lost card form"""
    if 'is_active' in request.session:
        if request.method == 'POST':
            report_lost_card_form = ReportLostCardForm(request.POST)
            if report_lost_card_form.is_valid():
                # The variable will be used when the API integration will be done
                # report_lost_card_data = report_lost_card_form.cleaned_data
                return HttpResponseRedirect('/confirmation_page/')
            else:
                return render(request, "WebApp/users/report_lost_card.html",
                              {"form": report_lost_card_form})
        else:
            report_lost_card_form = ReportLostCardForm()
            return render(request, "WebApp/users/report_lost_card.html", {
                "form": report_lost_card_form,
            })
    else:
        return HttpResponseRedirect('/')


# The confirmation page after reporting lost card or submitting the insurance claim
def confirmation_page(request):
    """To render the confirmation page"""
    if 'is_active' in request.session:
        return render(request, "WebApp/users/confirmation_page.html")
    else:
        return HttpResponseRedirect('/')


# The need emergency cash page
def need_emergency_cash(request):
    """To render the need emergency cash page"""
    if 'is_active' in request.session:
        return render(request, "WebApp/users/need_emergency_cash.html")
    else:
        return HttpResponseRedirect('/')


# The need emergency cash page
def change_language(request):
    """To render the change language page and update the changed language in session"""
    if 'is_active' in request.session:
        if request.method == 'POST':
            change_language_form = ChangeLanguageForm(request.POST)
            if change_language_form.is_valid():
                if 'language_code' in request.session:
                    del request.session['language_code']
                request.session['language_code'] = change_language_form.cleaned_data['language']
                request.session['django_language'] = change_language_form.cleaned_data['language']
                translation.activate(change_language_form.cleaned_data['language'])
                messages.success(request, _("Your language setting has been changed."))
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request, _("There is some problem."))
                return render(request, "WebApp/users/change_language.html",
                              {"form": change_language_form})
        else:
            change_language_form = ChangeLanguageForm()
            if 'language_code' in request.session:
                change_language_form.fields['language'].initial = request.session['language_code']
            else:
                change_language_form.fields['language'].initial = 'en'
            return render(request, "WebApp/users/change_language.html", {
                "form": change_language_form,
            })
    else:
        return HttpResponseRedirect('/')


# Help page which displays the user with email and phone number listings of Magpie Call center
def magpie_help(request):
    """To render the help page"""
    if 'is_active' in request.session:
        help_data = webapp_utils.get_help_data(request)
        contact_email = None
        contact_phone = None
        if help_data is not None:
            if 'customerSupportEmail' in help_data:
                contact_email = help_data['customerSupportEmail']
            if 'customerSupportNumber' in help_data:
                contact_phone = help_data['customerSupportNumber']
        return render(request, 'WebApp/help.html',
                      {'contact_email': contact_email,'contact_phone': contact_phone})
    else:
        return HttpResponseRedirect('/')


def bitdefender_parental_control(request):
    """To render the bit defender parental control screen"""
    if 'is_active' in request.session:
        return render(request, "WebApp/bitdefender_parental_control.html")
    else:
        return HttpResponseRedirect('/')


def bitdefender_antivirus(request):
    """To render the bit defender antivirus screen"""
    if 'is_active' in request.session:
        return render(request, "WebApp/bitdefender_antivirus.html")
    else:
        return HttpResponseRedirect('/')


def bitdefender_total_security(request):
    """To render the bit defender total security screen"""
    if 'is_active' in request.session:
        return render(request, "WebApp/bitdefender_total_security.html")
    else:
        return HttpResponseRedirect('/')


def bitdefender_internet_security(request):
    """To render the bit defender internet security screen"""
    if 'is_active' in request.session:
        return render(request, "WebApp/bitdefender_internet_security.html")
    else:
        return HttpResponseRedirect('/')


def subscription_info(request):
    """To render the subscription information  screen"""
    if 'is_active' in request.session:
        return render(request, "WebApp/subscription_info.html",
                      {'subscription': webapp_utils.get_subscription_info(request)})
    else:
        return HttpResponseRedirect('/')


def activate_services_languages(request, language='en', is_mobile=0):
    """
    Updates the language code in session variable and redirect to next action
    """
    if 'is_mobile' in request.session:
        del request.session['is_mobile']

    if int(is_mobile) == 1:
        if 'language_code' in request.session:
            del request.session['language_code']
        request.session['is_mobile'] = is_mobile
        request.session['language_code'] = language

    return HttpResponseRedirect('/activate_bundle_services/')


def activate_my_bundle_services(request):
    """
    Renders the activate my bundle services page
    and sends the submitted data to DESK.com APIs
    """
    is_mobile = 0
    if request.method == 'POST':
        activate_bundle_services_form = ActivateBundleServicesForm(request.POST)
        if activate_bundle_services_form.is_valid():
            activate_bundle_services_data = activate_bundle_services_form.cleaned_data

            body = {
                'type': 'email',
                'subject': 'test activate bundle services',
                'priority': 4,
                'status': 'open',
                'labels': ["Spam", "Ignore"],
                'message': {
                    "direction": "in",
                    "body": json.dumps(activate_bundle_services_data),
                    "to":"claims@magpieint.com",
                    "from":activate_bundle_services_data['email'],
                    "subject":"My email subject"},
                "_links": {
                    "customer": {
                        "class":"customer",
                        "href":"/api/v2/customers/289072912"}}}
            api_response = post_details_in_api(json.dumps(body))
            if api_response == 201:
                if 'is_mobile' in request.session:
                    is_mobile = request.session['is_mobile']
                    del request.session['is_mobile']
                if int(is_mobile) == 1:
                    if 'language_code' in request.session:
                        del request.session['language_code']
                messages.success(request, _('The request is submitted successfully.'))
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, _("Something went wrong !!!!"))
                return render(request, "WebApp/users/activate_bundle_services.html",
                              {"form": activate_bundle_services_form})
        else:
            messages.error(request, _("Something went wrong !!!!"))
            return render(request, "WebApp/users/activate_bundle_services.html",
                          {"form": activate_bundle_services_form})
    else:
        activate_bundle_services_form = ActivateBundleServicesForm()
        return render(request, "WebApp/users/activate_bundle_services.html",
                      {"form": activate_bundle_services_form})


def check_personal_info_changes(request):
    """
    Check if the contact information of insurance claim is same as
    contact information of my account and returns true or false
    """
    is_same = False
    if request.method == "POST":
        personal_info_obj = PersonalInformation()
        is_same = personal_info_obj.check_information(request)
    return HttpResponse(is_same)


# Creating Static pages for the PIB mobile app
def activate_pin(request, country_code):
    """
    The static login page for the PIB mobile app to serve the request
    """
    if 'is_active' in request.session:
        return HttpResponseRedirect('/')
    else:

        # Code for activate translation
        if 'language_code' in request.session:
            del request.session['language_code']
        if country_code.lower() == 'mx':
            request.session['language_code'] = 'es'
        elif country_code.lower() == 'cn':
            request.session['language_code'] = 'zh-cn'
        return HttpResponseRedirect('/activate_pin/' + country_code)

def activate_pin_translated(request, country_code):
    """
    The activate pin page after translations
    """
    if request.method == 'POST' and 'pin' in request.POST:
        activate_pin_form = ActivatePinForm(request.POST)
        if activate_pin_form.is_valid():
            activate_pin_data = activate_pin_form.cleaned_data
            user_details = webapp_utils.user_activation(activate_pin_data['pin'])
            if 'status' in user_details and 'code' in user_details['status']:
                if user_details['status']['code'] == 200:
                    return HttpResponseRedirect(
                        'https://api.infobank.me/' + country_code + '/register?userId=' + str(user_details['data']['id']))
                elif user_details['status']['code'] == 409:
                    messages.error(request, _('This PIN has already been used.'))
                elif user_details['status']['code'] == 400:
                    messages.error(request, _('Invalid 8 digit PIN, please try again!'))
                else:
                    messages.error(request, _('Error in Magpie user activation'))
            else:
                messages.error(request, _('Error in Magpie user activation'))
    else:
        activate_pin_form = ActivatePinForm()
    return render(request, 'static_pages/activate_pin.html', {"form": activate_pin_form})
