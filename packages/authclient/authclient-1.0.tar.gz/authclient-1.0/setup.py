from setuptools import setup, find_packages


with open("README.rst") as description_file:
    setup(
        name="authclient",
        version="1.0",
        description="Simple authentication client",
        long_description=description_file.read(),
        packages=find_packages(),
        url="https://git.yurzs.dev/yurzs/authclient",
        install_requires=["aiohttp"],
    )
