#!/bin/bash

# script to start a ssh session on my Amazon EC2 instance that I run the App off
cd ~/AWS/KEYPAIRS

ssh -i "MK3_KEYPAIR1.pem" ubuntu@ec2-3-140-251-38.us-east-2.compute.amazonaws.com


