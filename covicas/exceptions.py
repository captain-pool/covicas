class Error(Exception):
    pass
class CameraNotOpenError(Error):
    def __init__(self):
        self.message = "The video source is not open"
    def __str__(self):
        return self.message
class TrainDataSourceNotProvidedError(Error):
    def __init__(self):
        self.message = "You need to provide image data directory to 'datadir' paramater when set to Training Mode"
    def __str__(self):
        return self.message
class TrainedModelNotProvidedError(Error):
    def __init__(self):
        self.message = "Trained Model not provided. Provide path to the yml file to 'trained_model' parameter"
    def __str__(self):
        return self.message
class InvalidGeneratorError(Error):
    def __init__(self):
        self.message = "Live Feed Frame Generator not Provided"
    def __str__(self):
        return self.message
class DatabaseNotBuiltError(Error):
    def __init__(self):
        self.message = "The Database of Images is Not built"
    def __str__(self):
        return self.message
