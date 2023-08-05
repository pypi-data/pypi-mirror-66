import tensorflow.compat.v1 as tf


# from bob.learn.tensorflow.network import MLP
# import numpy
import logging

import numpy

logger = logging.getLogger("LSTM Logger:")


def lstm_audio_to_video( inputs, 
                          audio_feature_length=41,
                          video_feature_length=128,
                          audio_cell_size=16,
                          video_cell_size=16,
                          num_time_steps=10,
                          batch_size=16,
                          block_size=1,
                          scope='lstm_regres',
                          activation=tf.nn.relu,
                          reuse=None,
                          mode=tf.estimator.ModeKeys.TRAIN,
                          trainable_variables=None,
                          rnn_cell=tf.nn.rnn_cell.LSTMCell
                        ):
                        
    #
    inputs = tf.layers.batch_norm(inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))
    
    video_outputs = []
    audio_outputs = []
    
    video_inputs = inputs[:,:,:video_feature_length]
    audio_inputs = inputs[:,:,video_feature_length:] 
    # audio lstm  
    ashape = audio_inputs.get_shape().as_list()
    ainput_lstm = tf.reshape( audio_inputs, [-1, 4*num_time_steps, ashape[2]//4] ) # -1 inferred to be the batch size.
    aoutput_minilstm = tf.python.layers.base_lstm(ainput_lstm, lstm_cell_size=audio_cell_size,
    # aoutput_minilstm = tf.python.layers.base_lstm(audio_inputs, lstm_cell_size=audio_cell_size,
                              num_time_steps=num_time_steps*4,
                              # num_time_steps=num_time_steps,
                              batch_size=batch_size,
                              rnn_cell=rnn_cell,
                              scope=scope,
                              activation=activation,
                              # name='audio_lstm_layer{0}_{1}'.format(0, audio_cell_size),
                              name='audio_lstm',
                              trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                              reuse=reuse)
    
    #
    initializer = tf.layers.xavier_initializer(uniform=False, dtype=tf.float32, seed=10)
    # audio_fc_1 = tf.layers.dense(aoutput_minilstm[-1], audio_cell_size*2, activation=activation, reuse=reuse,
    #            trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='audio_fc_1', kernel_initializer=initializer) # video_cell_size                
    # audio_fc_2 = tf.layers.dense(audio_fc_1, audio_cell_size*4, activation=activation, reuse=reuse,
    #            trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='audio_fc_2', kernel_initializer=initializer) # video_cell_size
    # audio_fc_3 = tf.layers.dense(audio_fc_2, audio_cell_size*8, activation=activation, reuse=reuse,
    #            trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='audio_fc_3', kernel_initializer=initializer) # video_cell_size           
    # #
    # return {'audio_fc':audio_fc_3, 'video_labels':video_inputs[:,1,:]}, None
    #
    audio_fc_1 = tf.layers.dense(aoutput_minilstm[-1], audio_cell_size*2, activation=activation, reuse=reuse,
               trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='audio_fc_1', kernel_initializer=initializer)
    return {'audio_fc':audio_fc_1, 'video_labels':video_inputs[:,1,0:16]}, None          

def lstm_regressor_input( inputs, 
                          audio_feature_length=41,
                          video_feature_length=128,
                          audio_cell_size=16,
                          video_cell_size=16,
                          num_time_steps=2,
                          batch_size=16,
                          block_size=1,
                          scope='lstm_regres',
                          activation=tf.nn.relu,
                          reuse=None,
                          mode=tf.estimator.ModeKeys.TRAIN,
                          trainable_variables=None,
                          rnn_cell=tf.nn.rnn_cell.LSTMCell
                        ):
                        
    inputs = tf.layers.batch_norm(inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))
                        
    video_outputs = []
    audio_outputs = []
    video_inputs = inputs[:,:,:video_feature_length]
    audio_inputs = inputs[:,:,video_feature_length:] 
    
    # import numpy
    # print( numpy.shape( inputs ) )
    # print( numpy.shape( video_inputs ) )
    # print( numpy.shape( audio_inputs ) )
    
    # video lstm
    vshape = video_inputs.get_shape().as_list()
    # print( 'lstm_regressor_input, size of video', vshape )
    # video_inputs = tf.layers.batch_norm( video_inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN) )
    voutput_minilstm = tf.python.layers.base_lstm(video_inputs, lstm_cell_size=video_cell_size,
                              num_time_steps=num_time_steps,
                              batch_size=batch_size,
                              rnn_cell=rnn_cell,
                              scope=scope,
                              activation=activation,
                              # name='video_lstm_layer{0}_{1}'.format(0, video_cell_size),
                              name='video_lstm',
                              trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                              reuse=reuse)
        
    # audio lstm  
    ashape = audio_inputs.get_shape().as_list()
    ainput_lstm = tf.reshape( audio_inputs, [-1, 4*num_time_steps, ashape[2]//4] ) # -1 inferred to be the batch size.
    # print( 'lstm_regressor_input, size of audio thing : ', ainput_lstm.get_shape().as_list() )    
    # ainput_lstm = tf.layers.batch_norm( ainput_lstm, is_training=(mode == tf.estimator.ModeKeys.TRAIN) )
    aoutput_minilstm = tf.python.layers.base_lstm(ainput_lstm, lstm_cell_size=audio_cell_size,
                              num_time_steps=num_time_steps*4,
                              batch_size=batch_size,
                              rnn_cell=rnn_cell,
                              scope=scope,
                              activation=activation,
                              # name='audio_lstm_layer{0}_{1}'.format(0, audio_cell_size),
                              name='audio_lstm',
                              trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                              reuse=reuse)

    # print( 'video size', numpy.shape( voutput_minilstm[-1] ) )
    # print( 'audio size', numpy.shape( aoutput_minilstm[-1] ) )
    
    # regress the outputs
    initializer = tf.layers.xavier_initializer(uniform=False, dtype=tf.float32, seed=10)
    video_fc_1 = tf.layers.dense(voutput_minilstm[-1], video_cell_size*4, activation=activation, reuse=reuse,
                trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='video_fc_1', kernel_initializer=initializer)                
    video_fc_2 = tf.layers.dense(video_fc_1, video_cell_size*2, activation=activation, reuse=reuse,
                trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='video_fc_2', kernel_initializer=initializer)   
                
    audio_fc_1 = tf.layers.dense(aoutput_minilstm[-1], audio_cell_size*4, activation=activation, reuse=reuse,
                trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='audio_fc_1', kernel_initializer=initializer)                
    audio_fc_2 = tf.layers.dense(audio_fc_1, audio_cell_size*2, activation=activation, reuse=reuse,
                trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='audio_fc_2', kernel_initializer=initializer)  
    # print( 'video fc', numpy.shape( video_fc_2 ) )
    # print( 'audio fc', numpy.shape( audio_fc_2 ) )
    # import ipdb; ipdb.set_trace()    
    # output
                                       
    return {'video_fc':video_fc_2, 'audio_fc':audio_fc_2, 'video_labels':voutput_minilstm[-1], 'audio_labels':aoutput_minilstm[-1]}, None
    # return {'video_fc':video_fc_1, 'audio_fc':audio_fc_1, 'video_labels':voutput_minilstm[-1], 'audio_labels':aoutput_minilstm[-1]}, None

def lstm_dimreduction_stacked_lstm(inputs, block_size=5, video_features_length=256, cell_sizes=[64], num_time_steps=20,
                              batch_size=10, scope='lstm_stack', activation=tf.nn.relu, reuse=None,
                              mode=tf.estimator.ModeKeys.TRAIN, trainable_variables=None,
                              rnn_cell=tf.nn.rnn_cell.LSTMCell):
    # inputs = tf.layers.batch_norm(inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))

    video_outputs = []
    audio_outputs = []

    video_inputs = inputs[:, :, :video_features_length]
    audio_inputs = inputs[:, :, video_features_length:]
    mini_lstm_cell_size = 32

    vshape = video_inputs.get_shape().as_list()
    for i in range(vshape[1]):
        vinput_mini_lstm = video_inputs[:, i, :]
        vinput_mini_lstm = tf.reshape(vinput_mini_lstm, [-1, block_size, vshape[2]//block_size])
        voutput_minilstm = tf.python.layers.base_lstm(vinput_mini_lstm, lstm_cell_size=mini_lstm_cell_size,
                                  num_time_steps=block_size,
                                  batch_size=batch_size,
                                  rnn_cell=rnn_cell,
                                  scope=scope,
                                  activation=activation,
                                  name='video_lstm_layer{0}_{1}'.format(i, mini_lstm_cell_size),
                                  trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                                  reuse=reuse)
        # add only the last output of the lstm
        # essentially, the dimensionality of our features are reduced from vshape[2] to mini_lstm_cell_size
        video_outputs.append(voutput_minilstm[-1])

    ashape = audio_inputs.get_shape().as_list()
    for i in range(ashape[1]):
        ainput_mini_lstm = audio_inputs[:, i, :]
        ainput_mini_lstm = tf.reshape(ainput_mini_lstm, [-1, block_size, ashape[2]//block_size])

        aoutput_minilstm = tf.python.layers.base_lstm(ainput_mini_lstm, lstm_cell_size=mini_lstm_cell_size,
                                  num_time_steps=block_size,
                                  batch_size=batch_size,
                                  rnn_cell=rnn_cell,
                                  scope=scope,
                                  activation=activation,
                                  name='audio_lstm_layer{0}_{1}'.format(i, mini_lstm_cell_size),
                                  trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                                  reuse=reuse)
        # add only the last output of the lstm
        # essentially, the dimensionality of our features are reduced from vshape[2] to mini_lstm_cell_size
        audio_outputs.append(aoutput_minilstm[-1])

    joined_outputs = [tf.concat([video_out, audio_out], 1) for video_out, audio_out in
                      zip(video_outputs, audio_outputs)]

    joined_outputs = tf.stack(joined_outputs, 1)

    return stacked_lstm(joined_outputs, cell_sizes, num_time_steps,
                        batch_size, scope=scope, activation=activation, reuse=reuse,
                        mode=mode, trainable_variables=trainable_variables,
                        rnn_cell=rnn_cell)


def audio_video_separate_lstm(inputs, video_features_length=256, cell_sizes=[64], num_time_steps=20,
                 batch_size=10, scope='lstm_stack', activation=tf.nn.relu, reuse=None,
                 mode=tf.estimator.ModeKeys.TRAIN, trainable_variables=None, rnn_cell=tf.nn.rnn_cell.LSTMCell):

    inputs = tf.layers.batch_norm(inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))

    video_inputs = inputs[:, :, :video_features_length]
    audio_inputs = inputs[:, :, video_features_length:]

    lstm_cell_size = cell_sizes[0]

    audio_outputs = tf.python.layers.base_lstm(audio_inputs, lstm_cell_size=lstm_cell_size,
                       num_time_steps=num_time_steps,
                       batch_size=batch_size,
                       rnn_cell=rnn_cell,
                       scope=scope,
                       activation=activation,
                       name='audio_lstm_layer_{}'.format(lstm_cell_size),
                       trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                       reuse=reuse)

    video_outputs = tf.python.layers.base_lstm(video_inputs, lstm_cell_size=lstm_cell_size,
                       num_time_steps=num_time_steps,
                       batch_size=batch_size,
                       rnn_cell=rnn_cell,
                       scope=scope,
                       activation=activation,
                       name='video_lstm_layer_{}'.format(lstm_cell_size),
                       trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                       reuse=reuse)

#    joined_outputs = tf.concat([audio_outputs[-1], video_outputs[-1]], 1)

    joined_outputs = [tf.concat([audio_out, video_out], 1) for audio_out, video_out in zip(audio_outputs, video_outputs)]
 
    joined_outputs = tf.stack(joined_outputs, 1)

#    joined_outputs = tf.layers.batch_norm(joined_outputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))
#    initializer = tf.layers.xavier_initializer(uniform=False, dtype=tf.float32, seed=10)

#    fc_layer = tf.layers.dense(joined_outputs, 64, activation=activation, reuse=reuse,
#                 trainable=(mode == tf.estimator.ModeKeys.TRAIN), name='mlp', kernel_initializer=initializer)
#    fc_layer = tf.layers.batch_norm(fc_layer, is_training=(mode == tf.estimator.ModeKeys.TRAIN))
#    return fc_layer, None
    return stacked_lstm(joined_outputs, cell_sizes, num_time_steps,
                      batch_size, scope=scope, activation=activation, reuse=reuse,
                      mode=mode, trainable_variables=trainable_variables,
                         rnn_cell=rnn_cell)


def stacked_lstm_contrastive_regression( inputs, 
                                         video_feature_length=60,
                                         cell_sizes=[64], 
                                         num_time_steps=20,
                                         batch_size=10, 
                                         scope='lstm_stack', 
                                         activation=tf.nn.relu, 
                                         reuse=None,
                                         mode=tf.estimator.ModeKeys.TRAIN, 
                                         trainable_variables=None, 
                                         rnn_cell=tf.nn.rnn_cell.LSTMCell 
                                       ):
                 
    """This is a staked lstm version for the contrastive loss with regression tf.python.layers.based output
       This does the audio and video in seperate lstms as the contrastive loss needs a left and right side
    """             
    
    # batch normalisation
    inputs = tf.layers.batch_norm(inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))             
    
    # seperate the features
    video_inputs = inputs[:,:,:video_feature_length]
    audio_inputs = inputs[:,:,video_feature_length:]
    
    # stacked lstm
    # import ipdb; ipdb.set_trace()
    for i, lstm_cell_size in enumerate( cell_sizes ):
        # video lstm
        video_inputs = tf.python.layers.base_lstm( video_inputs,
                                  lstm_cell_size=lstm_cell_size,
                                  num_time_steps=num_time_steps,
                                  batch_size=batch_size,
                                  rnn_cell=rnn_cell,
                                  scope=scope,
                                  activation=activation,
                                  name='lstm_{}_video'.format( i ),
                                  trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                                  reuse=reuse,
                                )
                                
        # audio lstm
        audio_inputs = tf.python.layers.base_lstm( audio_inputs,
                                  lstm_cell_size=lstm_cell_size,
                                  num_time_steps=num_time_steps,
                                  batch_size=batch_size,
                                  rnn_cell=rnn_cell,
                                  scope=scope,
                                  activation=activation,
                                  name='lstm_{}_audio'.format( i ),
                                  trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                                  reuse=reuse,
                                ) 
        
    # output                        
    return {'video_lstm':video_inputs[-1], 'audio_lstm':audio_inputs[-1]}, None                                               


def stacked_lstm(inputs, cell_sizes=[64], num_time_steps=20,
                 batch_size=10, scope='lstm_stack', activation=tf.nn.relu, reuse=None,
                 mode=tf.estimator.ModeKeys.TRAIN, trainable_variables=None, rnn_cell=tf.nn.rnn_cell.LSTMCell):
    """
    """
    print( 'stacked lstm input size', numpy.shape( inputs ) )
    inputs = tf.layers.batch_norm(inputs, is_training=(mode == tf.estimator.ModeKeys.TRAIN))
    for lstm_cell_size in cell_sizes:
        inputs = tf.python.layers.base_lstm(inputs, lstm_cell_size=lstm_cell_size,
                           num_time_steps=num_time_steps,
                           batch_size=batch_size,
                           rnn_cell=rnn_cell,
                           scope=scope,
                           activation=activation,
                           name='lstm_layer_{}'.format(lstm_cell_size),
                           trainable=(mode == tf.estimator.ModeKeys.TRAIN),
                           reuse=reuse)    
        inputs = [tf.layers.batch_norm(input, is_training=(mode == tf.estimator.ModeKeys.TRAIN)) for input in inputs]

    logger.info("LSTM: the shape of the overall output: {0}".format(inputs[-1].shape))

    return inputs[-1], None



def base_lstm(inputs, lstm_cell_size, num_time_steps=20,
              batch_size=10, scope='lstm_1l', activation=tf.nn.relu, reuse=None, name='lstm', trainable=True,
              rnn_cell=tf.nn.rnn_cell.LSTMCell):
    """
    """
    outputs = LSTM(lstm_cell_size=lstm_cell_size,
                  num_time_steps=num_time_steps,
                  batch_size=batch_size,
                  rnn_cell=rnn_cell,
                  scope=scope,
                  activation=activation,
                  name=name,
                  trainable=trainable,
                  reuse=reuse)(inputs)
    logger.info("LSTM layer: the number of outputs {0} of shape {1}".format(len(outputs), outputs[-1].shape))
    return outputs


class LSTM(tf.layers.Layer):
    """
    Basic LSTM layer in the format of tf-slim
    """

    def __init__(self, lstm_cell_size,
                 num_time_steps=20,
                 batch_size=10,
                 rnn_cell=tf.nn.rnn_cell.LSTMCell,
                 scope='rnn',
                 activation=tf.nn.relu,
                 name=None,
                 reuse=None,
                 dropout=False,
                 input_dropout=1.0,
                 output_dropout=1.0,
                 trainable=False,
                 **kwargs):
        """
        :param lstm_cell_size [int]: size of the LSTM cell, i.e., the length of the output form each cell
        :param batch_size [int]: input data batch size
        :param num_time_steps [int]: the number of time steps of the input, i.e.,
        the number of LSTM cells in one layer
        """
        super(LSTM, self).__init__(name=scope, trainable=trainable, **kwargs)

        self.lstm_cell_size = lstm_cell_size
        self.lstm = rnn_cell(self.lstm_cell_size,
                             activation=activation,
                             state_is_tuple=True,
                             name=name,
                             dtype=tf.float32,
                             reuse=reuse,
                             **kwargs)

        # print("self.lstm_cell_size: ", self.lstm_cell_size)
        if dropout:
            self.lstm = tf.nn.rnn_cell.DropoutWrapper(self.lstm, input_keep_prob=input_dropout,
                                                      output_keep_prob=output_dropout)
        self.batch_size = batch_size
        self.num_time_steps = num_time_steps
        # print("self.num_time_steps:", self.num_time_steps)
        self.scope = scope

        hidden_state = tf.Variable(tf.zeros([self.batch_size, self.lstm_cell_size]), trainable=trainable)
        current_state = tf.Variable(tf.zeros([self.batch_size, self.lstm_cell_size]), trainable=trainable)
        self.states = tf.contrib.rnn.LSTMStateTuple(current_state, hidden_state)

        self.sequence_length = None

    def __call__(self, inputs):
        """
        :param inputs: The input is expected to have shape (batch_size, num_time_steps, input_vector_size).
        """
        # shape inputs correctly
        inputs = tf.python.framework.ops.convert_to_tensor(inputs)
        shape = inputs.get_shape().as_list()
        logger.info("LSTM: the shape of the inputs: {0}".format(shape))
        
        # if the input is already formatted correctly, just use it as is
        if shape[1] == self.batch_size and shape[0] == self.num_time_steps:
            inputs.set_shape((shape[0], None, shape[2]))
            logger.info("LSTM: undefine batch shape inputs: {0}".format(inputs.get_shape().as_list()))
            list_inputs = tf.unstack(inputs, self.num_time_steps, 0)
        # here we consider all special cases
        else:
            input_time_steps = shape[1]  # second dimension must be the number of time steps in LSTM

            if len(shape) == 4:  # when inputs shape is 4, the last dimension must be 1
                if shape[-1] == 1:  # we accept last dimension to be 1, then we just reshape it
                    inputs = tf.reshape(inputs, shape=(-1, shape[1], shape[2]))
                    logger.info(
                        "LSTM: after reshape, the shape of the inputs: {0}".format(inputs.get_shape().as_list()))
                else:
                    raise ValueError(
                        'The shape of input must be either (batch_size, num_time_steps, input_vector_size) or '
                        '(batch_size, num_time_steps, input_vector_size, 1), but it is {}'.format(shape))

            if input_time_steps % self.num_time_steps:
                raise ValueError('number of rows in one batch of input ({}) should be '
                                 'the same as the num_time_steps of LSTM ({})'
                                 .format(input_time_steps, self.num_time_steps))
            
            # convert inputs into the num_time_steps list of the inputs each of shape (batch_size, input_vector_size)
            list_inputs = tf.unstack(inputs, self.num_time_steps, 1)

        # run LSTM training on the batch of inputs
        # return the output (a list of self.num_time_steps outputs each of size input_vector_size)
        # and remember the final states
        # import ipdb; ipdb.set_trace()
        outputs, self.states = tf.nn.static_rnn(self.lstm,
                                                         inputs=list_inputs,
                                                         initial_state=self.states,
                                                         dtype=tf.float32,
                                                         scope=self.scope)

        # consider the output of the last cell
        return outputs
        # return tf.matmul(outputs[-1], self.output_activation_weights['out']) + self.output_activation_biases['out']
