
SETUP_INFO = dict(
    name = 'agile_item_master',
    version = '2.post6',
    author = 'Lilach',
    author_email = 'lelvi@infinidat.com',

    url = 'https://git.infinidat.com/support/agile-item-master',
    license = 'BSD',
    description = """agile item master""",
    long_description = """agile item master""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'docopt',
'infi.credentials_store',
'infi.pyutils',
'python-dateutil',
'requests',
'setuptools',
'unicodecsv'
],
    namespace_packages = [],

    package_dir = {'': 'src'},
    package_data = {'': [
'AgileAPI.jar'
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [
'agile = agile_item_master.agile:main',
'sku-generator = agile_item_master.sku_generator:main',
'workato = agile_item_master.workato:main'
],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

