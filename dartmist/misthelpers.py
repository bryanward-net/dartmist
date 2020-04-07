#!/usr/bin/env python

import requests
import string
import logging

####################
###
### misthelpers.py
###
### Python wrapper for interacting with the Mist API
### Written by Felix Windt and Bryan Ward, 2019-2020
###
### Version 20200308
###
####################

class MistHelpers:
    def __init__(self, api):
        self.api = api


    def get_sites(self):
        sites = self.api.get("orgs/{0}/sites".format(self.api.org_id))
        return sites


    def get_site_by_name(self, name):
        for site in self.get_sites():
            if site["name"] == name:
                return site
        return None


    def get_devices_stats_in_site(self, site_id):
        devices = self.api.get("/sites/{0}/stats/devices".format(site_id))
        logging.debug(devices)
        return devices


    def get_device_stats_in_site_by_mac(self, site_id, mac):
        mac = mac.replace(":", "").replace("-", "").replace(".", "").lower()
        devices = self.api.get("/sites/{0}/stats/devices".format(site_id))
        device=list(filter(lambda device: device['mac'] == mac, devices))
        if len(device) == 1:
            return device[0]
        elif len(device) < 1:
            return None
        else:
            if self.api.ignore_failures:
                return None
            else:
                raise Exception("Found more than one matching AP")


    def get_devices_in_site(self, site_id):
        devices = self.api.get("/sites/{0}/devices/search?limit=-1".format(site_id))["results"]
        logging.debug(devices)
        return devices


    def get_device_in_site_by_mac(self, site_id, mac):
        mac = mac.replace(":", "").replace("-", "").replace(".", "").lower()
        results = self.api.get("sites/{0}/devices/search?mac={1}".format(site_id, mac))
        logging.debug(results)
        if results["total"] == 1:
            return results["results"][0]
        elif results["total"] < 1:
            return None
        else:
            if self.api.ignore_failures:
                return None
            else:
                raise Exception("Found more than one matching AP")


    def get_all_devices(self):
        result = []
        for site in self.get_sites():
            this_site = {"site": site["name"], "site_id": site["id"]}
            this_site["devices"] = self.get_devices_in_site(site["id"])
            result.append(this_site)


    def get_ap_by_mac(self, mac, site):
        mac = mac.replace(":", "").replace("-", "").replace(".", "").lower()
        aps = self.api.get("sites/{0}/devices".format(site))
        for ap in aps:
            if ap["mac"] == mac:
                return ap
        return None


    def get_ap_fw_ver_by_mac(self, mac, site):
        mac = mac.replace(":", "").replace("-", "").replace(".", "").lower()
        ap = self.get("sites/{0}/devices/search?mac={1}".format(site,mac))
        if (ap['total'] == 1):   ###and mac in ap['results']['mac']['hostname']):
            print(ap['results'][0]['version'])
            return ap['results'][0]['version']
        return None

    def get_devices(self, site):
        devices = None
        devices = self.api.get("sites/{0}/stats/devices".format(site))
        return devices

    def get_device_by_id(self, device_id, site):
        device = None
        device = self.api.get("sites/{0}/stats/devices/{1}".format(site,device_id))
        return device

    def get_device_by_name(self, device_name, site):
        device = None
        device = self.api.get("sites/{0}/stats/devices?name={1}".format(site,device_name))
        return device

    def get_device_by_mac2(self, device_mac, site):
        device = None
        device = self.api.get("sites/{0}/stats/devices/00000000-0000-0000-1000-{1}".format(site,device_mac.translate(str.maketrans('', '', string.punctuation)).lower()))
        return device

    def get_device_fw(self, device):
        fw = None
        fw = device['version']
        return fw

    def update_fw(self, site, device, version):
        status = None
        if version is not None:
            logging.debug("About to command FW update...")
            #from pudb import set_trace
            #logging.disable(logging.CRITICAL)
            #set_trace()
            status = self.api.post("sites/{0}/devices/{1}/upgrade".format(site, device['id']), payload={'version': version})
            return status
        return


