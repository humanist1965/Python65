#!/bin/bash

# script to start a ssh session on my Amazon EC2 instance that I run the App off
cd ~/AWS/KEYPAIRS
# ssh -i "MK_KEYPAIR1.pem" ubuntu@ec2-18-130-245-71.eu-west-2.compute.amazonaws.com
ssh -i "MK_KEYPAIR1.pem" ubuntu@ec2-52-56-214-201.eu-west-2.compute.amazonaws.com



