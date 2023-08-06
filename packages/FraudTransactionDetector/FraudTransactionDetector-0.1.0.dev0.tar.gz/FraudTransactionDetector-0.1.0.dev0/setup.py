from setuptools import setup

setup(
    name='FraudTransactionDetector',
    version='0.1.0dev',
    author='Venkata Siva Rama Sastry Kavuri',
    author_email='sivaram.kavuri@gmail.com',
    packages=['fraudtransactiondetector',],
    scripts=['bin/sample-fraud-identifier.py',],
    url='http://pypi.python.org/pypi/FraudTransactionDetector/',
    license='License.txt',
    description='Scalable Fraud Transaction Identifier using Clustering, Anamoly Detection and Classification ML Algorithms',
    long_description=open('README.txt').read(),
    install_requires=[
        "h2o == 3.30.0.1",
        "pandas == 0.25.1",
        "numpy == 1.16.5",
        "matplotlib == 3.1.3",
        "sklearn == 0.21.3",
    ],
)
