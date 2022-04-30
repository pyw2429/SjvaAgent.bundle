# -*- coding: UTF-8 -*-
import os, sys, platform, traceback
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import logging
    import logging.handlers
    logger = logging.getLogger('sjva_music_normal')
    logger.setLevel(logging.DEBUG) 
    formatter = logging.Formatter(u'[%(asctime)s|%(levelname)s|%(filename)s|%(lineno)d] : %(message)s')
    file_max_bytes = 10 * 1024 * 1024 
    filename = os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), '../../', 'Logs', 'sjva.scanner.music_chart.log')
    #fileHandler = logging.FileHandler(filename, encoding='utf8')
    fileHandler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=file_max_bytes, backupCount=5, encoding='utf8')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
except:
    pass



def Scan(path, files, mediaList, subdirs, language=None, root=None):
  Filter.Scan(path, files, mediaList, subdirs, audio_exts, root)
  Process(path, files, mediaList, subdirs, language, root)


import Filter, Media
import os.path
import re, os, string


audio_exts = ['mp3', 'm4a', 'm4b', 'flac', 'aac', 'rm', 'rma', 'mpa', 'wav', 'wma', 'ogg', 'mp2', 'mka',
              'ac3', 'dts', 'ape', 'mpc', 'mp+', 'mpp', 'shn', 'oga', 'aiff', 'aif', 'wv', 'dsf', 'dsd', 'opus']

# Unicode control characters can appear in ID3v2 tags but are not legal in XML.
RE_UNICODE_CONTROL =  u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                      u'|' + \
                      u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                      (
                        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff)
                      )

def Process(path, files, mediaList, subdirs, language=None, root=None):
  if len(files) < 1: return
  albumTracks = []
  for f in files:
    try:
      logger.info(f)
      
      (artist, album, title, track, disc, album_artist, compil) = getInfoFromTag(f, language)

      artist = album = os.path.basename(os.path.dirname(f))
      disc = '1'

      file = os.path.splitext(os.path.basename(f))[0]
      match = re.match("^(?P<track>\d+)-(?P<title>.*?)-(?P<album_artist>[^-]+)-(?P<album>[^-]+)$", file)
      if match:
        track = int(match.group('track'))
        title = match.group('title')
        #album_artist = match.group('album_artist')
       
      logger.debug('=============================================')
      logger.debug('LAST artist : %s', cleanPass(artist))
      logger.debug('LAST album : %s', cleanPass(album))
      logger.debug('LAST title : %s', cleanPass(title))
      logger.debug('LAST track : %s', track)
      logger.debug('LAST disc : %s', disc)
      logger.debug('LAST album_artist : %s', cleanPass(album_artist))

      t = Media.Track(cleanPass(artist), cleanPass(album), cleanPass(title), track, disc=disc, album_artist=cleanPass(album_artist), guid=None, album_guid=None)
      t.parts.append(f)
      mediaList.append(t)
      logger.debug('Adding: [Artist: %s] [Album: %s] [Title: %s] [Tracknumber: %s] [Disk: %s] [Album Artist: %s] [File: %s]' % (artist, album, title, track, disc, album_artist, f))
    except Exception as e:
      logger.error('Exception:%s', e)
      logger.error(traceback.format_exc())
      logger.debug("Skipping (Metadata tag issue): " + f)


def cleanPass(t):
  try:
    t = re.sub(RE_UNICODE_CONTROL, '', t.strip().encode('utf-8'))
  except:
    pass
  return t


def getInfoFromTag(filename, language):
  return (None, None, None, None, None, None, None)