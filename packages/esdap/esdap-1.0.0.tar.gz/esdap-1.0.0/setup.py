import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="esdap",
    version="1.0.0",
    description="Epileptic Seizure Detection and Prediction from EEG data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/idupanloup/ESDaP",
    author="Isabelle Dupanloup",
    author_email="isabelle.dupanloup@sib.swiss",
    license="GNU General Public License v3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["esdap"],
    include_package_data=True,
    install_requires=["mne", "networkx", "networkx","numba","pywavelets","tensorflow","joblib","scikit-learn","xgboost"],
    scripts=['examples/run_compute_features.sh']
)

