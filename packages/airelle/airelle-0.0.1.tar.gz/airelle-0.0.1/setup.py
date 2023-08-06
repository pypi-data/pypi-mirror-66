import setuptools

setuptools.setup(
    name="airelle",
    packages=setuptools.find_packages(),
    description="The Pytorch Reinforcement Learning toolkit "
    "- Algorithms, Best-Practices and Baselines",
    author="Facebook Artificial Intelligence Research",
    url="https://github.com/facebookresearch/airelle",
    version="0.0.1",
    python_requires=">=3.7",
    keywords=["deep learning", "pytorch", "reinforcement learning"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
