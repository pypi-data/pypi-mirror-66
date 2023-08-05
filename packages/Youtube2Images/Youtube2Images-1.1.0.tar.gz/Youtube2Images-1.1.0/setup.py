import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Youtube2Images", # Replace with your own username
    version="1.1.0",
    author="Falah.G.Saleh",
    author_email="falahgs07@gmail.com",
    description="Python Package to Convert youtube vieo to images frames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://iraqprogrammer.wordpress.com/",
    packages=["Youtube2Images"],
	keywords = ['yuotube', 'images', 'dataset images'],
	install_requires=[            # I get to this in a second
          'pytube3',
          'opencv-python',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)