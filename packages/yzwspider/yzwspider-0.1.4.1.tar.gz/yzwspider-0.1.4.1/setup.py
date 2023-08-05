import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
   
setuptools.setup(
    name="yzwspider",
    version="0.1.4.1",
    author="Hthing",
    author_email="hxcnly@gmail.com",
    description="A web spider for Chinese graduate student examination catalogue.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hthing/yzw/tree/master/",
    license = "MIT Licence",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = ["xlwt", 'pymysql', 'scrapy'] ,
    package_data = {
        'yzwspider': [ 'scrapy.cfg'],
    },
)