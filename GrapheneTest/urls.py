from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from mysteryroom import urls as MRUrls
from app1 import urls as AppUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include(AppUrls)),
    path('mysteryroom/', include(MRUrls)),
    path('gql', GraphQLView.as_view(graphiql=True))
]
