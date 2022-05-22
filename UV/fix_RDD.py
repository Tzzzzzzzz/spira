from spira.yevon.process.all import *
from spira.technologies.default import RDD

RDD.PROCESS.M0 = ProcessLayer(name='Metal 0', symbol='M0')

RDD.PLAYER.M0.METAL = PhysicalLayer(name='M0', process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M0.HOLE = PhysicalLayer(name='M0_HOLE', process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M0.BBOX = PhysicalLayer(name='M0_BBOX', process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M0.PORT_CONTACT = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.CONTACT)
RDD.PLAYER.M0.PORT_BRANCH = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.BRANCH)
RDD.PLAYER.M0.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M0.PORT_PIN = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.PIN)
RDD.PLAYER.M0.PORT_DUMMY = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.DUMMY)
RDD.PLAYER.M0.INSIDE_EDGE_ENABLED = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED)
RDD.PLAYER.M0.INSIDE_EDGE_DISABLED = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED)
RDD.PLAYER.M0.OUTSIDE_EDGE_ENABLED = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED)
RDD.PLAYER.M0.OUTSIDE_EDGE_DISABLED = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)
# RDD.PLAYER.M0.EDGE_INSIDE = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.INSIDE)
# RDD.PLAYER.M0.EDGE_OUTSIDE = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.OUTSIDE)

RDD.PLAYER.M4.GND = PhysicalLayer(process=RDD.PROCESS.GND, purpose=RDD.PURPOSE.GROUND)

RDD.PROCESS.I0 = ProcessLayer(name='VIA 0', symbol='I0')
RDD.PROCESS.I1 = ProcessLayer(name='VIA 1', symbol='I1')
RDD.PROCESS.I2 = ProcessLayer(name='VIA 2', symbol='I2')
RDD.PROCESS.I3 = ProcessLayer(name='VIA 3', symbol='I3')
RDD.PROCESS.I4 = ProcessLayer(name='VIA 4', symbol='I4')
RDD.PROCESS.I5 = ProcessLayer(name='VIA 5', symbol='I5')
RDD.PROCESS.I6 = ProcessLayer(name='VIA 6', symbol='I6')
RDD.PROCESS.I7 = ProcessLayer(name='VIA 7', symbol='I7')
RDD.PROCESS.C5R = ProcessLayer(name='Resistor Metal 5', symbol='C5R')
RDD.PROCESS.C5J = ProcessLayer(name='Junction 5', symbol='C5R')
RDD.PROCESS.IXPORT = ProcessLayer(name='IXPORT 1', symbol='IXPORT')
RDD.PROCESS.J5 = ProcessLayer(name='Junction 5', symbol='J5')
RDD.PROCESS.R5 = ProcessLayer(name='Resistor Metal 5', symbol='R5')

RDD.PURPOSE.DEVICE_METAL = ProcessLayer(name='DEVICE_METAL 1', symbol='DEVICE_METAL')
RDD.PURPOSE.CIRCUIT_METAL = ProcessLayer(name='CIRCUIT_METAL 1', symbol='CIRCUIT_METAL')

RDD.PLAYER.I0 = PhysicalLayerDatabase()
RDD.PLAYER.I1 = PhysicalLayerDatabase()
RDD.PLAYER.I2 = PhysicalLayerDatabase()
RDD.PLAYER.I3 = PhysicalLayerDatabase()
RDD.PLAYER.I4 = PhysicalLayerDatabase()
RDD.PLAYER.I5 = PhysicalLayerDatabase()
RDD.PLAYER.I6 = PhysicalLayerDatabase()
RDD.PLAYER.I7 = PhysicalLayerDatabase()
RDD.PLAYER.C5R = PhysicalLayerDatabase()
RDD.PLAYER.C5J = PhysicalLayerDatabase()
RDD.PLAYER.J5 = PhysicalLayerDatabase()
RDD.PLAYER.R5 = PhysicalLayerDatabase()


RDD.PLAYER.I0.VIA = PhysicalLayer(process=RDD.PROCESS.I0, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I1.VIA = PhysicalLayer(process=RDD.PROCESS.I1, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I2.VIA = PhysicalLayer(process=RDD.PROCESS.I2, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I3.VIA = PhysicalLayer(process=RDD.PROCESS.I3, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I4.VIA = PhysicalLayer(process=RDD.PROCESS.I4, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I5.VIA = PhysicalLayer(process=RDD.PROCESS.I5, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I6.VIA = PhysicalLayer(process=RDD.PROCESS.I6, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.I7.VIA = PhysicalLayer(process=RDD.PROCESS.I7, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.C5R.VIA = PhysicalLayer(process=RDD.PROCESS.C5R, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.C5J.VIA = PhysicalLayer(process=RDD.PROCESS.C5J, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.IXPORT = PhysicalLayer(process=RDD.PROCESS.IXPORT, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.J5.JUNCTION = PhysicalLayer(process=RDD.PROCESS.J5, purpose=RDD.PURPOSE.JUNCTION)
RDD.PLAYER.R5.METAL = PhysicalLayer(process=RDD.PROCESS.R5, purpose=RDD.PURPOSE.METAL)

RDD.GDSII.PROCESS_LAYER_MAP.update({
    # RDD.PROCESS.VIRTUAL : 199,
    # RDD.PROCESS.GND : 0,
    # RDD.PROCESS.M1 : 1,
    # RDD.PROCESS.M2 : 2,
    # RDD.PROCESS.M3 : 3,
    # RDD.PROCESS.M4 : 4,
    # RDD.PROCESS.M5 : 5,
    # RDD.PROCESS.M6 : 6,
    # RDD.PROCESS.M7 : 7,
    # RDD.PROCESS.R1 : 8,
    # RDD.PROCESS.C1 : 10,
    # RDD.PROCESS.C2 : 20,
    # RDD.PROCESS.C3 : 30,
    # RDD.PROCESS.SKY : 99,

    RDD.PROCESS.I0 : 95,
    RDD.PROCESS.I1 : 81,
    RDD.PROCESS.I2 : 82,
    RDD.PROCESS.I3 : 83,
    RDD.PROCESS.I4 : 84,
    RDD.PROCESS.I5 : 85,
    RDD.PROCESS.I6 : 86,
    RDD.PROCESS.I7 : 87,

    RDD.PROCESS.C5R : 91,
    RDD.PROCESS.C5J : 92,
    RDD.PROCESS.IXPORT : 93,
    RDD.PROCESS.J5 : 94,
    RDD.PROCESS.R5 : 96,
    RDD.PROCESS.M0 : 97,
})