from pandas.plotting import register_matplotlib_converters
import matplotlib as mpl
from adcircpy.mesh import (
    AdcircMesh,
    )
from adcircpy.model import (
    AdcircRun,
    TidalForcing,
    )
from adcircpy.model.winds import (
    BestTrackForcing,
    OwiForcing
    )
from adcircpy.server import (
    ServerConfig,
    SlurmConfig,
    )

__all__ = [
    "AdcircMesh",
    "AdcircRun",
    "TidalForcing",
    "BestTrackForcing",
    "OwiForcing",
    "ServerConfig",
    "SlurmConfig"
]

mpl.rcParams['agg.path.chunksize'] = 10000
register_matplotlib_converters()


try:
    import colored_traceback
    colored_traceback.add_hook(always=True)
except ModuleNotFoundError:
    pass
