from setuptools import setup

setup(
    name='file-processor',
    version='1.0',
    py_modules=['processor'],
    install_requires=[
        'click',
        'numpy',
        'pandas',
    ],
    entry_points='''
        [console_scripts]
        processor=processor:cli
    ''',
)
