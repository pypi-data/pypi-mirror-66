#!/usr/bin/env python3
import requests
from os import environ
import argparse
import colorlog
import logging
import sys
import urllib.parse

"""
ToDo:
* Search in multithreads (https://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python)
* Case insensetive search
* Search by RegEx
"""
SUFFIX = "data/"
MIDDLE_SUFFIX = "/ui/vault/secrets/"


def logger():
    LOGGER = logging.getLogger('Switchboard monitor')
    LOGGER.setLevel(logging.DEBUG)
    CH = logging.StreamHandler()
    CH.setLevel(logging.DEBUG)
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S %z'
    CFORMAT = '%(log_color)s' + FORMAT
    F = colorlog.ColoredFormatter(
        CFORMAT, DATE_FORMAT, log_colors={
            'DEBUG': 'reset',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red'
            })
    CH.setFormatter(F)
    LOGGER.addHandler(CH)
    LOGGER.setLevel(20)
    return LOGGER


log = logger()


def check_env_var(var_name, default_val="", sys_exit=False, verbose=True,
                  secure=False):
    env_var = environ.get(var_name)
    if env_var is None or env_var == "":
        if default_val != "":
            return default_val
        log.error(f'{var_name} environment variable is not defined')
        print_help()
        if sys_exit:
            sys.exit(1)
    else:
        if not secure:
            log.debug(f'{var_name} is set to {env_var}')
        else:
            log.debug(f'{var_name} is set to ***secured***')
        return env_var


def print_help():
    print('This script is searching inside vault KV storage')
    print('There are couple required ENV variables for this script:\n')
    print('\t* VAULT_ADDR - Format is PROTOCOL+FQDN of vault instance;')
    print('\t* VAULT_NS - Vault namespace;')
    print('\t* VAULT_KV_PATH - name of KV where search will start from.\n')


def compute_url(VAULT_ADDR, PATH, VAULT_NS, VAULT_KV_PATH,
                VAULT_INIT_KV_WEB, TYPE=""):
    if TYPE == "section":
        return PATH.replace("/v1/" + VAULT_NS + VAULT_KV_PATH + "metadata",
                            VAULT_ADDR + MIDDLE_SUFFIX + VAULT_INIT_KV_WEB +
                            "list") + "?namespace=" + VAULT_NS[:-1]
    else:
        return PATH.replace("/v1/" + VAULT_NS + VAULT_KV_PATH + SUFFIX,
                            VAULT_ADDR + MIDDLE_SUFFIX + VAULT_INIT_KV_WEB +
                            "show/") + "?namespace=" + VAULT_NS[:-1]


def get_creds(PATH, VAULT_TOKEN, VAULT_ADDR, TEXT, VAULT_NS, VAULT_KV_PATH,
              VAULT_INIT_KV_WEB):
    if PATH == '/v1/' + VAULT_NS + VAULT_KV_PATH + 'metadata/' + SUFFIX:
        return
    elif PATH[-1] == '/':
        METHOD = 'List'
        if '/data/' in PATH:
            PATH = PATH.replace('/data/', '/metadata/')
    else:
        METHOD = "Get"
        if "/metadata/" in PATH:
            PATH = PATH.replace("/metadata/", "/data/")
    r = requests.request(METHOD,
                         VAULT_ADDR + PATH,
                         headers={"X-Vault-Token": VAULT_TOKEN})
    r.raise_for_status()
    if 'keys' in r.json()['data']:
        log.debug(f'Discovering {VAULT_ADDR + PATH}')
        if TEXT.lower() in PATH.lower():
            log.info('Found matching in key name ' +
                     compute_url(VAULT_ADDR, PATH, VAULT_NS, VAULT_KV_PATH,
                                 VAULT_INIT_KV_WEB, TYPE='section'))
        for KEY in r.json()['data']['keys']:
            get_creds(PATH=PATH + KEY, VAULT_TOKEN=VAULT_TOKEN,
                      VAULT_ADDR=VAULT_ADDR, TEXT=TEXT, VAULT_NS=VAULT_NS,
                      VAULT_KV_PATH=VAULT_KV_PATH,
                      VAULT_INIT_KV_WEB=VAULT_INIT_KV_WEB)
    else:
        log.debug(f'Discovering {PATH}')
        if TEXT.lower() in PATH.lower():
            log.warning(f'Found matching in path ' +
                        compute_url(VAULT_ADDR, PATH, VAULT_NS, VAULT_KV_PATH,
                                    VAULT_KV_PATH, VAULT_INIT_KV_WEB))
        if r.json()['data']['metadata']['deletion_time'] != '':
            log.info(f'This path was deleted '+compute_url(VAULT_ADDR, PATH, 
                                                           VAULT_NS, 
                                                           VAULT_KV_PATH,
                                                           VAULT_INIT_KV_WEB))
            return
        try:
            for DICT_KEY, DICT_VALUE in r.json()['data']['data'].items():
                if TEXT.lower() in str(DICT_KEY).lower():
                    log.info(f'Found matching for key {DICT_KEY} ' +
                             'in path '+compute_url(VAULT_ADDR, PATH, VAULT_NS,
                                                    VAULT_KV_PATH,
                                                    VAULT_INIT_KV_WEB))
                elif TEXT.lower() in str(DICT_VALUE).lower():
                    log.info(f'Found matching for value in key {DICT_KEY} ' +
                             'in path '+compute_url(VAULT_ADDR, PATH, VAULT_NS,
                                                    VAULT_KV_PATH,
                                                    VAULT_INIT_KV_WEB))
        except Exception as e:
            log.error(f'Got the exception {e}')
            log.error(f'Discovering {VAULT_ADDR + PATH}')
            print(f'Response {r.json()}')
            print(f'Status code: {r.status_code}')
    return


def vs():
    parser = argparse.ArgumentParser('Vault KV search')
    parser.add_argument('TEXT', metavar='TEXT', type=str)
    args = parser.parse_args()

    VAULT_ADDR = check_env_var('VAULT_ADDR', secure=True, sys_exit=True)
    VAULT_NS = check_env_var('VAULT_NAMESPACE', secure=True) + '/'
    VAULT_KV_PATH = check_env_var('VAULT_KV_PATH', secure=True,
                                  sys_exit=True) + '/'
    VAULT_INIT_KV_WEB = urllib.parse.quote(VAULT_KV_PATH[:-1], safe='') + '/'
    TEXT = vars(args)['TEXT']
    APP_DEBUG = check_env_var('APP_DEBUG', default_val=False)

    if APP_DEBUG:
        log.setLevel(10)
    try:
        with open(f"{check_env_var('HOME',secure=True)}/.vault-token") as file:
            VAULT_TOKEN = file.read()
    except Exception as e:
        log.error(f"Can't get auth token from Vault - {e}")
        log.error(f"Please make sure that you are logged into vault")
        sys.exit(1)

    try:
        get_creds(PATH='/v1/'+VAULT_NS + VAULT_KV_PATH + SUFFIX,
                VAULT_TOKEN=VAULT_TOKEN, VAULT_ADDR=VAULT_ADDR, TEXT=TEXT,
                VAULT_NS=VAULT_NS, VAULT_KV_PATH=VAULT_KV_PATH,
                VAULT_INIT_KV_WEB=VAULT_INIT_KV_WEB)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            log.error(f"Got a 403 - Forbidden URL, indicating you are not logged in or lack appropriate permissions")
            log.error(f"Please make sure that you are logged into vault")
            sys.exit(1)
        raise
    except KeyboardInterrupt:
        log.error("OMG, you hit CTRL+C. Don't do it anymore!!!")
        sys.exit(1)
