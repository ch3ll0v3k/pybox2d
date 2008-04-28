#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlepages.com)
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from pygame.locals import *
import test_main
from test_main import box2d
from test_main import fwContactTypes

class SensorTest (test_main.Framework):
    name="SensorTest"
    m_sensor=None
    def __init__(self):
        super(SensorTest, self).__init__()
        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, -10.0)

        ground = self.world.CreateBody(bd) 

        sd=box2d.b2PolygonDef() 
        sd.userData = -2
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)

        cd=box2d.b2CircleDef() 
        cd.isSensor = True
        cd.radius = 5.0
        cd.localPosition.Set(0.0, 20.0)
        cd.userData = -1
        self.m_sensor = ground.CreateShape(cd)

        sd=box2d.b2CircleDef() 
        sd.radius = 1.0
        sd.density = 1.0

        for i in range(7):
            bd=box2d.b2BodyDef() 
            bd.position.Set(-10.0 + 3.0 * i, 20.0)
            
            sd.userData = i
            body = self.world.CreateBody(bd) 

            body.CreateShape(sd)
            body.SetMassFromShapes()

    def Step(self, settings) :
        # Traverse the contact results. Apply a force on shapes
        # that overlap the sensor.
        for point in self.points:
            if (point.state == fwContactTypes.contactPersisted):
                continue
            
            shape1=point.shape1
            shape2=point.shape2
            other=None
            
            # Regular pointer comparisons don't work, so we use the userData here in Python.
            if (shape1.GetUserData() == -1):
                other = shape2.GetBody()
            elif (shape2.GetUserData() == -1):
                other = shape1.GetBody()
            else:
                continue

            ground = self.m_sensor.GetBody()
            circle = self.m_sensor.getAsType()
            center = ground.GetWorldPoint(circle.GetLocalPosition())

            d = center - point.position

            # Not in the bindings yet
            FLT_EPSILON = 1.192092896e-07
            if (d.LengthSquared() < FLT_EPSILON * FLT_EPSILON) :
                continue

            d.Normalize()
            F = 100.0 * d
            other.ApplyForce(F, point.position)

        super(SensorTest, self).Step(settings)


if __name__=="__main__":
     test_main.main(SensorTest)
