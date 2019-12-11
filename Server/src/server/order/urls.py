from django.urls import path
from django.conf.urls import url

from order.views import OrdersView, OrderView, AddOrderView, UploadGalleryPhotoView, OrderRespondView, \
    OrderConfirmView, SubCategoryJsonView, CategoryJsonView, CitiesJsonView, BookmarkOrderJsonView
from order.views import OrdersJsonView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'order_app'

urlpatterns = [
    url(
        'api/orders',
        OrdersJsonView.as_view(),
        name="api_orders"
    ),
    url('api/subs',
        SubCategoryJsonView.as_view(),
        name='api_subcategories',
    ),
    url('api/categories',
        CategoryJsonView.as_view(),
        name="api_categories",
    ),
    url('api/cities',
        CitiesJsonView.as_view(),
        name="api_cities",
    ),
    url('api/bookmarkorder',
        BookmarkOrderJsonView.as_view(),
        name="bookmark_order",
    ),

    path('', OrdersView.as_view(), name='orders'),
    path('add_order', AddOrderView.as_view(), name='add_order'),
    path('upload_gallery_photo', UploadGalleryPhotoView.as_view(),
         name='upload_gallery_photo'),
    path('respond', OrderRespondView.as_view(), name="respond"),
    path('confirm', OrderConfirmView.as_view(), name="confirm"),
    path('<int:id>', OrderView.as_view(), name='order'),
    
    url(
        r'^(?P<category_value>[-\w]+)$',
        OrdersView.as_view(),
        name='orders',
    ),
    
    url(
        r'^(?P<category_value>[-\w]+)/(?P<sub_category_value>[-\w]+)$',
        OrdersView.as_view(),
        name='orders',
    ),
]
