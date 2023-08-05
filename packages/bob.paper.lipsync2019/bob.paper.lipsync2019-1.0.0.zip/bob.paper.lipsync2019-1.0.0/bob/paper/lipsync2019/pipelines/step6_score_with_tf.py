import os
import numpy
from bob.bio.video.algorithm import Wrapper as AlgoWrapper
import bob.paper.lipsync2019

_path, _basename = os.path.split(model_dir)
projected_directory = 'projections'

# projected_directory = os.path.join(model_dir, 'projections')

# projected_directory = os.path.join('..', os.path.basename(model_dir), 'projections')
# score_directories = ['lstm']


def read_toscore_object(self, toscore_object_file):
    return self.read_feature(toscore_object_file)

{% if projectname == 'crossmode_regressor' %}
def score(self, toscore):
    # expect toscore to be FrameContainer
    scores = [frame[1] for frame in self.frame_selector(toscore)]
    scores = numpy.asarray(scores, dtype=numpy.float32)
    real_scores = scores[:]
    return [numpy.mean(real_scores)]
{% else %}
def score(self, toscore):
    # expect toscore to be FrameContainer
    scores = [frame[1] for frame in self.frame_selector(toscore)]
    scores = numpy.asarray(scores, dtype=numpy.float32)
    real_scores = scores[:, 1]
    return [numpy.mean(real_scores)]
{% endif %}

AlgoWrapper.read_toscore_object = read_toscore_object
AlgoWrapper.score = score
algorithm = AlgoWrapper(bob.paper.lipsync2019.algorithm.Scoring())

{% if projectname == 'crossmode_regressor' %}
sub_directory = 'scores_' + sub_directory + '_mean_entropy_lr-{0}_epochs-{1}_vft_{2}_aft{3}_ws_{4}_lstm{5}'.format(
    learning_rate, epochs, video_features, audio_features, num_time_steps, '_'.join(map(str, network_size)))
{% else %}
sub_directory = os.path.join(os.path.basename(_path), _basename)
{% endif %}

# + '_mean_entropy_lr-{0}_epochs-{1}_ft_{2}_ws_{3}_lstm{4}'.format(learning_rate, epochs, feature_size, sliding_win_len, '_'.join(map(str, network_size))))


skip_extraction = True
skip_preprocessing = True
skip_extractor_training = True
skip_projector_training = True
skip_projection = True
skip_score_computation = False
