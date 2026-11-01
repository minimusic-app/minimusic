from utils.hashing import hash_text
from dataclasses import dataclass

@dataclass
class ArtistMinimal():
    artistName: str = ""
    artistHash: str = ""
    artistImage: str = ""

    def __init__(self):
        self.artistName = str or ""
        self.artistHash = hash_text(self.artistName)
        self.artistImage = self.artistHash + ".webp"

        # easter egg aleatório do código pq sim
        # random easter agg of the code
        if self.artistHash == "a":
            self.artistName = "Astronaut"

    def artist_to_json(self):
        return {
            "name": self.artistName,
            "hash": self.artistHash
        }

class ArtistModel:
    name: str
    artistHash: str
    date: int
    duration: int
    extra: dict
    