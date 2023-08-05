"""
Template for the generic config file for SAVI. It should be used in combinaiton with other config files.
"""

from bob.paper.lipsync2019.database import SAVIPadDatabase
import os

db_name = '{{ dbname[0] }}'
location = '{{ location }}'

from bob.pad.base.tools.command_line import is_idiap

if is_idiap():
    temp_dir = '/idiap/temp/{}/{}'.format(os.environ['USER'], db_name)
else:
    temp_dir = 'temp/{}/..'.format(db_name)


database = SAVIPadDatabase(db_name=db_name)

# a dummy preprocessor 
preprocessor = "test"

# a dummy extractor for protocol
extractor = "test"

# a dummy algorithm for protocol
algorithm = "test"

sub_directory = '{{ projectname }}_{{ dbname[0] }}'

preprocessed_directory = '../{{ projectname }}_preprocessed'

groups = ['train', 'dev']
# groups = ['dev']

# change the path to the actual audio data inside "path_to_data.txt" file
database_directories_file = "path_to_data_{{ location }}.txt"

verbose = 3

protocol = '{{ protocol }}'

allow_missing_files = True
skip_preprocessing = True
skip_extraction = True
skip_extractor_training = True
skip_projector_training = True
skip_projection = True
skip_score_computation = True
