import configparser
import os


def get_config(section, key=None):
    conf = configparser.ConfigParser()
    path = os.getcwd()
    confpath = path + "/settings.conf"
    conf.read(confpath, encoding="UTF-8")
    if key is not None:
        return conf.get(section, key)
    else:
        return conf.items(section)


def is_exist(section):
    # Don't use this function anymore.
    return is_section_exist(section)


def is_section_exist(section):
    conf = configparser.ConfigParser()
    path = os.getcwd()
    confpath = path + "/settings.conf"
    conf.read(confpath, encoding="UTF-8")
    return conf.has_section(section)


def is_option_exist(section, option):
    conf = configparser.ConfigParser()
    path = os.getcwd()
    confpath = path + "/settings.conf"
    conf.read(confpath, encoding="UTF-8")
    return conf.has_option(section, option)


def set_config(section, key, text):
    conf = configparser.ConfigParser()
    path = os.getcwd()
    confpath = path + "/settings.conf"
    if is_exist(section) == False:
        create_section(section)
    conf.read(confpath)
    conf.set(section, key, text)
    conf.write(open(confpath, "w"))


def create_section(section):
    conf = configparser.ConfigParser()
    path = os.getcwd()
    confpath = path + "/settings.conf"
    conf.read(confpath)
    conf.add_section(section)
    conf.write(open(confpath, "w"))