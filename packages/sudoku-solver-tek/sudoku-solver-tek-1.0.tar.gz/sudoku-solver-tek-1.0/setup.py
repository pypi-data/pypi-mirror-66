import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sudoku-solver-tek',
    version='1.0',
    scripts=['sudoku-solver'],
    author="Tralah M Brian",
    author_email="musyoki.brian@tralahtek.com",
    description="Sudoku puzzle solver program",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/TralahM/sudoku-solver",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
