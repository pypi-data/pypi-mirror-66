# cython: language_level=3
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
#python setup_cython.py build_ext --inplace
#进行速度检查：cython agent.pyx -a。注意要先进入python3的虚拟环境才能进行！

extensions = [
    Extension(
        "takagiabm.agents.agent",["takagiabm/agents/agent.pyx"]
    ),
    Extension(
        "takagiabm.containers.grid",["takagiabm/containers/grid.pyx"]
    ),
    Extension(
        "takagiabm.toolbox.kinematics", ["takagiabm/toolbox/kinematics.pyx"]
    ),
    Extension(
        "takagiabm.toolbox.taktimecounter", ["takagiabm/toolbox/taktimecounter.pyx"]
    ),
    # Extension(
    #     "takagiabm.models.model", ["takagiabm/models/model.pyx"]
    # ),
    Extension(
        "takagiabm.toolbox.typeutils", ["takagiabm/toolbox/typeutils.pyx"]
    )

]

setup(
    name = "takagiabm1",
    ext_modules=cythonize(extensions),
)