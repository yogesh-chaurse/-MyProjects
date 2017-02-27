"""
This script has the basic functions which will be used globally in the application
"""
from MagPie import settings
import base64
import json
import os
import time
import requests


def upload_file(file_obj, path):
    """Upload the given file and returns its name"""

    # Checking if path exists or not. If not then create a directory for it
    if not os.path.exists(path):
        os.makedirs(path)

    file_obj.name = rename_duplicate_file(file_obj.name, path)

    # Opening/Creating the file and changing it's mode to write the data in it
    dest = open(os.path.join(path, file_obj.name), 'wb')

    # Writing the byte data in the file to create/upload the image
    for chunk in file_obj.chunks():
        dest.write(chunk)

    # closing the file after writing it completely
    dest.close()
    return file_obj.name


def rename_duplicate_file(file_name, path):
    """Rename the file if the duplicity occurs"""

    if os.path.exists(os.path.join(path, file_name)):
        split_name = file_name.split(".")
        file_name = '%s_%s.%s' % (split_name[0], int(time.time()), split_name[1])
    return file_name


def check_file_size(uploaded_file, size):
    """Check the file size by given params"""
    if int(uploaded_file.size) > size:
        return False
    else:
        return True


def get_business_partner_theme(request):
    """Used for making API call to CMS for getting Business Partners theme"""
    business_partner_id = get_business_partner_id(request)
    if business_partner_id == '' or business_partner_id is None:
        business_partner_id = str(business_partner_id)
    headers = {'content-type': 'application/json'}
    url = 'https://' if request.is_secure() else 'http://' +\
           settings.API_URL+'/get_web_theme/' + business_partner_id
    response = requests.get(
        url, headers=headers
    )
    return response.json()


def post_details_in_api(details):
    """
    Used to post the insurance claim details and
    checks for the response if it is posted successfully
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode("james.haig@magpieint.com" + ":" + "Haigman02")
    }
    url = "https://magpie.desk.com/api/v2/cases"
    response = requests.post(url, details, headers=headers)
    return response.status_code


def login_api(login_details):
    """
    Sends the user credentials to the PIB
    and after authentication, returns the access token
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode("lifemanager" + ":" + "xxLsaWGz7D2R4Rtg")
    }
    url = "https://api.infobank.me/oauth/token"
    response = requests.post(url, login_details, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_business_partner_id(request):
    if 'user_id' in request.session:
        user_details = fetch_user_details(request.session['user_id'])
        if user_details is not None and 'data' in user_details:
            if 'user_details' in request.session:
                del request.session['user_details']
            request.session['user_details'] = user_details
            if 'businessPartner' in user_details['data']:
                if 'uuid' in user_details['data']['businessPartner']:
                    return user_details['data']['businessPartner']['uuid']
    else:
        return ''


def fetch_user_details(user_id):
    """
    Fetch the list of all the business partners from the PORT
    and then checks if it is there in the CMS db
    if not present then saves it in the DB
    """
    api_url = "https://platform.livemore.life:51001/api/" + str(user_id) + "/details"
    user_detail = get_json_data_from_api(api_url)
    return user_detail


def get_json_data_from_api(api_url):
    """Send request to the given API and returns the response
    The response is in json format so it is returned after decoded"""
    headers = {'Authorization': get_authorization_key(), 'X-Port': '2222'}
    response_data = requests.get(api_url, headers=headers, verify=False)
    if response_data.status_code == 200:
        response = json.loads(response_data.content)
    else:
        response = None
    return response


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


def add_initial_values(information, form_obj):
    """ To add pre filled values in the edit form """
    information_form = form_obj
    if 'forename' in information_form.fields:
        information_form.fields['forename'].initial = check_key_exist('forename', information)
        information_form.fields['surname'].initial = check_key_exist('surname', information)
        information_form.fields['mobile'].initial = check_key_exist('mobile', information)

    if information is not None:
        address_information = information['address']
    else:
        address_information = information
    information_form.fields['addressLine1'].initial = check_key_exist('addressline1', address_information)
    information_form.fields['addressLine2'].initial = check_key_exist('addressLine2', address_information)
    information_form.fields['addressLine3'].initial = check_key_exist('addressLine3', address_information)
    information_form.fields['city'].initial = check_key_exist('city', address_information)
    information_form.fields['country'].initial = check_key_exist('country', address_information)
    information_form.fields['postcode'].initial = check_key_exist('postcode', address_information)
    information_form.fields['email'].initial = check_key_exist('email', information)
    return information_form


def check_key_exist(key, data):
    """
    Checks if the given key exists in the given data
    then return the value of that key else returns None
    """
    if data is not None:
        if key in data:
            return data[key]
    return 'N/A'


def get_personal_info(request):
    """
    Fetches the personal information from the session
    or from the API and then return it's data
    """
    user_details = None
    if 'user_details' in request.session:
        user_details = request.session['user_details']
    elif 'user_id' in request.session:
        user_details = fetch_user_details(request.session['user_id'])
    if user_details is not None:
        return user_details['data']['subscriber']
    else:
        return user_details


def get_subscription_info(request):
    """
    Fetches the subscription information from the session
    or from the API and then return it's data
    """
    user_details = None
    if 'user_details' in request.session:
        user_details = request.session['user_details']
    elif 'user_id' in request.session:
        user_details = fetch_user_details(request.session['user_id'])
    if user_details is not None:
        return user_details['data']['subscription']
    else:
        return user_details


def get_help_data(request):
    """
    Fetches the help email and phone number from the session
    or from the API and then return it's data
    """
    user_details = None
    if 'user_details' in request.session:
        user_details = request.session['user_details']
    elif 'user_id' in request.session:
        user_details = fetch_user_details(request.session['user_id'])
    if user_details is not None:
        return user_details['data']['businessPartner']
    else:
        return user_details


def user_activation(pin):
    """
    Request magpie server with authorization key and pin
    and fetches the response
    """
    headers = {'Authorization': get_authorization_key(), 'X-Port': '2222'}
    api_url = 'https://platform.livemore.life:51001/api/activate?code=' + pin + '&deviceToken=2222'
    response = requests.post(api_url, headers=headers, verify=False)
    return json.loads(response.content)