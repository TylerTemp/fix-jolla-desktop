#!/usr/bin/env python
"""
NAME
    fix-jolla-desktop - a collection for jolla android support desktop fixer

SYNOPSIS
    fix (taobao | zhifubao | alipay | smartbanking | cmb)

ABOUT
    author: TylerTemp <tylertempdev@gmail.com>
"""
import logging
import sys
import os
from contextlib import closing
try:
    from urllib.request import urlopen, HTTPError, URLError
except ImportError:
    from urllib import urlopen, HTTPError, URLError

if sys.version_info[0] <= 2:
    from codecs import open


# urlretrieve do not give info if it succeed (status code checking)
def url_retrieve(url, path):
    with closing(urlopen(url)) as urlfile:
        with open(path, 'wb') as outfile:
            finished = False
            while not finished:
                chunk = urlfile.read(8192)
                if not chunk:
                    finished = True
                outfile.write(chunk)
            else:
                return None


FMT = '\033[34m[%(levelname)1.1s]\033[0m  %(lineno)3d  %(asctime)s | %(message)s'
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(logging.Formatter(FMT))
logger = logging.getLogger()
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

config = {
    'taobao': {
        'path': '/usr/share/applications/apkd_launcher_fix_taobao.desktop',
        'url': 'https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/apkd_launcher_fix_taobao.desktop',
        'icon': 'https://raw.githubusercontent.com/TylerTemp/DroidSailizedIcon/master/apkd/apkd_launcher_com_taobao_taobao-com_taobao_tao_welcome_Welcome.png'
    },
    'alipay': {
        'path': '/usr/share/applications/apkd_launcher_fix_alipay.desktop',
        'url': 'https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/apkd_launcher_fix_alipay.desktop',
        'icon': 'https://raw.githubusercontent.com/TylerTemp/DroidSailizedIcon/master/apkd/apkd_launcher_com_eg_android_AlipayGphone-com_eg_android_AlipayGphone_AlipayLogin.png'
    },
    'smartbanking': {
        'path': '/usr/share/applications/apkd_launcher_fix_smartbanking.desktop',
        'url': 'https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/apkd_launcher_fix_smartbanking.desktop',
    },
    'cmb': {
        'path': '/usr/share/applications/apkd_launcher_fix_cmb.desktop',
        'url': 'https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/apkd_launcher_fix_cmb.desktop',
        'icon': 'https://raw.githubusercontent.com/TylerTemp/DroidSailizedIcon/master/apkd/apkd_launcher_cmb_pb-cmb_pb_ui_PBInitActivity.png'
    },
    'xiami': {
        'path': '/usr/share/applications/apkd_launcher_fix_fm_xiami.desktop',
        'url': 'https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/apkd_launcher_fix_fm_xiami.desktop',
        'icon': 'https://raw.githubusercontent.com/TylerTemp/DroidSailizedIcon/master/apkd/apkd_launcher_fm_xiami_main-fm_xiami_main_SplashActivity.png'
    }
}


err_msg = []
suc_app = []
for name in sys.argv[1:]:
    name = name.lower()
    if name == 'zhifubao':
        name = 'alipay'

    logger.info('fixing %s', name)
    if name not in config:
        logger.error('not support: %s', name)
        err_msg.append('%s is not supported so far' % name)
        continue

    detail = config[name]
    url = detail['url']
    path = detail['path']
    icon = detail.get('icon', None)

    logger.debug('save %s from %s', path, url)
    try:
        url_retrieve(url, path)
    except (HTTPError, URLError) as e:
        logger.info('failed to fix desktop %s: %s', name, e)
        err_msg.append(e)
        continue
    else:
        suc_app.append(name)
        logger.debug('saved to %s', path)

    if icon:
        logger.debug('check icon')
        with open(path, 'r', encoding='utf-8') as f:
            for each in f:
                pref, _, subf = each.partition('=')
                if pref == 'Icon':
                    icon_path = subf.strip()
                    if not os.path.exists(icon_path):
                        logger.debug('try fix icon %s', icon_path)
                        try:
                            url_retrieve(icon, icon_path)
                        except (HTTPError, URLError) as e:
                            logger.info('failed to fix icon: %s; %s',
                                        icon_path,
                                        e)
                            err_msg.append(e)
                        else:
                            logger.info('icon fixed: %s', icon_path)
                    break
            else:
                logger.error('no icon found in %s', path)

if suc_app:
    print('%s %s been fixed!' % (
        ', '.join(suc_app),
        'has' if len(suc_app) == 1 else 'have'
    ))

exit_code = 1 if err_msg else 0
for each in err_msg:
    sys.stderr.write('%s\n' % each)

sys.exit(exit_code)
