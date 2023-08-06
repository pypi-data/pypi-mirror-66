from distutils.core import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='redbanjo',
    packages=['redbanjo'],
    version='0.1.6',
    license='MIT',
    description='RedBanjo python bindings.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michael L. Gantz',
    author_email='gantzm@gantzgulch.com',
    url='https://www.gantzgulch.com',
    download_url='https://github.com/GantzGulch-RedBanjo/RedBanjoPythonClient/archive/v_0.1.tar.gz',
    keywords=['RedBanjo'],
    install_requires=[
        'validators',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
