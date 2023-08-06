import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='huetui',
    version='0.2',
    scripts=['huetui'],
    author="Channel 42",
    author_email="",
    description="A TUI for Philips Hue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channel-42/hue-tui",
    packages=setuptools.find_packages(),
    install_requires=['py-cui', 'hue-snek-channel42', 'Pillow', 'colormath'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
