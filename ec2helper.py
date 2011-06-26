#!/usr/bin/env python

from boto.ec2.connection import EC2Connection

class EC2Helper(object):

  def __init__(self):
    self._access_key = '0YP6HQ4VJYH6ZZP7C282'
    self._secret_key = 'ZcbnVhb7oOpPolTW7KGuYBCBcS+z2rQjSD0s4F2Y'
    self._conn = EC2Connection(self._access_key, self._secret_key)

  def ReadConfiguration(self):
    pass

  def ListSecurityGroups(self, security_group=None):
    if self._conn:
      security_groups = self._conn.get_all_security_groups(groupnames=security_group)
      for sg in security_groups:
        print ' Security Group: %s' % sg.name
        print '------------------------------------------------------'
        for rule in sg.rules:
          print ' %s\t%s\t%s\t%s' % (rule.grants, rule.ip_protocol, rule.from_port, rule.to_port)
        print ''

  def AddSecurityGroupEntry(self, security_group, host=None, port=None):
    """Adds a hostname/port tuple to an existing security group."""
    if self._conn:
      security_groups = self._conn.get_all_security_groups(groupnames=security_group)
      for sg in security_groups:
        if sg.name == security_group:
          return self._conn.authorize_security_group(sg.name, ip_protocol='tcp', from_port=port, to_port=port, cidr_ip='%s/32' % host) 

  def RevokeSecurityGroupEntry(self, security_group, host=None, port=None):
    """Revokes a hostname/port tuple from an existing security group."""
    if self._conn:
      security_groups = self._conn.get_all_security_groups(groupnames=security_group)
      for sg in security_groups:
        if sg.name == security_group:
          return self._conn.revoke_security_group(sg.name, ip_protocol='tcp', from_port=port, to_port=port, cidr_ip='%s/32' % host)
