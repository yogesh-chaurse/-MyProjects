"""
Every request come here, check for the particular function
and then render the response after processing
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from CMS.forms import ChangePasswordForm, LoginForm, AddThemeForm, \
    EditThemeForm, AddInstituteForm, ChangeVersionForm
from django.contrib.auth.hashers import check_password, make_password
from CMS.models import Business_Partners, Themes, \
    Institutions, Languages, Dynamic_Contents, Version_Updates
from django.core.files.images import get_image_dimensions
from MagPie import settings
from os import listdir
from os.path import isfile, join
import json
import shutil
import os
import zipfile
import requests
import CMS.utils as cms_utils


def index(request):
    """
    Home page for application
    """
    return HttpResponseRedirect("/login", {'request': request})


def login_user(request):
    """To render the login page and process the functionality"""
    if not request.user.is_authenticated():
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                login_form_data = login_form.cleaned_data
                user = authenticate_user(request, login_form_data)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    messages.success(request, 'You are logged in successfully!')
                    return HttpResponseRedirect("/dashboard")
                else:
                    return HttpResponseRedirect('/login')
            else:
                return render(request, 'CMS/index.html', {'form': login_form})
        else:
            login_form = LoginForm()
            return render(request, 'CMS/index.html', {'form': login_form})
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url='/login')
def logout_user(request):
    """To process the logout functionality"""

    logout(request)
    return HttpResponseRedirect('/login')


def authenticate_user(request, data):
    """To authenticate the user by using the entered credentials"""

    user = User.objects.filter(email=data['email'])
    if user.exists():
        if user.first().check_password(data['password']):
            return user.first()
        else:
            messages.error(request, "Invalid email id or password")
            return None
    else:
        messages.error(request, "Invalid email id or password")
        return None

@login_required(login_url='/login')
def dashboard(request):
    """To render the dashboard after login"""
    return render(request, 'CMS/dashboard.html')

@login_required(login_url='/login')
def change_password(request):
    """To render the change password age and process the functionality"""

    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            change_password_form_data = change_password_form.cleaned_data
            passwords_valid = validate_passwords(request, change_password_form_data)
            if passwords_valid:
                User.objects.filter(id=request.user.id).update(password=passwords_valid)
                messages.success(request, "Password is updated successfully.")
                return HttpResponseRedirect('/dashboard/')
            else:
                return render(request, 'CMS/change_password.html',
                              {'form': change_password_form})
        else:
            return render(request, 'CMS/change_password.html',
                          {'form': change_password_form})
    else:
        change_password_form = ChangePasswordForm()
        return render(request, 'CMS/change_password.html',
                      {'form': change_password_form})


def validate_passwords(request, passwords):
    """To validate the passwords and process the functionality"""
    if check_password(passwords['old_password'], request.user.password):
        if passwords['new_password'] == passwords['confirm_password']:
            return make_password(passwords['new_password'])
        else:
            messages.error(request, "New and confirm passwords do not match")
            return False
    else:
        messages.error(request, "Old Password is incorrect")
        return False

@login_required(login_url='/login')
def business_partner_list(request):
    """To render the business partner listing page"""

    business_partner_obj = Business_Partners()
    business_partners_list = business_partner_obj.get_all_business_partners()

    return render(
        request,
        'CMS/business_partner_list.html',
        {
            'business_partner_list': cms_utils.apply_pagination(request, business_partners_list),
            'business_partner_list_tab': 'active',
            'media_url': settings.MEDIA_ROOT,
            'count': -1
        }
    )

@login_required(login_url='/login')
def add_theme(request, business_partner_id):
    """To render the add theme page and process the functionality"""
    business_partner_obj = Business_Partners()
    business_partner = business_partner_obj.get_business_partner(business_partner_id)
    if request.method == 'POST':
        add_theme_form = AddThemeForm(request.POST, request.FILES)
        if add_theme_form.is_valid():
            add_theme_form_data = add_theme_form.cleaned_data
            fav_icon = add_theme_form_data.get("fav_icon")
            uploaded_files = check_and_upload(request, add_theme_form_data, fav_icon, business_partner)
            if uploaded_files:
                themes_obj = Themes.objects.create(
                    business_partner_id=business_partner.id,
                    theme_color=request.POST['theme_color'],
                    font_color=request.POST['font_color'],
                    logo=uploaded_files['logo'],
                    splash_screen=uploaded_files['splash_screen'],
                    fav_icon=uploaded_files['fav_icon'],
                    app_icon=uploaded_files['app_icon'],
                )

                if themes_obj.pk:
                    messages.success(request, "Theme is added for %s." % business_partner.name)
                    return HttpResponseRedirect('/business_partner_list/')
                else:
                    messages.error(request, "Something went wrong. Please try again.")
                    return HttpResponseRedirect('/business_partner_list/')
            else:
                add_theme_form = AddThemeForm()
                messages.error(request, "Please check image dimensions")
                return render(
                    request,
                    'CMS/theme_customisation.html',
                    {'form': add_theme_form, 'business_partner': business_partner}
                )
        else:
            messages.error(request, "Something went wrong. Please try again.")
            return HttpResponseRedirect('/business_partner_list/')
    else:
        add_theme_form = AddThemeForm()
        return render(
            request,
            'CMS/theme_customisation.html',
            {'form': add_theme_form, 'business_partner': business_partner}
        )

def create_zip(business_partner_id):
    """To create the zip file for Android and IOS of the uploaded images"""
    business_partner_obj = Business_Partners()
    business_partner = business_partner_obj.get_business_partner(business_partner_id)
    os_types = ['android', 'ios']
    if hasattr(business_partner, 'theme_of'):
        for os_type in os_types:
            main_folder_path = os.path.join(settings.MEDIA_ROOT, business_partner.name, os_type)
            zip_filename = "%s.zip" % os_type
            file_obj = zipfile.ZipFile(settings.ZIP_ROOT + zip_filename, "w")
            subirs = cms_utils.get_immediate_subdirectories(main_folder_path)
            for dirs in subirs:
                dir_path = os.path.join(main_folder_path, dirs)
                onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
                for files in onlyfiles:
                    zip_path = os.path.join(dirs, files)
                    file_obj.write(os.path.join(dir_path, files), zip_path)
            file_obj.close()
        return HttpResponseRedirect('/business_partner_list/')
    else:
        return False

@login_required(login_url='/login')
def create_default_business_partners(request):
    """Until we get the business partner list from the API,
    We are running migration to enter the dummy business partners for testing and demo purpose"""
    Business_Partners.objects.create(
        name="Vodafone",
        business_partner_id='101')
    Business_Partners.objects.create(
        name="BOA",
        business_partner_id='102')
    Business_Partners.objects.create(
        name="HSBC",
        business_partner_id='103')
    Business_Partners.objects.create(
        name="HDFC",
        business_partner_id='104')
    return HttpResponseRedirect('/business_partner_list/', {'request', request})

@login_required(login_url='/login')
def edit_theme(request, business_partner_id):
    """Editing theme of Business partner"""
    business_partner = Business_Partners().get_business_partner(business_partner_id)
    if request.method == 'POST':
        edit_theme_form = EditThemeForm(request.POST, request.FILES)
        if edit_theme_form.is_valid():
            edit_theme_form_data = edit_theme_form.cleaned_data
            if edit_theme_form_data.get("fav_icon") is not None:
                fav_icon = edit_theme_form_data.get("fav_icon")
            else:
                fav_icon = None
            if edit_theme_form_data.get("logo") is not None\
                    and edit_theme_form_data.get("splash_screen") is not None\
                    and edit_theme_form_data.get("app_icon") is not None:

                uploaded_files = check_and_upload(
                    request,
                    edit_theme_form_data,
                    fav_icon,
                    business_partner)
                if uploaded_files:
                    business_partner.theme_of.logo = uploaded_files['logo']
                    business_partner.theme_of.splash_screen = uploaded_files['splash_screen']
                    business_partner.theme_of.app_icon = uploaded_files['app_icon']
                else:
                    messages.error(request, "Please check the image dimensions.")
                    return render(request, 'CMS/edit_theme_customisation.html',
                                  {'form': get_prepopulated_form_obj(business_partner),
                                   'business_partner': business_partner})
            if edit_theme_form_data.get("splash_screen") is not None:
                splash_screen_width, splash_screen_height = get_image_dimensions(
                    edit_theme_form_data.get("splash_screen"))

                if splash_screen_width >= settings.MIN_UPLOAD_DIMENSIONS['splash_screen']['width'] \
                        and splash_screen_height >= \
                                settings.MIN_UPLOAD_DIMENSIONS['splash_screen']['height']:
                    cms_utils.remove_orignal_files(
                        business_partner.name,
                        business_partner.theme_of.splash_screen)

                    uploaded_files = dict()
                    uploaded_files['splash_screen'] = cms_utils.upload_file(
                        request.FILES['splash_screen'],
                        os.path.join(settings.MEDIA_ROOT, business_partner.name)
                    )
                    business_partner.theme_of.splash_screen = uploaded_files['splash_screen']
                else:
                    messages.error(request, "Please check the image dimensions.")
                    return render(request, 'CMS/edit_theme_customisation.html',
                                  {'form': get_prepopulated_form_obj(
                                      business_partner),
                                   'business_partner': business_partner})

            if edit_theme_form_data.get("app_icon") is not None:
                cms_utils.remove_android_files(business_partner.name, 'app_icon.png')
                cms_utils.remove_ios_files(business_partner.name, 'appicons')
                cms_utils.remove_orignal_files(business_partner.name, business_partner.theme_of.app_icon)

                uploaded_files = dict()
                uploaded_files['app_icon'] = cms_utils.upload_file(
                    request.FILES['app_icon'],
                    os.path.join(settings.MEDIA_ROOT, business_partner.name)
                )
                business_partner.theme_of.app_icon = uploaded_files['app_icon']

            if edit_theme_form_data.get("fav_icon") is not None:
                cms_utils.remove_orignal_files(business_partner.name, business_partner.theme_of.fav_icon)

                uploaded_files = dict()
                uploaded_files['fav_icon'] = cms_utils.upload_file(
                    request.FILES['fav_icon'],
                    os.path.join(settings.MEDIA_ROOT, business_partner.name),
                    'fav_icon.ico'
                )
                business_partner.theme_of.fav_icon = uploaded_files['fav_icon']

            if edit_theme_form_data.get("logo") is not None:
                logo_width, logo_height = get_image_dimensions(edit_theme_form_data.get("logo"))
                if logo_width >= settings.MIN_UPLOAD_DIMENSIONS['logo']['width'] \
                        and logo_height >= settings.MIN_UPLOAD_DIMENSIONS['logo']['height']:
                    cms_utils.remove_android_files(business_partner.name, 'icon.png')
                    cms_utils.remove_ios_files(business_partner.name, 'appicons')
                    cms_utils.remove_orignal_files(business_partner.name, business_partner.theme_of.logo)
                    uploaded_files = dict()
                    uploaded_files['logo'] = cms_utils.upload_file(
                        request.FILES['logo'],
                        os.path.join(settings.MEDIA_ROOT, business_partner.name)
                    )
                    cms_utils.handle_ios_uploads(request, business_partner.name)
                    cms_utils.edit_android_uploads(request, business_partner.name, 'logo')
                    business_partner.theme_of.logo = uploaded_files['logo']
                else:
                    messages.error(request, "Please check the image dimensions.")
                    return render(request, 'CMS/edit_theme_customisation.html',
                                  {'form': get_prepopulated_form_obj(business_partner),
                                   'business_partner': business_partner})
            business_partner.theme_of.theme_color = request.POST['theme_color']
            business_partner.theme_of.font_color = request.POST['font_color']
            business_partner.theme_of.save()
            messages.success(request, "Theme is updated for %s." % business_partner.name)
            return HttpResponseRedirect('/business_partner_list/')

        else:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'CMS/business_partner_list.html',
                          {'form': edit_theme_form, 'business_partner': business_partner})

    else:
        return render(request,
                      'CMS/edit_theme_customisation.html',
                      {'form': get_prepopulated_form_obj(business_partner),
                       'business_partner': business_partner})


def get_prepopulated_form_obj(business_partner_obj):
    """Returns the edit theme form object after initialising with pre populated value"""

    theme = business_partner_obj.theme_of
    edit_theme_form = EditThemeForm()
    edit_theme_form.fields['theme_color'].initial = theme.theme_color
    edit_theme_form.fields['font_color'].initial = theme.font_color
    edit_theme_form.fields['logo'].initial = theme.logo
    edit_theme_form.fields['splash_screen'].initial = theme.splash_screen
    edit_theme_form.fields['fav_icon'].initial = theme.fav_icon
    edit_theme_form.fields['app_icon'].initial = theme.app_icon
    return edit_theme_form


def get_web_theme(request, business_partner_id=None):
    """Returns theme for WebApp for a Business partner"""
    theme = {
        'app_theme': {
            'color_primary': '#02A9D8',
            'color_primary_light': '#02A9D8'
        },
        'background': {
            'background_color_primary': '#FFFFFF',
            'background_color_secondary': '#F7F7F7'
        },
        'text_color': {
            'text_color_primary': '#ffffff',
            'text_color_secondary': '#000000',
            'text_color_tertiary': '#6D6E71',
            'text_color_quaternary': '#d3d3d3'
        },
        'button_normal': {
            'button_color_normal': '#02A9D8',
            'button_color_pressed': '#02A9D8',
            'button_color_disabled': '#02A9D8'
        },
        'button_delete': {
            'button_color_normal': '#FF3300',
            'button_color_pressed': '#FF3300',
            'button_color_disabled': '#FF3300'
        },
        'button_confirmation': {
            'button_color_normal': '#02A9D8',
            'button_color_pressed': '#009933',
            'button_color_disabled': '#009933'
        },
        'divider_color': '#E7E8E9',
        'theme_color': '#02A9D8',
        'font_color': '#ffffff',
        'logo': '/static/WebApp/images/logoMagpie.png',
        'app_logo': '/static/WebApp/images/logoMagpie.png',
        'fav_icon': None,
        'header_logo_ios': ('https://' if request.is_secure()
                            else 'http://'+request.META['HTTP_HOST'] +
                                 '/static/CMS/images/magpie_logo_@1x.png').replace(" ", "%20"),
        'header_logo_android': {
            'drawable_hdpi': ('https://' if request.is_secure()
                              else 'http://'+request.META['HTTP_HOST'] +
                                   '/static/CMS/images/hdpi/bp_logo.png').replace(" ", "%20"),
            'drawable_xhdpi': ('https://' if request.is_secure()
                               else 'http://'+request.META['HTTP_HOST'] +
                                    '/static/CMS/images/xhdpi/bp_logo.png').replace(" ", "%20"),
            'drawable_xxhdpi': ('https://' if request.is_secure()
                                else 'http://'+request.META['HTTP_HOST'] +
                                     '/static/CMS/images/xxhdpi/bp_logo.png').replace(" ", "%20")
        },
    }
    if business_partner_id is not None:
        business_partner = Business_Partners()
        business_partner_obj = business_partner.get_business_partner_by_id(business_partner_id)
        if hasattr(business_partner_obj, 'theme_of'):
            business_partner_theme = business_partner_obj.theme_of

            if business_partner_theme.fav_icon is not None:
                fav_icon = 'https://' if request.is_secure() else 'http://'+request.META['HTTP_HOST']\
                                                                  + '/static/CMS/uploads'\
                                                                  + '/' + business_partner_obj.name\
                                                                  + '/' + business_partner_theme.fav_icon
            else:
                fav_icon = None

            theme = {
                'app_theme': {
                    'color_primary': business_partner_theme.theme_color,
                    'color_primary_light': '#02A9D8'
                },
                'background': {
                    'background_color_primary': '#FFFFFF',
                    'background_color_secondary': '#F7F7F7'
                },
                'text_color': {
                    'text_color_primary': business_partner_theme.font_color,
                    'text_color_secondary': '#000000',
                    'text_color_tertiary': '#6D6E71',
                    'text_color_quaternary': '#d3d3d3'
                },
                'button_normal': {
                    'button_color_normal': business_partner_theme.theme_color,
                    'button_color_pressed': '#02A9D8',
                    'button_color_disabled': '#02A9D8'
                },
                'button_delete': {
                    'button_color_normal': business_partner_theme.theme_color,
                    'button_color_pressed': '#FF3300',
                    'button_color_disabled': '#FF3300'
                },
                'button_confirmation': {
                    'button_color_normal': business_partner_theme.theme_color,
                    'button_color_pressed': '#009933',
                    'button_color_disabled': '#009933'
                },
                'divider_color': '#E7E8E9',
                'theme_color': business_partner_theme.theme_color,
                'font_color': business_partner_theme.font_color,
                'logo': ('https://' if request.is_secure()
                         else 'http://'+request.META['HTTP_HOST']+
                              '/static/CMS/uploads'+
                              '/' + business_partner_obj.name+
                              '/' + business_partner_theme.logo).replace(" ", "%20"),
                'app_logo': ('https://' if request.is_secure()
                         else 'http://'+request.META['HTTP_HOST']+
                              '/static/CMS/uploads'+
                              '/' + business_partner_obj.name+
                              '/' + business_partner_theme.app_icon).replace(" ", "%20"),
                'fav_icon': fav_icon,
                'header_logo_ios': ('https://' if request.is_secure()
                                    else 'http://'+request.META['HTTP_HOST']+
                                         '/static/CMS/uploads'+
                                         '/' + business_partner_obj.name+
                                         '/ios/appicons/icon.png').replace(" ", "%20"),
                'header_logo_android': {
                    'drawable_hdpi': ('https://' if request.is_secure()
                                      else 'http://'+request.META['HTTP_HOST']+
                                           '/static/CMS/uploads'+
                                           '/' + business_partner_obj.name+
                                           '/android/drawable-hdpi/icon.png').replace(" ", "%20"),
                    'drawable_xhdpi': ('https://' if request.is_secure()
                                       else 'http://'+request.META['HTTP_HOST']+
                                            '/static/CMS/uploads'+
                                            '/' + business_partner_obj.name+
                                            '/android/drawable-xhdpi/icon.png').replace(" ", "%20"),
                    'drawable_xxhdpi': ('https://' if request.is_secure()
                                        else 'http://'+request.META['HTTP_HOST']+
                                             '/static/CMS/uploads'+
                                             '/' + business_partner_obj.name+
                                             '/android/drawable-xxhdpi/icon.png').replace(" ", "%20")
                },
            }
    return HttpResponse(json.dumps(theme), content_type="application/json; charset=utf-8")

@login_required(login_url='/login')
def preview_theme_data(request):
    """Submit theme Data for preview"""
    business_partner_obj = Business_Partners()
    business_partner = None
    if 'business_partner_id' in request.POST:
        business_partner = business_partner_obj.get_business_partner(
            request.POST['business_partner_id']
        )
    if request.method == 'POST':
        add_theme_form = AddThemeForm(request.POST, request.FILES)
        if add_theme_form.is_valid():
            add_theme_form_data = add_theme_form.cleaned_data

            return HttpResponse(cms_utils.check_image_dimensions(request,
                                                                 add_theme_form_data, business_partner),
                                content_type='application/json')
        else:
            return HttpResponse(
                json.dumps({'Error-invalid': 'Something went wrong. Please try again'}),
                content_type='application/json'
            )
    else:
        add_theme_form = AddThemeForm()
        return render(
            request,
            'CMS/theme_customisation.html',
            {'form': add_theme_form, 'business_partner': business_partner}
        )

@login_required(login_url='/login')
def cancel_preview(request, business_partner_id):
    """
    Remove the logo and splash screen once user clicks on cancel after the theme preview
    """
    print request.method
    business_partner_obj = Business_Partners()
    business_partner = business_partner_obj.get_business_partner(business_partner_id)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, business_partner.name)):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, business_partner.name), True)
    return HttpResponseRedirect('/business_partner_list/')

@login_required(login_url='/login')
def institution_list(request, sort_by='created', order='desc'):
    """
    The static html page for theme customisation
    """
    language_obj = Languages()
    language_obj.create_default_languages()
    institution_obj = Institutions()
    institutions_list = institution_obj.get_all_institutions(sort_by, order)
    regions_list = institution_obj.get_all_regions()
    if 'filter_institution' in request.session:
        del request.session['filter_institution']

    return render(request, 'CMS/institution_list.html',
                  {'institutions': cms_utils.apply_pagination(request, institutions_list),
                   'count': -1, 'sort_by': sort_by, 'order': order, 'regions': regions_list})

@login_required(login_url='/login')
def add_institution(request):
    """
    Add institution page to add institution details
    """
    institution_obj = Institutions()
    if request.method == 'POST':
        add_institute_form = AddInstituteForm(request.POST)
        if add_institute_form.is_valid():
            add_institute_form_data = add_institute_form.cleaned_data

            if institution_obj.save_institution(add_institute_form_data):
                messages.success(request, "The institution is added successfully")
                return HttpResponseRedirect('/institution_list/')
            else:
                messages.error(request, "Something went wrong. Please try again.")
                return render(request, 'CMS/add_institution.html',
                              {'form': add_institute_form})
        else:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'CMS/add_institution.html',
                          {'form': add_institute_form})
    else:
        add_institute_form = AddInstituteForm()
        return render(
            request,
            'CMS/add_institution.html',
            {'form': add_institute_form}
        )

@login_required(login_url='/login')
def institution_detail(request, institution_id):
    """
    The static html page for theme customisation
    """
    institution_obj = Institutions()
    institution = institution_obj.get_institution_by_id(institution_id)
    if institution is not None:
        dynamic_content_obj = Dynamic_Contents()
        contents = dynamic_content_obj.get_contents_by_content_id(institution.id)
    else:
        messages.error(request, "Something went wrong. Please try again.")
        return HttpResponseRedirect('/institution_list/')
    return render(request, 'CMS/institution_detail.html',
                  {'institution': institution, 'contents': contents})

@login_required(login_url='/login')
def delete_institution(request, institution_id):
    """
    The static html page for delete the institution
    """
    institution_obj = Institutions()
    if institution_obj.delete_institute(institution_id):
        messages.success(request, "The institution is deleted successfully")
    else:
        messages.error(request, "Something went wrong or the institution does not exist.")
    return HttpResponseRedirect('/institution_list/')

@login_required(login_url='/login')
def edit_institution(request, institution_id):
    """
    Add institution page to add institution details
    """
    institution_obj = Institutions()
    institution = institution_obj.get_institution_by_id(institution_id)
    if institution is not None:
        dynamic_content_obj = Dynamic_Contents()
        contents = dynamic_content_obj.get_contents_by_content_id(institution.id)
    else:
        messages.error(request, "Something went wrong. Please try again.")
        return HttpResponseRedirect('/institution_list/')

    if request.method == 'POST':
        edit_institute_form = AddInstituteForm(request.POST)

        if edit_institute_form.is_valid():
            edit_institute_form_data = edit_institute_form.cleaned_data
            edit_institute_form_data['id'] = institution.id

            if institution_obj.save_institution(edit_institute_form_data):
                messages.success(request, "The institution is updated successfully")
                return HttpResponseRedirect('/institution_list/')
            else:
                messages.error(request, "Something went wrong. Please try again.")
                return render(request, 'CMS/edit_institution.html',
                              {'form': edit_institute_form})
        else:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'CMS/edit_institution.html',
                          {'form': edit_institute_form})
    else:
        edit_institute_form = cms_utils.add_initial_values(institution, contents)
        return render(
            request,
            'CMS/edit_institution.html',
            {
                'form': edit_institute_form,
                'institution': institution,
                'contents': contents})

@login_required(login_url='/login')
def edit_preview(request):
    """Edit theme preview"""
    if 'business_partner_id' in request.POST:
        business_partner = Business_Partners().get_business_partner(
            request.POST['business_partner_id']
        )
    if request.method == 'POST':
        edit_theme_from = EditThemeForm(request.POST, request.FILES)
        if edit_theme_from.is_valid():
            edit_theme_form_data = edit_theme_from.cleaned_data

            upload_path = os.path.join(settings.EDIT_MEDIA_ROOT, business_partner.name)
            if os.path.exists(upload_path):
                shutil.rmtree(upload_path)
            else:
                os.makedirs(upload_path)

            if edit_theme_form_data.get("logo") is not None \
                    and edit_theme_form_data.get("splash_screen") is not None \
                    and edit_theme_form_data.get("app_icon") is not None:
                return HttpResponse(cms_utils.check_image_dimensions(request,
                                                                     edit_theme_form_data, business_partner),
                                    content_type='application/json')
            elif edit_theme_form_data.get("splash_screen") is not None:
                splash_screen_width, splash_screen_height = get_image_dimensions(
                    edit_theme_form_data.get("splash_screen"))
                if splash_screen_width >= settings.MIN_UPLOAD_DIMENSIONS['splash_screen']['width'] \
                        and splash_screen_height >= \
                                settings.MIN_UPLOAD_DIMENSIONS['splash_screen']['height']:
                    uploaded_files = dict()
                    uploaded_files['splash_screen'] = cms_utils.upload_file(request.FILES['splash_screen'], upload_path)
                    return HttpResponse(json.dumps({
                        'theme_color': request.POST['theme_color'],
                        'font_color': request.POST['font_color'],
                        'logo_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.logo,
                        'app_icon_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.app_icon,
                        'splash_screen_path': cms_utils.get_splash_screen_path(business_partner.name, uploaded_files['splash_screen'])
                    }), content_type='application/json')
                else:
                    return HttpResponse(
                        json.dumps({'Error-dimension-splash': 'Please check the image dimensions'}),
                        content_type='application/json'
                    )
            elif edit_theme_form_data.get("app_icon") is not None:
                uploaded_files = dict()
                uploaded_files['app_icon'] = cms_utils.upload_file(request.FILES['app_icon'], upload_path)
                return HttpResponse(json.dumps({
                    'theme_color': request.POST['theme_color'],
                    'font_color': request.POST['font_color'],
                    'logo_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.logo,
                    'app_icon_path': '/static/CMS/uploads/'+business_partner.name+'/' + uploaded_files['app_icon'],
                    'splash_screen_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.splash_screen
                }), content_type='application/json')
            elif edit_theme_form_data.get("fav_icon") is not None:
                uploaded_files = dict()
                uploaded_files['fav_icon'] = cms_utils.upload_file(request.FILES['fav_icon'], upload_path, 'fav_icon.ico')
                return HttpResponse(json.dumps({
                    'theme_color': request.POST['theme_color'],
                    'font_color': request.POST['font_color'],
                    'logo_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.logo,
                    'app_icon_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.app_icon,
                    'fav_icon_path': uploaded_files['fav_icon'],
                    'splash_screen_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.splash_screen
                }), content_type='application/json')
            elif edit_theme_form_data.get("logo") is not None:
                logo_width, logo_height = get_image_dimensions(edit_theme_form_data.get("logo"))
                if logo_width >= settings.MIN_UPLOAD_DIMENSIONS['logo']['width'] \
                        and logo_height >= settings.MIN_UPLOAD_DIMENSIONS['logo']['height']:
                    if os.path.exists(upload_path):
                        shutil.rmtree(upload_path)
                    else:
                        os.makedirs(upload_path)
                    uploaded_files = dict()
                    uploaded_files['logo'] = cms_utils.upload_file(request.FILES['logo'], upload_path)
                    return HttpResponse(json.dumps({
                        'theme_color': request.POST['theme_color'],
                        'font_color': request.POST['font_color'],
                        'logo_path': '/static/CMS/edit_theme/'+business_partner.name+'/'+uploaded_files['logo'],
                        'app_icon_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.app_icon,
                        'splash_screen_path': '/static/CMS/uploads/'+business_partner.name+'/'
                                              + business_partner.theme_of.splash_screen,
                    }), content_type='application/json')
                else:
                    return HttpResponse(
                        json.dumps({'Error-dimension-logo': 'Please check the image dimensions'}),
                        content_type='application/json'
                    )

            return HttpResponse(json.dumps({
                'theme_color': request.POST['theme_color'],
                'font_color': request.POST['font_color'],
                'logo_path': '/static/CMS/uploads/'+ business_partner.name+'/'+business_partner.theme_of.logo,
                'app_icon_path': '/static/CMS/uploads/'+business_partner.name+'/' + business_partner.theme_of.app_icon,
                'fav_icon_path': business_partner.theme_of.fav_icon,
                'splash_screen_path': '/static/CMS/uploads/'+business_partner.name+'/'
                                      +business_partner.theme_of.splash_screen,
                }), content_type='application/json')
        else:
            return HttpResponse(
                json.dumps({'Error-invalid': 'Something went wrong. Please try again'}),
                content_type='application/json'
            )

@login_required(login_url='/login')
def cancel_edit(request, business_partner_id):
    """Remove temporary uploaded files on Cancel Edit """
    print request.method
    business_partner_obj = Business_Partners()
    business_partner = business_partner_obj.get_business_partner(business_partner_id)
    upload_path = os.path.join(settings.EDIT_MEDIA_ROOT, business_partner.name)
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path, True)
    return HttpResponseRedirect('/business_partner_list/')


def get_institutions(request, language='en', country_code=''):
    """
    Fetch all the institutions with the data in local languages
     and returns in the json format to be used by the mobile app
    """
    if request.method == 'GET' and language is not None and country_code is not None:
        institution_obj = Institutions()
        institutions_list = institution_obj.get_institutions_in_language(language, country_code)
        all_institutions = []
        for institution in institutions_list:
            all_institutions.append({
                'id': institution.id,
                'name': institution.name + ' (' + institution.postal_address + ')',
                'direct_claim_allowed': institution.direct_claim_allowed,
                'contact_no': institution.contact_no,
                'email': institution.email,
                'postal_address': institution.postal_address,
                'instructional_text': institution.instructional_text,
                'region': institution.region
            })
        return HttpResponse(json.dumps({'institutions':all_institutions}), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse("Something went wrong. Please try again.")

@login_required(login_url='/login')
def fetch_business_partners(request):
    """
    Fetch the list of all the business partners from the PORT
    and then checks if it is there in the CMS db
    if not present then saves it in the DB
    """
    api_url = "https://platform.livemore.life:51001/api/partners"
    all_business_partners = get_json_data_from_api(api_url)

    if Business_Partners.update_business_partner_list(all_business_partners):
        messages.success(request, "Business partner list is updated successfully.")
    else:
        messages.error(request, "No new business partner is added.")

    return HttpResponseRedirect('/business_partner_list/')


def get_json_data_from_api(api_url):
    """Send request to the given API and returns the response
    The response is in json format so it is returned after decoded"""
    headers = {'Authorization': cms_utils.get_authorization_key()}
    response_data = requests.get(api_url, headers=headers, verify=False)
    if response_data.status_code == 200:
        response = json.loads(response_data.content)
    else:
        response = None
    return response

@login_required(login_url='/login')
def delete_bp_theme(request, business_partner_id):
    """
    The static html page for delete the business partner and it's theme
    """
    business_partner_obj = Business_Partners()
    if business_partner_obj.delete_business_partner(business_partner_id):
        messages.success(request, "The business partner and it's theme is deleted successfully")
    else:
        messages.error(request, "Something went wrong or the business partner does not exist.")
    return HttpResponseRedirect('/business_partner_list/')


def get_version_updates(request):
    """
    Fetch all the institutions with the data in local languages
     and returns in the json format to be used by the mobile app
    """
    if request.method == 'GET':
        version_update_obj = Version_Updates()
        if 'iPhone' in request.META['HTTP_USER_AGENT']:
            version_info = version_update_obj.get_version_info('iOS')
        elif 'Android' in request.META['HTTP_USER_AGENT']:
            version_info = version_update_obj.get_version_info('android')
        else:
            version_info = None

        if version_info is not None:
            return HttpResponse(
                json.dumps({'success': True,
                            'version':{
                                'LatestVersion': version_info.latest_version,
                                'MinimumVersion': version_info.minimum_version}}),
                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def create_default_version_updates(request):
    """We need to update the version information list for Android and iOS separately,
    We are running migration to enter the dummy version information for testing and demo purpose"""
    if request.method == 'GET':
        ios = Version_Updates.objects.filter(os_type="iOS").first()
        if ios is None:
            Version_Updates.objects.create(
                os_type="iOS",
                minimum_version="1.0.0",
                latest_version="1.0.0")
        else:
            Version_Updates.objects.filter(os_type="iOS").update(
                minimum_version="1.0.0",
                latest_version="1.0.0")

        android = Version_Updates.objects.filter(os_type="android").first()
        if android is None:
            Version_Updates.objects.create(
                os_type="android",
                minimum_version="1.0.0",
                latest_version="1.0.0")
        else:
            Version_Updates.objects.filter(os_type="android").update(
                minimum_version="1.0.0",
                latest_version="1.0.0")
        messages.success(request, "Versions are updated.")
        return HttpResponseRedirect('/dashboard/')
    else:
        messages.error(request, "Versions are not updated.")
        return HttpResponseRedirect('/dashboard/')


def check_and_upload(request, theme_form_data, fav_icon, business_partner):
    """
    It checks the dimensions and uploads the file
    """
    logo = theme_form_data.get("logo")
    splash_screen = theme_form_data.get("splash_screen")
    logo_width, logo_height = get_image_dimensions(logo)
    splash_screen_width, splash_screen_height = get_image_dimensions(splash_screen)

    if logo_width >= settings.MIN_UPLOAD_DIMENSIONS['logo']['width']\
            and logo_height >= settings.MIN_UPLOAD_DIMENSIONS['logo']['height']\
            and splash_screen_width >= settings.MIN_UPLOAD_DIMENSIONS['splash_screen']['width']\
            and splash_screen_height >= settings.MIN_UPLOAD_DIMENSIONS['splash_screen']['height']:
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, business_partner.name)):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, business_partner.name), True)
        uploaded_files = dict()
        uploaded_files['logo'] = cms_utils.upload_file(
            request.FILES['logo'],
            os.path.join(settings.MEDIA_ROOT, business_partner.name)
        )
        uploaded_files['splash_screen'] = cms_utils.upload_file(
            request.FILES['splash_screen'],
            os.path.join(settings.MEDIA_ROOT, business_partner.name)
        )
        if fav_icon is not None:
            uploaded_files['fav_icon'] = cms_utils.upload_file(
                request.FILES['fav_icon'],
                os.path.join(settings.MEDIA_ROOT, business_partner.name),
                'fav_icon.ico'
            )
        else:
            uploaded_files['fav_icon'] = None

        uploaded_files['app_icon'] = cms_utils.upload_file(
            request.FILES['app_icon'],
            os.path.join(settings.MEDIA_ROOT, business_partner.name)
        )

        cms_utils.handle_ios_uploads(request, business_partner.name)
        cms_utils.handle_android_uploads(request, business_partner.name)
        return uploaded_files
    else:
        return False

@login_required(login_url='/login')
def search_business_partners(request):
    """To search and render the searched business partner listing page"""

    business_partner_obj = Business_Partners()
    business_partners_list = business_partner_obj.get_all_business_partners()
    if request.method == 'POST' or 'search_bp' in request.session:
        if 'search' in request.POST:
            if 'search_bp' in request.session:
                del request.session['search_bp']
            request.session['search_bp'] = request.POST['search']
            search_bp = request.POST['search']
        else:
            search_bp = request.session['search_bp']
        business_partners_list = business_partner_obj.get_searched_business_partners(
            search_bp)

    return render(
        request,
        'CMS/business_partner_list.html',
        {
            'business_partner_list': cms_utils.apply_pagination(request, business_partners_list),
            'business_partner_list_tab': 'active',
            'media_url': settings.MEDIA_ROOT,
            'count': len(business_partners_list)
        }
    )

@login_required(login_url='/login')
def search_institutions(request):
    """To search and render the searched institutions listing page"""

    institution_obj = Institutions()
    institutions_list = institution_obj.get_all_institutions()
    regions_list = institution_obj.get_all_regions()
    if 'filter_institution' in request.session:
        del request.session['filter_institution']

    if request.method == 'POST' or 'search_institution' in request.session:
        if 'search' in request.POST:
            if 'search_institution' in request.session:
                del request.session['search_institution']
            request.session['search_institution'] = request.POST['search']
            search_institution = request.POST['search']
        else:
            search_institution = request.session['search_institution']
        institutions_list = institution_obj.get_searched_institutions(
            search_institution)

    return render(request, 'CMS/institution_list.html',
                  {'institutions': cms_utils.apply_pagination(request, institutions_list),
                   'count': len(institutions_list), 'regions': regions_list})

@login_required(login_url='/login')
def filter_institutions(request):
    """
    Fetches the institutions for the selected regions and returns
    """
    institution_obj = Institutions()
    institutions_list = institution_obj.get_all_institutions()
    regions_list = institution_obj.get_all_regions()
    if request.method == 'POST' or 'filter_institution' in request.session:
        if 'region' in request.POST:
            if 'filter_institution' in request.session:
                del request.session['filter_institution']
            request.session['filter_institution'] = request.POST.getlist('region')
            filter_institution = request.POST.getlist('region')
        else:
            filter_institution = request.session['filter_institution']
        institutions_list = institution_obj.get_filtered_institutions(filter_institution)

    return render(request, 'CMS/institution_list.html',
                  {'institutions': cms_utils.apply_pagination(request, institutions_list),
                   'count': -1, 'regions': regions_list})

@login_required(login_url='/login')
def change_versions(request, os_type='android'):
    """To render the change version of mobile based on the os and process the functionality"""
    version_update_obj = Version_Updates()
    version_info = version_update_obj.get_version_info(os_type)
    if version_info is not None:
        os_type = version_info.os_type

    if request.method == 'POST':
        change_versions_form = ChangeVersionForm(request.POST)
        if change_versions_form.is_valid():
            change_versions_form_data = change_versions_form.cleaned_data
            version_update_obj.save_version_info(os_type, change_versions_form_data)
            messages.success(request, "Version is updated successfully.")
            return HttpResponseRedirect('/dashboard/')
    else:
        change_versions_form = cms_utils.add_version_initial_values(version_info, ChangeVersionForm())

    return render(request, 'CMS/change_versions.html',
                  {'form': change_versions_form, 'os_type': os_type})
