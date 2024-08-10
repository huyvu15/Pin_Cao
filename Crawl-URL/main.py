from selenium import webdriver
from pinterest import Pinterest
from sys import exit
from exceptions import *
import chromedriver_autoinstaller
import json
import yaml
import os.path
import argparse
import csv

if __name__ == "__main__":
    currentdir = os.getcwd()

    # Using argparse
    parser = argparse.ArgumentParser(description='An infinite Pinterest crawler. Author: mirusu400')

    parser.add_argument('-e', '--email', required=False, default="", help='Your Pinterest account email')
    parser.add_argument('-p', '--password', required=False, default="", help='Your Pinterest account password')
    parser.add_argument('-n', '--name', required=False, default="", help='Name to save URLs')
    parser.add_argument('-l', '--link', required=False, default="", help='Link of Pinterest which you want to scrape')
    parser.add_argument('-g', '--page', required=False, default="", help='Number of pages which you want to scrape')
    parser.add_argument('-b', '--batch', required=False, default=False, action="store_true", help='Enable batch mode (Please read README.md!!)')
    args = parser.parse_args()

    email = args.email
    password = args.password
    name = args.name
    link = args.link
    pages = args.page
    batch = args.batch
    
    yaml_email = ""
    yaml_password = ""
    yaml_name = ""
    

    # Check chromedriver exists
    chromedriver_autoinstaller.install()

    # Check yaml exists
    if os.path.isfile(currentdir + "/config.yaml"):
        with open("./config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            yaml_email = config["email"]
            yaml_password = config["password"]
            yaml_name = config["name"]

    if email == "":
        if yaml_email != "":
            email = yaml_email
        else: 
            email = ''

    if password == "":
        if yaml_password:
            password = yaml_password
        else: 
            password = ''
    
    name_list = []
    link_list = []
    if batch:
        print("Batch mode Enabled. You will collect a bunch of URLs..")
        if not os.path.exists(currentdir + "/batch.json"):
            print("Batch.json file not found! Please read README.md...")
            exit()
        batch_list = json.loads(open(currentdir + "/batch.json").read())
        for item in batch_list:
            name_list.append(item["name"])
            link_list.append(item["link"])
    else:
        if name == "":
            if yaml_name:
                name = yaml_name
            else: 
                # name = "download/" + input("Enter the name to save the URLs (Blank if you set default): ")
                name = input("Enter the name to save the URLs (Blank if you set default): ")
        if name == "":
            name = "default"

        if link == "":
            link = input("Enter the link to scrape (Blank if default; Pinterest main page): ")
        if link == "":
            link = "https://pinterest.com/"

    if pages == "":
        pages = 10
    if pages == "" or int(pages) == 0:
        pages = 999
    else:
        pages = int(pages)

    print("Open selenium...")
    p = Pinterest(email, password)
    
    if not batch:
        print("Collecting URLs")
        p.single_download(pages, link, name)
    else:
        print("Collecting URLs in Batch mode...")
        p.batch_download(pages, link_list, name_list)

