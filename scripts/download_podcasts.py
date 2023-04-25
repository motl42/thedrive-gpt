import feedparser
import json
import re
import urllib.request
from pprint import pprint
from pod_utils import get_podcast_guests
from dotenv import load_dotenv
import os
import funcy

load_dotenv()

# Parse the RSS feed
feed_url = 'https://peterattiadrive.libsyn.com/rss'
feed = feedparser.parse(feed_url)

# Create an empty list to store the podcast episodes
new_podcasts = []

with open('data/thedrive.json') as json_file:
    podcasts = json.load(json_file)

#create a podcast folder with the name of the podcast if it does not exist in the data folder
import os

podcast_dir = 'data/thedrive'
if not os.path.exists(podcast_dir):
    os.makedirs(podcast_dir)

entries = [entry for entry in feed.entries if "rebroadcast" not in entry.title.lower()]    

new_entries = [entry for entry in entries if entry.id not in [podcasts[i]['id'] for i in range(0, len(podcasts))]]

print("found {} new entries".format(len(new_entries)))


# Loop through each entry in the feed
for entry in new_entries:

   
    title = entry.title.replace('\u00a0', ' ').replace('\u2012', '-').replace('\u2019', "'").replace("‘", "'").replace("‘", "'")
    description = entry.summary
    date = entry.published
    link = entry.link
    id = entry.id
    
    
    audio_url = entry.enclosures[0].href
    audio_file = f'{title}.mp3'

    folder_path = f"{podcast_dir}/{title}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Download the audio file
    urllib.request.urlretrieve(audio_url, f'{folder_path}/pod.mp3')
    
    # Create a dictionary to store the metadata for this podcast episode
    podcast = {
        'id': id,
        'title': title,
        'description': description,
        'date': date,
        'link': link,
        'audio_url': audio_url,
        'audio_file': audio_file,
        'folder': title
    }
    
    new_podcasts.append(podcast)


batch_size = 20*4

chunks = funcy.chunks(batch_size, new_podcasts)

for chunk in chunks:
    titles = [pod["title"] for pod in chunk]
    guests = get_podcast_guests(titles)
    for pod, guest in zip(chunk, guests):
        pod["guest"] = guest


new_podcasts.reverse()
for podcast in new_podcasts:
    podcasts.insert(0, podcast)

# Save the list of podcasts to a JSON file
with open('data/thedrive.json', 'w') as f:
    json.dump(podcasts, f, indent=4)
