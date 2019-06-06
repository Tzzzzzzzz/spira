from spira.yevon.process.all import *
from spira.yevon.process import RULE_DECK_DATABASE as RDD

# --------------------------------- Metals --------------------------------------

RDD.GND = ParameterDatabase()

RDD.M1 = ParameterDatabase()
RDD.M1.MIN_SIZE = 0.35
RDD.M1.MAX_WIDTH = 1.5
RDD.M1.MIN_SURROUND_OF_C1 = 0.3

RDD.M2 = ParameterDatabase()
RDD.M2.WIDTH = 1.5

RDD.M3 = ParameterDatabase()
RDD.M3.WIDTH = 1.5

# --------------------------------- Vias ----------------------------------------

RDD.C1 = ParameterDatabase()
RDD.C1.WIDTH = 0.5
RDD.C1.M5_METAL = 1.0

RDD.C2 = ParameterDatabase()
RDD.C2.WIDTH = 0.5
RDD.C2.M5_METAL = 1.0

RDD.C3 = ParameterDatabase()
RDD.C3.WIDTH = 0.5
RDD.C3.M5_METAL = 1.0

# ------------------------------- Physical Metals -------------------------------

RDD.PLAYER.M0 = PhysicalLayerDatabase()
RDD.PLAYER.M1 = PhysicalLayerDatabase()
RDD.PLAYER.M2 = PhysicalLayerDatabase()
RDD.PLAYER.M3 = PhysicalLayerDatabase()
RDD.PLAYER.M4 = PhysicalLayerDatabase()
RDD.PLAYER.M5 = PhysicalLayerDatabase()
RDD.PLAYER.M6 = PhysicalLayerDatabase()
RDD.PLAYER.M7 = PhysicalLayerDatabase()

RDD.PLAYER.BBOX = PhysicalLayer(process=RDD.PROCESS.VIRTUAL, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.PORT = PhysicalLayer(process=RDD.PROCESS.VIRTUAL, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M0.GND = PhysicalLayer(process=RDD.PROCESS.GND, purpose=RDD.PURPOSE.GROUND)

RDD.PLAYER.M1.METAL = PhysicalLayer(name='M1', process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M1.HOLE = PhysicalLayer(name='M1_HOLE', process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M1.BBOX = PhysicalLayer(name='M1_BBOX', process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M1.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M1.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M1.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M2.METAL = PhysicalLayer(name='M2', process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M2.HOLE = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M2.BBOX = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M2.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M2.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M2.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M3.METAL = PhysicalLayer(name='M3', process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M3.HOLE = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M3.BBOX = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M3.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M3.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M3.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M4.METAL = PhysicalLayer(name='M4', process=RDD.PROCESS.M4, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M4.HOLE = PhysicalLayer(process=RDD.PROCESS.M4, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M4.BBOX = PhysicalLayer(process=RDD.PROCESS.M4, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M4.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M4, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M4.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M4, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M4.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M4, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M5.METAL = PhysicalLayer(name='M5', process=RDD.PROCESS.M5, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M5.HOLE = PhysicalLayer(process=RDD.PROCESS.M5, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M5.BBOX = PhysicalLayer(process=RDD.PROCESS.M5, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M5.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M5, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M5.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M5, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M5.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M5, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M6.METAL = PhysicalLayer(name='M6', process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M6.HOLE = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M6.BBOX = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M6.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M6.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M6.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M7.METAL = PhysicalLayer(name='M7', process=RDD.PROCESS.M7, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M7.HOLE = PhysicalLayer(process=RDD.PROCESS.M7, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M7.BBOX = PhysicalLayer(process=RDD.PROCESS.M7, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M7.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M7, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M7.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M7, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M7.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M7, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

# ------------------------------- Physical Vias ----------------------------------

RDD.PLAYER.C1 = PhysicalLayerDatabase()
RDD.PLAYER.C2 = PhysicalLayerDatabase()
RDD.PLAYER.C3 = PhysicalLayerDatabase()
RDD.PLAYER.J1 = PhysicalLayerDatabase()

RDD.PLAYER.J1.JUNCTION = PhysicalLayer(process=RDD.PROCESS.J1, purpose=RDD.PURPOSE.JUNCTION)
RDD.PLAYER.C1.VIA = PhysicalLayer(process=RDD.PROCESS.C1, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.C2.VIA = PhysicalLayer(process=RDD.PROCESS.C2, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.C3.VIA = PhysicalLayer(process=RDD.PROCESS.C3, purpose=RDD.PURPOSE.VIA)

# ------------------------------ Map GDSII Layers -------------------------------

RDD.GDSII.PROCESS_LAYER_MAP = {
    RDD.PROCESS.VIRTUAL : 199,
    RDD.PROCESS.GND : 0,
    RDD.PROCESS.M1 : 1,
    RDD.PROCESS.M2 : 2,
    RDD.PROCESS.M3 : 3,
    RDD.PROCESS.M4 : 4,
    RDD.PROCESS.M5 : 5,
    RDD.PROCESS.M6 : 6,
    RDD.PROCESS.M7 : 7,
    RDD.PROCESS.C1 : 10,
    RDD.PROCESS.C2 : 20,
    RDD.PROCESS.C3 : 30,
    RDD.PROCESS.SKY : 99,
}

RDD.GDSII.PURPOSE_DATATYPE_MAP = {
    RDD.PURPOSE.GROUND : 0,
    RDD.PURPOSE.METAL : 1,
    RDD.PURPOSE.SKY : 3,
    RDD.PURPOSE.HOLE : 4,
    RDD.PURPOSE.BOUNDARY_BOX : 5,
    RDD.PURPOSE.PORT.DIRECTION : 6,
    RDD.PURPOSE.PORT.EDGE_ENABLED : 7,
    RDD.PURPOSE.PORT.EDGE_DISABLED : 8,
    RDD.PURPOSE.VIA : 9,
    RDD.PURPOSE.JUNCTION : 10,
    RDD.PURPOSE.ROUTE : 11,
    RDD.PURPOSE.INTERSECTED : 12,
    RDD.PURPOSE.UNION : 13,
    RDD.PURPOSE.DIFFERENCE : 14,
    RDD.PURPOSE.TEXT : 64,
}

RDD.GDSII.EXPORT_LAYER_MAP = MapPhysicalToGdsii(
    process_layer_map=RDD.GDSII.PROCESS_LAYER_MAP,
    purpose_datatype_map=RDD.GDSII.PURPOSE_DATATYPE_MAP
)

RDD.GDSII.IMPORT_LAYER_MAP = MapGdsiiToPhysical(
    process_layer_map=RDD.GDSII.PROCESS_LAYER_MAP,
    purpose_datatype_map=RDD.GDSII.PURPOSE_DATATYPE_MAP
)

# ------------------------------------- Virtual Modelling ----------------------------------------------

# from spira.yevon.vmodel.process_flow import VModelProcessFlow

RDD.VMODEL = PhysicalLayerDatabase()

RDD.VMODEL.PROCESS_FLOW = VModelProcessFlow(
    active_processes=[RDD.PROCESS.M1, RDD.PROCESS.M2, RDD.PROCESS.M3]
)

# ------------------------------------- Net FIlters ----------------------------------------------

# f = ToggledCompoundFilter()

# RDD.NETS.FILTER = 


# RDD.NETS = NetDatabase()
