from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

from authentication.models import User
from location.models import City, Location
from location.services import get_cities
from order.models import SubCategory, Category
from order.services import get_subcategories_by_category_value, get_subcategory_by_value
from performer.models import PerformingSubCategory, Language, Education
from performer.services import get_language_by_value

GENDER_CHOICES = [
    ('m', 'Мужской'),
    ('f', 'Женский'),
]
class BasicSettingsFormBase(forms.Form):
    about = forms.CharField(max_length=500,label="О себе",
                                required=False,widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    location = forms.CharField(
        label="Адрес",
        widget=forms.TextInput(attrs={"class": "location"}),required=False)
    city = forms.ChoiceField(
        label="Город",
        widget=forms.Select(attrs={"class": "selectpicker with-border city","data-live-search":"true"}),required=False)
    birth_date = forms.DateField(label="Дата рождения",required=False)
    gender = forms.ChoiceField(
                               choices= GENDER_CHOICES,
                            label="Пол",required=False)
    profile_picture = forms.ImageField(required=False)
    lat = forms.FloatField(required=False, widget=forms.HiddenInput())
    lon = forms.FloatField(required=False, widget=forms.HiddenInput())
    about.widget.attrs.update({"class": "with-border"})
    birth_date.widget.attrs.update({"class": "with-border","id":"datepicker",'autocomplete': 'off',"readonly":"readonly"})
    gender.widget.attrs.update({"class": "selectpicker"})
    profile_picture.widget.attrs.update({"class":"file-upload"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cities = get_cities()
        self.fields['city'].choices = list(
            cities.values_list('value', 'name'))
        self.fields['city'].choices.insert(0,('','Выберите город'))
    def save(self,user):
        user.profile.about = self.cleaned_data['about']
        user.profile.gender = self.cleaned_data['gender']
        user.profile.birth_date = self.cleaned_data['birth_date']
        city_value = self.cleaned_data['city']
        location_value = self.cleaned_data['location']
        if self.cleaned_data['lat'] and self.cleaned_data['lon'] and city_value:
            lat_value = float(self.cleaned_data['lat'])
            lon_value = float(self.cleaned_data['lon'])
            hh = City.objects.get(value=city_value)
            if user.profile.location:
                if lat_value!=user.profile.location.lat or lon_value != user.profile.location.lon:
                    user.profile.location.lon = lon_value
                    user.profile.location.lat = lat_value
                    user.profile.location.city = hh
                    user.profile.location.address = location_value
                    user.profile.location.save()
            else:
                l = Location(city=hh, lon=lon_value,
                        lat=lat_value, address=location_value)
                l.save()
                user.profile.location = l
        elif not city_value:
            user.profile.location = None
        return user


class BasicSettingsFormPrivatePerson(BasicSettingsFormBase):
    first_name = forms.CharField(max_length=128,label="Имя",
                                required=True)
    last_name = forms.CharField(max_length=128, label="Фамилия",
                                 required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self,user):
        user = BasicSettingsFormBase.save(self,user)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        return user

class BasicSettingsFormFirm(BasicSettingsFormBase):
    name = forms.CharField(max_length=128,label="Название фирмы",
                                required=True)
    employee_number = forms.IntegerField(max_value=200,min_value=1,required=False,label="Количество сотрудников")
    website = forms.CharField(max_length=128,required=False,label="Сайт фирмы")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self,user):
        user = BasicSettingsFormBase.save(self,user)
        user.firm.name = self.cleaned_data['name']
        user.firm.website = self.cleaned_data['website']
        user.firm.employee_number = self.cleaned_data['employee_number']
        user.firm.save()
        return user


class BasicSettingsPerformerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SUB_CATEGORY_CHOICES = []
        LANGUAGE_CHOICES = []
        categories = Category.objects.all()
        for category in categories:
            sub_categories = get_subcategories_by_category_value(category.value)
            SUB_CATEGORY_CHOICES.append(
                (category.name, [(sub_category.value, sub_category.name) for sub_category in sub_categories]))

        languages_all = Language.objects.all()
        for language in languages_all:
            LANGUAGE_CHOICES.append((language.value,language.name))
        self.fields["languages"] = forms.MultipleChoiceField(
                                         choices=LANGUAGE_CHOICES,label="Иностранные языки",required=False)
        self.fields["languages"].widget.attrs.update({"class":"selectpicker","title":"Выберите языки которыми владеете..."})

        self.fields["educational_institution_name"] = forms.CharField(max_length=128,required=False, widget=forms.TextInput(attrs={"class":"with-border"}),label="Название учебного заведения")
        self.fields["education_type"] = forms.ChoiceField(label="Тип образования", widget=forms.Select(attrs={"class": "selectpicker with-border","id":"education-type"}),required=False,choices=Education.EDUCATION_CHOICES)
        self.fields['education_type'].choices.insert(0, ('', '---Выберите тип образования---'))
        self.number_sub_categories = 10
        for i in range(self.number_sub_categories):
            field_name_category = 'sub_category_%s' % (i,)
            field_name_price = 'price_%s' % (i,)
            field_name_negotiated = 'is_negotiated_%s' % (i,)
            field_name_hidden = "hidden_%s" % (i,)
            self.fields[field_name_category] = forms.ChoiceField(label="Категория" ,choices=SUB_CATEGORY_CHOICES)
            self.fields[field_name_category].widget.attrs.update({"class": "selectpicker", "data-live-search": "true"})
            self.fields[field_name_price] = forms.IntegerField(label="Цена",required=False)
            self.fields[field_name_price].widget.attrs.update({"class": "with-border","min":"0","max":"10000","step":"50"})
            self.fields[field_name_negotiated] = forms.BooleanField(label="Цена договорная",widget=forms.CheckboxInput(attrs={'checked': False}),required=False)
            self.fields[field_name_negotiated].widget.attrs.update({"class": "input-negotiated"})
            self.fields[field_name_hidden] = forms.BooleanField(widget=forms.HiddenInput(), initial=True,required=False)


    def get_sub_categories(self):
        for i in range(self.number_sub_categories):
            yield self['sub_category_%s' % (i,)], self['price_%s' % (i,)], self['is_negotiated_%s' % (i,)],self['hidden_%s' % (i,)],i

    def clean(self):
        super(BasicSettingsPerformerForm, self).clean()
        sub_categories_values = set()
        for i in range(self.number_sub_categories):
            if self.cleaned_data["hidden_%s" % (i,)]:
                if self.cleaned_data["is_negotiated_%s" % (i,)]:
                    pass
                elif not self.cleaned_data["price_%s" % (i,)]:
                    raise ValidationError("Price %s can't be null!" % (i,))
                else:
                    try:
                        price = int(self.cleaned_data["price_%s" % (i,)])
                    except ValueError:
                        raise ValidationError("Price must be integer!")
                sub_category = get_subcategory_by_value(self.cleaned_data["sub_category_%s" % (i,)])
                if not sub_category:
                    raise ValidationError("Subcategory with such name doesn't exist!")
                if sub_category.value in sub_categories_values:
                    raise ValidationError("Subcategory should be unique!")
                sub_categories_values.add(sub_category.value)
        if self.cleaned_data["education_type"]:
            if not self.cleaned_data["educational_institution_name"]:
                raise ValidationError("Заполните название учебного заведения")
    def save(self,performer):
        PerformingSubCategory.objects.filter(performer=performer).delete()
        for i in range(self.number_sub_categories):
            if self.cleaned_data["hidden_%s" % (i,)]:
                is_negotiated = False
                price = None
                if self.cleaned_data["is_negotiated_%s" % (i,)]:
                    is_negotiated = True
                else:
                    price = int(self.cleaned_data["price_%s" % (i,)])
                sub_category = get_subcategory_by_value(self.cleaned_data["sub_category_%s" % (i,)])
                PerformingSubCategory.objects.create(performer=performer,price=price,is_price_negotiated=is_negotiated,sub_category=sub_category)
        performer.languages.clear()
        for language_value in self.cleaned_data["languages"]:
            language = get_language_by_value(language_value)
            if language:
                performer.languages.add(language)
        if self.cleaned_data["education_type"]:
                if performer.education:
                    performer.education.education_type = self.cleaned_data["education_type"]
                    performer.education.educational_institution_name = self.cleaned_data["educational_institution_name"]
                    performer.education.save()
                else:
                    education = Education.objects.create(education_type=self.cleaned_data["education_type"],educational_institution_name=self.cleaned_data["educational_institution_name"])
                    performer.education = education
                    performer.save()
        else:
            if performer.education:
                Education.objects.get(pk=performer.education.pk).delete()






class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(max_length=128,widget=forms.PasswordInput(attrs={"class":"with-border"}),label="Текущий пароль")
    repeat_password = forms.CharField(max_length=128,widget=forms.PasswordInput(attrs={"class":"with-border"}),label="Повторите пароль")

    def __init__(self,user,*args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', None)
        if not self.user.check_password(old_password):
            raise ValidationError('Пароль не верный!')
        return old_password
    def clean_repeat_password(self):
        password = self.cleaned_data.get('password', None)
        repeat_password = self.cleaned_data.get('repeat_password', None)
        if password != repeat_password:
            raise ValidationError('Пароли должны совпадать!')
        return repeat_password

    class Meta:
        model = User
        fields = ("password",)
        labels={"password":"Новый пароль"}
        widgets = {
            "password":forms.PasswordInput(attrs={"class":"with-border"})
        }

    def save(self, commit=True):
        m = super(ChangePasswordForm, self).save(commit=False)
        m.set_password(self.cleaned_data["password"])
        if commit:
            m.save()
        return m


class ChangeEmailAndPhoneForm(forms.Form):
    email = forms.EmailField(max_length=128,required=False,label="Почта")
    phone_number = forms.CharField(max_length=13,required=False,label="Номер телефона")

    #TODO clean email and phone

    def save(self,user):
        user.email = self.cleaned_data["email"]
        user.profile.phone_number = self.cleaned_data["phone_number"]
        user.save()
        return user