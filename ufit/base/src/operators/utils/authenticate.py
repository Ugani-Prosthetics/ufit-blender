import bpy
import json
import requests
from ....src import base_globals
from .....config_ufit import logger


def set_ufit_authetication_vars(context):
    try:
        ufit_prefs = context.preferences.addons['ufit'].preferences

        if ufit_prefs.username and ufit_prefs.password:
            context.scene.ufit_user = ufit_prefs.username
            context.scene.ufit_password = ufit_prefs.password

    except Exception as e:
        pass


def get_ufit_login_params(context):
    url_connect = f'{context.scene.ufit_platform}/ugani/session/authenticate'
    data_connect = {
        "params": {
            "db": "ugani_odoo",
            "login": context.scene.ufit_user,
            "password": context.scene.ufit_password,
        }
    }

    return url_connect, data_connect


def start_session(url, data, headers):
    session = requests.Session()

    r = session.post(url=url, data=json.dumps(data), headers=headers)

    if r.ok:
        result_dict = r.json()

        if not result_dict.get('error'):
            # not required - already stored in cookie (kept here for safety)
            if result_dict.get('result') and result_dict.get('result').get('sessions_id'):
                session.cookies['session_id'] = result_dict.get('result').get('sessions_id')

            return {
                'session': session,
                'status_code': r.status_code
            }

    return {
        'session': None,
        'status_code': r.status_code
    }


def platform_authenticate(context):
    set_ufit_authetication_vars(context)
    url_connect, data_connect = get_ufit_login_params(context)

    try:
        login_res = start_session(url=url_connect, data=data_connect, headers=base_globals.headers)

        if login_res["session"]:
            logger.info('uFit authentication successful')
            base_globals.platform_session = login_res['session']
        else:
            base_globals.platform_session = None
            logger.info('uFit authentication unsuccessful')
    except Exception as e:
        pass
        # raise Exception(f'Make sure you have internet connection when using the uFit plugin')


def is_authenticated():
    return isinstance(base_globals.platform_session, requests.sessions.Session)
