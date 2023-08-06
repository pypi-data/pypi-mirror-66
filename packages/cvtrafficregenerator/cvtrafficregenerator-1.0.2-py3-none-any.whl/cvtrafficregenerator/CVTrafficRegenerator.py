import time
import random
import requests
import json
import string
import os

from cvapianalyser import CommunityEdition
from openapispecdiff import OpenApiSpecDiff

class CVTrafficRegenerator(object):
    def __init__(self, APISpecOne, APISpecTwo, ce_host, ce_username, ce_password):
        self.apispec_one_path = APISpecOne
        self.apispec_two_path = APISpecTwo
        self.ceobj = CommunityEdition.CommunityEdition("http://" + ce_host, ce_username, ce_password)
        print("\n\t\t\t\t\t\t\t\t\t----------------- Traffic Regeneator - For CloudVector APIShark events "
                                                                                                    "-----------------")
        self.regenerate_traffic(self._get_changed_apis())

    def get_captured_events(self):
        return self.ceobj.get_all_raw_events()  # last 3 weeks data

    def _get_changed_apis(self):
        return OpenApiSpecDiff.OpenApiSpecDiff(self.apispec_one_path, self.apispec_two_path).diff

    def _process_event_data(self, apis_to_check=[]):
        cv_requests = []
        events = self.ceobj.get_all_raw_events(apis_to_check)
        for event in events:
            #print("....."+str(event))
            #print(event["attributes"]["http_path"])
            iflag = False
            # params_to_add = []
            for _ in apis_to_check:
                if str(_).lower() in str(event["attributes"]["http_path"]).lower():
                    iflag = True
                    params_to_add = apis_to_check[_]
                if iflag:
                    break

            if not iflag:
                continue
            request = {"url": str(event["attributes"]["event_protocol"]).lower() + "://" + \
                              str(event["attributes"]["http_host"]) + \
                              str(event["attributes"]["http_path"]), "method": str(event["attributes"]["http_method"])}
            header = {}
            body = {}
            for k, v in event["attributes"]["event_json"].items():
                if "http-req-header" in k:
                    if k == "http-req-headers-params":
                        continue
                    header[str(k).replace("http-req-header-", "")] = v
                if "http-req-body" in k:
                    if k == "http-req-body-params":
                        continue
                    body[str(k).replace("http-req-body-", "")] = v
            request["header"] = header
            to_skip = False
            for param in params_to_add:
                if param["type"] == "string":
                    value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
                elif param["type"] in ["number", "integer"]:
                    value = random.randint(1, 9999)
                if param["name"] not in body:
                    body.update({param["name"]: value})
                else:
                    to_skip = True
            request["body"] = body
            if not to_skip:
                cv_requests.append(request)
        return cv_requests

    def _trigger_requests(self, cv_requests):
        print("\n\nRegenerating traffic from CloudVector events....")
        for cv_request in cv_requests:
            print("------------" * 20)
            print("\nRecreating the request: " + str(cv_request))
            resp = requests.request(method=cv_request["method"], url=cv_request["url"], headers=cv_request["header"],
                                    data=json.dumps(cv_request["body"]))
            print("\nStatus Code:" + str(resp.status_code))
            print("------------" * 20)

    def regenerate_traffic(self, changed_apis):
        #cv_events = self.get_captured_events()
        # print(changed_apis["changed"])
        print("\nQuerying for events from APIShark.....")
        cv_requests = self._process_event_data(changed_apis["changed"])
        # print("\n\n\n\n\n" + str(cv_requests))
        self._trigger_requests(cv_requests)
        print("------------" * 20)
        print("\t\t\t\t\t\t Traffic Regenerator - Overall Stats")
        print("\n\t\tTotal APIs newly added: " + str(len(changed_apis["new"])))
        print("\t\tTotal APIs modified: " + str(len(changed_apis["changed"])))
        print("\t\tTotal events regenerated: " + str(len(cv_requests)))
        print("\n\t\tAPIShark host: "+str(self.ceobj.host_url))
        print("------------" * 20)

def main():
    import sys
    import getpass
    import yaml
    if os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml")) as fobj:
            ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
    else:
        ce_details = {}
    print("*****" * 20)
    print ("CloudVector APIShark - Traffic Regenerator")
    print("*****" * 20)
    print("\nAPIShark details from my_cesetup.yaml:\n\t" + str(ce_details) + "\n")
    if ce_details.get("ce_host"):
        ce_host = ce_details["ce_host"]
    else:
        ce_host = input("Enter APIShark host in format <host>:<port> : ")
    if ce_details.get("ce_username"):
        ce_username = ce_details["ce_username"]
    else:
        ce_username = input("Enter your APIShark username : ")
    ce_password = getpass.getpass(prompt="APIShark password:")
    input_spec_one = input("Enter absolute path to Old API SPEC(Version A): ")
    input_spec_two = input("Enter absolute path to New API SPEC(Version B) : ")
    if not os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml"),"w+") as fobj:
            yaml.dump({"ce_host":str(ce_host),"ce_username":str(ce_username)},fobj)
    CVTrafficRegenerator(input_spec_one,input_spec_two,ce_host,ce_username,ce_password)


if __name__ == "__main__":
    main()
