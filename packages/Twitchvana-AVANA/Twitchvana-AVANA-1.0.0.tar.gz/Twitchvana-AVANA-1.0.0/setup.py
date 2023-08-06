import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name="Twitchvana-AVANA", # Replace with your own username
    version="1.0.0",
    author="Avana",
    author_email="avana.artz@gmail.com",
    description="Twitchvana for Twitch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
)