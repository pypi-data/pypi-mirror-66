# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coherence',
 'coherence.backends',
 'coherence.backends.models',
 'coherence.extern',
 'coherence.extern.galleryremote',
 'coherence.extern.youtubedl',
 'coherence.upnp',
 'coherence.upnp.core',
 'coherence.upnp.devices',
 'coherence.upnp.services',
 'coherence.upnp.services.clients',
 'coherence.upnp.services.servers',
 'coherence.web',
 'docs',
 'misc',
 'tests',
 'tests.backends',
 'tests.upnp',
 'tests.upnp.core']

package_data = \
{'': ['*'],
 'coherence.upnp.core': ['xml-service-descriptions/*'],
 'coherence.web': ['static/images/*',
                   'static/js/*',
                   'static/styles/*',
                   'templates/*'],
 'docs': ['source/*',
          'source/backends/*',
          'source/backends/models/*',
          'source/extern/*',
          'source/extern/galleryremote/*',
          'source/extern/youtubedl/*',
          'source/upnp/core/*',
          'source/upnp/devices/*',
          'source/upnp/services/clients/*',
          'source/upnp/services/servers/*'],
 'misc': ['design/*', 'device-icons/*', 'other-icons/*']}

modules = \
['CHANGELOG', 'LICENCE']
install_requires = \
['configobj>=4.3',
 'eventdispatcher==1.9.4',
 'lxml',
 'pyopenssl',
 'python-dateutil',
 'service_identity>=18.1.0,<19.0.0',
 'twisted>=20.3.0',
 'zope.interface']

extras_require = \
{'dbus': ['dbus-python'],
 'dev': ['autobahn',
         'dbus-python',
         'pycairo>=1.17.1',
         'pygobject>=3.30.0',
         'flake8',
         'nose',
         'nose-cov',
         'pylint==2.1.1',
         'python-coveralls==2.9.1',
         'recommonmark>=0.4.0',
         'sphinx>=1.3.5',
         'sphinx-rtd-theme>=0.1.9',
         'sphinxcontrib-napoleon>=0.4.4'],
 'docs': ['recommonmark>=0.4.0',
          'sphinx>=1.3.5',
          'sphinx-rtd-theme>=0.1.9',
          'sphinxcontrib-napoleon>=0.4.4'],
 'feed': ['feedparser'],
 'gstreamer': ['pycairo>=1.17.1', 'pygobject>=3.30.0'],
 'test': ['flake8',
          'nose',
          'nose-cov',
          'pylint==2.1.1',
          'python-coveralls==2.9.1'],
 'twitch': ['livestreamer'],
 'web': ['autobahn']}

