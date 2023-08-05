from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pypowerprojects",
    version="1.1.5",
    description="A Python Library with 4 GUI Projects : Gmail, Captcha, TicTacToe Game and Currency Conversion",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tirth-2001/ttt.git",
    author="PyPower Projects",
    author_email="projectspypower@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pypowerprojects"],
    include_package_data=True,
    install_requires=["pyttsx3","captcha","opencv-python","pillow","wget","forex-python"],
    entry_points={
        "console_scripts": [
            "pypowerprojects=lkj.call:currency",
        ]
   
    },
)