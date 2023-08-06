import setuptools

long_description = '''
This is a personalized dashboard for stock trading,
focusing primarily on showing metrics and portfolio
health for long-term investors. Derivatives, options,
futures are not emphasized here, nor is their trading
and tracking supported much.
This package uses Python 3.7 and support is not 
guaranteed for other versions.
'''
setuptools.setup(
    name="Sestertii",
    version="0.0.7",
    author="Harish Kumar",
    author_email="harishk1908@gmail.com",
    description="A personalized stock trading dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harishk1908/sestertii",
    packages=setuptools.find_packages(),
    install_requires=['numpy==1.18.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
