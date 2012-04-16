# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys
import unittest


from balancer.storage.storage import *
from balancer.loadbalancers.loadbalancer import LoadBalancer
from openstack.common import exception
from balancer.devices.device import LBDevice
from balancer.loadbalancers.probe import DNSprobe

class StorageTestCase(unittest.TestCase):
    
    def test_device_save(self):
        device = LBDevice()
        device.id = 111
        device.name = "DeviceName001"
        device.type = "ACE"
        device.version = "1.0"
        device.requires_vip_ip = True
        device.has_acl = True
        device.supports_vlan = False
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.writeDevice(device)
        read  = stor.getReader()
        new_device = read.getDeviceById(111)
        self.assertEquals(new_device.name,  "DeviceName001")
        
    
    def test_lb_save(self):
        lb = LoadBalancer()
        lb.name  = "testLB"
        lb.id = 123
        lb.algorithm = "ROUND_ROBIN"
        lb.status = "ACTIVE"
        lb.created = "01-01-2012 11:22:33"
        lb.updated = "02-02-2012 11:22:33"
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.writeLoadBalancer(lb)
        read  = stor.getReader()
        newlb = read.getLoadBalancerById(123)
        self.assertEquals(newlb.name,  "testLB")
    
    def test_exception_on_nonexistent_lb(self):
        stor = Storage( {'db_path':'./db/testdb.db'})
        read  = stor.getReader()
        try:
            newlb = read.getLoadBalancerById(1234)
        except exception.NotFound:
            pass
        else:
            self.fail("No exception was raised for non-existent LB")
            
    def test_multiple_lb_select(self):
        lb = LoadBalancer()
        lb.name  = "testLB2"
        lb.id = 124
        lb.algorithm = "ROUND_ROBIN"
        lb.status = "ACTIVE"
        lb.created = "01-01-2012 11:22:33"
        lb.updated = "02-02-2012 11:22:33"
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.writeLoadBalancer(lb)
        lb.name  = "testLB3"
        lb.id = 125
        lb.algorithm = "ROUND_ROBIN"
        lb.status = "DOWN"
        lb.created = "01-01-2012 11:22:33"
        lb.updated = "02-02-2012 11:22:33"
        wr.writeLoadBalancer(lb)
        read  = stor.getReader()
        lb_list = read.getLoadBalancers()
        self.assertEquals(len(lb_list), 3)

    def test_probe_save(self):
        prb = DNSprobe()
        prb.name  = "testProbe"
        prb.type = 'DNSprobe'
        prb.id = '1234'
        prb.description = 'Test Probe'
        prb.probeInterval = '20'
        prb.isRouted = 'True'
        prb.passDetectInterval = '60'
        prb.receiveTimeout = '10'
        prb.port = '8080'
        prb.passDetectCount = '4'
        prb.failDetect = '6'
        prb.domainName = 'domainname'
        
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.writeProbe(prb)
        read  = stor.getReader()
        newprb = read.getProbeById(1234)
        self.assertEquals(prb.name,  "testProbe")
    
    def test_probe_update(self):
        prb = DNSprobe()
        prb.name  = "testProbe"
        prb.type = 'DNSprobe'
        prb.id = '1234'
        prb.description = 'Test Probe updated'
        prb.probeInterval = '20'
        prb.isRouted = 'False'
        prb.passDetectInterval = '60'
        prb.receiveTimeout = '10'
        prb.port = '443'
        prb.passDetectCount = '4'
        prb.failDetect = '6'
        prb.domainName = 'domainname'
        
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.updateObjectInTable(prb)
        read  = stor.getReader()
        newprb = read.getProbeById(1234)
        self.assertEquals(prb.name,  "testProbe")    

    def test_lb_update(self):
        lb = LoadBalancer()
        lb.name  = "testLB"
        lb.id = 123
        lb.algorithm = "ROUND_ROBIN"
        lb.status = "DOWN"
        lb.created = "01-01-2012 11:22:33"
        lb.updated = "02-04-2012 11:22:33"
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.updateObjectInTable(lb)
        read  = stor.getReader()
        newlb = read.getLoadBalancerById(123)
        self.assertEquals(newlb.name,  "testLB")

    def test_rserver_save(self):
        rs = RealServer()
        rs.id = 123
        rs.sf_id = 123
        rs.name = "testRS"
        rs.type = "Host"
        rs.webHostRedir = ""
        rs.redirectionCode = ""
        rs.ipType = "IPv4"
        rs.address = "10.10.10.10"
        rs.port = "8080"
        rs.state= "inservice" #standby, outofservice
        rs.opstate = "inservice"
        rs.description = "Test rserver save in DB"
        rs.failOnAll = None
        rs.minCon = 4000000
        rs.maxCon = 4000000
        rs.weight = 8
        rs.probes = [1, 23]
        rs.rateBandwidth = ""
        rs.rateConnection = ""
        rs.backupRS = ""
        rs.backupRSport = ""
        rs.created = "01-01-2012 11:22:33"
        rs.updated = "02-04-2012 11:22:33"
        rs.status = "ACTIVE"
        rs.cookieStr = None
        rs.condition = "ENABLED"
        
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.writeRServer(rs)
        read  = stor.getReader()
        newrs = read.getRServerById(123)
        self.assertEquals(newrs.name,  "testRS")

    def test_rserver_update(self):
        rs = RealServer()
        rs.id = 123
        rs.sf_id = "123"
        rs.name = "testRS"
        rs.type = "Host"
        rs.webHostRedir = ""
        rs.redirectionCode = ""
        rs.ipType = "IPv6"
        rs.address = "2002:12:23:34::1"
        rs.port = "8080"
        rs.state= "inservice" #standby, outofservice
        rs.opstate = "inservice"
        rs.description = "Test rserver update in DB"
        rs.failOnAll = None
        rs.minCon = 4000000
        rs.maxCon = 4000000
        rs.weight = 8
        rs.probes = [1, 23]
        rs.rateBandwidth = ""
        rs.rateConnection = ""
        rs.backupRS = ""
        rs.backupRSport = ""
        rs.created = "01-01-2012 11:22:33"
        rs.updated = "02-04-2012 11:22:33"
        rs.status = "DOWN"
        rs.cookieStr = None
        rs.condition = "ENABLED"
        
        stor = Storage( {'db_path':'./db/testdb.db'})
        wr = stor.getWriter()
        wr.updateObjectInTable(rs)
        read  = stor.getReader()
        newrs = read.getRServerById(123)
        self.assertEquals(newrs.name,  "testRS")
