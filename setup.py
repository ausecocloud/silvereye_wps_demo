from setuptools import setup, find_packages

version = '0.1'

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
install_requires = [
    'setuptools',
    'paste',
    'numpy',
    'pydap',
    'pyramid',
    'pywps',
    'python-swiftclient',
    'python-keystoneclient',
    'pyramid_chameleon',
    'waitress',
]

# List of dependencies installed via `pip install -r ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
]

setup(
    name='silvereye_wps_demo',
    version=version,
    description="Silvereye WPS demo services",
    long_description=(open("README.md").read() + "\n\n" +
                      open("HISTORY.rst").read()),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Apache Software License"
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        'Topic :: Scientific/Engineering :: GIS'
    ],
    keywords='ogc wps pyramid',
    author='',
    author_email='',
    maintainer='',
    maintainer_email='',
    url='https://github.com/ausecocloud/silvereye_wps_demo',
    license='Apache License 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'paste.app_factory': [
            'main = silvereye_wps_demo:main',
        ],
        'pywps_processing': [
            'threads = silvereye_wps_demo.pywps.processing:ThreadProcessing',
        ],
        'pywps_storage': [
            'SwiftStorage = silvereye_wps_demo.pywps.swiftstorage:SwiftStorage',
        ]
    },
    extras_require={
        'dev': dev_requires,
    }

)
