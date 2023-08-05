"""
Template for the config script to train PCA on the features from the training set to reduce their dimensionality.
Steps 1 to 2 should be run first.
"""

from bob.paper.lipsync2019.extractor import CepstralMouthDeltas
from bob.paper.lipsync2019.extractor import PCAReduction

_mfccenergy = '{{ mfccenergy }}'
_project_name = '{{ projectname }}'
_block_size = {{ blocksize }}

_feature_length = {{ pcafeaturesize }}

preprocessed_directory = '../extracted_{{ projectname }}_{{ mfccenergy }}_blk{{ blocksize }}'

preprocessor = CepstralMouthDeltas(concatenate_features=True)

extracted_directory = '../extracted_{{ projectname }}_{{ mfccenergy }}_blk{{ blocksize }}_pca{{ pcafeaturesize }}'

extractor = PCAReduction(resulted_features_size={{ pcafeaturesize }},
                         per_modality_pca=False,
                         train_on_genuine_only=False,
                         limit_data=20000)

extractor_file = 'Extractor_' + db_name + '.hdf5'

sub_directory = '{{ projectname }}_{{ mfccenergy }}_blk{{ blocksize }}_pca{{ pcafeaturesize }}'

algorithm = "test"

skip_extraction = False
skip_extractor_training = False

