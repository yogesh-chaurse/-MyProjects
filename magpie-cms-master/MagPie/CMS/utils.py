"""
This script has the basic functions which will be used globally in the application
"""
from MagPie import settings
from PIL import Image
from CMS.forms import AddInstituteForm
from django.core.files.images import get_image_dimensions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, json, time, shutil, requests, base64


def get_os_specifications(os_name, selected_type=None):
    """Returns the OS specification as per the argument passed"""
    os_type = {
        'android': {
            'drawable-hdpi': {
                'logo': {'width': 140,
                         'height': 40,
                         'file_name': 'icon.png'}
            },
            'drawable-xhdpi': {
                'logo': {'width': 187,
                         'height': 53,
                         'file_name': 'icon.png'},
                },
            'drawable-xxhdpi': {
                'logo': {'width': 280,
                         'height': 80,
                         'file_name': 'icon.png'},
                }
        },
        'ios': {
            'logo': {
                'upload_path': 'ios/appicons',
                'resize_paths': {
                    '200x40': {'width': 200,
                                'height': 40,
                                'file_name': 'icon.png'},
                }
            }
        }
    }

    if os_type.has_key(os_name):
        if selected_type is not None:
            return os_type[os_name][selected_type]
        else:
            return os_type[os_name]
    else:
        return None


def handle_ios_uploads(request, business_partner_slug):
    """To handle the image upload functionality for IOS"""
    folder_path = os.path.join(settings.MEDIA_ROOT, business_partner_slug)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    file_type = []
    files = []
    if 'logo' in request.FILES:
        files.append(request.FILES['logo'])
        file_type.append('logo')

    counter = 0
    for key in files:
        os_folder_info = get_os_specifications('ios', file_type[counter])
        os_folder_path = os.path.join(folder_path, os_folder_info['upload_path'])
        resize_paths = os_folder_info['resize_paths']
        for resize_path_key, resize_path_value in resize_paths.iteritems():
            file_name = upload_file(key, os_folder_path, resize_path_value['file_name'])

            resize_image(os.path.join(os_folder_path, file_name),
                         resize_path_value['width'],
                         resize_path_value['height'])

        counter = counter + 1
    return None


def handle_android_uploads(request, business_partner_slug):
    """To handle the image upload functionality for Android"""
    # Creating the folder path and saving into a variable

    files = []
    if 'logo' in request.FILES:
        files.append(request.FILES['logo'])

    folder_path = os.path.join(settings.MEDIA_ROOT, business_partner_slug, 'android')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path, True)
    else:
        os.mkdir(folder_path)
    for image_file in files:
        os_folder_info = get_os_specifications('android')
        for folder_name, folder_content in os_folder_info.iteritems():
            upload_path = os.path.join(folder_path, folder_name)
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            for key, value in folder_content.iteritems():
                file_name = upload_file(image_file, upload_path, value['file_name'])
                resize_image(os.path.join(upload_path, file_name),
                             value['width'],
                             value['height'])
    return None


def resize_image(file_path, width, height):
    """To resize the images for Android and IOS"""
    image = Image.open(file_path)
    image = image.resize((width, height), Image.ANTIALIAS)
    image.save(file_path, 'png', quality=90)


def upload_file(file_obj, path, file_name=None):
    """To upload the file and returns the file name"""
    # Checking if path exists or not. If not then create a directory for it
    if not os.path.exists(path):
        os.makedirs(path)

    if file_name is None:
        file_obj.name = rename_duplicate_file(file_obj.name, path)
    else:
        file_obj.name = file_name

    # Opening/Creating the file and changing it's mode to write the data in it
    dest = open(os.path.join(path, file_obj.name), 'wb')

    # Writing the byte data in the file to create/upload the image
    for chunk in file_obj.chunks():
        dest.write(chunk)

    # closing the file after writing it completely
    dest.close()
    return file_obj.name


def rename_duplicate_file(file_name, path):
    """To rename the file if file name already exists"""
    if os.path.exists(os.path.join(path, file_name)):
        split_name = file_name.split(".")
        file_name = '%s_%s.%s' % (split_name[0], int(time.time()), split_name[1])
    return file_name


def get_immediate_subdirectories(a_dir):
    """To get the immediate subdirectories of a particular root directory"""
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def edit_android_uploads(request, business_partner_slug, file_type):
    """To handle the splash screen, app logo and logo upload functionality for Android during edit theme  """
    files = [request.FILES[file_type]]
    folder_path = os.path.join(settings.MEDIA_ROOT, business_partner_slug, 'android')
    for image_file in files:
        os_folder_info = get_os_specifications('android')
        for folder_name, folder_content in os_folder_info.iteritems():
            upload_path = os.path.join(folder_path, folder_name)
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            file_name = upload_file(image_file, upload_path, folder_content[file_type]['file_name'])
            resize_image(os.path.join(upload_path, file_name),
                         folder_content[file_type]['width'],
                         folder_content[file_type]['height'])
    return None


def remove_android_files(slug, file_type):
    """ Removes android logo/Splash_screens while edit theme"""
    dir_structure = ['drawable-hdpi', 'drawable-xhdpi', 'drawable-xxhdpi']
    for folder in dir_structure:
        folder_path = os.path.join(settings.MEDIA_ROOT, slug, 'android')
        folder_path = os.path.join(folder_path, folder, file_type)
        if os.path.isfile(folder_path):
            os.remove(folder_path)
    return None


