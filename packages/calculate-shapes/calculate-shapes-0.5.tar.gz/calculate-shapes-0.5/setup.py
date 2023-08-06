import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='calculate-shapes',  
    version='0.5',
    author="Deepesh Ahuja",
    author_email="deepeshahuja141291@gmail.com",
    description="Geometry Calculation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'Click',
    ],
    packages=[
        'calculator',
        'TwoD',
        'ThreeD'
    ],
    entry_points={
       'console_scripts': [
           'calculate=calculator.calculate:main'
       ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )