# Copyright (c) 2020 Philippe Proulx <eepp.ca>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import requests
import packaging.version
import urllib.parse
import ftplib
import logging
import os.path


def _build_tarball_name_regex(project_name):
    ext_regex = '|'.join([
        r'tbz2',
        r'tbz',
        r'tgz',
        r'tlz',
        r'txz',
        r'zip',
        r'tar\.bz2',
        r'tar\.gz',
        r'tar\.xz',
        r'tar(?!\.)',
    ])

    return re.escape(project_name) + r'-(\d+[^/"\s]+?)\.(' + ext_regex + r')'


def _find_all_in_text(page, regex):
    items = set()

    for match in re.finditer(regex, page, re.I):
        items.add(match[0])

    return items


def _make_url(base_name, file_name):
    return '{}/{}'.format(base_name.rstrip('/'), file_name.lstrip('/'))


def _find_tarball_urls_in_text(page, project_name, base_url):
    regex = _build_tarball_name_regex(project_name)
    names = _find_all_in_text(page, regex)
    return set([_make_url(base_url, name) for name in names])


def _log_info(logger, msg):
    if logger is not None:
        logger.info(msg)


class Error(Exception):
    pass


def _try_ftp_cwd(ftp, path, logger):
    _log_info(logger, 'FTP: changing working directory to `{}`.'.format(path))
    return ftp.cwd(path)


def _ftp_cwd(ftp, path, logger):
    try:
        _try_ftp_cwd(ftp, path, logger)
    except ftplib.all_errors as exc:
        raise Error('FTP: cannot change working directory to `{}`'.format(path))


def _ftp_list(ftp, path, logger):
    lines = []
    _log_info(logger, 'FTP: listing files in `{}`.'.format(path))

    try:
        ftp.dir(lines.append)
    except ftplib.all_errors as exc:
        raise Error('FTP: cannot list directory `{}`'.format(path))

    return lines


def _find_tarball_urls_in_lines(lines, project_name, url, logger):
    urls = set()

    for line in lines:
        line_urls = _find_tarball_urls_in_text(line, project_name, url)
        urls |= line_urls

    return urls


def _find_tarball_urls_in_ftp_dir(project_name, url, logger):
    url_parts = urllib.parse.urlparse(url)
    _log_info(logger, 'FTP: connecting to `{}`.'.format(url_parts.netloc))
    ftp = ftplib.FTP(url_parts.netloc)
    ftp.login()
    urls = set()
    path = url_parts.path
    _ftp_cwd(ftp, path, logger)
    base_lines = _ftp_list(ftp, path, logger)

    # immediate tarballs
    urls = _find_tarball_urls_in_lines(base_lines, project_name, url, logger)

    # tarballs in minor/patch version directories
    dir_re = r'(?:\s|^)((?:' + re.escape(project_name) + r'-)?[Vv]?\d+\.\d+(?:\.\d+)?)(?:\s|$)'
    dirs = _find_all_in_text('\n'.join(base_lines), dir_re)

    for dir in dirs:
        dir = dir.strip()
        dir_path = os.path.join(path, dir)
        dir_url = _make_url(url, dir)

        try:
            _try_ftp_cwd(ftp, dir_path, logger)
            dir_lines = _ftp_list(ftp, dir_path, logger)
            urls |= _find_tarball_urls_in_lines(dir_lines, project_name, dir_url,
                                                logger)
            _ftp_cwd(ftp, '..', logger)
        except ftplib.all_errors as exc:
            # ignore: probably not a directory
            pass

    _log_info(logger, 'FTP: quitting `{}`.'.format(url_parts.netloc))
    ftp.quit()
    return urls


def _get_http_page_text(url, logger):
    _log_info(logger, 'Fetching page `{}`.'.format(url))

    try:
        r = requests.get(url)

        if r.status_code != 200:
            fmt = 'cannot fetch page `{}`: got HTTP status {}'
            raise Error(fmt.format(url, r.status_code))

        return r.text
    except Exception as exc:
        raise Error('cannot fetch page `{}`'.format(url)) from exc


def find_tarball_urls(project_name, url, logger=None):
    url_parts = urllib.parse.urlparse(url)

    if url_parts.scheme == 'ftp':
        try:
            return _find_tarball_urls_in_ftp_dir(project_name, url, logger)
        except ftplib.all_errors as exc:
            raise Error('FTP: cannot get tarball URLs from `{}`'.format(url))

    # immediate tarballs
    page = _get_http_page_text(url, logger)
    urls = _find_tarball_urls_in_text(page, project_name, url)

    # tarballs in minor/patch version directories
    href_re = r'(?:./)?(?:' + re.escape(project_name) + r'-)?[Vv]?\d+\.\d+(?:\.\d+)?/?'
    dirs = _find_all_in_text(page, r'href\s*=\s*"' + href_re + '"')

    if dirs is not None:
        for dir in dirs:
            m = re.search(r'"([^"]+)"', dir, re.I)
            dir_url = _make_url(url, m.group(1))
            page = _get_http_page_text(dir_url, logger)
            dir_urls = _find_tarball_urls_in_text(page, project_name, dir_url)
            urls |= dir_urls

    return urls


class Tarball:
    def __init__(self, project_name, url):
        self._project_name = project_name
        self._url = url
        url_parts = urllib.parse.urlparse(url)
        self._name = os.path.basename(url_parts.path)
        m = re.match(_build_tarball_name_regex(project_name), self._name, re.I)
        assert(m is not None)
        self._version = packaging.version.parse(m.group(1))
        self._name_ext = m.group(2)

    @property
    def url(self):
        return self._url

    @property
    def name(self):
        return self._name

    @property
    def name_no_ext(self):
        return self._name[:-len(self._name_ext) - 1]

    @property
    def name_ext(self):
        return self._name_ext

    @property
    def project_name(self):
        return self._project_name

    @property
    def version(self):
        return self._version

    def __hash__(self):
        return hash(self._url)

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        return self._url == other._url

    def __lt__(self, other):
        if type(other) is not type(self):
            raise TypeError('wrong types for `<` operator')

        return self._url < other._url

    def __repr__(self):
        return '{}.{}({!r}, {!r})'.format(__name__,
                                          self.__class__.__qualname__,
                                          self._project_name, self._url)


def find_tarballs(project_name, url, logger=None):
    urls = find_tarball_urls(project_name, url, logger)
    return set([Tarball(project_name, url) for url in urls])
