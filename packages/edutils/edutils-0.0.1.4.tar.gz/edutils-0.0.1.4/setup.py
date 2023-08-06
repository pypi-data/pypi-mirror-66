import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edutils",
    version="0.0.1.4",
    author="endlessday3",
    author_email="endlessday3@qq.com",
    description="A small utils for Personal use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",  # 项目地址
    packages=setuptools.find_packages(),  # 包含的包，可以多个，这是一个列表
    # packages="edutils",
    install_requires=[  # 模块所依赖的python模块
        "pymysql",
    ],
    classifiers=[  # 详细定义参考PyPI Classifiers 这里有这3行就够了
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)