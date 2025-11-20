import requests
import logging
import json
from urllib3.exceptions import InsecureRequestWarning
import xml.etree.ElementTree as ET

# logger will return the source module name
logger = logging.getLogger(__name__)
# display logging info level
logging.basicConfig(level=logging.INFO)
# Suppress certificate warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

api_url = ""
# the easiest way is to regenerate API key is to change the password
# pa_api_key = get_api_key(api_url, "", "")
pa_api_key = ""

# PAN-OS XML API
# The PAN-OS XML API is powerful and low-level, allowing you to take full control of every aspect of your security, 
# and build deep integrations with a variety of other systems. You can make XML API calls directly to the firewall,
#  directly to Panorama, or to a firewall via Panorama.

# PAN-OS REST API
# The PAN-OS REST API simplifies access to resources as high-level URIs. 
# You can use this API to create, change, and delete resources.
# REST API on-device documentation: https://HOSTNAME/restapi

# 1. Enable API access: 
# https://docs.paloaltonetworks.com/ngfw/api/api-authentication-and-security/pan-os-api-authentication
# 2. Generate an API key certificate:
# https://docs.paloaltonetworks.com/ngfw/api/api-authentication-and-security/generate-api-key
# https://www.mbtechtalker.com/generate-a-self-signed-certificate-on-a-pan-os-firewall/
# 3. Get API Key
# run get_api_key() function


