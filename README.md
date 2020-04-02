# Setup
The project is setup to run inside a docker container. To install the package run the following in a terminal window:
```bash
docker pull elwevvo/michael_weatherby_lyrics:latest
```

If running outside of docker, clone the project to local and install the required packages. The code can then be ran by changing to that directory and running:
```bash
python master.py
```
# Running the code
To run the code, run the below:
```bash
docker run -it elwevvo/michael_weatherby_lyrics:latest
```
At this point you'll be prompted to input an artist/band's name. Do this and hit enter.

The process then goes away and grabs that info. The process is limited to 50 tracks, however increasing this should not make any noticeable difference to runtime, since I'm using multithreading to pull in the data in parallel.

# Overview of code
The code uses two APIs:
- last_fm for artist info
- lyrics ovh for the lyrics data

The lyrics data is the slowest part of the process, and so I've applied multithreading to this to pull in many songs at once. I'm using TQDM to track the progress of this.

The process is currently set to pull only the top 50 songs in for each artist. This can be increased and there shouldn't be a noticeable difference on performance due to the multithreading.

The code is packaged inside a docker container, this makes the code nice and transportable without assuming the end user has anything (apart from docker) installed on their device.

# Improvements for next versions
- It'd be great to have the credentials being pulled in from AWS secrets, or another cloud hosted password manager.
- Using an NLP library such as NLTK to filter out words such as "a" or "to".
- Using an NLP to perform sentiment analysis on the words to provide more insight into what type of band it is.
- The data is slightly different between runs, this is due to inconsistent lyrics returned from  the lyrics API. This could be improved by using a more well established API, such as lyricsgenius.
- Given the code is packaged inside a docker container, it would be nice to include a web interface to the project that would run on a local port.
