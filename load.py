#!/usr/bin/env python3
"""plugin that lists every body you discovered in the system you're scanning,
with their type (ww, elw, gg) and a mention if they're terraformable."""

import logging
import os
import ctypes
import sys
import tkinter as tk

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

    this.mewcontainer = tk.Frame(this.frame)
    this.mewcontainer.rowconfigure(6)
    this.mewcontainer.columnconfigure(2)
    
    r = 0

    this.mewlabelelw = tk.Label(this.mewcontainer, text="ELW:")
    this.mewlabelelw.grid(row=0, column=0, sticky=tk.W)
    this.mewelw = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewelw.grid(row=0, column=1, sticky=tk.W)

    r += 1

    this.mewlabelww = tk.Label(this.mewcontainer, text="Water worlds:")
    this.mewlabelww.grid(row=r, column=0, sticky=tk.W)
    this.mewww = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewww.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabelaw = tk.Label(this.mewcontainer, text="Ammonia worlds:")
    this.mewlabelaw.grid(row=r, column=0, sticky=tk.W)
    this.mewaw = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewaw.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabelhmc = tk.Label(this.mewcontainer, text="HMC:")
    this.mewlabelhmc.grid(row=r, column=0, sticky=tk.W)
    this.mewhmc = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewhmc.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabelgg = tk.Label(this.mewcontainer, text="Gas giants:")
    this.mewlabelgg.grid(row=r, column=0, sticky=tk.W)
    this.mewgg = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewgg.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabelwg = tk.Label(this.mewcontainer, text="Water giants:")
    this.mewlabelwg.grid(row=r, column=0, sticky=tk.W)
    this.mewwg = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewwg.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabelriw = tk.Label(this.mewcontainer, text="Rocky icy worlds:")
    this.mewlabelriw.grid(row=r, column=0, sticky=tk.W)
    this.mewriw = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewriw.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabelrw = tk.Label(this.mewcontainer, text="Rocky worlds:")
    this.mewlabelrw.grid(row=r, column=0, sticky=tk.W)
    this.mewrw = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewrw.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabeliw = tk.Label(this.mewcontainer, text="Icy worlds:")
    this.mewlabeliw.grid(row=r, column=0, sticky=tk.W)
    this.mewiw = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewiw.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabeltf = tk.Label(this.mewcontainer, text="TF:")
    this.mewlabeltf.grid(row=r, column=0, sticky=tk.W)
    this.mewtf = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewtf.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabellatest = tk.Label(this.mewcontainer, text="Last Scan:")
    this.mewlabellatest.grid(row=r, column=0, sticky=tk.W)
    this.mewlatest = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewlatest.grid(row=r, column=1, sticky=tk.W)

    r += 1

    this.mewlabeldg = tk.Label(this.mewcontainer, text="Debug:")
    this.mewlabeldg.grid(row=r, column=0, sticky=tk.W)
    this.mewdg = tk.Label(this.mewcontainer, text="", fg="white")
    this.mewdg.grid(row=r, column=1, sticky=tk.W)

    this.mewcontainer.pack()

    return this.frame


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
    if entry['event'] == 'Scan' or entry['event'] == 'Location' or entry['event'] == 'FSDJump':
        this.mewdg["text"] = entry['event']

    # Then, we check many things to add to the different list (elw, ww, aw and tf) if the event is a scan
    if entry['event'] == 'Scan':
        bodyname = str(entry["Bodyname"])
        bodyname.replace(this.current_system+" ", '')

        if entry['PlanetClass'] == 'Earthlike body':
            this.elw_list.append(bodyname)
            this.mewelw["text"] = this.elw_list
        if entry['PlanetClass'] == 'Water world':
            this.ww_list.append(bodyname)
            this.mewww["text"] = this.ww_list
        if entry['PlanetClass'] == 'Ammonia world':
            this.aw_list.append(bodyname)
            this.mewaw["text"] = this.aw_list
        if entry['PlanetClass'] == 'High metal content body':
            this.hmc_list.append(bodyname)
            this.mewhmc["text"] = this.hmc_list
        if entry['PlanetClass'] == 'Rocky body ':
            this.rw_list.append(bodyname)
            this.mewrw["text"] = this.rw_list
        if entry['PlanetClass'] == 'Icy body ':
            this.iw_list.append(bodyname)
            this.mewiw["text"] = this.iw_list
        if entry['PlanetClass'] == 'Rocky ice body ':
            this.riw_list.append(bodyname)
            this.mewriw["text"] = this.riw_list
        if str(entry['PlanetClass']).find('Gas giant') > -1:
            this.gg_list.append(bodyname)
            this.mewgg["text"] = this.gg_list
        if str(entry['PlanetClass']).find('Water giant') > -1:
            this.wg_list.append(bodyname)
            this.mewwg["text"] = this.wg_list
        if entry['TerraformState'] != 'null':
            this.tf_list.append(bodyname)
            this.mewtf["text"] = this.tf_list

    if entry['event'] == 'Location' or entry['event'] == 'FSDJump':
        this.current_system = entry["StarSystem"]

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