entry_points = \
{'coherence.plugins.backend.media_renderer': ['BuzztardPlayer = '
                                              'coherence.backends.buzztard_control:BuzztardPlayer',
                                              'ElisaPlayer = '
                                              'coherence.backends.elisa_renderer:ElisaPlayer',
                                              'GStreamerPlayer = '
                                              'coherence.backends.gstreamer_renderer:GStreamerPlayer'],
 'coherence.plugins.backend.media_server': ['AmpacheStore = '
                                            'coherence.backends.ampache_storage:AmpacheStore',
                                            'AppleTrailersStore = '
                                            'coherence.backends.appletrailers_storage:AppleTrailersStore',
                                            'AudioCDStore = '
                                            'coherence.backends.audiocd_storage:AudioCDStore',
                                            'AxisCamStore = '
                                            'coherence.backends.axiscam_storage:AxisCamStore',
                                            'BansheeStore = '
                                            'coherence.backends.banshee_storage:BansheeStore',
                                            'BuzztardStore = '
                                            'coherence.backends.buzztard_control:BuzztardStore',
                                            'DVBDStore = '
                                            'coherence.backends.dvbd_storage:DVBDStore',
                                            'ElisaMediaStore = '
                                            'coherence.backends.elisa_storage:ElisaMediaStore',
                                            'FSStore = '
                                            'coherence.backends.fs_storage:FSStore',
                                            'FeedStore = '
                                            'coherence.backends.feed_storage:FeedStore',
                                            'FlickrStore = '
                                            'coherence.backends.flickr_storage:FlickrStore',
                                            'Gallery2Store = '
                                            'coherence.backends.gallery2_storage:Gallery2Store',
                                            'IRadioStore = '
                                            'coherence.backends.iradio_storage:IRadioStore',
                                            'ITVStore = '
                                            'coherence.backends.itv_storage:ITVStore',
                                            'LastFMStore = '
                                            'coherence.backends.lastfm_storage:LastFMStore',
                                            'LolcatsStore = '
                                            'coherence.backends.lolcats_storage:LolcatsStore',
                                            'MediaStore = '
                                            'coherence.backends.mediadb_storage:MediaStore',
                                            'MiroGuideStore = '
                                            'coherence.backends.miroguide_storage:MiroGuideStore',
                                            'PicasaStore = '
                                            'coherence.backends.picasa_storage:PicasaStore',
                                            'PlaylistStore = '
                                            'coherence.backends.playlist_storage:PlaylistStore',
                                            'RadiotimeStore = '
                                            'coherence.backends.radiotime_storage:RadiotimeStore',
                                            'SWR3Store = '
                                            'coherence.backends.swr3_storage:SWR3Store',
                                            'TEDStore = '
                                            'coherence.backends.ted_storage:TEDStore',
                                            'TestStore = '
                                            'coherence.backends.test_storage:TestStore',
                                            'TrackerStore = '
                                            'coherence.backends.tracker_storage:TrackerStore',
                                            'TwitchStore = '
                                            'coherence.backends.twitch_storage:TwitchStore',
                                            'YamjStore = '
                                            'coherence.backends.yamj_storage:YamjStore',
                                            'YouTubeStore = '
                                            'coherence.backends.youtube_storage:YouTubeStore'],
 'console_scripts': ['cohen3 = coherence.cli:main']}

