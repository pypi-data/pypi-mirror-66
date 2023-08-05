from .mixins import ExternalURLMixin, ImageMixin, TrackMixin
from .object import SpotifyObject
from .user import PublicUser
from .track import PlaylistTrack


class _BasePlaylist(SpotifyObject, TrackMixin, ExternalURLMixin, ImageMixin):
	_type = 'playlist'
	_track_class = PlaylistTrack

	def __init__(self, client, data):
		super().__init__(client, data)

		TrackMixin.__init__(self, data)
		ExternalURLMixin.__init__(self, data)
		ImageMixin.__init__(self, data)

		self.snapshot_id = data.pop('snapshot_id')
		self.collaborative = data.pop('collaborative')
		self.public = data.pop('public')

		self.owner = PublicUser(client, data.pop('owner'))

	async def edit(self, name=None, public=None, collaborative=None, description=None):
		'''
		Edit the playlist.
		
		:param str name: New name of the playlist.
		:param str description: New description of the playlist.
		:param bool public: New public state of the playlist.
		:param bool collaborative: New collaborative state of the playlist.
		'''

		await self._client.edit_playlist(
			playlist=self.id,
			name=name,
			public=public,
			collaborative=collaborative,
			description=description,
		)

	async def add_track(self, track, position=None):
		'''
		Add a track to the playlist.

		:param track: Spotify ID or :class:`Track` instance.
		:param int position: Position in the playlist to insert tracks.
		'''

		await self._client.playlist_add_tracks(self.id, track, position=position)

	async def add_tracks(self, *tracks, position=None):
		'''
		Add several tracks to the playlist.

		:param tracks: Several Spotify IDs or :class:`Track` instances (or a mix).
		:param int position: Position in the playlist to insert tracks.
		'''

		await self._client.playlist_add_tracks(self.id, *tracks, position=position)


class SimplePlaylist(_BasePlaylist):
	'''
	Represents a playlist object.

	.. note::
	   To iterate all tracks, you have to use the ``async for`` construct or fill the object with ``.fill()`` before iterating ``.tracks``.

	id: str
		Spotify ID of the playlist.
	name: str
		Name of the playlist.
	tracks: List[:class:`SimpleTrack`]
		All tracks in the playlist.
	track_count: int
		The expected track count as advertised by the last paging object. ``is_filled()`` can return True even if fewer tracks than this exists in ``tracks``, since some fetched tracks from the API can be None for various reasons.
	uri: str
		Spotify URI of the playlist.
	link: str
		Spotify URL of the playlist.
	snapshot_id: str
		Spotify ID of the current playlist snapshot. Read about snapshots `here. <https://developer.spotify.com/documentation/general/guides/working-with-playlists/>`_
	collaborative: bool
		Whether the playlist is collaborative.
	public: bool
		Whether the playlist is public.
	owner: :class:`PublicUser`
		Owner of the playlist.
	external_urls: dict
		Dictionary that maps type to url.
	images: List[:class:`Image`]
		List of associated images.
	'''


class FullPlaylist(_BasePlaylist):
	'''
	Represents a complete playlist object.
	
	This type has some additional attributes not existent in :class:`SimplePlaylist`.
	
	description: str
		Description of the playlist, as set by the owner.
	primary_color: str
		Primary color of the playlist, for aesthetic purposes.
	follower_count: int
		Follower count of the playlist.
	'''

	def __init__(self, client, data):
		super().__init__(client, data)

		self.description = data.pop('description')
		self.primary_color = data.pop('primary_color')
		self.follower_count = data['followers']['total']
