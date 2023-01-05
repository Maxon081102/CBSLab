from distutils.core import setup, Extension
import numpy

dir = 'CExtension/'

module1 = Extension(
    dir + 'lightspeed',
    sources=[
        dir + 'lightspeed.c',
        dir + 'src/Algorithm.c',
        dir + 'src/Map.c',
        dir + 'src/Node.c',
        dir + 'src/Allocator.c',
        dir + 'src/PriorityQueue.c',
        dir + 'src/hashset.c',
        dir + 'src/vector.c'
    ],
    include_dirs=[
        dir + 'include',
        numpy.get_include()
    ]
)

setup(
    name='lightspped',
    version='1.0',
    description='Packed with super fast path finding algorithm',
    ext_modules=[module1]
)
