from django import forms
from django.forms import TextInput, DateTimeInput, DateTimeField, ImageField
from order.models import SimpleOrder, Category, SubCategory

from django.utils.translation import ugettext_lazy as _

from string import Template
from django.utils.safestring import mark_safe

from order.models import Category, Payment
from location.models import Location

from order.services import get_subcategories_by_category_value, get_subcategory_by_value
from location.services import get_cities


class SimpleOrderForm(forms.ModelForm):

    subcategory = forms.ChoiceField(
        label="Подкатегория заказа",
        widget=forms.Select(attrs={"class": "selectpicker with-border subcategory"}), required=False)

    city = forms.ChoiceField(
        label="Город",
        widget=forms.Select(attrs={"class": "selectpicker with-border city"}))

    location = forms.CharField(
        label="Адрес",
        widget=forms.TextInput(attrs={"class": "location", "placeholder": "Улица, дом"}), required=False)

    payment = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(SimpleOrderForm, self).__init__(*args, **kwargs)

        subcategories = get_subcategories_by_category_value(
            'repetitory-i-obuchenie')

        self.fields['subcategory'].choices = list(
            subcategories.values_list('value', 'name'))

        cities = get_cities()
        self.fields['city'].choices = list(
            cities.values_list('value', 'name'))

        self.fields['payment'].choices = list(
            Payment.objects.all().values_list('value', 'name'))

        self.fields['category'].to_field_name = "value"
        self.fields['category'].empty_label = None

        self.fields['order_location_type'].to_field_name = "value"
        self.fields['order_location_type'].empty_label = None

        self.fields['price_low'].required = False

    class Meta():
        model = SimpleOrder
        fields = ('name', 'time_start', 'time_end',
                  'price_low', 'price_high', 'is_fixed_price',
                  'description', 'order_image_preview',
                  'category', 'subcategory',
                  'order_location_type', 'payment')

        labels = {'name': _('Название заказа'),
                  'time_start': _('Начать задание'),
                  'time_end': _('Выполнить до'),
                  'price_high': _('Стоимость'),
                  'order_image_preview': _('Превью'),
                  'description': _('Описание'),
                  'category': _('Категория заказа'),
                  'city': _('Город')}

        # need date format DD/MM/YYYY HH:mm

        widgets = {
            'name': TextInput(attrs={
                'placeholder': "Напишите, что нужно сделать...",
                'autocomplete': 'off'}),
            'time_start': DateTimeInput(attrs={
                'placeholder': "Начать работу",
                'class': "input border p-3 w-100 my-2",
                'id': "datetimepicker-start",
                'readonly': "readonly"},
                format=['%m/%d/%Y %H:%M']),
            'time_end': DateTimeInput(attrs={
                'placeholder': "Закончить работу",
                'class': "input border p-3 w-100 my-2",
                'id': "datetimepicker-end",
                'readonly': "readonly"},
                format=['%m/%d/%Y %H:%M']),
            'price_low': TextInput(),
            'price_high': TextInput(attrs={
                'class': "input input border p-3 w-100 my-2",
                'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Подробное описание работы",
                'class': "input input border p-3 w-100 my-2",
                'autocomplete': 'off'}),
            'category': forms.Select(attrs={"class": "selectpicker with-border categories"})
        }

    def clean_subcategory(self):
        print("clean_subcategory")
        subcategory_value = self.cleaned_data['subcategory']

        return get_subcategory_by_value(subcategory_value)

    def clean_orderlocationtype(self):
        print("order_location_type")

    def clean_category(self):
        print("clean_category")
        category_name = self.cleaned_data['category']

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise ValidationError(_('Выберите категорию заказа'))

        return category

    def clean_payment(self):
        print("clean_payment")
        print("payment ", self.cleaned_data['payment'])
        try:
            payment = Payment.objects.get(value=self.cleaned_data['payment'])
        except Payment.DoesNotExist:
            pass
        return payment

    def clean(self):
        # self.clean_orderlocationtype()
        pass
