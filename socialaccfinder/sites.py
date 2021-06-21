"""SocialAccFinder Sites Information Module

This module supports storing information about web sites.
This is the raw data that will be used to search for usernames.
"""
import os
import json
import operator
import requests
import sys


class SiteInformation():
    def __init__(self, name, url_home, url_username_format, username_claimed,
                 username_unclaimed, information):
        self.name                = name
        self.url_home            = url_home
        self.url_username_format = url_username_format

        self.username_claimed    = username_claimed
        self.username_unclaimed  = username_unclaimed
        self.information         = information

        return

    def __str__(self):

        return f"{self.name} ({self.url_home})"


class SitesInformation():
    def __init__(self, data_file_path='resources/data.json'):

        if data_file_path is None:
            data_file_path = "https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock/resources/data.json"

        # Ensure that specified data file has correct extension.
        if not data_file_path.lower().endswith(".json"):
            raise FileNotFoundError(f"Incorrect JSON file extension for data file '{data_file_path}'.")

        if "http://"  == data_file_path[:7].lower() or "https://" == data_file_path[:8].lower():
            # Reference is to a URL.
            try:
                response = requests.get(url=data_file_path)
            except Exception as error:
                raise FileNotFoundError(f"Problem while attempting to access "
                                        f"data file URL '{data_file_path}':  "
                                        f"{str(error)}"
                                       )
            if response.status_code == 200:
                try:
                    site_data = response.json()
                except Exception as error:
                    raise ValueError(f"Problem parsing json contents at "
                                     f"'{data_file_path}':  {str(error)}."
                                    )
            else:
                raise FileNotFoundError(f"Bad response while accessing "
                                        f"data file URL '{data_file_path}'."
                                       )
        else:
            # Reference is to a file.
            try:
                with open(data_file_path, "r", encoding="utf-8") as file:
                    try:
                        site_data = json.load(file)
                    except Exception as error:
                        raise ValueError(f"Problem parsing json contents at "
                                         f"'{data_file_path}':  {str(error)}."
                                        )
            except FileNotFoundError as error:
                raise FileNotFoundError(f"Problem while attempting to access "
                                        f"data file '{data_file_path}'."
                                       )

        self.sites = {}

        # Add all of site information from the json file to internal site list.
        for site_name in site_data:
            try:

                self.sites[site_name] = \
                    SiteInformation(site_name,
                                    site_data[site_name]["urlMain"],
                                    site_data[site_name]["url"],
                                    site_data[site_name]["username_claimed"],
                                    site_data[site_name]["username_unclaimed"],
                                    site_data[site_name]
                                   )
            except KeyError as error:
                raise ValueError(f"Problem parsing json contents at "
                                 f"'{data_file_path}':  "
                                 f"Missing attribute {str(error)}."
                                )

        return

    def site_name_list(self):
        site_names = sorted([site.name for site in self], key=str.lower)

        return site_names

    def __iter__(self):
        for site_name in self.sites:
            yield self.sites[site_name]

    def __len__(self):
        return len(self.sites)
