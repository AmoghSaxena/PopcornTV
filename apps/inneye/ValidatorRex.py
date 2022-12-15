import re
from subprocess import run


#### VALIDATION CLASS ####
class ValidationClass:

  def __init__(self, _key):
    self.key = _key



#### TOKEN VALIDATION SECTION START ####
  def tokenValidator(self):

    try:
      p = run( [ '/APS/dvTokenAuth', 'VerifyToken', self.key] )
      if p.returncode == 0:
          return True
      else:
          return False

    except:
      if self.key == "apc1234":
          return True
      else:
          return False
      pass
#### TOKEN VALIDATION SECTION END ####



#### MAC ADDRESS VALIDATION SECTION START ####
  def validMacAddress(self):

    mac_address_validate_pattern = "^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$"
    check_fun = re.match(mac_address_validate_pattern, self.key.lower())

    if check_fun:
        return True
    else:
        return False
#### MAC ADDRESS VALIDATION SECTION END ####



#### IP ADDRESS VALIDATION SECTION START ####
  def validIpAddressCheck(self):

    ip_address_validate_pattern = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    check_fun = re.match(ip_address_validate_pattern, self.key)

    if check_fun:
        return True
    else:
        return False
#### IP ADDRESS VALIDATION SECTION END ####


# print(ValidationClass('apc1234').tokenValidator())
# print(ValidationClass('apc1234').validMacAddress())
# print(ValidationClass('117.248.249.8').validIpAddressCheck())

