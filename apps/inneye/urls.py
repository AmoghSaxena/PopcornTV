from django.urls import path, re_path
from apps.inneye import views

urlpatterns = [

    # The page
    path('', views.inneyeHome, name='inneyeHome'),
    path('movies', views.inneyeMovies, name='inneyeMovies'),
    path('series', views.inneyeSeries, name='inneyeSeries'),
    path('categories/<str:movieType>', views.inneyeCategories, name='inneyeCategories'),
    path('watch/<str:movieId>', views.inneyeWatch, name='inneyeWatch'),
    path('series/watch', views.inneyeWatchSeries, name='inneyeWatchSeries'),
    path('play/<str:movieId>', views.inneyePlay, name='inneyePlay'),
    # path('cloud/dvs/register', views.serverRegistration, name = 'serverRegistretion'),
    # path('cloud/dvs/info', views.serverInfo, name = 'serverInfo'),
    # path('cloud/dvs/detail/<str:macAddress>', views.serverDetail, name = 'serverDetail'),
    # path('cloud/dvs/update/<str:macAddress>', views.serverUpdate, name = 'serverUpdate'),
    # path('cloud/dvs/remove/<str:macAddress>', views.serverRemove, name = 'serverRemove'),
    # path('cloud/dvs/room-mac-binding/<str:macAddress>', views.configFile, name = 'configFile'),
    # path('cloud/dvc/info/<str:hotelName>', views.dvcInfo, name = 'dvcInfo'),
    # path('cloud/unknowndvc/info', views.unknownController, name = 'unknownController'),
    # path('cloud/unknowndvc/remove/<str:macAddress>', views.unknownControllerRemove, name = 'unknownControllerRemove'),
    # path('cloud/info/log', views.sysLog, name = 'sysLog'),
    # path('cloud/error/log', views.errorLog, name = 'errorLog'),
    # path('cloud/debug/log', views.debugLog, name = 'debugLog'),

    # API 
    # path('cloud/api/common/get-public-key', views.getPublicKey, name = 'publicKey'),
    # path('cloud/api/common/exchange-session-key', views.key, name = 'sessionKey'),
    # path('cloud/api/dvs/registration', views.server, name = 'server'),
    # path('cloud/api/dvs/room-mac-binding', views.config, name = 'config'),
    # path('cloud/api/dvc/get-server-details', views.dvc, name = 'dvc'),
    # path('cloud/api/dvc/get-environment', views.getEnvironment, name = 'Environment'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

