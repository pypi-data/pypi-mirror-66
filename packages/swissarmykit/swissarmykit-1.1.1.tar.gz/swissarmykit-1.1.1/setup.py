import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swissarmykit",
    version="1.1.1",
    author="Will Nguyen",
    author_email="will.ng.nguyen@gmail.com",
    description="Swiss Army Kit package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/swissarmykit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fake_useragent',
        'openpyxl',
        'peewee',
        'requests',
        'scrapy',
        'selenium',
        'us',
        'usaddress',
        'Pillow',
        'json-cfg',
        'tablib',
        'redis',
        'brotli',
        'scikit-image',
        'texttable',
        'wordcloud',
        'nltk',
        'validate_email',
        'mongoengine',
        'tika',
        'wget',
    ]
)
