from api.artists import ArtistSchema
import json

class ArtistMap:
    def __init__(self, artist: ArtistSchema, track: int) -> None:
        self.artist = artist
        self.track = track

class ArtistStore:
    @classmethod
    def load_artist(cls, trackhash: list[str] = []):

        global LOAD_KEY
        print("Loading Artists...", end="")
        cls.artistmap.clear()

        # TODO: Artist Load Logic

        print("Done!")