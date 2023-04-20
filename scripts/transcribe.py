from pod_utils import PodHandler, get_podcasts
import os

pod_handler = PodHandler()

podcasts = get_podcasts()

for podcast in podcasts:
    try:
        file = os.path.join("data/thedrive", podcast["folder"], "pod.mp3")
        pod_handler.transcribe_audio_file_with_speaker(file)
    except Exception as e:
        handle_error(e)