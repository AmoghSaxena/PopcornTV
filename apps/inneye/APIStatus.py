""" Response Output """
from email import header


res = {
    "status": None,
    "statusCode": None,
    "message": None,
    "data": None
}

movieTypeDB = {
        "28":"Action",
        "12":"Adventure",
        "16":"Animation",
        "35":"Comedy",
        "80":"Crime",
        "99":"Documentary",
        "18":"Drama",
        "10751":"Family",
        "14":"Fantasy",
        "36":"History",
        "27":"Horror",
        "10402":"Music",
        "9648":"Mystery",
        "10749":"Romance",
        "878":"Science Fiction",
        "10770":"TV Movie",
        "53":"Thriller",
        "10752":"War",
        "37":"Western"
    }   


""" Public Key Generate Case """    #### STATUS 6XX #### 
publicKeySuccess = {"message": "Public Key Fetched Successfully", "statusCode": 601}
publicKeyFailure = {"message": "Unable To Fetch Public Key", "statusCode": 602}
requestPublicKey = {"message": "Request For Public Key With Token", "statusCode": 603}


""" Encryption Decryption Case """    #### STATUS 7XX ####
NotEncrypt = {"message": "Can't Encrypt With Key", "statusCode": 701}
NotDecrypt = {"message": "Can't Decrypt With Key", "statusCode": 702} 


""" Session Key Exchanged Case """    #### STATUS 8XX ####
sessionKeySuccess = {"message": "Session Key Exchanged Successfully", "statusCode": 801}
sessionKeyFailure = {"message": "Unable To Exchange Session Key", "statusCode": 802}
sessionKeyUpdated = {"message": "Key Updated", "statusCode": 803}
sessionKeyGenerated = {"message": "Key Generated", "statusCode": 804}
sessionKeyNotUpdated = {"message": "Key Not Updated", "statusCode": 805}
sessionKeyNotSave = {"message": "Unable To Save", "statusCode": 806}
sessionKeyNotExists = {"message": "Session Key Not Exists", "statusCode": 807}
sessionKeyError = {"message": "Error occurred during exchange session key", "statusCode": 808}
requestSessionKey = {"message": "Request For Exchange Session Key With Token", "statusCode": 809}
sessionKeyDecrypt = {"message": "Session Key Decrypt Successfully, Session Key : ", "statusCode": 810}
sessionKeyData = {"message": "Session Key : ", "statusCode": 811}


""" Server Register Case """    #### STATUS 9XX ####
serverRegisterSuccess = {"message": "Server Registered Successfully", "statusCode": 901}
serverRegisterFailure = {"message": "Unable To Register Server", "statusCode": 902}
serverAlreadyRegister = {"message": "Server Already Register", "statusCode": 903}
serverRegisterError = {"message": "Error Occurred During Register Server", "statusCode": 904}
serverUpdateStatus = {"message": "Server Updated", "statusCode": 905}
serverRemoveStatus = {"message": "Server Deleted Successfully", "statusCode": 906}
serverDeleteError = {"message": "Unable To Delete Server", "statusCode": 907}
unableServerUpdateStatus = {"message": "You do not have Permission to Edit Server", "statusCode": 908}
unableServerRegisterStatus = {"message": "You do not have Permission to Register Server", "statusCode": 909}
unableServerRemoveStatus = {"message": "You do not have Permission to Remove Server", "statusCode": 910}
requestServerRegister = {"message": "Request For Server Register With MAC Address", "statusCode": 911}
serverDecrypt = {"message": "Decryption Successfully, Server Data : ", "statusCode": 912}


""" Config File Upload """    #### STATUS 10XX ####
configFileSuccess = {"message": "Config File Upload Successfully", "statusCode": 1001}
configFileFailure = {"message": "Config File Not Upload", "statusCode": 1002}
configFileError = {"message": "Error Occurred During Config Data Upload", "statusCode": 1003}
configFileServerNotPresent = {"message": "Server Not Found", "statusCode": 1004}
configFileUpdate = {"message": "File Updated", "statusCode": 1005}
requestConfigFile = {"message": "Request For Config File Store With MAC Address : ", "statusCode": 1006}
configFileDecrypt = {"message": "Decryption Successfully, Config File : ", "statusCode": 1007}


