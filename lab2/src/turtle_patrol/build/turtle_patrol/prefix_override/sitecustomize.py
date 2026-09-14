import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cc/ee106a/fa26/class/ee106a-act/ros_workspaces/lab2/src/turtle_patrol/install/turtle_patrol'
