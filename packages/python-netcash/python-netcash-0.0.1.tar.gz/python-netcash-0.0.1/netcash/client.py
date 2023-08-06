from .payloads import (
    ValidateServiceKey,
    RequestMerchantStatement,
    RetrieveMerchantStatement,
)
from benedict import benedict as bdict
from io import StringIO
from datetime import date
import requests
import csv


class Netcash:

    NIWS_INBOUND = "https://ws.netcash.co.za/NIWS/niws_nif.svc"
    NIWS_PARTNER = "https://ws.netcash.co.za/NIWS/NIWS_Partner.svc"
    STATEMENT_SERVICE = "https://ws.netcash.co.za/NIWS/NIWS_NIF.svc"

    def __init__(self, merchant_account, software_vendor_id):
        self.merchant_account = merchant_account
        self.software_vendor_id = software_vendor_id

    def __get_soap_result(self, raw_result, soap_action):
        print(raw_result)
        data = bdict.from_xml(raw_result.decode("utf-8"))
        return (
            data.get("s:Envelope")
            .get("s:Body")
            .get("{}Response".format(soap_action))
            .get("{}Result".format(soap_action))
        )

    def validate_service_key(self, service_id: str, service_key: str) -> bool:
        """
        Returns true or false
        """
        url = self.NIWS_PARTNER
        body = ValidateServiceKey.format(
            **{
                "software_vendor_id": self.software_vendor_id,
                "merchant_account": self.merchant_account,
                "service_id": service_id,
                "service_key": service_key,
            }
        )
        headers = {
            "Content-Type": 'application/soap+xml;charset=UTF-8;action="http://tempuri.org/INIWS_Partner/ValidateServiceKey"',
        }

        result = requests.post(url, body, headers=headers)
        return "<b:ServiceStatus>001</b:ServiceStatus>" in result.content.decode(
            "utf-8"
        )

    def request_merchant_statement(self, from_date: date, service_key: str) -> str:
        url = self.STATEMENT_SERVICE
        date_formatted = from_date.isoformat().replace("-", "")
        options = {"service_key": service_key, "from_date": date_formatted}
        body = RequestMerchantStatement.format(**options)
        print(body)
        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": "http://tempuri.org/INIWS_NIF/RequestMerchantStatement",
        }

        res = requests.post(url, body, headers=headers)
        if res.ok:
            return self.__get_soap_result(res.content, "RequestMerchantStatement")

    def retrieve_merchant_statement(
        self, polling_id: str, service_key: str, as_csv_reader: bool = True
    ) -> csv:

        url = self.STATEMENT_SERVICE
        body = RetrieveMerchantStatement.format(
            **{"service_key": service_key, "polling_id": polling_id}
        )
        print(body)
        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": "http://tempuri.org/INIWS_NIF/RetrieveMerchantStatement",
        }

        res = requests.post(url, body, headers=headers)
        if res.ok:
            csvdata = self.__get_soap_result(res.content, "RetrieveMerchantStatement")
            if as_csv_reader:
                f = StringIO(csvdata)
                return csv.reader(f, delimiter="\t")
            return csvdata
