from setuptools import setup, find_packages


setup(
    name="COAsT",
    version="0.0.1.dev1",
    description="Coastal Ocean Assessment Tool",  # TODO
    url="https://www.bodc.ac.uk",  # TODO
    author="British Oceanographic Data Centre (BODC)",
    license="Put something here",  # TODO,

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Hydrology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="Put something here",  # TODO
    project_urls={"home": "https://www.bodc.ac.uk"},  # TODO
    install_requires=[],  # TODO
    python_requires=">=3",
    packages=find_packages("coast"),
    include_package_data=True
)
