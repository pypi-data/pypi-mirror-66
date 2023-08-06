import setuptools
from OpticsLab import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpticsLab", 
    version=__version__,
    author="Abdulaziz Alqasem",
    author_email="OpticsLab.py@gmail.com",
    description="Simulate Optics Physics Experements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://azizalqasem.github.io/OpticsLab/index.html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",    
    ],
    python_requires='>=3.4',
    keywords=('OpticsLab', 'math', 'Optics', 'Laser', "Ultrafst Optics"
              'physics', 'Science', 'Engineering', 'Scientific Research'),
    
    project_urls={
    'Documentation': 'https://azizalqasem.github.io/OpticsLab/index.html',
    'Source': 'https://github.com/AzizAlqasem/OpticsLab'},
    install_requires=['numpy', 'FormulaLab'],
)

#packages=find_packages(include=['OpticsLab', 'OpticsLab.*'], exclude = []),

"""
Reference:
# Naming versions conventions
1.2.0.dev1  # Development release
1.2.0a1     # Alpha Release
1.2.0b1     # Beta Release
1.2.0rc1    # Release Candidate
1.2.0       # Final Release
1.2.0.post1 # Post Release
15.10       # Date based release
23          # Serial release

# Increment version convention
MAJOR version when they make incompatible API changes,
MINOR version when they add functionality in a backwards-compatible manner, and
MAINTENANCE version when they make backwards-compatible bug fixes.
"""
