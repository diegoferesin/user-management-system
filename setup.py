from setuptools import setup, find_packages

setup(
    name="user-management-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-decouple==3.8",
        "python-dotenv==1.0.0",
        "colorama==0.4.6",
        "pytest==7.4.3"
    ],
) 