""" DVC Register Case """    #### STATUS 11XX ####
serverDetailSuccess = {"message": "Server Details Fetched Successfully", "statusCode": 1101}
serverDetailFailure = {"message": "Unable To Fetched Server Details", "statusCode": 1102}
serverDetailRequired = {"message": "Invalid Data", "statusCode": 1103}
serverDetailError = {"message": "Error Occurred During Fetched Server Details", "statusCode": 1104}
serverDetailNotExists = {"message": "Server Not Found", "statusCode": 1105}
unknownDVCRemove = {"message": "Controller Deleted Successfully", "statusCode": 1106}
unknownDVCError = {"message": "Unknown Controller Error", "statusCode": 1107}
unableUnknownDVCRemove = {"message": "You do not have Permission to Remove Controller", "statusCode": 1108}
multipleServerFound = {"message": "Multiple Server Found With Same Public IP, Room MAC Binding is Required", "statusCode": 1109}
requestServerDetail = {"message": "Request For Get Server Detail With MAC Address", "statusCode": 1110}
requestDecrypt = {"message": "Decryption Successfully, Request Body : ", "statusCode": 1111}
responseEncrypt = {"message": "Encryption Successfully, Response : ", "statusCode": 1112}


""" Request Response Verify Case """    #### STATUS 12XX ####
requestInvalid = {"message": "Invalid Request", "statusCode": 1201}
requestBody = {"message": "Data Not Exists at Body", "statusCode": 1202}
requestBodyData = {"message": "Request Body", "statusCode": 1203}
responseBodyData = {"message": "Response", "statusCode": 1204}
requestQueryParam = {"message": "Data Not Exists at Query Param", "statusCode": 1205}


""" header data Case """    #### STATUS 13XX ####
tokenNotPresent = {"message": "Token Not Found", "statusCode": 1301}
macAddressPresent = {"message": "Mac Address Not Found", "statusCode": 1302}
headerData = {"message": "Header", "statusCode": 1303}


""" Verify Case"""    #### STATUS 14XX ####
macAddressInvalid = {"message": "Invalid Mac Address", "statusCode": 1401}
ipAddressInvalid = {"message": "Invalid IP Address", "statusCode": 1402}
tokenFailure = {"message": "Invalid Token", "statusCode": 1403}
validationError = {"message": "Validation Crash", "statusCode": 1404}
serverFinderError = {"message": "Server Finder Crash", "statusCode": 1405}
tokenSuccess = {"message": "Token Verify Successfully, Token", "statusCode": 1406}
macAddressSuccess = {"message": "MAC Address Verify Successfully, MAC Address", "statusCode": 1407}
ipAddressSuccess = {"message": "IP Address Verify Successfully, IP Address", "statusCode": 1408}
ipAddress = {"message": "IP Address  ", "statusCode": 1409}


""" Databases Error """   #### STATUS 15XX ####
DBError = {"message": "DB Error", "statusCode": 1501}


""" Template Error """   #### STATUS 16XX ####
templateNotFound = {"message": "Template Does Not Exist", "statusCode": 1601}
templateError = {"message": "Template Error", "statusCode": 1602}
unableToAccessLog = {"message": "You do not have Permission to Access debug log ", "statusCode": 1603}


""" Authentication """   #### STATUS 17XX ####
authenticationSuccess = {"message": "User Login Successfully, user_name : ", "statusCode": 1701}
authenticationError = {"message": "Invalid credentials, user_name : ", "statusCode": 1702}
authenticationLogout = {"message": "Logout, user_name : ", "statusCode": 1703}
ldapSuccess = {"message": "Ldap Connection Established", "statusCode": 1704}
ldapError = {"message": "Ldap Connection Failure", "statusCode": 1705}


""" Get Environment Case """    #### STATUS 18XX ####
getEnvSuccess = {"message": "Environment Fetched Successfully", "statusCode": 1801}
getEnvFailure = {"message": "Unable To Fetch Environment", "statusCode": 1802}
requestGetEnv = {"message": "Request For Get Environment With Token ", "statusCode": 1803}
EnvNotFound = {"message": "Environment Not Found", "statusCode": 1804}
multipleEnvFound = {"message": "Multiple Environment Found With Same Public IP", "statusCode": 1805}
defaultEnv = {"message": "Default Environment Fetched Successfully", "statusCode": 1806}


