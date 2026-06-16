from setuptools import setup
from setuptools.dist import Distribution

class BinDist(Distribution):
    def has_ext_modules(self):
        return super().has_ext_modules()
    
setup(distclass=BinDist)