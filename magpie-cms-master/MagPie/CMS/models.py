"""The module is created to write the business logic of the application"""
from django.db import models
from django_countries import countries

class Business_Partners(models.Model):
    """The operations related to business partners will be here"""

    objects = models.Manager()

    business_partner_id = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

    @classmethod
    def get_all_business_partners(cls):
        """Return s the list of all the business partners"""
        business_partners = Business_Partners.objects.order_by('-created')
        return business_partners

    @classmethod
    def get_business_partner(cls, business_partner_id):
        """Returns the business partner matched with the id"""
        business_partner = Business_Partners.objects.filter(id=business_partner_id).first()
        return business_partner

    @classmethod
    def get_business_partner_by_id(cls, business_partner_id):
        """Returns the business partner matched with the business_partner_id"""
        business_partner = Business_Partners.objects.filter(
            business_partner_id=business_partner_id).first()
        return business_partner

    @classmethod
    def update_business_partner_list(cls, all_business_partners):
        """
        Checks if the business partner is not present in the DB
        then create a new record else do nothing
        """
        is_added = 0
        if all_business_partners is not None and 'data' in all_business_partners:
            for business_partner in all_business_partners['data']:
                check_bp = cls.get_business_partner_by_id(business_partner['uuid'])
                if check_bp is None:
                    cls.create_business_partners(business_partner)
                    is_added = 1
        if is_added == 1:
            return True
        else:
            return False

    @classmethod
    def create_business_partners(cls, business_partner_data):
        """
        Create a new business partner in the DB
        """
        cls.objects.create(
            name=business_partner_data['name'],
            business_partner_id=business_partner_data['uuid'])

    @classmethod
    def delete_business_partner(cls, business_partner_id):
        """
        Deletes the business partner and its related theme and returns true or false
        """
        business_partner = cls.objects.filter(id=business_partner_id).first()
        if business_partner is None:
            return False
        else:
            cls.objects.filter(id=business_partner_id).delete()
            return True

    @classmethod
    def get_searched_business_partners(cls, business_partner_name):
        """
        Search the entered business partner name
        and returns the searched results in ascending order of name
        """
        return cls.objects.filter(name__icontains=business_partner_name).\
            order_by('-created')

class Themes(models.Model):
    """The operations related to themes will be here"""

    objects = models.Manager()

    business_partner = models.OneToOneField(
        Business_Partners,
        related_name='theme_of'
    )

    theme_color = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    font_color = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    logo = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    splash_screen = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    fav_icon = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    app_icon = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )

    is_deleted = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=False
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

    @classmethod
    def delete_respective_theme(cls, business_partner_id):
        """
        Deletes the respective theme of the particular business partner
        and returns true or false based on the status
        """
        theme = cls.objects.filter(business_partner_id=business_partner_id).all()
        if not theme:
            return True
        else:
            cls.objects.filter(business_partner_id=business_partner_id).delete()
            return True

class Regions(models.Model):
    """The operations related to Regions will be here"""

    objects = models.Manager()

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

class Business_Partner_Regions(models.Model):
    """The operations related to business partner regions will be here"""

    objects = models.Manager()

    business_partner = models.OneToOneField(
        Business_Partners,
        related_name='region_of'
    )

    region = models.OneToOneField(
        Regions,
        related_name='business_partner_of'
    )

    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

class Languages(models.Model):
    """The operations related to languages will be here"""

    objects = models.Manager()

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    code = models.CharField(
        max_length=5,
        blank=False,
        null=False
    )
    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

    @classmethod
    def get_language_by_code(cls, language_code):
        """Returns the language matched with the code"""
        language = cls.objects.filter(code=language_code).first()
        return language

    @classmethod
    def create_default_languages(cls):
        """Check if the languages are present in the languages table
        and insert if it is not"""
        language_en = cls.get_language_by_code('en')
        language_es = cls.get_language_by_code('es')
        language_zh = cls.get_language_by_code('zh_CN')

        if language_en is None:
            Languages.objects.create(
                name="English",
                code='en')
        if language_es is None:
            Languages.objects.create(
                name="Spanish",
                code='es')
        if language_zh is None:
            Languages.objects.create(
                name="Chinese",
                code='zh_CN')

    @classmethod
    def get_language_id_by_code(cls, language_code):
        """Returns the language id matched with the code"""
        language = cls.objects.filter(code=language_code).first()
        return language.id

