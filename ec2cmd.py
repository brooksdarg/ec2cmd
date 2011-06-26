#!/usr/bin/env python

import getopt
import sys
import urllib2

import ec2helper

def main(action, argv):
  """Core logic."""
  try:
    opts, args = getopt.getopt(argv, "h:g:p:", ["host=", "group=", "port="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  security_group = None
  host = None
  port = None

  for opt, arg in opts:
    if opt in ('--help'):
      usage()
      sys.exit(0)
    elif opt in ('-g', '--group'):
      security_group = arg
    elif opt in ('-h', '--host'):
      host = arg
    elif opt in ('-p', '--port'):
      port = arg

  # Instantiate the helper
  helper = ec2helper.EC2Helper()

  if action in ('listgroups', 'list_security_groups', 'lsg'):
    helper.ListSecurityGroups(security_group=security_group)
  elif action in ('addgroupentry', 'add_group_entry', 'age'):
    if host is None:
      host = get_external_ip()
    if host and port:
      if helper.AddSecurityGroupEntry(security_group, host, port):
        print '%s/%s added to group %s' % (host, port, security_group)
    else:
      usage()
      sys.exit(2)
  elif action in ('revokegroupentry', 'revoke_group_entry', 'rge'):
    if host is None:
      host = get_external_ip()
    if host and port and security_group:
      if helper.RevokeSecurityGroupEntry(security_group, host, port):
        print '%s/%s revoked from group %s' % (host, port, security_group)
    else:
      usage()
      sys.exit(2)
  elif action in ('ip'):
    print get_external_ip()
  else:
    print 'Action "%s" not found.' % action
    usage()
    sys.exit(2)

def get_external_ip():
  try:
    response = urllib2.urlopen('http://wwwdargnet.appspot.com/ip')
  except urllib2.URLError:
    return None
  return response.read()

def usage():
  print """Commands:
  Get External IP Address
    ec2cmd ip
  Authorize Security Group Entry
    ec2cmd age --host=<host> --port=<port>
  Revoke Security Group Entry
    ec2cmd rge --host=<host> --port=<port>
  List Security Groups
    ec2cmd lsg"""

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1], sys.argv[2:])
  else:
    usage()
