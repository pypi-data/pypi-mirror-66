import json

import phonenumbers
import requests


class ErrorCodes:
    MISSING_REQUIRED_PARAM = "ERR_1"
    INVALID_PHONE_NO = "ERR_2"


class Wavecell:
    """
    This is the Python Class client library for use Wavecell's API. To use this, you'll need a Wavecell API Keys.
    See wavecell documentation for more information.
    """

    BASE_URL_FMT = "https://api.wavecell.com/{}/{}/{}"
    VERSION = "v1"
    ACTION_SMS = "sms"
    METHOD_SMS_SINGLE = "/single"

    def __init__(self, sub_account_id, api_key, default_region="ID"):
        """
        The constructor for Wavecell class.

        Parameters :
            sub_account_id (str) : your Sub Account ID
            api_key (str) : your API Key
        """
        self.sub_account_id = sub_account_id
        self.api_key = api_key
        self.default_region = default_region

    def clean_phone(self, phone):
        try:
            # Parse without region
            tmp = phonenumbers.parse(phone, None)
        except phonenumbers.NumberParseException:
            # If failed, fallback to default region
            tmp = phonenumbers.parse(phone, self.default_region)

        # If phone number is not valid
        if not phonenumbers.is_valid_number(tmp):
            return {
                "valid": False
            }

        # Return numbers as E.164
        return {
            "valid": True,
            "phone": phonenumbers.format_number(tmp, phonenumbers.PhoneNumberFormat.E164)
        }

    def send_sms_single(self, param):
        """
        Send single SMS

        Parameters :
            param (dict)

        Returns :
            (dict)
        
        """
        # Validate required parameter
        validation_result = Wavecell.validate_param(["destination", "text"], param)
        if not validation_result["valid"]:
            return {
                "success": False,
                "code": ErrorCodes.MISSING_REQUIRED_PARAM,
                "message": validation_result["errors"]
            }

        # Clean destination phone no
        dest_phone = param["destination"]
        clean_result = self.clean_phone(dest_phone)
        if not clean_result["valid"]:
            return {
                "success": False,
                "code": ErrorCodes.INVALID_PHONE_NO,
                "message": "invalid phone no format. PhoneNo={}".format(dest_phone)
            }
        param["destination"] = clean_result["phone"]

        # Create url
        url = Wavecell.BASE_URL_FMT.format(
            Wavecell.ACTION_SMS, Wavecell.VERSION, self.sub_account_id
        )
        url += Wavecell.METHOD_SMS_SINGLE

        # Do request
        resp = self.send_request("POST", url, param)

        return {
            "success": True,
            "code": "OK",
            "message": "Request sent",
            "data": json.loads(resp)
        }

    def send_request(self, method, url, param):
        """
        Sending request to Wavecell API

        Parameters :
            method (str)
            url (str)
            param (dict)

        Returns :
            res (str)

        """
        content = json.dumps(param)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key),
            "Content-Length": str(len(content))
        }

        response = requests.request(method, url, data=content, headers=headers)
        res = response.text
        return res

    @staticmethod
    def validate_param(keys, param):
        errs = []
        for k in keys:
            if k not in param.keys():
                errs.append(k)

        if len(errs) == 0:
            return {
                "valid": True
            }

        return {
            "valid": False,
            "errors": "{} param required".format(", ".join(errs))
        }