def remove_ios_files(slug, file_type):
    """ Removes ios logo/Splash_screens while edit theme"""
    folder_path = os.path.join(settings.MEDIA_ROOT, slug, 'ios')
    folder_path = os.path.join(folder_path, file_type)
    if os.path.isfile(folder_path):
        shutil.rmtree(folder_path)
    return None


def remove_orignal_files(slug, filename):
    """ Removes ios/android  logo/Splash_screens original files while edit theme"""
    orignal_file_path = os.path.join(settings.MEDIA_ROOT, slug, str(filename))
    if os.path.isfile(orignal_file_path):
        os.remove(orignal_file_path)
    return None


def add_initial_values(institution, contents):
    """ To add pre filled values in the edit form """
    edit_institute_form = AddInstituteForm()
    edit_institute_form.fields['name_en'].initial = institution.name
    edit_institute_form.fields['name_es'].initial = contents['content_es']
    edit_institute_form.fields['name_zh'].initial = contents['content_zh']
    edit_institute_form.fields['allow_reorder_cards'].initial = institution.direct_claim_allowed
    edit_institute_form.fields['contact_no'].initial = institution.contact_no
    edit_institute_form.fields['email'].initial = institution.email
    edit_institute_form.fields['postal_address'].initial = institution.postal_address
    edit_institute_form.fields['instructional_text'].initial = institution.instructional_text
    edit_institute_form.fields['region'].initial = institution.region
    return edit_institute_form


def check_image_dimensions(request, edit_theme_form_data, business_partner):
    """
    Checks the image dimension for preview functionality for add / edit theme
    and returns the json response
    """
    min_upload_dimensions = settings.MIN_UPLOAD_DIMENSIONS

    upload_path = os.path.join(settings.EDIT_MEDIA_ROOT, business_partner.name)

    logo_width, logo_height = get_image_dimensions(edit_theme_form_data.get("logo"))
    splash_screen_width, splash_screen_height = get_image_dimensions(
        edit_theme_form_data.get("splash_screen"))

    if logo_width >= \
            min_upload_dimensions['logo']['width'] \
            and \
                    logo_height >= \
                    min_upload_dimensions['logo']['height'] \
            and \
                    splash_screen_width >= \
                    min_upload_dimensions['splash_screen']['width'] \
            and \
                    splash_screen_height >= \
                    min_upload_dimensions['splash_screen']['height']:
        uploaded_files = dict()
        uploaded_files['logo'] = upload_file(request.FILES['logo'], upload_path)
        uploaded_files['splash_screen'] = upload_file(request.FILES['splash_screen'], upload_path)
        uploaded_files['app_icon'] = upload_file(request.FILES['app_icon'], upload_path)
        if 'fav_icon' in request.FILES and request.FILES['fav_icon'] is not None:
            uploaded_files['fav_icon'] = upload_file(request.FILES['fav_icon'], upload_path, 'fav_icon.ico')
        else:
            uploaded_files['fav_icon'] = None

        theme_set = {
            'theme_color': request.POST['theme_color'],
            'font_color': request.POST['font_color'],
            'logo_path': '/static/CMS/edit_theme/'
                         + business_partner.name
                         + '/' +
                         uploaded_files['logo'],
            'app_icon_path': '/static/CMS/edit_theme/'
                             + business_partner.name
                             + '/' +
                             uploaded_files['app_icon'],
            'fav_icon_path': uploaded_files['fav_icon'],
            'splash_screen_path': get_splash_screen_path(business_partner.name,
                                                         uploaded_files['splash_screen'])
        }
        return json.dumps(theme_set)

    else:
        if (logo_width < min_upload_dimensions['logo']['width'] \
            or logo_height < min_upload_dimensions['logo']['height']) \
                and (splash_screen_width < min_upload_dimensions['splash_screen']['width']
                     or splash_screen_height < min_upload_dimensions['splash_screen']['height']):
            return json.dumps({'Error-dimension': 'Please check the image dimensions'})

        elif splash_screen_width < min_upload_dimensions['splash_screen']['width'] \
                or splash_screen_height < min_upload_dimensions['splash_screen']['height']:
            return json.dumps({'Error-dimension-splash': 'Please check the image dimensions'})

        else:
            return json.dumps({'Error-dimension-logo': 'Please check the image dimensions'})


def get_splash_screen_path(business_partner_name, file_name):
    """
    Format and returns the splash screen path
    """
    return '/static/CMS/edit_theme/' + business_partner_name + '/' + file_name


def get_authorization_key():
    """
    fetches the access token and token type and returns the authorization key
    """
    response_data = requests.post(
        url='https://platform.livemore.life:51001/oauth/token',
        data={'grant_type': 'client_credentials', 'scope': 'magpie'},
        verify=False,
        headers={'Authorization': 'Basic ' + base64.b64encode('magpie:13wFtQ1L_ISVGNJTAjPQoJZ7YDF5n6Ka')})
    response = json.loads(response_data.content)
    authorization_key = response['token_type'].title() + ' ' + response['access_token']
    return authorization_key


def apply_pagination(request, data_list):
    """
    The function takes the complete list an an argument
    and then apply pagination in it and returns it
    """
    paginator = Paginator(data_list, 10)  # Show 10 business partners per page

    page = request.GET.get('page')
    try:
        data_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_pages = paginator.page(paginator.num_pages)

    return data_pages

def add_version_initial_values(information, form_obj):
    """ To add pre filled values in the edit form """
    latest_version = minimum_version = None
    if information is not None:
        latest_version = information.latest_version
        minimum_version = information.minimum_version
    information_form = form_obj
    information_form.fields['latest_version'].initial = latest_version
    information_form.fields['minimum_version'].initial = minimum_version
    return information_form
