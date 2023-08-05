"""
Template for the config script to process Audio and extract features for SAVI
Step 1 should be run first.
"""
import os
from bob.paper.lipsync2019.extractor import CepstralMouthDeltas

_mfccenergy = '{{ mfccenergy }}'
_project_name = '{{ projectname }}'
_block_size = {{ blocksize }}

extracted_directory = '../extracted_{{ projectname }}_{{ mfccenergy }}_blk{{ blocksize }}'
# sub_directory = '{{ projectname }}_{{ mfccenergy }}_blk{{ blocksize }}'

if _mfccenergy == 'mfcc40':
    _with_energy = True
    _audio_features_length = 42  # Number of MFCC features if energy is used
else:
    _with_energy = False
    _audio_features_length = 39  # Number of MFCC features if energy is not used

if _project_name == 'audio_sri_senones' or _project_name == 'audio_saeed_senones':
    _audio_features_length = 80  # Number of senones extracted by SRI or Saeed

_take_video_features_asis = False
_video_features_length = 42  # number of distances between mouth landmarks

# the total number of the audio and video features fit into the block
_feature_length = 4 * _block_size * _audio_features_length + _block_size * _video_features_length

# special preprocessor for audio_sri_senones project
if _project_name == 'audio_sri_senones':
    from bob.paper.lipsync2019.preprocessor import VideoMouthRegion
    path_to_saved_senones = os.path.join(temp_dir, db_name, '{{ projectname }}')
    path_to_tamper_mapping = os.path.join(temp_dir, db_name, db_name + '_tampered_data.txt')
    _external_audio_features_file = dict()
    _external_audio_features_file['db_name'] = db_name
    if db_name == 'vidtimit':
        _external_audio_features_file['senones_db'] = os.path.join(path_to_saved_senones, db_name + '.h5')
        _external_audio_features_file['tamper_mapping'] = path_to_tamper_mapping
        _external_audio_features_file['features_type'] = 'file'
    elif db_name == 'grid':
        _external_audio_features_file['senones_dir'] = path_to_saved_senones
        _external_audio_features_file['tamper_mapping'] = path_to_tamper_mapping
        _external_audio_features_file['features_type'] = 'dir_samplename'
    elif db_name == 'ami':
        _external_audio_features_file['senones_dir'] = path_to_saved_senones
        _external_audio_features_file['features_type'] = 'dir_samplename'
    else:
        _external_audio_features_file['features_type'] = 'dir_simple'
        _external_audio_features_file['feature_name'] = 'array'

    preprocessor = VideoMouthRegion(landmarks_range=(0, 68),
                                    external_audio_features_file=_external_audio_features_file)

if _project_name == 'audio_saeed_senones':
    from bob.paper.lipsync2019.preprocessor import VideoMouthRegion
    path_to_saved_senones = os.path.join(temp_dir, db_name, '{{ projectname }}')
    _external_audio_features_file = dict()
    _external_audio_features_file['features_type'] = 'dir_simple'
    _external_audio_features_file['senones_dir'] = path_to_saved_senones
    _external_audio_features_file['feature_name'] = 'feat'
    _external_audio_features_file['original_preprocess_dir'] = preprocessed_directory

    preprocessor = VideoMouthRegion(landmarks_range=(0, 68),
                                    external_audio_features_file=_external_audio_features_file)


extractor = CepstralMouthDeltas(n_ceps=13,
                                n_filters=40,
                                f_min=300,
                                f_max=3700,
                                num_video_frames_per_block={{ blocksize }},
                                frame_dim=({{ dbname[1] }}, {{ dbname[2] }}),
                                continuous_feature_blocks={{ frontalfaceonly }},
                                with_energy=_with_energy,
                                take_video_features_asis=_take_video_features_asis,
                                concatenate_features=True,
                                audio_context_instead_of_deltas=False)
                                    
                                    
algorithm = "test"

skip_preprocessing = True
skip_extraction = False

