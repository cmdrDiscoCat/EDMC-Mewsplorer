#!/usr/bin/env python3
"""plugin that lists every body you discovered in the system you're scanning,
with their type (ww, elw, gg) and a mention if they're terraformable."""

import logging
import os
import re
import ctypes
import sys
import tkinter as tk
from tkinter import LEFT

# This could also be returned from plugin_start3()
appname = "Mewsplorer"
plugin_name = os.path.basename(os.path.dirname(__file__))

this = sys.modules[__name__]
this.terraformables_text = ""
this.status_text = "waiting for scans"

# Lists for the elements we want to keep in memory
this.elw_list = []
this.ww_list = []
this.aw_list = []
this.hmc_list = []
this.rw_list = []
this.riw_list = []
this.iw_list = []
this.gg_list = []
this.wg_list = []
this.tf_list = []
this.current_system = ""

# Logger per found plugin, so the folder name is included in
# the logging format.
logger = logging.getLogger(f'{appname}.{plugin_name}')
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_channel.setLevel(level)
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')  # noqa: E501
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)


def debug(d):
    print(('[Mewsplorer] ' + str(d)))


def plugin_start3(plugin_dir):
    plugin_start(plugin_dir)


def plugin_start(plugin_dir):
    """
    Plugin startup method.
    :param plugin_dir:
    :return: 'Pretty' name of this plugin.
    """
    debug("plugin_start")
    logger.info(f'[Mewsplorer]Folder is {plugin_dir}')

    return plugin_name


def plugin_stop():
    """
    Plugin stop method.
    :return:
    """
    debug("plugin_stop")
    logger.info('[Mewsplorer] Stopping')


def plugin_app(parent):
    this.frame = tk.Frame(parent)

    wcategory = 10
    wlist = 28

    this.mewcontainer = tk.Frame(this.frame)
    this.mewcontainer.rowconfigure(6)
    this.mewcontainer.columnconfigure(2)
    
    r = 0

    this.mewlabelelw = tk.Label(this.mewcontainer, text="ELW:", width=wcategory)
    this.mewlabelelw.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelelw.configure(anchor="w")
    this.mewelw = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewelw.grid(row=r, column=1, sticky=tk.W)
    this.mewelw.configure(anchor="w")

    r += 1

    this.mewlabelww = tk.Label(this.mewcontainer, text="WW:", width=wcategory)
    this.mewlabelww.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelww.configure(anchor="w")
    this.mewww = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewww.grid(row=r, column=1, sticky=tk.W)
    this.mewww.configure(anchor="w")

    r += 1

    this.mewlabelaw = tk.Label(this.mewcontainer, text="AW:", width=wcategory)
    this.mewlabelaw.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelaw.configure(anchor="w")
    this.mewaw = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewaw.grid(row=r, column=1, sticky=tk.W)
    this.mewaw.configure(anchor="w")

    r += 1

    this.mewlabelhmc = tk.Label(this.mewcontainer, text="HMC:", width=wcategory)
    this.mewlabelhmc.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelhmc.configure(anchor="w")
    this.mewhmc = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewhmc.grid(row=r, column=1, sticky=tk.W)
    this.mewhmc.configure(anchor="w")

    r += 1

    this.mewlabelgg = tk.Label(this.mewcontainer, text="GG:", width=wcategory)
    this.mewlabelgg.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelgg.configure(anchor="w")
    this.mewgg = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewgg.grid(row=r, column=1, sticky=tk.W)
    this.mewgg.configure(anchor="w")

    r += 1

    this.mewlabelwg = tk.Label(this.mewcontainer, text="WG:", width=wcategory)
    this.mewlabelwg.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelwg.configure(anchor="w")
    this.mewwg = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewwg.grid(row=r, column=1, sticky=tk.W)
    this.mewwg.configure(anchor="w")

    r += 1

    this.mewlabelriw = tk.Label(this.mewcontainer, text="Rocky icy:", width=wcategory)
    this.mewlabelriw.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelriw.configure(anchor="w")
    this.mewriw = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewriw.grid(row=r, column=1, sticky=tk.W)
    this.mewriw.configure(anchor="w")

    r += 1

    this.mewlabelrw = tk.Label(this.mewcontainer, text="Rocky:", width=wcategory)
    this.mewlabelrw.grid(row=r, column=0, sticky=tk.W)
    this.mewlabelrw.configure(anchor="w")
    this.mewrw = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewrw.grid(row=r, column=1, sticky=tk.W)
    this.mewrw.configure(anchor="w")

    r += 1

    this.mewlabeliw = tk.Label(this.mewcontainer, text="Icy:", width=wcategory)
    this.mewlabeliw.grid(row=r, column=0, sticky=tk.W)
    this.mewlabeliw.configure(anchor="w")
    this.mewiw = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewiw.grid(row=r, column=1, sticky=tk.W)
    this.mewiw.configure(anchor="w")

    r += 1

    this.mewlabeltf = tk.Label(this.mewcontainer, text="TF:", width=wcategory)
    this.mewlabeltf.grid(row=r, column=0, sticky=tk.W)
    this.mewlabeltf.configure(anchor="w")
    this.mewtf = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewtf.grid(row=r, column=1, sticky=tk.W)
    this.mewtf.configure(anchor="w")

    r += 1

    this.mewlabellatest = tk.Label(this.mewcontainer, text="Last Scan:", width=wcategory)
    this.mewlabellatest.grid(row=r, column=0, sticky=tk.W)
    this.mewlabellatest.configure(anchor="w")
    this.mewlatest = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewlatest.grid(row=r, column=1, sticky=tk.W)
    this.mewlatest.configure(anchor="w")

    r += 1

    this.mewlabeldg = tk.Label(this.mewcontainer, text="Debug:", width=wcategory)
    this.mewlabeldg.grid(row=r, column=0, sticky=tk.W)
    this.mewlabeldg.configure(anchor="w")
    this.mewdg = tk.Label(this.mewcontainer, text="", fg="white", width=wlist, wraplength=200)
    this.mewdg.grid(row=r, column=1, sticky=tk.W)
    this.mewdg.configure(anchor="w")

    this.mewcontainer.pack(side=LEFT)

    return this.frame



