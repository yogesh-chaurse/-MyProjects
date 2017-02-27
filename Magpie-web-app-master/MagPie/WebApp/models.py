"""The module is created to write the business logic of the application"""
from django.db import models
from MagPie import settings

import os
import json
import WebApp.utils as webapp_utils

class PersonalInformation(models.Model):
    """The operations related to personal information will be here"""

    @classmethod
    def file_operations(cls, file_name):
        """To read te json file"""
        file_to_open = open(os.path.join(settings.BASE_DIR, 'WebApp', file_name), 'r+')
        read_file = file_to_open.read()
        dict_format = json.loads(read_file)
        return dict_format['personal_information']


    @classmethod
    def save_personal_info(cls, personal_info):
        """To save the data in json format in file"""
        personal_info = {
            'forename': personal_info['forename'],
            'surname': personal_info['surname'],
            'address': {
                'addressLine1': personal_info['address']['addressLine1'],
                'addressLine2': personal_info['address']['addressLine2'],
                'addressLine3': personal_info['address']['addressLine3'],
                'city': personal_info['address']['city'],
                'country': personal_info['address']['country'],
                'postcode': personal_info['address']['postcode'],
                },
            'mobile': personal_info['mobile'],
            'email': personal_info['email']
        }

        save_personal_info = open(os.path.join(settings.BASE_DIR,
                                               'WebApp',
                                               'dummy_personal_info.json'), 'w')
        save_personal_info.write('{"personal_information": ' + json.dumps(personal_info) + '}')
        save_personal_info.close()

    @classmethod
    def check_information(cls, request):
        """
        Check the difference between the contact info provided
        and the contact info saved in the port
        """
        personal_information = webapp_utils.get_personal_info(request)
        if request.POST['addressLine1'] != personal_information['address']['addressLine1'] or \
                        request.POST['addressLine2'] != personal_information['address']['addressLine2'] or \
                        request.POST['addressLine3'] != personal_information['address']['addressLine3'] or \
                        request.POST['city'] != personal_information['address']['city'] or \
                        request.POST['country'] != personal_information['address']['country'] or \
                        request.POST['zipcode'] != personal_information['address']['zipcode'] or \
                        request.POST['email'] != personal_information['email']:
            return True
        else:
            return False


class InsuranceClaim(models.Model):
    """The operations related to insurance claim will be here"""

    @classmethod
    def file_operations(cls, dictionary_name):
        """To read te json file"""
        dict_format = json.loads(cls.open_and_read_file())
        return dict_format[dictionary_name]


    @classmethod
    def open_and_read_file(cls):
        """Returns the open and read file"""
        file_to_open = open(os.path.join(settings.BASE_DIR, 'WebApp', 'dummy_data.json'), 'r+')
        return file_to_open.read()
