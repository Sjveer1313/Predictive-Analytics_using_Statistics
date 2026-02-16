from setuptools import setup

setup(
    name="Topsis-Sukhmanpreet-102317112",
    version="1.1.0",
    description="A command line python package to implement TOPSIS",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Sukhmanpreet Singh",
    packages=["topsis_sukhmanpreet_102317112"],
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': [
            'topsis=topsis_sukhmanpreet_102317112.topsis:main',
        ],
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)