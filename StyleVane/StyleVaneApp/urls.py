from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    
    path('shop/', views.shop, name='shop'),
    path('product-single/<product_id>', views.productSingle, name='product-single'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog-single/<blog_id>', views.blogSingle, name='blog-single'),
    path('contact/', views.contact, name='contact'),
    path('add_to_cart/<product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    # path('update_quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/<cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

]


# Serve static files during development

APPEND_SLASH = False
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)