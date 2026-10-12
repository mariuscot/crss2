from dataclasses import dataclass
from enum import Enum


LEVELS = ("L1", "L2", "L3", "L4")


class Goals(Enum):
    ANT = ("ANT", 0)
    WITH = ("WITH", 1)
    REC = ("REC", 2)
    ADPT = ("ADPT", 3)


class Layers(Enum):
    HW = ("HW", 0)
    FW = ("FW", 1)
    NETW = ("NETW", 2)
    APPL = ("APPL", 3)


@dataclass
class ResNode:
    id: int
    #tupple
    layer: Layers
    goal: Goals
    # component identification
    compId: int
    compType: int | str
    # ids of nodes that current node depends on
#    dependencies: int[]  
    direction : int
    resilienceValue : float
    realizedImpact : float  # Fraction of the initial resilience lost, in [0, 1].
    # denoted participation to resilience formation
    participating : bool
    mop : float = 0.0 # measure fo protection for the particular node