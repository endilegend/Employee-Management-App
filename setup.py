"""
This is a setup.py script generated for packaging the EMS application
"""

from setuptools import setup

APP = ['ems.py']
DATA_FILES = [
    ('', ['icon.jpg', 'clwbeach.jpg']),
    ('', ['database.sql']),
    ('', ['employee.ui']),
    ('', ['lebron.mp4', 'wrong.mp4', 'chaching.mp4'])
]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'packages': ['PyQt5'],
    'includes': [
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'mysql.connector',
        'pkg_resources',
        'packaging',
        'platformdirs',
        'jaraco.text',
        'jaraco.functools',
        'jaraco.context',
        'more_itertools',
        'autocommand'
    ],
    'excludes': ['tkinter'],
    'plist': {
        'CFBundleName': 'EMS',
        'CFBundleDisplayName': 'EMS',
        'CFBundleExecutable': 'EMS',
        'CFBundleIdentifier': 'com.ems.app',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSPrincipalClass': 'NSApplication',
        'LSMinimumSystemVersion': '10.10',
        'NSHumanReadableCopyright': 'Copyright © 2024, All Rights Reserved'
    }
}

setup(
    app=APP,
    name='EMS',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 