def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

def prepare_lists():
    """
    Sorts and put the join character in all the lists so I don't have to do it everywhere
    :return:
    """
    this.elw_list = natural_sort(this.elw_list)
    this.ww_list = natural_sort(this.ww_list)
    this.aw_list = natural_sort(this.aw_list)
    this.hmc_list = natural_sort(this.hmc_list)
    this.rw_list = natural_sort(this.rw_list)
    this.riw_list = natural_sort(this.riw_list)
    this.iw_list = natural_sort(this.iw_list)
    this.gg_list = natural_sort(this.gg_list)
    this.wg_list = natural_sort(this.wg_list)
    this.tf_list = natural_sort(this.tf_list)


def journal_entry(cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
    """
    Handle the given journal entry.
    :param cmdrname:
    :param is_beta:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return: None
    """
    logger.debug(f'[Mewsplorer] cmdr = "{cmdrname}", is_beta = "{is_beta}", system = "{system}", station = "{station}"')
    found = ''
    if entry['event'] in ['Scan', 'Location', 'FSDJump', 'SAAScanComplete']:
        if entry['event'] == 'SAAScanComplete':
            this.mewdg["text"] = entry
        else:
            this.mewdg["text"] = entry["event"]

    # Then, we check many things to add to the different list (elw, ww, aw and tf) if the event is a scan
    if entry['event'] == 'Scan':
        bodyname = str(entry["BodyName"])
        bodyname = bodyname.replace(system+" ", '').replace(" ", "")
        bodyname_mapped = bodyname+"*"

        if "Earthlike body" in str(entry['PlanetClass']):
            if not bodyname in this.elw_list and not bodyname_mapped in this.elw_list:
                this.elw_list.append(bodyname)
                prepare_lists()
                this.mewelw["text"] = ' | '.join(this.elw_list)
                this.mewlatest["text"] = bodyname

        if "Water world" in str(entry['PlanetClass']):
            if not bodyname in this.ww_list and not bodyname_mapped in this.ww_list:
                this.ww_list.append(bodyname)
                prepare_lists()
                this.mewww["text"] = ' | '.join(this.ww_list)
                this.mewlatest["text"] = bodyname

        if "Ammonia world" in str(entry['PlanetClass']):
            if not bodyname in this.aw_list and not bodyname_mapped in this.aw_list:
                this.aw_list.append(bodyname)
                prepare_lists()
                this.mewaw["text"] = ' | '.join(this.aw_list)
                this.mewlatest["text"] = bodyname

        if 'High metal content body' in str(entry['PlanetClass']):
            if not bodyname in this.hmc_list and not bodyname_mapped in this.hmc_list:
                this.hmc_list.append(bodyname)
                prepare_lists()
                this.mewhmc["text"] = ' | '.join(this.hmc_list)
                this.mewlatest["text"] = bodyname

        if "Rocky body" in str(entry['PlanetClass']):
            if not bodyname in this.rw_list and not bodyname_mapped in this.rw_list:
                this.rw_list.append(bodyname)
                prepare_lists()
                this.mewrw["text"] = ' | '.join(this.rw_list)
                this.mewlatest["text"] = bodyname

        if "Icy body" in str(entry['PlanetClass']):
            if not bodyname in this.iw_list and not bodyname_mapped in this.iw_list:
                this.iw_list.append(bodyname)
                prepare_lists()
                this.mewiw["text"] = ' | '.join(this.iw_list)
                this.mewlatest["text"] = bodyname

        if "Rocky ice body" in str(entry['PlanetClass']):
            if not bodyname in this.riw_list and not bodyname_mapped in this.riw_list:
                this.riw_list.append(bodyname)
                prepare_lists()
                this.mewriw["text"] = ' | '.join(this.riw_list)
                this.mewlatest["text"] = bodyname

        if str(entry['PlanetClass']).find("Gas giant") != -1:
            if not bodyname in this.gg_list and not bodyname_mapped in this.gg_list:
                this.gg_list.append(bodyname)
                prepare_lists()
                this.mewgg["text"] = ' | '.join(this.gg_list)
                this.mewlatest["text"] = bodyname
        else:
            if str(entry['PlanetClass']).find("gas giant") != -1:
                if not bodyname in this.gg_list and not bodyname_mapped in this.gg_list:
                    this.gg_list.append(bodyname)
                    prepare_lists()
                    this.mewgg["text"] = ' | '.join(this.gg_list)
                    this.mewlatest["text"] = bodyname

        if str(entry['PlanetClass']).find("Water giant") != -1:
            if not bodyname in this.wg_list and not bodyname_mapped in this.wg_list:
                this.wg_list.append(bodyname)
                prepare_lists()
                this.mewwg["text"] = ' | '.join(this.wg_list)
                this.mewlatest["text"] = bodyname

        if entry['TerraformState'] != '':
            if not bodyname in this.tf_list and not bodyname_mapped in this.tf_list:
                this.tf_list.append(bodyname)
                prepare_lists()
                this.mewtf["text"] = ' | '.join(this.tf_list)
    else:
        if entry['event'] == 'SAAScanComplete':
            # This happens when we fully mapped a body
            # We recreate the same name as we could find on list
            bodyname = str(entry["BodyName"])
            bodyname = bodyname.replace(system+" ", '').replace(" ", "")
            this.mewdg['text'] = "Mapped "+bodyname
            prepare_lists()

            #Then we check each list to find that body
            for index, item in enumerate(this.elw_list):
                if (item == bodyname):
                    this.elw_list[index] = bodyname + '*'
                    this.mewelw["text"] = ' | '.join(this.elw_list)

            for index, item in enumerate(this.ww_list):
                if (item == bodyname):
                    this.ww_list[index] = bodyname + '*'
                    this.mewww["text"] = ' | '.join(this.ww_list)

            for index, item in enumerate(this.aw_list):
                if (item == bodyname):
                    this.aw_list[index] = bodyname + '*'
                    this.mewaw["text"] = ' | '.join(this.aw_list)

            for index, item in enumerate(this.hmc_list):
                if (item == bodyname):
                    this.hmc_list[index] = bodyname + '*'
                    this.mewhmc["text"] = ' | '.join(this.hmc_list)

            for index, item in enumerate(this.rw_list):
                if (item == bodyname):
                    this.rw_list[index] = bodyname + '*'
                    this.mewrw["text"] = ' | '.join(this.rw_list)

            for index, item in enumerate(this.iw_list):
                if (item == bodyname):
                    this.iw_list[index] = bodyname + '*'
                    this.mewiw["text"] = ' | '.join(this.iw_list)

            for index, item in enumerate(this.riw_list):
                if (item == bodyname):
                    this.riw_list[index] = bodyname + '*'
                    this.mewriw["text"] = ' | '.join(this.riw_list)

            for index, item in enumerate(this.gg_list):
                if (item == bodyname):
                    this.gg_list[index] = bodyname + '*'
                    this.mewgg["text"] = ' | '.join(this.gg_list)

            for index, item in enumerate(this.wg_list):
                if (item == bodyname):
                    this.wg_list[index] = bodyname + '*'
                    this.mewwg["text"] = ' | '.join(this.wg_list)

            for index, item in enumerate(this.tf_list):
                if (item == bodyname):
                    this.tf_list[index] = bodyname + '*'
                    this.mewtf["text"] = ' | '.join(this.tf_list)



    if entry['event'] == 'Location' or entry['event'] == 'FSDJump':
        this.elw_list.clear()
        this.ww_list.clear()
        this.aw_list.clear()
        this.hmc_list.clear()
        this.rw_list.clear()
        this.riw_list.clear()
        this.iw_list.clear()
        this.gg_list.clear()
        this.wg_list.clear()
        this.tf_list.clear()

        this.mewelw["text"] = ""
        this.mewww["text"] = ""
        this.mewaw["text"] = ""
        this.mewhmc["text"] = ""
        this.mewrw["text"] = ""
        this.mewiw["text"] = ""
        this.mewriw["text"] = ""
        this.mewgg["text"] = ""
        this.mewwg["text"] = ""

        this.mewtf["text"] = ""
        this.mewlatest["text"] = ""

