"""
A Python library for interacting asynchronously with the Spotify API
"""

__title__ = 'asyncspotify'
__author__ = 'RUNIE'
__version__ = '0.12.1'
__license__ = 'MIT'

import logging

from . import utils
from .album import FullAlbum, SimpleAlbum
from .artist import FullArtist, SimpleArtist
from .audioanalysis import AudioAnalysis
from .audiofeatures import AudioFeatures
from .client import Client
from .device import Device
from .exceptions import *
from .http import Route
from .image import Image
from .oauth import AuthorizationCodeFlow, ClientCredentialsFlow, EasyAuthorizationCodeFlow
from .object import SpotifyObject
from .playing import CurrentlyPlaying, CurrentlyPlayingContext
from .playlist import FullPlaylist, SimplePlaylist
from .scope import Scope
from .track import FullTrack, PlaylistTrack, SimpleTrack
from .user import PrivateUser, PublicUser

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
