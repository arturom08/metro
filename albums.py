class Track:
    def __init__(self, id, name, duration, link):
        self.id = id
        self.name = name
        self.duration = duration
        self.link = link

class Albums:
    def __init__(self, id, name, description, cover, published, genre, artist, tracklist):
        self.id = id
        self.name = name
        self.description = description
        self.cover = cover
        self.published = published
        self.genre = genre
        self.artist = artist
        self.tracklist = []
        for track_data in tracklist:
            track = Track(track_data['id'], track_data['name'], track_data['duration'], track_data['link'])
            self.tracklist.append(track)
