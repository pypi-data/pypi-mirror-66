# import numpy as np
# feed_dict = {
# 'deep_layer/sequence:0': np.array([[-0.184154898, -2.59719634, -0.0439090878 ,-1.0149796],
#   [-0.451936752, 3.24952364 ,-3.99610043, -2.94358253],
#   [1.16041446, 6.17435408, -2.26343656, 3.13882113],
#   [-2.51578903, -1.06081808, -1.94339526, -0.373771667],
#   [-0.184154898, -2.59719634, -0.0439090878, -1.0149796],
#   [-1.36145425, 5.64153576, 1.71881521, -2.70508862],
#   [-1.36145425, 5.64153576, 1.71881521, -2.70508862],
#   [-1.36145425, 5.64153576, 1.71881521, -2.70508862],
#   [-1.36145425, 5.64153576, 1.71881521 ,-2.70508862],
#   [0.430151224, 1.42843509, -4.1790247, -2.99058676],
#   [0.430151224, 1.42843509, -4.1790247, -2.99058676],
#   [-0.184154898, -2.59719634, -0.0439090878 ,-1.0149796],
#   [0.430151224, 1.42843509, -4.1790247, -2.99058676],
#   [-1.26148415, 5.54065466 ,-3.09401178, 2.68605185],
#   [-0.936168551, 1.26759303 ,-0.377744257, -0.972414494],
#   [1.16041446, 6.17435408, -2.26343656, 3.13882113],
#   [-0.936168551, 1.26759303, -0.377744257, -0.972414494],
#   [-3.04807949, 1.46883917 ,-3.19800472, 1.14978659],
#   [0.527214408, 0.908681214, -0.739776134, -0.867915928],
#   [0.315995842, 5.40439272, -5.3037281 ,-1.62441516]]), 'deep_layer/itemid:0': np.array([[1.12601876, -1.46433055, -0.064487949, 0.713679075]])
# }
#
# sess.run("output_layer/predict_value:0", feed_dict=feed_dict)


configurations=[
   {
    "Classification": "hive-site",
    "Properties": {
      "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
    }
  },
  {
    "Classification": "spark-hive-site",
    "Properties": {
      "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
    }
  },
  {
    "Classification": "capacity-scheduler",
    "Properties": {
      "yarn.scheduler.capacity.resource-calculator": "org.apache.hadoop.yarn.util.resource.DominantResourceCalculator"
    }
  }
]

import argparse
import json
import time
import logging


parser = argparse.ArgumentParser()
parser.add_argument("--tags", type=str,default="cfdp='temple cluster'")
parser.add_argument("--release_label", type=str,default="emr-5.29.0")
parser.add_argument("--customer",action="store_true",default=False)
parser.add_argument("--auto_terminate",action="store_true",default=True)
parser.add_argument("--use_default_roles",action="store_true",default=True)
parser.add_argument("--cluster_name", type=str,default="Started By Airflow emrCli",help="cluster name")
parser.add_argument("--instance_type", type=str,default="r4.4xlarge",help="""
Shortcut parameter as an alternative to --instance-groups . Specifies the type of Amazon EC2 instance to use in a cluster. 
If used without the --instance-count parameter, the cluster consists of a single master node running on the EC2 instance type specified. 
When used together with --instance-count , one instance is used for the master node, and the remainder are used for the core node type.
""")
parser.add_argument("--ec2_attributes", type=str,default="KeyName=wennaisong_id_rsa")
parser.add_argument("--instance_fleets", type=str,default="file:///home/ubuntu/data-sync/emr-fleets.json")
parser.add_argument("--configurations", type=str,default="'"+json.dumps(configurations)+"'")

args = parser.parse_args()
options = vars(args)

