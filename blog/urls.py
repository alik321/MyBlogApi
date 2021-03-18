from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.routers import DefaultRouter

from main_app.views import PostView, CategoryView, CommentView, PostImageView, LikeViewSet, RatingViewSet

schema_view = get_schema_view(
    openapi.Info(
          title="MyBlog",
          default_version='v1',
          description="Welcome to My Blog",
       ),
    public=True,
)

router = DefaultRouter()
router.register('posts', PostView)
router.register('categories', CategoryView)
router.register('comments', CommentView)
router.register('likes', LikeViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('v1/api/docs/', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path("v1/api/", include(router.urls)),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/images/', PostImageView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
