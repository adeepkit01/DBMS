from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

from items.views import *
from profiles.views import *


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rental.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"^grapppelli/", include("grappelli.urls")),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^$", index, name="index"),
    url(r"^price$", indexprice, name="indexprice"),
    url(r"^pricerev$", indexpriced, name="indexpriced"),


    # Items
    url(r"^item/(?P<item_id>\d+)/$", view_item, name="view_item"),
    url(r"^item/(?P<item_id>\d+)/reserve/$", reserve_item, name="reserve_item"),
    url(r"^tag/(?P<tag_id>\d+)/$", tagview, name="tag_list"),
    url(r"^tags/(?P<tag_id>\d+)/$", subs, name="create_sub"),
    url(r"^deltags/(?P<tag_id>\d+)/$", unsub, name="delete_sub"),
    url(r"^upload/$", upload, name="upload_item"),

    # Profiles
    url(r"^profile/(?P<user_name>\w+)/$", view_user, name="view_user"),
    url(r"^group/(?P<group_name>)\w+/$", view_group, name="view_group"),

    # Login/Register
    url(r"^login/$", login_user, name="login"),
    url(r"^logout/$", logout_user, name="logout"),
    url(r"^register/$", register, name="register"),
    url(r"^fill/$", detail, name="fill details"),
    url(r"^verify/$", verify, name="verify"),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
