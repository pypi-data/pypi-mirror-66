import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='twilioSMS',
    version='0.0.1',
    description='twilio package required (https://pypi.org/project/twilio/), credit goes to cleverprogrammer, who made the code that I added a GUI to',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["send_sms", "credentials"],
    package_dir={'': 'src'},
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
