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
    'packages': ['PyQt5', 'mysql.connector'],
    'includes': [
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'mysql.connector',
        'jaraco.text',
        'jaraco.functools',
        'jaraco.context',
        'more_itertools',
        'autocommand',
        'pkg_resources'
    ],
    'iconfile': 'icon.jpg',
    'plist': {
        'CFBundleName': 'EMS',
        'CFBundleDisplayName': 'Employee Management System',
        'CFBundleGetInfoString': "Employee Management System",
        'CFBundleIdentifier': "com.ems.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'NSHumanReadableCopyright': "Copyright © 2024, All Rights Reserved"
    }
}

setup(
    app=APP,
    name='EMS',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'PyQt5',
        'mysql-connector-python',
        'jaraco.text',
        'jaraco.functools',
        'jaraco.context',
        'more_itertools',
        'autocommand'
    ]
) 