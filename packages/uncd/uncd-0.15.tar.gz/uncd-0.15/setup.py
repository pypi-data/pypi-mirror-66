from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='uncd',
    version='0.15',
    packages=find_packages(),
    install_requires=[
        'Click', 'requests', 'BeautifulSoup4', 'lxml'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points='''
        [console_scripts]
        uncd=uncd.__init__:cli
    ''',
    author='hpencilb',
    author_email='haemoglob.j.ben@gmail.com',
    license='MIT Licence',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
