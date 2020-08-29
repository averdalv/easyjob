from rest_framework import serializers
from order.models import SimpleOrder

from performer.models import Performer
from order.models import OrderRespond, SimpleOrder
from order.services import order_status_style_dict


class SimpleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleOrder
        fields = '__all__'
        # exclude = ['order_image_preview']
        depth = 2

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        if OrderRespond.objects.filter(order=obj, performer=self.performer).exists():
            ret['is_respond'] = True
        else:
            ret['is_respond'] = False

        if obj.customer.user == self.user:
            ret['is_my'] = True
        else:
            ret['is_my'] = False

        ret['status_style'] = order_status_style_dict[obj.status.id]

        return ret

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        if self.user.is_anonymous:
            self.performer = None
        else:
            try:
                self.performer = Performer.objects.get(user=self.user)
            except Performer.DoesNotExist:
                self.performer = None

        super(SimpleOrderSerializer, self).__init__(*args, **kwargs)
