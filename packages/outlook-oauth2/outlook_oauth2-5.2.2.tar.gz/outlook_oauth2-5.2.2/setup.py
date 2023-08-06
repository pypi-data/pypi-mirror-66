import setuptools

from pyOutlook import __release__

setuptools.setup(
    name='outlook_oauth2',
    version=__release__,
    packages=['outlook_oauth2', 'outlook_oauth2.internal', 'outlook_oauth2.core'],
    url='https://gitlab.com/alexbishop/pyOutlook',
    license='MIT',
    author='Alex Bishop',
    author_email='alexbishop1234@gmail.cpm',
    description='This is a fork of pyOutlook (https://pypi.python.org/pypi/pyOutlook). '
                'A Python module for connecting to the Outlook REST API, without the hassle of dealing with the '
                'JSON formatting for requests/responses and the REST endpoints and their varying requirements',
    install_requires=['requests', 'python-dateutil'],
    tests_require=['coverage', 'nose'],
    keywords='outlook office365 microsoft email',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Communications :: Email :: Email Clients (MUA)',
        'Topic :: Office/Business',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English'
    ]
)
