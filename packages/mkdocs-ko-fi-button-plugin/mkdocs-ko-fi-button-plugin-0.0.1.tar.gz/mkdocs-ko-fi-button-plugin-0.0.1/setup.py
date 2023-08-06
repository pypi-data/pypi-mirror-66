from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-ko-fi-button-plugin',
    version='0.0.1',
    packages=find_packages(),
    url='https://gitlab.com/berghton/mkdocs-ko-fi-button-plugin',
    license='MIT',
    author='Tony Bergh',
    author_email='tony.bergh@gmail.com',
    description="Ko-fi button is a simple plugin that let's you add a Ko-fi button with markdown.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    entry_points={
        'mkdocs.plugins': [
            'ko-fi-button = mkdocs_ko_fi_button_plugin.mkdocs_ko_fi_button_plugin:KofiButtonPlugin'
        ]
    },
)

