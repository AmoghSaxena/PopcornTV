function loadPage() {

    document.getElementById("hotelNameEmpty").hidden = true;
    document.getElementById("dvsUrlEmpty").hidden = true;
    document.getElementById("dvsMacAddressEmpty").hidden = true;
    document.getElementById("invalidDvsMacAddress").hidden = true;
    document.getElementById("publicIpEmpty").hidden = true;
    document.getElementById("invalidDvsPublicIp").hidden = true;
    document.getElementById("dvsLocalIpEmpty").hidden = true;
    document.getElementById("invalidDvsLocalIp").hidden = true;
    document.getElementById("kongUrlEmpty").hidden = true;
    document.getElementById("kongFQDNEmpty").hidden = true;
    document.getElementById("kongLocalIpEmpty").hidden = true;
    document.getElementById("invalidKongLocalIp").hidden = true;
    document.getElementById("clientIdEmpty").hidden = true;
    document.getElementById("clientSecretEmpty").hidden = true;
}

function validateForm() {

    var flag = true;

    var hotelName = document.forms["addServer"]["hotelName"].value;
        if (hotelName == "") {

            document.getElementById("hotelNameEmpty").hidden = false;
            flag = false;

        } else {

            document.getElementById("hotelNameEmpty").hidden = true;
        }



    var dvsUrl = document.forms["addServer"]["dvsUrl"].value;
        if (dvsUrl == "") {

            document.getElementById("dvsUrlEmpty").hidden = false;
            flag = false;

        } else {

            document.getElementById("dvsUrlEmpty").hidden = true;
        }
    


    var dvsMacAddress = document.forms["addServer"]["dvsMacAddress"].value;
        if (dvsMacAddress == "") {

            document.getElementById("dvsMacAddressEmpty").hidden = false;
            document.getElementById("invalidDvsMacAddress").hidden = true;
            flag = false;

        } else {

            if(/^[0-9a-fA-F:]+$/.test(dvsMacAddress)) {
                
                document.getElementById("invalidDvsMacAddress").hidden = true;
                document.getElementById("dvsMacAddressEmpty").hidden = true;

            } else {

                document.getElementById("invalidDvsMacAddress").hidden = false;
                document.getElementById("dvsMacAddressEmpty").hidden = true;
                flag = false;
            }
        }



    var dvsPublicIp = document.forms["addServer"]["dvsPublicIp"].value;
        if (dvsPublicIp == "") {

            document.getElementById("publicIpEmpty").hidden = false;
            document.getElementById("invalidDvsPublicIp").hidden = true;
            flag = false;

        } else {

            const publicIpList = dvsPublicIp.split(",");
            
            for (let index = 0; index < publicIpList.length; index++) {

                if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(publicIpList[index])) {
                                
                    document.getElementById("invalidDvsPublicIp").hidden = true;
                    document.getElementById("publicIpEmpty").hidden = true;

                } else {

                    document.getElementById("invalidDvsPublicIp").hidden = false;
                    document.getElementById("publicIpEmpty").hidden = true;
                    flag = false;
                }
            }
        }



    var dvsLocalIp = document.forms["addServer"]["dvsLocalIp"].value;
        if (dvsLocalIp == "") {

            document.getElementById("dvsLocalIpEmpty").hidden = false;
            document.getElementById("invalidDvsLocalIp").hidden = true;
            flag = false;

        } else {

            if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(dvsLocalIp)) {
                            
                document.getElementById("invalidDvsLocalIp").hidden = true;
                document.getElementById("dvsLocalIpEmpty").hidden = true;

            } else {

                document.getElementById("invalidDvsLocalIp").hidden = false;
                document.getElementById("dvsLocalIpEmpty").hidden = true;
                flag = false;
            }
        }



    var kongUrl = document.forms["addServer"]["kongUrl"].value;
        if (kongUrl == "") {

            document.getElementById("kongUrlEmpty").hidden = false;
            flag = false;

        } else {

            document.getElementById("kongUrlEmpty").hidden = true;
        }



    var kongFqdn = document.forms["addServer"]["kongFqdn"].value;
        if (kongFqdn == "") {

            document.getElementById("kongFQDNEmpty").hidden = false;
            flag = false;

        } else {

            document.getElementById("kongFQDNEmpty").hidden = true;
        }



    var kongLocalIp = document.forms["addServer"]["kongLocalIp"].value;
        if (kongLocalIp == "") {

            document.getElementById("kongLocalIpEmpty").hidden = false;
            document.getElementById("invalidKongLocalIp").hidden = true;
            flag = false;

        } else {

            if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(kongLocalIp)) {
                            
                document.getElementById("invalidKongLocalIp").hidden = true;
                document.getElementById("kongLocalIpEmpty").hidden = true;

            } else {

                document.getElementById("invalidKongLocalIp").hidden = false;
                document.getElementById("kongLocalIpEmpty").hidden = true;
                flag = false;
            }
        }



    var dvcClientId = document.forms["addServer"]["dvcClientId"].value;
        if (dvcClientId == "") {

            document.getElementById("clientIdEmpty").hidden = false;
            flag = false;

        } else {

            document.getElementById("clientIdEmpty").hidden = true;
        }



    var dvcClientSecret = document.forms["addServer"]["dvcClientSecret"].value;
        if (dvcClientSecret == "") {

            document.getElementById("clientSecretEmpty").hidden = false;
            flag = false;

        } else {

            document.getElementById("clientSecretEmpty").hidden = true;
        }



    if (flag) {

        return true;

    } else {

        return false;
    }
}
