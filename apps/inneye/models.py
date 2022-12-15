from django.db import models



# class DVC(models.Model):

#     id = models.BigAutoField(primary_key=True)
#     hotelName = models.CharField(max_length=100,null=True)
#     publicIp = models.CharField(max_length=50,null=False)
#     localIp = models.CharField(max_length=50,null=False)
#     macAddress = models.CharField(max_length=50,null=False, unique=True)
#     createdOn = models.DateTimeField(blank=True, null=True)
#     modifiedOn = models.DateTimeField(blank=True, null=True)



# class unknownDVC(models.Model):

#     id = models.BigAutoField(primary_key=True)
#     publicIp = models.CharField(max_length=50,null=False)
#     localIp = models.CharField(max_length=50,null=False)
#     macAddress = models.CharField(max_length=50,null=False, unique=True)
#     createdOn = models.DateTimeField(blank=True, null=True)
#     modifiedOn = models.DateTimeField(blank=True, null=True)



# class sessionKey(models.Model):

#     id = models.BigAutoField(primary_key=True)
#     token = models.CharField(max_length=500, null=False, blank=False)
#     sessionKeyVal = models.CharField(max_length=500, null=False, blank=False)
#     macAddress = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     createdOn = models.DateTimeField(blank=True, null=True)
#     modifiedOn = models.DateTimeField(blank=True, null=True)



# class serverRegister(models.Model):

#     id = models.BigAutoField(primary_key=True)
#     hotelName = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     dvsURL = models.CharField(max_length=500, null=False, blank=False, unique=True)
#     dvsLocalIP = models.CharField(max_length=30, null=False, blank=False)
#     kongURL = models.CharField(max_length=500, null=False, blank=False, unique=True)
#     kongFqdn = models.CharField(max_length=500, null=False, blank=False, unique=True)
#     kongLocalIP = models.CharField(max_length=30, null=False, blank=False)
#     publicIP = models.TextField(null=False, blank=False)
#     macAddress = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     clientId = models.CharField(max_length=500, null=False, blank=False)
#     clientSecret = models.CharField(max_length=500, null=False, blank=False)
#     createdOn = models.DateTimeField(blank=True, null=True)
#     modifiedOn = models.DateTimeField(blank=True, null=True)



# class roomConfig(models.Model):

#     id = models.BigAutoField(primary_key=True)
#     hotelName = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     macAddress = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     config = models.TextField(null=True)
#     createdOn = models.DateTimeField(blank=True, null=True)
#     modifiedOn = models.DateTimeField(blank=True, null=True)



# class setEnvironment(models.Model):

#     id = models.BigAutoField(primary_key=True)
#     envName = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     envFQDN = models.CharField(max_length=500, null=False, blank=False, unique=True)
#     publicIP = models.TextField(null=False, blank=False)
#     localIP =  models.CharField(max_length=30, null=False, blank=False)
#     createdOn = models.DateTimeField(("createdOn"), auto_now_add=True)
#     modifiedOn = models.DateTimeField(("modifiedOn"), auto_now_add=True)


class movieInformation(models.Model):

    id = models.BigAutoField(primary_key=True)
    movieName = models.CharField(max_length=255, default = None)
    genreId = models.CharField(max_length=255, default = None)
    movieType = models.CharField(max_length=255, default = None)
    movieId = models.CharField(max_length=255, null=False, unique=True)
    overview = models.TextField(default = None)
    releaseDate = models.CharField(max_length=255, default = None)
    language = models.CharField(max_length=255, default = None)
    popularity = models.CharField(max_length=255, default = None)
    voteAverage = models.CharField(max_length=255, default = None)
    voteCount = models.CharField(max_length=255, default = None)
    posterPath = models.CharField(max_length=255, default = None)
    backdropPath = models.CharField(max_length=255, default = None)
    watchCount = models.CharField(max_length=255, default = None)
    watchTime = models.CharField(max_length=255, default = None)
    teaser = models.CharField(max_length=255, default = None)
    movieURL = models.CharField(max_length=255, default = None)
    favourite = models.CharField(max_length=255, default = None)
    user = models.CharField(max_length=255, default = None)
    uploadedOn = models.DateTimeField(blank=True, null=True)
    modifiedOn = models.DateTimeField(blank=True, null=True)
    
