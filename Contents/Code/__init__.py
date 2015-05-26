#
# TvplexendAgent.bundle - A Tvheadend Agent Plugin for PLEX Media Server
# Copyright (C) 2015 Patrick Gaubatz <patrick@gaubatz.at>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import base64, time

NAME = 'Tvplexend'
CACHE_TIME = 60
MIN_URL_LEN = len('http://x')


def Start():
    HTTP.CacheTime = CACHE_TIME


def ValidatePrefs():
    if not Prefs['url'] or len(Prefs['url']) < MIN_URL_LEN:
        Log.Error(L('error_url'))
        return False

    Dict['auth'] = None

    if Prefs['username'] and Prefs['password']:
        u = Prefs['username']
        p = Prefs['password']
        Dict['auth'] = 'Basic ' + base64.b64encode(u + ':' + p)

    try:
        info = Tvheadend.ServerInfo()
        if not info:
            return False

        if info['api_version'] < 15:
            Log.Error(L('error_api'))
            return False

    except Exception as e:
        Log.Error(L('error_exception') + str(e))
        return False

    Log.Info(L('success'))


class TvplexendAgent(Agent.Movies):
    name = NAME
    languages = [Locale.Language.NoLanguage]
    primary_provider = True
    accepts_from = [
        'com.plexapp.agents.imdb',
        'com.plexapp.agents.themoviedb'
    ]

    def search(self, results, media, lang):
        recordings = Recordings()
        filename = media.items[0].parts[0].file

        if filename not in recordings:
            Log.Info('No Tvheadend recording information found for ' + filename)
            return

        recording = recordings[filename]

        results.Append(
            MetadataSearchResult(
                id=recording['uuid'],
                name=recording['disp_title'],
                lang=lang,
                score=100
            )
        )

    def update(self, metadata, media, lang):
        recording = Recordings()[media.items[0].parts[0].file]

        startDateTime = Datetime.FromTimestamp(recording['start'])
        stopDateTime = Datetime.FromTimestamp(recording['stop'])

        day = startDateTime.strftime('%d.%m.%Y')
        start = startDateTime.strftime('%H:%M')
        stop = stopDateTime.strftime('%H:%M')

        title = recording['disp_title']

        if Prefs['includeDatetimeInTitle']:
            title = '%s (%s %s)' % (title, day, start)

        metadata.title = title
        metadata.originally_available_at = startDateTime.date()
        metadata.summary = '%s ★ %s ★ %s - %s ★ %s' % (
            recording['channelname'],
            day, start, stop,
            recording['disp_description']
        )


def Recordings(timeout=CACHE_TIME):
    if 'timestamp' not in Dict or 'recordings' not in Dict or time.time() - Dict['timestamp'] > timeout:
        Dict['timestamp'] = time.time()
        try:
            Dict['recordings'] = Tvheadend.Recordings()
        except Exception:
            Dict['recordings'] = dict()

    return Dict['recordings']


class Tvheadend(object):
    @staticmethod
    def ServerInfo():
        return Tvheadend.fetch('/api/serverinfo')

    @staticmethod
    def Recordings():
        entries = Tvheadend.fetch('/api/dvr/entry/grid_finished')['entries']
        return dict((entry['filename'], entry) for entry in entries)

    @staticmethod
    def fetch(path, headers=dict(), values=None):
        url = Prefs['url'] + path

        if 'auth' in Dict:
            headers['Authorization'] = Dict['auth']

        try:
            return JSON.ObjectFromURL(url=url, headers=headers, values=values)

        except Ex.HTTPError as e:
            if e.code == 401 or e.code == 403:
                Log.Error(L('error_auth'))
            else:
                Log.Error('%s (%s)' % (L('error_net'), repr(e)))
