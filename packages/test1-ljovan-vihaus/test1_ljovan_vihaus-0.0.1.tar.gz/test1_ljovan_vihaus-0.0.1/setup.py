import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test1_ljovan_vihaus",
    version="0.0.1",
    author="vihaus & ljovan",
    author_email="stercus.cursus@pm.me",
    description="test of vihaus_ljovan_pckg",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
   'emoji',
   'nltk'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'tpp = cli.py:main'
        ]
    },
)    