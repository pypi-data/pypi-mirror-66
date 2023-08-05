# Config script to extracts Video features for SAVI video

import bob.paper.lipsync2019
import bob.bio.video

from bob.paper.lipsync2019.database import SAVIPadDatabase, SAVIBioFile

database = SAVIPadDatabase(db_name=db_name,
                           original_extension=".avi",
                           pad_file_class=SAVIBioFile,
                           )

CROPPED_IMAGE_HEIGHT = {{ roi_dimensions[0] }}
CROPPED_IMAGE_WIDTH = {{ roi_dimensions[1] }}

if CROPPED_IMAGE_WIDTH == 128:
    RIGHT_MOUTH_POS = (64, 4)
    LEFT_MOUTH_POS = (64, 124)

color_channel = 'rgb' # 'gray' or 'rgb'
use_flandmark = True
dtype = 'uint8'

preprocessed_directory = '../{{ projectname }}_roi_extraction_{{ samples }}'

{% if samples == 'negative' %}
faceregres = bob.paper.lipsync2019.preprocessor.VideoNonFaceCrop(
{% else %}
faceregres = bob.paper.lipsync2019.preprocessor.VideoFaceCrop(
{% endif %}
     face_cropper=bob.bio.face.preprocessor.FaceCrop(
         cropped_image_size=(CROPPED_IMAGE_HEIGHT, CROPPED_IMAGE_WIDTH),
         cropped_positions={'lmth': LEFT_MOUTH_POS, 'rmth': RIGHT_MOUTH_POS},
         color_channel=color_channel),
     use_flandmark=use_flandmark,
     color_channel=color_channel,
     dtype=dtype
  )
preprocessor = bob.bio.video.preprocessor.Wrapper(faceregres,
                                                  frame_selector=bob.bio.video.FrameSelector(selection_style='all'))

skip_preprocessing = False

