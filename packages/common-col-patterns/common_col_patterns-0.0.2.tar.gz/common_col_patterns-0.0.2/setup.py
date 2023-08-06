from distutils.core import setup

setup(
    name='common_col_patterns',
    packages=['common_col_patterns'],
    version='0.0.2',
    license='MIT',
    description='Some functional and collection patterns',
    author='Lev Gourevitch',
    author_email='lev.gourevitch@gmail.com',
    url='https://github.com/levgou/common_col_patters',
    download_url='https://github.com/levgou/common_col_patters/archive/head.tar.gz',
    keywords=['functional', 'collection', 'common'],
    install_requires=[
        'funcy',
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Utilities',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
