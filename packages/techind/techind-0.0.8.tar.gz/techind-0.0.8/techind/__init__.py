# Let users know if they're missing any of our hard dependencies
hard_dependencies = ["numpy"]
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append("{0}: {1}".format(dependency, str(e)))

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

from techind.doubleExponentialMovingAverage import (
    doubleExponentialMovingAverage as doubleExponentialMovingAverage,
)
from techind.exponentialMovingAverage import (
    exponentialMovingAverage as exponentialMovingAverage,
)
from techind.kaufmanAdaptiveMovingAverage import (
    kaufmanAdaptiveMovingAverage as kaufmanAdaptiveMovingAverage,
)
from techind.mesaAdaptiveMovingAverage import (
    mesaAdaptiveMovingAverage as mesaAdaptiveMovingAverage,
)
from techind.simpleMovingAverage import simpleMovingAverage as simpleMovingAverage
from techind.triangularMovingAverage import (
    triangularMovingAverage as triangularMovingAverage,
)
from techind.trippleExponentialMovingAverage import (
    trippleExponentialMovingAverage as trippleExponentialMovingAverage,
)
from techind.weightedMovingAverage import weightedMovingAverage as weightedMovingAverage