setup_kwargs = {
    'name': 'cohen3',
    'version': '0.9.3',
    'description': 'Cohen3 - DLNA/UPnP Media Server',
    'long_description': 'Cohen3\n======\n\n.. image:: https://travis-ci.com/opacam/Cohen3.svg?branch=master\n        :target: https://travis-ci.com/opacam/Cohen3\n\n.. image:: https://img.shields.io/pypi/status/Cohen3.svg\n        :target: https://pypi.python.org/pypi/Cohen3/\n\n.. image:: https://codecov.io/gh/opacam/Cohen3/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/opacam/Cohen3\n        :alt: PyPI version\n\n.. image:: http://img.shields.io/pypi/v/Cohen3.svg?style=flat\n        :target: https://pypi.python.org/pypi/Cohen3\n        :alt: PyPI version\n\n.. image:: https://img.shields.io/github/tag/opacam/Cohen3.svg\n        :target: https://github.com/opacam/Cohen3/tags\n        :alt: GitHub tag\n\n.. image:: https://img.shields.io/github/release/opacam/Cohen3.svg\n        :target: https://github.com/opacam/Cohen3/releases\n        :alt: GitHub release\n\n.. image:: http://hits.dwyl.io/opacam/Cohen3.svg\n        :target: http://hits.dwyl.io/opacam/Cohen3\n\n.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat\n        :target: https://github.com/opacam/Cohen3/issues\n\n.. image:: https://img.shields.io/github/commits-since/opacam/Cohen3/latest.svg\n        :target: https://github.com/opacam/Cohen3/commits/master\n        :alt: Github commits (since latest release)\n\n.. image:: https://img.shields.io/github/last-commit/opacam/Cohen3.svg\n        :target: https://github.com/opacam/Cohen3/commits/master\n        :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/opacam/Cohen3.svg\n        :target: https://github.com/opacam/Cohen3/blob/master/LICENSE\n\nOverview\n--------\n\n**Dlna/UPnP framework**\n\n|cohen-image|\n\n**For the Digital Living**\n\nCohen3 Framework is a DLNA/UPnP Media Server for `Python 3`, based on the\n`Python 2` version named `Cohen <https://github.com/unintended/Cohen>`_.\nProvides several UPnP MediaServers and MediaRenderers to make simple publishing\nand streaming different types of media content to your network.\n\nCohen3 is the Python 3\'s version of the\n`Coherence Framework <https://github.com/coherence-project/Coherence>`_\nproject, originally created by\n`Frank Scholz <mailto:dev@coherence-project.org>`_. If you ever used the\noriginal Coherence project you could use Cohen3 like you do in the original\nCoherence project.\n\n- Documentation: https://opacam.github.io/Cohen3/\n- GitHub: https://github.com/opacam/Cohen3\n- Issue tracker: https://github.com/opacam/Cohen3/issues\n- PyPI: https://pypi.python.org/pypi/cohen3\n- Free software: MIT licence\n\n.. |cohen-image| image:: coherence/web/static/images/coherence-icon.png\n   :height: 12.5 em\n   :width: 12.5 em\n\nFeatures\n--------\nThe original `Coherence Framework` were know to work with different kind of\ndlna/UPnP clients and Cohen3 should also work for them:\n\n    - Sony Playstation 3/4\n    - XBox360/One\n    - Denon AV Receivers\n    - WD HD Live MediaPlayers\n    - Samsung TVs\n    - Sony Bravia TVs\n\nAnd provides a lot of backends to fulfil your media streaming needs:\n\n    - Local file storage\n    - Apple Trailers\n    - Lol Cats\n    - ShoutCast Radio\n    - and much more...\n\nProject Status\n--------------\nRight now Cohen is in development mode. All the code has been refactored in\norder to work for Python 3, moreover, some additions has been made to make\neasier to create a custom Backend (check the\n`coherence.backends.models <https://opacam.github.io/Cohen3/source/coherence.\nbackends.html#coherence-backends-models-package>`_ package documentation for\nmore information). The original Coherence project was unmaintained for a while\nand some of the backends has become obsolete. You can see the backends status\nin the below table.\n\n.. list-table::\n   :widths: 10 25 65\n   :header-rows: 1\n\n   * - Status\n     - Backend Name\n     - Description/Notes\n   * - |question|\n     - AmpacheStore\n     -\n   * - |success|\n     - AppleTrailersStore\n     -\n   * - |question|\n     - AudioCDStore\n     -\n   * - |question|\n     - AxisCamStore\n     -\n   * - |question|\n     - BansheeStore\n     -\n   * - |question|\n     - BuzztardStore\n     -\n   * - |question|\n     - DVBDStore\n     -\n   * - |question|\n     - ElisaPlayer\n     -\n   * - |question|\n     - ElisaMediaStore\n     -\n   * - |question|\n     - FeedStore\n     -\n   * - |question|\n     - FlickrStore\n     -\n   * - |success|\n     - FSStore\n     -\n   * - |question|\n     - Gallery2Store\n     -\n   * - |question|\n     - GStreamerPlayer\n     -\n   * - |success|\n     - IRadioStore (ShoutCast)\n     -\n   * - |question|\n     - ITVStore\n     -\n   * - |fails|\n     - LastFMStore\n     - *service moved to new api...needs update*\n   * - |success|\n     - LolcatsStore\n     -\n   * - |question|\n     - MediaStore\n     -\n   * - |fails|\n     - MiroGuideStore\n     - The miroguide\'s api is not working anymore :(\n   * - |question|\n     - PicasaStore\n     - *Partially tested, may work until starting year 2019, where google will\n       begin to shutdown this service, the source code should be rewrite using\n       the api for the new service `Google Photos`*\n   * - |success|\n     - PlayListStore\n     -\n   * - |question|\n     - RadiotimeStore\n     -\n   * - |question|\n     - SWR3Store\n     -\n   * - |success|\n     - TEDStore\n     -\n   * - |question|\n     - TestStore\n     -\n   * - |question|\n     - TrackerStore\n     -\n   * - |question|\n     - TestStore\n     -\n   * - |fails|\n     - TwitchStore\n     - *Partially working, video play is not working*\n   * - |question|\n     - YamjStore\n     -\n   * - |fails|\n     - YouTubeStore\n     - *Google moved to new api...backend should be rewrite with new api in\n       mind*\n\nNotes:\n\n    - Some of the listed backends it may be removed in a future releases...\n      depending on if the target service is still available, dependencies of\n      the backend, maintainability...keep in mind that the main goal of this\n      project is to have a working media server/client capable of serve local\n      files into a dlna/upnp network, all the backends are extra features which\n      may be handy for some end-users and also may be useful as a reference of\n      how to make your own backend using the Cohen3\'s modules.\n\n.. |success| image:: misc/other-icons/checked.png\n   :align: middle\n   :height: 5\n   :width: 5\n\n.. |fails| image:: misc/other-icons/cross.png\n   :align: middle\n   :height: 5\n   :width: 5\n\n.. |question| image:: misc/other-icons/question.png\n   :align: middle\n   :height: 5\n   :width: 5\n\nInstallation with pip\n---------------------\nIf you want to install with pip, first make sure that the `pip` command\ntriggers the python3 version of python or use `pip3` instead. You can install\nthe `Cohen3` python package from `pypi` or github\n\nTo install from pypi:\n^^^^^^^^^^^^^^^^^^^^^\n\n  $ pip3 install --user Cohen3\n\nTo install from git:\n^^^^^^^^^^^^^^^^^^^^\n\n  $ pip3 install --user https://github.com/opacam/Cohen3/archive/master.zip\n\n.. note::\n    - An user install is recommended or use an virtualenv\n\n.. tip::\n      If you encounter problems while installing, caused by some dependency,\n      you may try to bypass this error by installing the conflicting dependency\n      before `Cohen3`, so if you face an error like this for `Twisted`:\n\n        ERROR: Could not find a version that satisfies the requirement\n        Twisted>=19.2.1 (from Cohen3) (from versions: none)\n\n      You should be able to fix it installing Twisted before the install of\n      `Cohen3`:\n\n        pip3 install --upgrade --user Twisted\n\nInstall from source with `poetry`\n---------------------------------\nAfter downloading and extracting the archive or having done a git\nclone, move into the freshly created \'Cohen3\' folder and install\nall dependencies (dev included) with `poetry`, but first upgrade `pip`::\n\n  $ pip3 install pip --upgrade\n  $ pip3 install poetry\n  $ poetry install\n\nPersonalized install from source with `pip`\n-------------------------------------------\nAlso, you can perform a personalized install using `pip`. This will allow you\nto install only certain dependencies, if you want the basic dependencies to run\nthe project::\n\n  $ pip install .\n\nIf you want to install Cohen3 with development dependencies::\n\n  $ pip install .[dev]\n\nNote: Here you have all supported install modes:\n\n    - dev: all the dependencies will be installed except docs\n    - test: used by travis builds (omits dbus and docs)\n    - docs: install build dependencies to generate docs\n    - dbus: install dependencies needed by tube service or dvbd storage\n    - gstreamer: needed if you use GStreamerPlayer\n    - picasa: needed by the picasa storage\n    - youtube: needed by the youtube backend\n\nQuickstart\n----------\nTo just export some files on your hard-disk fire up Cohen with\nan UPnP MediaServer with a file-system backend enabled::\n\n  $ cohen3 --plugin=backend:FSStore,content:/path/to/your/media/files\n\nYou can also configure cohen via a config file. Feel free to check our example\n``misc/cohen.conf.example``. The config file can be placed anywhere, cohen\nlooks by default for ``$HOME/.cohen``, but you can pass the path via the\ncommand line option \'-c\' to it too::\n\n  $ cohen3 -c /path/to/config/file\n\nFor developers\n--------------\nStarting from version 0.9.0 the event system has changed from louie/dispatcher\nto EventDispatcher (external dependency). Here are the most important changes:\n\n    - The new event system is not a global dispatcher anymore\n    - All the signal/receivers are connected between them only if it is\n      necessary.\n    - We don\'t connect/disconnect anymore, instead we will bind/unbind.\n    - The events has been renamed (this is necessary because the old event\n      names contains dots in his names, and this could cause troubles with the\n      new event system)\n\nPlease, check the documentation for further details at\n`"The events system" <https://opacam.github.io/Cohen3/events.html>`_ section.\n\nContributing\n------------\nReport bugs at https://github.com/opacam/Cohen3/issues\n\nFeel free to fetch the repo and send your\n`pull requests! <https://github.com/opacam/Cohen3/pulls>`_\n',
    'author': 'opacam',
    'author_email': 'canellestudi@gmail.com',
    'maintainer': 'opacam',
    'maintainer_email': 'canellestudi@gmail.com',
    'url': 'https://github.com/opacam/Cohen3/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
