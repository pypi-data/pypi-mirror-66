import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fraudtransaction_task",
    version="0.0.1dev",
    author="Srijith M",
    author_email="srijithm7@gmail.com",
    description="Technical task anamoly detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/srijithm7_bb/fraudtransactiondetection/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        "numpy == 1.18.3",
        "pandas == 1.0.3",
        "joblib == 0.14.1",
        "scipy == 1.4.1",
        "scikit-learn == 0.22.2.post1",
        "matplotlib == 3.2.1",
        "pandas_ods_reader == 0.0.7",
    ],
    python_requires='>=3.6',
)