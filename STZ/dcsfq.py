import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.process import get_rule_deck

RDD = get_rule_deck()

class Jj(spira.Cell):

    def create_elements(self, elems):
        
        elems += spira.Circle(layer=RDD.PLAYER.C1.VIA,box_size=(4.00, 4.00),center=(77.5,63.5))#box_size中的是直径,发现center()并不能改变圆心坐标，仍是（0，0）
        elems += spira.Circle(layer=RDD.PLAYER.C2.VIA,box_size=(5.00, 5.00),center=(77.5,63.5))
        elems += spira.Circle(layer=RDD.PLAYER.C3.VIA,box_size=(2.00, 2.00),center=(77.5,63.5))
        #elems += spira.Circle(layer=RDD.PLAYER.C3.VIA,box_size=(1.00, 1.00))
        return elems

class NAN(spira.Cell): 
     def create_elements(self, elems):
        elems += spira.Rectangle(p1=(73.5,48.0), p2=(81.5, 67.5), layer=RDD.PLAYER.M1.METAL)
        return elems

class BE(spira.Cell):
    def create_elements(self,elems):
        elems += spira.Rectangle(p1=(74.5,59.0), p2=(80.5, 66.5), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(74.5,49.0), p2=(80.5, 52.0), layer=RDD.PLAYER.M2.METAL)
        return elems

class VI(spira.Cell):
    def create_elements(self,elems):
        elems += spira.Rectangle(p1=(76.5,59.5), p2=(78.5, 60.5), layer=RDD.PLAYER.C3.VIA)
        elems += spira.Rectangle(p1=(76.5,50.0), p2=(78.5, 51.0), layer=RDD.PLAYER.C3.VIA)
        return elems

class RES(spira.Cell):
    def create_elements(self,elems):
        elems += spira.Rectangle(p1=(76.5,53.0), p2=(78.5, 58.0), layer=RDD.PLAYER.R1.METAL)
        return elems

class Junction2(spira.Cell):
    """Josephson junction 2. """

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((77.5, 63.5))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.SRef(alias='nan', reference=NAN(), transformation=t1)
        elems += spira.SRef(alias='be', reference=BE(), transformation=t1)
        elems += spira.SRef(alias='vi', reference=VI(), transformation=t1)
        elems += spira.SRef(alias='res', reference=RES(), transformation=t1)
        elems += spira.SRef(alias='jj', reference=Jj(), transformation=t2)
        return elems

class Junction1(spira.Cell):
    """ Josephson junction 2. """

    def get_transforms(self):
        t1 = spira.Translation((-13, 0))
        t2 = spira.Translation((64.5, 63.5))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.SRef(alias='nan', reference=NAN(), transformation=t1)
        elems += spira.Rectangle(p1=(52.0,61.0), p2=(60.5, 66.0), layer=RDD.PLAYER.M1.METAL)
        elems += spira.SRef(alias='be', reference=BE(), transformation=t1)
        elems += spira.Rectangle(p1=(52.5,61.5), p2=(61.5, 65.5), layer=RDD.PLAYER.M2.METAL)
        #elems += spira.SRef(alias='vi', reference=VI(), transformation=t1)
        elems += spira.Rectangle(p1=(54.0,62.5), p2=(55.0, 64.5), layer=RDD.PLAYER.C3.VIA)
        elems += spira.Rectangle(p1=(63.5,50.0), p2=(65.5, 51.0), layer=RDD.PLAYER.C3.VIA)


        elems += spira.SRef(alias='res', reference=RES(), transformation=t1)
        elems += spira.SRef(alias='jj', reference=Jj(), transformation=t2)
        return elems

class WR(spira.Cell):
    def create_elements(self,elems):
        elems += spira.Rectangle(p1=(48.0,62.0), p2=(55.5, 65.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(61.0,57.0), p2=(68.0, 67.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(61.0,48.5), p2=(68.0, 54.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(68.0,61.5), p2=(74.0, 65.5), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(74.0,57.0), p2=(81.0, 67.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(74.0,48.5), p2=(81.0, 54.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(81.0,61.5), p2=(98.0, 65.5), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(98.0,57.0), p2=(105.0, 67.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(98.0,48.5), p2=(105.0, 54.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(100.5,67.0), p2=(102.5, 92.5), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(98.0,92.5), p2=(102.5, 96.5), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(48.0,87.0), p2=(55.5, 97.0), layer=RDD.PLAYER.M4.METAL)
        elems += spira.Rectangle(p1=(80.0,87.5), p2=(84.5, 91.5), layer=RDD.PLAYER.M4.METAL)
        shape = spira.Shape(points=[(63.5,67.0),(65.5,67.0),(65.5,82.5),(84.5,82.5),(84.5,87.5),(82.5,87.5),(82.5,84.5),(63.5,84.5)])
        elems += spira.Polygon(layer=RDD.PLAYER.M4.METAL,shape=shape)
        return elems

class DCSFQ(spira.Cell):
    """DC/SFQ 1.0. """

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((24.0, 0))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.SRef(alias='JJ1', reference=Junction1(), transformation=t1)
        elems += spira.SRef(alias='JJ2', reference=Junction2(), transformation=t1)
        elems += spira.SRef(alias='JJ3', reference=Junction2(), transformation=t2)
        elems += spira.SRef(alias='WIR', reference=WR(), transformation=t1)
        elems += spira.Rectangle(p1=(54.5,88.5), p2=(81.0, 90.5), layer=RDD.PLAYER.R1.METAL)
        elems += spira.Rectangle(p1=(54.5,93.5), p2=(99.0, 95.5), layer=RDD.PLAYER.R1.METAL)
        
        return elems


if __name__ == '__main__':
    D=DCSFQ()


    D.gdsii_output(file_name='dcsfq')