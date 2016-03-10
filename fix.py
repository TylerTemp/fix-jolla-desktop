#!/usr/bin/python
"""
NAME
    fix-jolla-desktop - a collection for jolla android support desktop fixer

SYNOPSIS
    fix (taobao | zhifubao | alipay | smartbanking)

ABOUT
    author: TylerTemp <tylertempdev@gmail.com>
"""
import logging
import sys
import os
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

if sys.version_info[0] <= 2:
    from codecs import open


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
    }
}


for name in sys.argv[1:]:
    name = name.lower()
    if name == 'zhifubao':
        name = 'alipay'

    logger.info('fixing %s', name)
    if name not in config:
        logger.error('%s not support', name)
        continue

    detail = config[name]
    url = detail['url']
    path = detail['path']
    icon = detail.get('icon', None)

    logger.debug('save %s from %s', path, url)
    real_path, _ = urlretrieve(url, path)
    logger.debug('saved to %s', real_path)

    if icon:
        logger.debug('check icon')
        with open(path, 'r', encoding='utf-8') as f:
            for each in f:
                pref, _, subf = each.partition('=')
                if pref == 'Icon':
                    icon_path = subf.strip()
                    if not os.path.exists(icon_path):
                        logger.debug('try fix icon %s', icon_path)
                        real_path, _ = urlretrieve(icon, icon_path)
                        logger.info('icon fixed: %s', real_path)
                    break
            else:
                logger.error('no icon found in %s', path)
