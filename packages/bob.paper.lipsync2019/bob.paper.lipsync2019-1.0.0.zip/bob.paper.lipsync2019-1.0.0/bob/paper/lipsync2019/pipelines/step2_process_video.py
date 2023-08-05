# Config script to extracts Video features for SAVI video

from bob.paper.lipsync2019.preprocessor import VideoMouthRegion

database.original_extension = ".avi"

preprocessor = VideoMouthRegion(landmarks_range=(0, 68))

skip_preprocessing = False
