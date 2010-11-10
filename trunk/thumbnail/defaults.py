DEBUG = False
BASEDIR = ''
SUBDIR = ''
PREFIX = ''
QUALITY = 85
CONVERT = '/usr/bin/convert'
WVPS = '/usr/bin/wvPS'
EXTENSION = 'jpg'
PROCESSORS = (
    'MOX.thumbnail.processors.colorspace',
    'MOX.thumbnail.processors.autocrop',
    'MOX.thumbnail.processors.scale_and_crop',
    'MOX.thumbnail.processors.filters',
)
IMAGEMAGICK_FILE_TYPES = ('eps', 'pdf', 'psd')
