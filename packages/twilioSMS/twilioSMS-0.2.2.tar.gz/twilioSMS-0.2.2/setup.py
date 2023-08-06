import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='twilioSMS',
    version='0.2.2',
    description='a fun texting app',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["sms"],
    package_dir={'': 'src'},
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
