#!/bin/bash

# script to start a ssh session on my Amazon EC2 instance that I run the App off
cd ~/AWS/KEYPAIRS

ssh -i "MK65_3.pem" ubuntu@ec2-3-250-3-47.eu-west-1.compute.amazonaws.com



