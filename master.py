import requests
import pylast
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


# log into last_fm api
def login():
    # Since this is a test I'm passing these straight in. Otherwise I'd use AWS Secrets to access the API keys.
    api_key = "357f6564556ac9b88315f2a6f0eabae4"  # this is a sample key
    api_secret = "02f5a20871a0bd9adce3db0aa17ade9f"
    last_fm = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    return last_fm


# Pull in data from last_fm, this is used to get track info and bio summary about the artist
def get_tracks_from_last_fm(artist_input, last_fm, track_limit):
    artist = last_fm.get_artist(artist_input)
    # selecting only top tracks for testing purposes.
    tracks = artist.get_top_tracks(limit=track_limit)
    bio = artist.get_bio_summary()
    return tracks, bio


# pull in lyrics data from the lyrics api.
def get_track_lyrics(tracks):
    track_name = tracks[0].get_name()
    track_artist = tracks[0].get_artist()
    lyrics_dict = requests.get(f'https://api.lyrics.ovh/v1/{track_artist}/{track_name}').json()
    if list(lyrics_dict.keys()) == ["lyrics"]:
        return lyrics_dict["lyrics"]


# To avoid waiting for many song's lyrics to be pulled in, multithreading pulls the data in parallel
def multithread_get_lyrics(tracks, track_limit):
    with ThreadPoolExecutor(max_workers=track_limit) as executor:
        all_tracks_lyrics = list(tqdm(executor.map(get_track_lyrics, tracks), total=track_limit))
    return all_tracks_lyrics


# produce some analysis on the lyrics
def analyse_lyrics(all_tracks_lyrics, artist_input):
    total_words, distinct_total_words = 0, 0
    for track in all_tracks_lyrics:
        if track is not None:
            total_words = total_words + len(track.split())
            distinct_total_words = distinct_total_words + len(list(set(track.split())))
    amount_of_tracks_read = len(all_tracks_lyrics)
    average_words = int(total_words / amount_of_tracks_read)
    average_distinct_words = int(distinct_total_words / amount_of_tracks_read)
    print(f"The average number of words for a {artist_input} song is: {average_words}."
          f"The average number of distinct words for a {artist_input} song is: {average_distinct_words}")


# the main script to run the process, this loops over to allow the user to search many times over.
def main():
    try:
        while True:
            artist_input = input("Enter the artist you'd like info on : ")
            last_fm = login()
            track_limit = 50
            tracks, bio = get_tracks_from_last_fm(artist_input, last_fm, track_limit)
            print(f"\nHere's a little extra info about {artist_input} that may interest you while the process collects lyrics info:\n"
                  f"{bio}\n\n")
            all_tracks_lyrics = multithread_get_lyrics(tracks, track_limit)
            analyse_lyrics(all_tracks_lyrics, artist_input)
    except Exception as e:
        raise e


if __name__ == '__main__':
    main()
