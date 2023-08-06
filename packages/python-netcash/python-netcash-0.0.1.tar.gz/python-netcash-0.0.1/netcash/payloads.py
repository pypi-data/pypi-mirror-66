ValidateServiceKey = """
<soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:tem="http://tempuri.org/"
    xmlns:nc="http://schemas.datacontract.org/2004/07/NC.DG.TMS.C.WCF.NIWS">
   <soap:Header
    xmlns:wsa="http://www.w3.org/2005/08/addressing">
    <wsa:Action soap:mustUnderstand="0">http://tempuri.org/INIWS_Partner/ValidateServiceKey</wsa:Action>
    <wsa:To soap:mustUnderstand="0">https://ws.sagepay.co.za/NIWS/NIWS_Partner.svc</wsa:To>
   </soap:Header>
   <soap:Body>
      <tem:ValidateServiceKey>
         <!--Optional:-->
         <tem:request>
            <!--Optional:-->
            <nc:MerchantAccount>{merchant_account}</nc:MerchantAccount>
            <!--Optional:-->
            <nc:ServiceInfoList>
               <!--Zero or more repetitions:-->
               <nc:ServiceInfo>
                  <!--Optional:-->
                  <nc:ServiceId>{service_id}</nc:ServiceId>
                  <!--Optional:-->
                  <nc:ServiceKey>{service_key}</nc:ServiceKey>
               </nc:ServiceInfo>
            </nc:ServiceInfoList>
            <!--Optional:-->
            <nc:SoftwareVendorKey>{software_vendor_id}</nc:SoftwareVendorKey>
         </tem:request>
      </tem:ValidateServiceKey>
   </soap:Body>
</soap:Envelope>
"""

RequestMerchantStatement = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:RequestMerchantStatement>
         <!--Optional:-->
         <tem:ServiceKey>{service_key}</tem:ServiceKey>
         <!--Optional:-->
         <tem:FromActionDate>{from_date}</tem:FromActionDate>
      </tem:RequestMerchantStatement>
   </soapenv:Body>
</soapenv:Envelope>
"""

RetrieveMerchantStatement = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:RetrieveMerchantStatement>
         <!--Optional:-->
         <tem:ServiceKey>{service_key}</tem:ServiceKey>
         <!--Optional:-->
         <tem:PollingId>{polling_id}</tem:PollingId>
      </tem:RetrieveMerchantStatement>
   </soapenv:Body>
</soapenv:Envelope>
"""
