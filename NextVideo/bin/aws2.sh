#!/bin/bash

# script to start a ssh session on my Amazon EC2 instance that I run the App off
cd ~/AWS/KEYPAIRS

ssh -i "MK2_KEYPAIR1.pem" ubuntu@ec2-35-177-46-123.eu-west-2.compute.amazonaws.com



