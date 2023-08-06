import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='twilioSMS',
    version='1.1b1',
    description='a fun texting app',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["twilioSMS"],
    package_dir={'': 'src'},
    keywords=["twilioSMS", "twilio"],
    setup_requires=['wheel'],
    install_requires=[
        'twilio>=6.38.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
