#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
#   Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

from geotiler.provider import MapProvider, base_dir, obfuscate

from unittest import mock


def test_provider_init_default():
    """
    Test initialization of map provider with default configuration values.
    """
    data = {
        'name': 'OpenStreetMap',
        'attribution': '© OpenStreetMap contributors\nhttp://www.openstreetmap.org/copyright',
        'url': 'http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.{ext}',
    }
    provider = MapProvider(data)

    assert 'OpenStreetMap' == provider.name
    expected = '© OpenStreetMap contributors' \
        + '\nhttp://www.openstreetmap.org/copyright'
    assert expected == provider.attribution
    expected = 'http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.{ext}'
    assert expected == provider.url
    assert () == provider.subdomains
    assert 'png' == provider.extension
    assert 1 == provider.limit
    assert provider.api_key_ref is None

def test_provider_init_default_override():
    """
    Test initialization of map provider when overriding default
    configuration values.
    """
    data = {
        'name': 'OpenStreetMap',
        'attribution': '© OpenStreetMap contributors\nhttp://www.openstreetmap.org/copyright',
        'url': 'http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.{ext}',
        'subdomains': ('a', 'b', 'c'),
        'extension': 'jpg',
        'limit': 2,
        'api-key-ref': 'a-b-c',
    }
    provider = MapProvider(data)

    assert 'OpenStreetMap' == provider.name
    expected = '© OpenStreetMap contributors' \
        + '\nhttp://www.openstreetmap.org/copyright'
    assert expected == provider.attribution
    expected = 'http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.{ext}'
    assert expected == provider.url
    assert ('a', 'b', 'c') == provider.subdomains
    assert 'jpg' == provider.extension
    assert 2 == provider.limit
    assert 'a-b-c' == provider.api_key_ref

def test_provider_tile_url():
    """
    Test map provider tile url formatting.
    """
    data = {
        'name': 'OpenStreetMap',
        'attribution': '© OpenStreetMap contributors\nhttp://www.openstreetmap.org/copyright',
        'subdomains': ['a'],
        'url': 'http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.{ext}',
    }
    provider = MapProvider(data)
    url = provider.tile_url((1, 2), 15)
    assert 'http://a.tile.openstreetmap.org/15/1/2.png' == url

def test_provider_tile_url_api_key():
    """
    Test map provider tile url formatting with API key.
    """
    data = {
        'name': 'OpenStreetMap',
        'attribution': '© OpenStreetMap contributors\nhttp://www.openstreetmap.org/copyright',
        'subdomains': ['a'],
        'url': 'http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.{ext}?apikey={api_key}',
        'api-key-ref': 'a-key-ref',
    }
    provider = MapProvider(data, api_key='a-key-ref')
    url = provider.tile_url((1, 2), 15)
    assert 'http://a.tile.openstreetmap.org/15/1/2.png?apikey=a-key-ref' == url

def test_base_dir():
    """
    Test base dir retrieval.
    """
    fn = base_dir()
    assert fn.endswith('/geotiler/source')

def test_obfuscate_url():
    """
    Test obfuscation of API key in a tile URL.
    """
    # no api key, no change
    url = obfuscate('http://a.tile.openstreetmap.org/15/1/2.png')
    assert 'http://a.tile.openstreetmap.org/15/1/2.png' == url

    url = obfuscate('http://a.tile.openstreetmap.org/15/1/2.png?apikey=a-key-ref')
    assert 'http://a.tile.openstreetmap.org/15/1/2.png?apikey=<apikey>' == url

    url = obfuscate('http://a.tile.openstreetmap.org/15/1/2.png?apikey=a-key-ref&a=1&b=2')
    assert 'http://a.tile.openstreetmap.org/15/1/2.png?apikey=<apikey>&a=1&b=2' == url

    url = obfuscate('http://a.tile.openstreetmap.org/15/1/2.png?api-key=a-key-ref')
    assert 'http://a.tile.openstreetmap.org/15/1/2.png?api-key=<apikey>' == url

    url = obfuscate('http://a.tile.openstreetmap.org/15/1/2.png?api-key=a-key-ref&a=1&b=2')
    assert 'http://a.tile.openstreetmap.org/15/1/2.png?api-key=<apikey>&a=1&b=2' == url

# vim:et sts=4 sw=4:
