from django.contrib import admin
from .models import movieInformation
# from .models import DVC, roomConfig, serverRegister, unknownDVC, sessionKey, setEnvironment


# class DVCs(admin.ModelAdmin):
#     list_display = ('hotelName', 'publicIp', 'localIp', 'macAddress', 'createdOn', 'modifiedOn')
#     exclude = ['createdOn', 'modifiedOn']


# class unknownDVCs(admin.ModelAdmin):
#     list_display = ('publicIp', 'localIp', 'macAddress', 'createdOn', 'modifiedOn')
#     exclude = ['createdOn', 'modifiedOn']


# class serverRegisters(admin.ModelAdmin):
#     list_display = ('hotelName', 'publicIP', 'dvsLocalIP', 'macAddress', 'createdOn', 'modifiedOn')
#     exclude = ['createdOn', 'modifiedOn']


# class roomConfigs(admin.ModelAdmin):
#     list_display = ('hotelName', 'macAddress', 'createdOn', 'modifiedOn')
#     exclude = ['createdOn', 'modifiedOn']


# class sessionKeys(admin.ModelAdmin):
#     list_display = ('token', 'sessionKeyVal', 'macAddress', 'createdOn', 'modifiedOn')
#     exclude = ['createdOn', 'modifiedOn']


# class setEnvironments(admin.ModelAdmin):
#     list_display = ('envName', 'envFQDN', 'publicIP', 'localIP', 'createdOn', 'modifiedOn')
#     exclude = ['createdOn', 'modifiedOn']


# class AdminTable(admin.ModelAdmin):
#     pass

# admin.site.register(DVC,DVCs)
# admin.site.register(unknownDVC,unknownDVCs)
# admin.site.register(serverRegister,serverRegisters)
# admin.site.register(roomConfig,roomConfigs)
# admin.site.register(sessionKey,sessionKeys)
# admin.site.register(setEnvironment,setEnvironments)

admin.site.register(movieInformation)
