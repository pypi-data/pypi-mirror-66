""" Module that provide all exceptions
"""
import json


class OptOutException(Exception):
    """ Exception when we can't give a confidence
    """
    def __init__(self, number, msg=None):
        if msg is None:
            msg = 'OptOut - unknown'
        super().__init__(msg)
        self._number = number
        self._msg = msg

    def get_number(self): return self._number

    def get_msg(self): return self._msg

    def to_json(self):
        my_dict = {"error_number": self._number, "explanation": self._msg}
        return json.dumps(my_dict)


class GeneralErrorException(OptOutException):
    """ CONFIDENCE_GENERAL_ERROR=-1.0
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'General error'
        super().__init__(-1, msg)


class NoAudioStreamException(OptOutException):
    """ CONFIDENCE_NO_AUDIO_STREAM=-2.0
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'No audio stream in the video'
        super().__init__(-2, msg)


class NoSpeechDetectedException(OptOutException):
    """ CONFIDENCE_NO_SPEECH_DETECTED=-3.0
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'No speech detected'
        super().__init__(-3, msg)


class SkippingAvException(OptOutException):
    """ CONFIDENCE_SKIPPING_AV=-4
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Skipping AV'
        super().__init__(-4, msg)


class SceneDetectErrorException(OptOutException):
    """ CONFIDENCE_SCENE_DETECT_ERROR=-5
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Scene detect error'
        super().__init__(-5, msg)


class NotAVideoException(OptOutException):
    """ CONFIDENCE_NOT_A_VIDEO=-6
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Not a video'
        super().__init__(-6, msg)