def commit(pa_url: str, api_key: str, desc: str = "") -> None:
    api = "/restapi/v11.2/System/Configuration:commit"
    url = pa_url + api
    logger.info("Commit the changes...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "entry": {
            "description": desc,
            "force": {
                "partial": null
            }
        }
    })

    response = requests.post(
        url=url,
        headers=headers,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA config changes successfully commited.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to commit the changes: {response.status_code}")
        logger.info(response.text)


def get_api_key(pa_url: str, username: str, password: str) -> str:
    api = "/api/?type=keygen"
    url = pa_url + api
    logger.info("Generate API key...")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "user": username, 
        "password": password
    }

    response = requests.post(
        url=url,
        headers=headers,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA API key successfully retrieved.")
        # logger.info(response.text)
        root = ET.fromstring(response.text)
        # logger.info([elem.tag for elem in root.iter()])
        api_key_iter = root.iter("key")  # iterator, not possible to display directly
        api_key = list(api_key_iter)[0].text  # convert iterator to list to access the value
        logger.info(f"PA API key:\n{api_key}")
        return api_key
    else:
        logger.info(f"Failed to retrieved PA API key: {response.status_code}")
        logger.info(response.text)


# def xml_get_system_info(pa_url: str, api_key: str) -> str:
#     api = "/api?type=op&cmd=<show><system><info></info></system></show>"
#     url = pa_url + api
#     logger.info("Display system info...")
#     headers = {
#         "X-PAN-KEY": api_key
#     }

#     response = requests.post(
#         url=url,
#         headers=headers,
#         verify=False
#     )

#     if response.status_code == 200:
#         logger.info("PA system info successfully retrieved.")
#         logger.info(response.text)
#         return response.text
#     else:
#         logger.info(f"Failed to retrieved PA system info: {response.status_code}")
#         logger.info(response.text)


def display_obj_services(pa_url: str, api_key: str) -> dict:
    api = "/restapi/v11.2/Objects/Services"
    url = pa_url + api
    logger.info("Display object services...")
    headers = {
        "X-PAN-KEY": api_key
    }

    location = {
        "location": "vsys",
        "vsys": "vsys1",
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object services successfully retrieved.")
        logger.info(response.text)
        return json.loads(response.text)  # convert json to dictionary
    else:
        logger.info(f"Failed to retrieved PA object services data: {response.status_code}")
        logger.info(response.text)


def create_obj_services(pa_url: str, api_key: str, name: str, protocol: str, port: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Objects/Services"
    url = pa_url + api
    logger.info("Create object service...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
           {
                "@name": name,
                "description": desc,
                "protocol": {
                    protocol: {
                        "port": port,
                        # "source-port": "0,1-65535",
                        # "override": {
                        #     "no": {}
                        # }
                    }
                }
                # "tag": {
                #     "member": [
                #         "some_tag"
                #     ]
                # }
           }
    })

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object service successfully created.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to create object service: {response.status_code}")
        logger.info(response.text)


def update_obj_services(pa_url: str, api_key: str, name: str, protocol: str, port: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Objects/Services"
    url = pa_url + api
    logger.info("Update object services...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
           {
                "@name": name,
                "description": desc,
                "protocol": {
                    protocol: {
                        "port": port,
                        # "source-port": "0,1-65535",
                        # "override": {
                        #     "no": {}
                        # }
                    }
                }
                # "tag": {
                #     "member": [
                #         "some_tag"
                #     ]
                # }
           }
    })

    response = requests.put(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object service successfully updated.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to update object serivice: {response.status_code}")
        logger.info(response.text)


def delete_obj_services(pa_url: str, api_key: str, name: str) -> None:
    api = "/restapi/v11.2/Objects/Services"
    url = pa_url + api
    logger.info("Delete object service...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.delete(
        url=url,
        headers=headers,
        params=location,
        # data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object service successfully deleted.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to delete object service: {response.status_code}")
        logger.info(response.text)


def rename_obj_services(pa_url: str, api_key: str, name: str, new_name: str) -> None:
    api = "/restapi/v11.2/Objects/Services:rename"
    url = pa_url + api
    logger.info("Rename object service...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "newname": new_name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object service successfully renamed.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to rename object service: {response.status_code}")
        logger.info(response.text)


def display_obj_addresses(pa_url: str, api_key: str) -> dict:
    api = "/restapi/v11.2/Objects/Addresses"
    url = pa_url + api
    logger.info("Display object addresses...")
    headers = {
        "X-PAN-KEY": api_key
    }

    location = {
        "location": "vsys",
        "vsys": "vsys1",
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object addresses successfully retrieved.")
        logger.info(response.text)
        return response.text
    else:
        logger.info(f"Failed to retrieved PA object addresses data: {response.status_code}")
        logger.info(response.text)


def create_obj_addresses(pa_url: str, api_key: str, name: str, ip_add: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Objects/Addresses"
    url = pa_url + api
    logger.info("Create object addresses...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
           {
                "@name": name,
                "ip-netmask": ip_add,
                "description": desc,
                # "tag": {
                #     "member": [
                #         "some_tag"
                #     ]
                # }
           }
    })

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object addresses successfully created.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to create object address: {response.status_code}")
        logger.info(response.text)


def rename_obj_addresses(pa_url: str, api_key: str, name: str, new_name: str) -> None:
    api = "/restapi/v11.2/Objects/Addresses:rename"
    url = pa_url + api
    logger.info("Rename object addresses...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "newname": new_name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object addresses successfully renamed.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to rename object address: {response.status_code}")
        logger.info(response.text)


def update_obj_addresses(pa_url: str, api_key: str, name: str, ip_add: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Objects/Addresses"
    url = pa_url + api
    logger.info("Update object addresses...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
           {
                "@name": name,
                "ip-netmask": ip_add,
                "description": desc,
           }
    })

    response = requests.put(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object addresses successfully updated.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to update object address: {response.status_code}")
        logger.info(response.text)


def delete_obj_addresses(pa_url: str, api_key: str, name: str) -> None:
    api = "/restapi/v11.2/Objects/Addresses"
    url = pa_url + api
    logger.info("Delete object addresses...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.delete(
        url=url,
        headers=headers,
        params=location,
        # data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA object addresses successfully deleted.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to delete object address: {response.status_code}")
        logger.info(response.text)


def display_address_groups(pa_url: str, api_key: str) -> dict:
    api = "/restapi/v11.2/Objects/AddressGroups"
    url = pa_url + api
    logger.info("Display address groups...")
    headers = {
        "X-PAN-KEY": api_key
    }

    location = {
        "location": "vsys",
        "vsys": "vsys1",
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA address groups successfully retrieved.")
        logger.info(response.text)
        return response.text
    else:
        logger.info(f"Failed to retrieved PA address groups data: {response.status_code}")
        logger.info(response.text)


def create_address_group(pa_url: str, api_key: str, name: str, group: list, desc: str = "") -> None:
    api = "/restapi/v11.2/Objects/AddressGroups"
    url = pa_url + api
    logger.info("Create address group...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
           {
                "@name": name,
                "static": {
                    "member": group
                },
                "description": desc,
                # "tag": {
                #     "member": [
                #         "some_tag"
                #     ]
                # }
           }
    })

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA address group successfully created.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to create address group: {response.status_code}")
        logger.info(response.text)


def update_address_group(pa_url: str, api_key: str, name: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Objects/AddressGroups"
    url = pa_url + api
    logger.info("Update address group...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
           {
                "@name": name,
                "static": {
                    "member": [
                        "dns1",
                        "dns2"
                    ]
                },
                "description": desc,
           }
    })

    response = requests.put(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA address group successfully updated.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to update address group: {response.status_code}")
        logger.info(response.text)


def delete_address_group(pa_url: str, api_key: str, name: str) -> None:
    api = "/restapi/v11.2/Objects/AddressGroups"
    url = pa_url + api
    logger.info("Delete address group...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.delete(
        url=url,
        headers=headers,
        params=location,
        # data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA address group successfully deleted.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to delete address group: {response.status_code}")
        logger.info(response.text)


def rename_address_group(pa_url: str, api_key: str, name: str, new_name: str) -> None:
    api = "/restapi/v11.2/Objects/AddressGroups:rename"
    url = pa_url + api
    logger.info("Rename address group...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "newname": new_name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA address group successfully renamed.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to rename address group: {response.status_code}")
        logger.info(response.text)


def display_sec_policies(pa_url: str, api_key: str) -> dict:
    api = "/restapi/v11.2/Policies/SecurityRules"
    url = pa_url + api
    logger.info("Display policies...")
    headers = {
        "X-PAN-KEY": api_key
    }

    location = {
        "location": "vsys",
        "vsys": "vsys1",
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA policies data successfully retrieved.")
        # logger.info(response.text)
        return json.loads(response.text)  # convert json to dictionary
    else:
        logger.info(f"Failed to retrieved PA policies data: {response.status_code}")
        logger.info(response.text)


def create_sec_policy(pa_url: str, api_key: str, name: str, src_zone: str, src_addr: str,  
                      dst_zone: str, dst_addr: str, app: str, 
                      service: list, action: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Policies/SecurityRules"
    url = pa_url + api
    logger.info("Create security policy...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry":
        {
            "@name": name,
            "from": {  # source zone
                "member": [
                    src_zone
                ]
            },
            "to": {  # destination zone
                "member": [
                    dst_zone
                ]
            },
            "source": {
                "member": [
                    src_addr
                ]
            },
            "destination": {
                "member": [
                    dst_addr
                ]
            },
            "application": {
                "member": [
                    app
                ]
            },
            "service": {
                "member": service
            },
            "action": action,
            "description": desc
            # "source-user": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "category": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "source-imsi": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "source-imei": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "source-nw-slice": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "source-hip": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "destination-hip": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "saas-user-list": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "saas-tenant-list": {
            #     "member": [
            #         "any"
            #     ]
            # },
            # "negate-source": "no",
            # "negate-destination": "no",
            # "disabled": "no",
            # "tag": {
            #     "member": [
            #         "string"
            #     ]
            # },
            # "group-tag": "string",
            # "schedule": "string",
            # "icmp-unreachable": "no",
            # "disable-inspect": "no",
            # "rule-type": "universal",
            # "option": {
            #     "disable-server-response-inspection": "no"
            # },
            # "profile-setting": {},
            # "qos": {},
            # "log-setting": "string",
            # "log-start": "no",
            # "log-end": "yes",
        }
    })

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA security policy successfully created.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to create security policy: {response.status_code}")
        logger.info(response.text)


def update_sec_policy(pa_url: str, api_key: str, name: str, src_zone: str, src_addr: str,  
                      dst_zone: str, dst_addr: str, app: str, 
                      service: list, action: str, desc: str = "") -> None:
    api = "/restapi/v11.2/Policies/SecurityRules"
    url = pa_url + api
    logger.info("Update security policy...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    payload = json.dumps({
        "entry": 
        {
            "@name": name,
            "from": {  # source zone
                "member": [
                    src_zone
                ]
            },
            "to": {  # destination zone
                "member": [
                    dst_zone
                ]
            },
            "source": {
                "member": [
                    src_addr
                ]
            },
            "destination": {
                "member": [
                    dst_addr
                ]
            },
            "application": {
                "member": [
                    app
                ]
            },
            "service": {
                "member": service  # list
            },
            "action": action,
            "description": desc
        }
    })

    response = requests.put(
        url=url,
        headers=headers,
        params=location,
        data=payload,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA security policy successfully updated.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to update security policy: {response.status_code}")
        logger.info(response.text)


def delete_sec_policy(pa_url: str, api_key: str, name: str) -> None:
    api = "/restapi/v11.2/Policies/SecurityRules"
    url = pa_url + api
    logger.info("Delete security policy...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.delete(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA security policy successfully deleted.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to delete security policy: {response.status_code}")
        logger.info(response.text)


def rename_security_policy(pa_url: str, api_key: str, name: str, new_name: str) -> None:
    api = "/restapi/v11.2/Policies/SecurityRules:rename"
    url = pa_url + api
    logger.info("Rename security policy...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "newname": new_name,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA security policy successfully renamed.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to rename security policy: {response.status_code}")
        logger.info(response.text)


def move_security_policy(pa_url: str, api_key: str, name: str, from_where: str, to_where: str = "") -> None:
    api = "/restapi/v11.2/Policies/SecurityRules:move"
    url = pa_url + api
    logger.info("Move security policy...")
    headers = {
        "X-PAN-KEY": api_key,
        "Content-Type": "application/json"
    }

    location = {
        "name": name,
        "where": from_where,
        "dst": to_where,
        "location": "vsys",
        "vsys": "vsys1"
    }

    response = requests.post(
        url=url,
        headers=headers,
        params=location,
        verify=False
    )

    if response.status_code == 200:
        logger.info("PA security policy successfully moved.")
        logger.info(response.text)
        return None
    else:
        logger.info(f"Failed to move security policy: {response.status_code}")
        logger.info(response.text)


def main() -> None:
    # xml_get_system_info(api_url, pa_api_key)
    get_api_key(api_url, "api_rw", "Cisco123")

    display_obj_services(api_url, pa_api_key)
    # create_obj_services(api_url, pa_api_key, "csp2", "udp", "22,24-27", "Custom service port2")
    # update_obj_services(api_url, pa_api_key, "custom_service_port", "tcp", "22,24-31", "Updated2 custom service port")
    # delete_obj_services(api_url, pa_api_key, "proxy1")
    # rename_obj_services(api_url, pa_api_key, "csp1", "csp1_1")

    display_obj_addresses(api_url, pa_api_key)
    # create_obj_addresses(api_url, pa_api_key, "server2", "10.0.0.2/32", "Server 2")
    # update_obj_addresses(api_url, pa_api_key, "google_dns3", "1.1.1.1/32", "DNS server 3")
    # delete_obj_addresses(api_url, pa_api_key, "dns_server_5")
    # rename_obj_addresses(api_url, pa_api_key, "dns5", "dns_server_5")

    display_address_groups(api_url, pa_api_key)
    # create_address_group(api_url, pa_api_key, "Servers", ["server1", "server2"], "some servers")
    # update_address_group(api_url, pa_api_key, "DNS_servers", "updated description")
    # delete_address_group(api_url, pa_api_key, "DNS_servers2")
    # rename_address_group(api_url, pa_api_key, "DNS_servers", "All_DNS_servers")

    display_sec_policies(api_url, pa_api_key)
    # For custom services: application: "any", service: "custom_service_port"
    # create_sec_policy(api_url, pa_api_key, "CUST-A-app-99-man", "WAN_zone", "Users", 
    #                   "DC_zone", "Other_apps", "any", ["tcp_7700", "tcp_7701", "tcp_7702"], 
    #                   "allow", "APP manual")
    # update_sec_policy(api_url, pa_api_key, "Allow_all_7", "WAN_zone", "DC_zone", 
    #                   "Servers", "All_DNS_servers", "icmp", "application-default", 
    #                   "allow", "Allow all traffic rule 7")
    # delete_sec_policy(api_url, pa_api_key, "Allow_all_traffic4")
    # rename_security_policy(api_url, pa_api_key, "Allow_all_zones5", "Allow_all_5")
    # possible values for from_where: top, bottom, above, below
    # move_security_policy(api_url, pa_api_key, "Allow_all_7", "bottom")


if __name__ == "__main__":
    main()