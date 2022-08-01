from django.contrib import admin
from django.urls import include, path, re_path as url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny
from allauth.account.views import confirm_email
from dj_rest_auth.views import PasswordResetConfirmView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema configuration for swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Lunch Poll Service API Docs",
        default_version="v1",
        description="API docs for Lunch Poll Service, base OpenAPI Specifications",
        contact=openapi.Contact(email="livinusanayo96@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # to allow any person to access it
    permission_classes=[AllowAny],  # to allow any person to access it
)


urlpatterns = [
    # setting the base url to be pointing at the admin interface, this should be changed later
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    # for dj-rest-auth authentication services
    url(r"api/(?P<version>[v1]+)/auth/", include(("dj_rest_auth.urls", "dj_rest_auth"), namespace="auth_api")),
    url(r"restframework/", include(("rest_framework.urls", "rest_framework"), namespace="rest_framework")),
    url(r"api/(?P<version>[v1]+)/users/", include(("users.api.urls", "users"), namespace="user_api")),
    url(
        r"api/(?P<version>[v1]+)/restaurants/",
        include(("restaurants.api.urls", "restaurants"), namespace="restaurants_api"),
    ),
    # for dj-rest-auth registration service
    url(r"^accounts/", include("allauth.urls")),
    url(
        r"api/(?P<version>[v1]+)/registration/",
        include(("dj_rest_auth.registration.urls", "dj_rest_auth.registration"), namespace="auth_reg"),
    ),
    url(
        r"^api/(?P<version>[v1]+)/auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/$",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    url(
        r"^api/(?P<version>[v1]+)/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    # swagger docs (openapi)
    url(
        r"^api/(?P<version>[v1]+)/docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^api/(?P<version>[v1]+)/docs/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# There is implementation of version in the API, at this poin the only version that is allowed is only version one
# But if more API versions are created under same API app package,then those versions numbers can be included through
# the regular expression rule by including [v1|v2|v3], to allow any of v1, v2 or v3 at any point. The in the API view, you
# can use the request.version attribute to check and implement specific functionality for specific versions.
urlpatterns.append(path("", admin.site.urls))  # this url path should be tested last
