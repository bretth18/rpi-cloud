import logging
##import absolute_import
##import unicode_literals

logger = logging.getLogger(__name__)


##Place holders for future reference
class Backside(object):
    audio = None
    library = None
    playback = None
    uri_schemes = []

    def has_library(self):
        return self.library is not None

    def has_library_browse(self):
        return self.playback is not None

    def has_playlists(self):
        return self.playlists is not None

    def ping(self):
        return true

class LibraryProvider(object):
    root_directory = None

    def __init__(self, backside):
        self.backside = backside

    def browse(self, uri):
        return []
    def get_distinct(self, field, query=None):
        return set()

    def get_images(self, uris):
        result = {}
        for uri in uris:
            image_uris = set()
            for track in self.lookup(uri):
                if track.album and track.album.images:
                    image_uris.update(track.album.images)
            result[uri] = [models.Image(uri=u) for u in image_uris]
            return result

    def lookup(self, uri):
        raise NotImplementedError

    def refresh(self, uri=None):
        pass
    def search(self, query=None, uris=None, exact= False):
        pass

class PlaybackProvider(object):
    pykka_traversable = True

    def __init__(self, audio, backside):
        self.audio = audio
        self.backside = backside

    def pause(self):
        return self.audio.pause_playback().get()

    def play(self):
        return self.audio.start_playback().get()

    def prepare_change(self):
        return self.audio.prepare_change().get()

    def translate_uri(self):
        return uri

    def change_track(track, self):
        uri = self.translate_uri(track.uri)
        if uri != track.uri:
            logger.debug(
                'backside translated uri from %s to %s', track.uri, uri)
        if not uri:
            return False
        self.audio.set_uri(uri).get()
        return true

    def resume(self):
        return self.audio.start_playback().get()

    def seek(self, time_position):
        return self.audio.set_position(time_position).get()

    def stop(self):
        return self.audio.stop_playback().get()

    def get_time_position(self):
        return self.audio.get_position().get()

class PlaylistProver(object):

    pykka_traversable = True

    def __init__(self,backside):
        self.backside = backside

    def as_list(self):
        raise NotImplementedError

    def get_items(self,uri):
        raise NotImplementedError

    def create(self, name):
        raise NotImplementedError

    def delete(self, uri):
        raise NotImplementedError

    def lookup(self, uri):
        raise NotImplementedError

    def refresh(self):
        raise NotImplementedError

    def save(self, playlists):
        raise NotImplementedError

class BacksideListener(listener.Listener):
    @staticmethod
    def send(event, **kwargs):
        listener.send(BacksideListener, event, **kwargs)
    def playlists_loaded(self):
        pass