class Institutions(models.Model):
    """The operations related to institutions will be here"""

    objects = models.Manager()

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    direct_claim_allowed = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )
    contact_no = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    email = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    postal_address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    region = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    instructional_text = models.TextField(
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

    @classmethod
    def save_institution(cls, institution_data):
        """
        Save the institutions and its related contents
        """
        dynamic_content_obj = Dynamic_Contents()
        if 'id' in institution_data:
            cls.objects.filter(id=institution_data['id']).update(
                name=institution_data['name_en'],
                direct_claim_allowed=bool(institution_data['allow_reorder_cards']),
                contact_no=institution_data['contact_no'],
                email=institution_data['email'],
                postal_address=institution_data['postal_address'],
                instructional_text=institution_data['instructional_text'],
                region=institution_data['region'])
            dynamic_content_obj.update_in_local_languages(institution_data['id'], institution_data)
            return True
        else:
            institution_obj = cls.objects.create(
                name=institution_data['name_en'],
                direct_claim_allowed=bool(institution_data['allow_reorder_cards']),
                contact_no=institution_data['contact_no'],
                email=institution_data['email'],
                postal_address=institution_data['postal_address'],
                instructional_text=institution_data['instructional_text'],
                region=institution_data['region'],
            )
            if institution_obj.pk:
                dynamic_content_obj.save_in_local_languages(institution_obj.pk, institution_data)
                return True
            else:
                return False

    @classmethod
    def get_all_institutions(cls, sort_by='created', order='desc'):
        """Returns the list of all the institutions"""
        if order == 'asc':
            field_order = sort_by
        else:
            field_order = '-' + sort_by

        if sort_by != 'created':
            return cls.objects.filter(is_active=1).order_by(field_order, '-created')
        else:
            return cls.objects.filter(is_active=1).order_by(field_order)

    @classmethod
    def get_institution_by_id(cls, institution_id):
        """Returns the language matched with the code"""
        institution = cls.objects.filter(id=institution_id).first()
        return institution

    @classmethod
    def delete_institute(cls, institution_id):
        """ Deletes the institution and respective content from dynamic contents table
        and returns true or false"""
        institution = cls.objects.filter(id=institution_id).first()
        if institution is None:
            return False
        elif Dynamic_Contents.delete_respective_contents(institution_id):
            cls.objects.filter(id=institution_id).delete()
            return True
        else:
            return False

    @classmethod
    def get_institutions_in_language(cls, language, country_code):
        """
        Fetches the institutions list in the requested language
        and Returns it in normal format
        """
        if country_code.upper() in dict(countries):
            region_name = dict(countries)[country_code.upper()]
            institutions_en = cls.objects.filter(is_active=1, region=region_name).order_by('-modified')
        elif country_code == '':
            institutions_en = cls.objects.filter(is_active=1).order_by('-modified')
        else:
            institutions_en = dict()

        # institutions_en = cls.objects.filter(is_active=1).order_by('-modified')

        institutions_list = []
        for institution in institutions_en:
            inst = institution
            local_language_contents = Dynamic_Contents.get_contents_by_content_id(institution.id)
            if language == 'es':
                inst.name = local_language_contents['content_es']
            elif language == 'zh-cn':
                inst.name = local_language_contents['content_zh']
            inst_contact_no = inst.contact_no
            if ',' in inst_contact_no:
                contact_no = inst_contact_no.split(',')
                inst.contact_no = contact_no[0]
            elif '/' in inst_contact_no:
                contact_no = inst_contact_no.split('/')
                inst.contact_no = contact_no[0]
            else:
                contact_no = inst_contact_no
                inst.contact_no = contact_no
            institutions_list.append(inst)
        return institutions_list

    @classmethod
    def get_searched_institutions(cls, institution_name):
        """
        Search the entered business partner name
        and returns the searched results in ascending order of name
        """
        return cls.objects.filter(name__icontains=institution_name).\
            order_by('-created')

    @classmethod
    def get_filtered_institutions(cls, regions):
        """
        Search the entered business partner name
        and returns the searched results in ascending order of name
        """
        return cls.objects.filter(region__in=regions).\
            order_by('-created')

    @classmethod
    def get_all_regions(cls):
        """
        Returns all the distinct regions from the institutions table
        """
        return cls.objects.values('region').distinct()

class Dynamic_Contents(models.Model):
    """The operations related to dynamic contents will be here"""

    objects = models.Manager()

    language = models.ForeignKey(
        Languages,
        related_name='language_of'
    )
    content = models.ForeignKey(
        Institutions,
        related_name='content_of'
    )
    # These would be static.
    # For Institutes it's value would be "1"
    content_type = models.IntegerField(
        max_length=2,
        null=False,
        blank=False,
        default=1
    )
    value = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

    @classmethod
    def save_in_local_languages(cls, institution_id, local_language_data):
        """
        Saves the dynamic contents in the local languages
        """
        language_obj = Languages()

        value_es = local_language_data['name_es']
        value_zh = local_language_data['name_zh']

        if not local_language_data['name_es'] or local_language_data['name_es'] == None:
            value_es = local_language_data['name_en']

        cls.objects.create(
            language_id=language_obj.get_language_id_by_code('es'),
            content_id=institution_id,
            content_type=1,
            value=value_es
        )

        if not local_language_data['name_zh'] or local_language_data['name_zh'] == None:
            value_zh = local_language_data['name_en']

        cls.objects.create(
            language_id=language_obj.get_language_id_by_code('zh_CN'),
            content_id=institution_id,
            content_type=1,
            value=value_zh
        )

    @classmethod
    def update_in_local_languages(cls, institution_id, local_language_data):
        """
        Updates the values of dynamic contents in the local languages
        """
        language_obj = Languages()

        value_es = local_language_data['name_es']
        value_zh = local_language_data['name_zh']

        if not local_language_data['name_es'] or local_language_data['name_es'] == None:
            value_es = local_language_data['name_en']

        cls.objects.filter(
            language_id=language_obj.get_language_id_by_code('es'),
            content_id=institution_id).update(value=value_es)

        if not local_language_data['name_zh'] or local_language_data['name_zh'] == None:
            value_zh = local_language_data['name_en']

        cls.objects.filter(
            language_id=language_obj.get_language_id_by_code('zh_CN'),
            content_id=institution_id).update(value=value_zh)

    @classmethod
    def get_contents_by_content_id(cls, content_id):
        """
        Retrieve the contents from the db with the matching ids
        and returns it
        """
        language_obj = Languages()
        language_es = language_obj.get_language_id_by_code('es')
        language_zh = language_obj.get_language_id_by_code('zh_CN')
        content_es = cls.objects.filter(content_id=content_id, language_id=language_es).first()
        content_zh = cls.objects.filter(content_id=content_id, language_id=language_zh).first()
        return {
            'content_es': content_es.value, 'content_zh': content_zh.value
        }

    @classmethod
    def delete_respective_contents(cls, content_id):
        """Deletes respective contents and returns true or false"""
        contents = cls.objects.filter(content_id=content_id).all()
        if not contents:
            return False
        else:
            cls.objects.filter(content_id=content_id).delete()
            return True

class Version_Updates(models.Model):
    """The operations related to version updates will be here"""

    objects = models.Manager()

    os_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    minimum_version = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    latest_version = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    expiry = models.DateTimeField(
        editable=True,
        blank=True,
        null=True
    )

    is_forcefully = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=False
    )

    is_active = models.BooleanField(
        max_length=1,
        null=False,
        blank=False,
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True
    )

    @classmethod
    def get_version_info(cls, os_type):
        """
        Fetches the version information from the DB and returns it
        """
        return cls.objects.filter(os_type=os_type).first()

    @classmethod
    def save_version_info(cls, os_type, version_data):
        """
        Saves the version information into the DB
        """
        version = cls.objects.filter(os_type=os_type).first()
        if version is None:
            cls.objects.create(
                os_type=os_type,
                minimum_version=version_data['minimum_version'],
                latest_version=version_data['latest_version'])
        else:
            cls.objects.filter(os_type=os_type).update(
                minimum_version=version_data['minimum_version'],
                latest_version=version_data['latest_version'])
