import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="QcureUi",
    version="0.0.2",
    author="Lux",
    author_email="1223411083@qq.com",
    description="Used for pyqt5 beautification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= [
        'pywin32'
    ],
    project_urls={
        'Blog': 'https://blog.csdn.net/qq_45414559/article/details/105560090',
    },
)
