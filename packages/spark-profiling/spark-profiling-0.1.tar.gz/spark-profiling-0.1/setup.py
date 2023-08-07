from setuptools import setup, find_packages

setup(
    name="spark-profiling",
    version="0.01",
    packages=["spark_profiling"],
    description="Generate profile report for spark DataFrame",
    python_requires=">=3.6",
    install_requires="requirements",
    classifiers=[
        "Topic :: Software Development :: Build Tools",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
    ],
    keywords="",
    long_description="To be released",
    long_description_content_type="text/markdown",
    options={"bdist_wheel": {"universal": True}},
)

