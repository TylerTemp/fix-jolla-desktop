#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NAME
    fix-jolla-desktop - a collection for jolla android support desktop fixer

SYNOPSIS
    fix (taobao | zhifubao | alipay | smartbanking | cmb | <app>) ...

DESCRIPTION
    This script attempt to fix Android app installed in Jolla missing icon

ABOUT
    author: TylerTemp <tylertempdev@gmail.com>
"""
import logging
import sys
import os
from contextlib import closing
import os
import stat
import re
try:
    from urllib.request import urlopen, HTTPError, URLError
except ImportError:
    from urllib import urlopen


    class HTTPError(Exception):
        pass


    URLError = HTTPError
try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


if sys.version_info[0] <= 2:
    from codecs import open


try:
    input = raw_input
except NameError:
    pass


__version__ = '0.0.2'
__author__ = 'TylerTemp <tylertempdev@gmail.com>'


class Writer(StringIO):

    if sys.hexversion >= 0x03000000:
        def u(self, string):
            return string
    else:
        def u(self, string):
            return unicode(string)

    def write(self, string):
        return super(Writer, self).write(self.u(string))


# urlretrieve do not give info if it succeed (status code checking)
def url_retrieve(url, f):
    if hasattr(f, 'write'):
        return _url_retrieve_stream(url, f)
    else:
        with open(f, 'wb') as stream:
            return _url_retrieve_stream(stream)


def _url_retrieve_stream(url, stream):
    with closing(urlopen(url)) as urlfile:
        if urlfile.getcode() >= 400:
            raise HTTPError('HTTP Error %s' % urlfile.getcode())
        finished = False
        while not finished:
            chunk = urlfile.read(8192)
            if not chunk:
                finished = True
            stream.write(chunk.decode('utf-8'))
        else:
            stream.flush()


def find_apks(name):
    result = list(_find_apks(name.lower(), '/data/app'))
    if result:
        return result
    else:
        logger.info('not found in /app/data, try /. This may take a long time')
        return list(_find_apks(name.lower(), '/'))


def _find_apks(name, root):
    patten = re.compile('\W')
    for dirname, _folders, fnames in os.walk(root):
        # logger.debug((dirname, _folders, fnames))
        for fname in fnames:
            if fname.endswith('.apk'):
                # logger.debug('%s -> %s', name, fname)
                bname = fname[:-4]
                bases = [x.lower() for x in patten.split(bname)]
                for base in bases:
                    if name in base:
                        logger.debug('found %s' % fname)
                        yield os.path.normcase(
                            os.path.abspath(
                                os.path.join(root, dirname, fname)))
                        break


def choose(lis):
    if not lis:
        return None
    if len(lis) == 1:
        return lis[0]
    for index, each in enumerate(lis, 1):
        print('%s.  %s' % (index, each))

    result = None
    while result is None:
        raw_index = input(
            'Which one is the apk file (input number)?/q to quit:').strip()
        if raw_index == 'q':
            print('exit.')
            sys.exit(0)

        try:
            result = lis[int(raw_index.strip()) - 1]
        except BaseException as e:
            print('Not a correct number: %s (%s)' % (raw_index, e))
    return result


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


def fix(argv):
    err_msg = []
    warn_msg = []
    suc_app = []

    for name in argv[1:]:
        name = name.lower()
        if name == 'zhifubao':
            name = 'alipay'

        logger.info('fixing %s', name)

        auto_detect = True
        path = None
        icon = None
        desktop_filelines = []
        if name in config:
            _detail = config[name]
            url = _detail['url']
            path = _detail['path']
            icon = _detail.get('icon', None)
            logger.debug('save %s from %s', path, url)
            with Writer() as stream:
                try:
                    url_retrieve(url, stream)
                except (HTTPError, URLError) as e:
                    logger.info('failed to fix desktop %s: %s; try auto-detect',
                                name,
                                e)
                    warn_msg.append(
                        'Try auto detect %s; This may not work as expected' % name)
                else:
                    stream.seek(0)
                    desktop_filelines.extend(line for line in stream)
                    logger.debug('load desktop for %s' % name)

        if not desktop_filelines:
            logger.info('template not work: %s; try auto detect', name)
            if path is None:
                path = ('/usr/share/applications/apkd_launcher_fix_%s.desktop' %
                        name.lower())

            desktop_filelines.extend(
                ('[Desktop Entry]\n',
                 'Exec=apkd-launcher\n',
                 'Name=%s\n' % name,
                 'Type=Application\n',
                 'Version=1.0\n',
                 'X-Nemo-Application-Type=no-invoker\n',
                 'X-Nemo-Single-Instance=no\n',
                 'X-apkd-apkfile=\n',
                 'X-apkd-packageName=\n')
            )

            if icon:
                save_icon_folder = os.path.expanduser('~/.android_icon')
                if not os.path.isdir(save_icon_folder):
                    os.path.makedirs(save_icon_folder)
                if icon.endswith('/'):
                    fname = icon[:-1].split('/')[-1]
                else:
                    fname = icon.split('/')[-1]
                desktop_filelines.insert(
                    2,
                    'Icon=%s\n' % os.path.join(save_icon_folder, fname))

        logger.debug('check desktop file')
        apkfile = None
        length = len(desktop_filelines)
        for rev_index, each in enumerate(desktop_filelines[::-1]):
            index = length - 1 - rev_index
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
                        desktop_filelines.pop(index)
                    else:
                        logger.info('icon fixed: %s', icon_path)
            if pref == 'Exec':
                exec_args = subf.rstrip().split()
                this_index = None
                if exec_args != ['apkd-launcher']:
                    for this_index, content in enumerate(exec_args):
                        if content.endswith('.apk'):
                            if os.path.exists(content):
                                if apkfile is None:
                                    apkfile = content
                                continue  # no need to fix
                if apkfile is None:
                    _apkfiles = find_apks(name)
                    apkfile = choose(_apkfiles)
                    logger.debug('found apk %s' % apkfile)

                if apkfile is None:
                    logger.error('%s apk file missing' % name)
                    err_msg.append(
                    'apk file for %s desktop '
                    'is missing; please report at '
                    'https://github.com/TylerTemp'
                    '/fix-jolla-desktop/issues' % name)
                    break  # failed

                logger.warning(
                ('launch using found apk file %s; '
                 'this may not work as expected'),
                apkfile)
                warn_msg.append(
                    ('%s using found apk file %s; '
                     'which might not work as expected') %
                    (name, apkfile))
                if this_index is None:
                    exec_args.append(apkfile)
                else:
                    exec_args[this_index] = apkfile
                exec_args.append('\n')
                desktop_filelines[index] = ('Exec=' + ' '.join(exec_args))

            if pref == 'X-apkd-apkfile':
                this_apk = subf.rstrip()
                if os.path.exists(this_apk):
                    if apkfile is None:
                        apkfile = this_apk
                    continue

                if apkfile is None:
                    _apkfiles = find_apks(name)
                    apkfile = choose(_apkfiles)
                    if apkfile is None:
                        logger.info('%s apk file missing' % name)
                        err_msg.append(
                        '%s desktop apk '
                        'file is missing; please report at '
                        'https://github.com/TylerTemp'
                        '/fix-jolla-desktop/issues')
                        break

                    logger.warning(
                    ('launch using found apk file %s; '
                    'this may not work as expected'),
                    apkfile)
                    warn_msg.append(
                        ('%s using found apk file %s; '
                         'which might not work as expected') %
                        (name, apkfile))
                if apkfile is not None:
                    desktop_filelines[index] = 'X-apkd-apkfile=%s\n' % apkfile

        else:
            for index, content in enumerate(desktop_filelines):
                if content.startswith('X-apkd-packageName='):
                    _, _, oldname = content.partition('=')
                    if oldname.strip():
                        continue

                    if apkfile is None:
                        logger.error('ERROR: apkfile is None')
                        err_msg.append('%s apkfile is None' % name)
                        break
                    pkname = os.path.splitext(
                        os.path.split(apkfile)[-1])[0].replace(
                            'apkd_launcher_com_', '').replace(
                            'apkd_launcher_', ''
                        )
                    desktop_filelines[index] = 'X-apkd-packageName=%s\n' % pkname
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(desktop_filelines)
                st = os.stat(path)
                os.chmod(path, st.st_mode | stat.S_IREAD)
                logger.info('%s succeed!', name)
                suc_app.append(name)

    for each in warn_msg:
        print('WARNING: %s' % each)

    if suc_app:
        print('%s %s been fixed!' % (
            ', '.join(suc_app),
            'has' if len(suc_app) == 1 else 'have'
        ))

    exit_code = 1 if err_msg else 0
    for each in err_msg:
        sys.stderr.write('%s\n' % each)
    if err_msg:
        print('Please report to: '
              'https://github.com/TylerTemp/fix-jolla-desktop/issues')

    return exit_code


def main():
    if len(sys.argv) == 1:
        sys.stderr.write(__doc__)
        sys.stderr.write('\n')
        return 1
    return fix(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
