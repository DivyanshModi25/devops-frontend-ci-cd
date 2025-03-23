#!/bin/bash

# Step 1: Terraform apply
cd terraform
terraform init
terraform apply -auto-approve

# Step 2: Fetch EC2 IP
EC2_IP=$(terraform output -raw server_public_ip)


# # Step 3: Wait for SSH availability
# while ! nc -z $EC2_IP 22; do
#   echo "Waiting for SSH to become available at $EC2_IP..."
#   sleep 5
# done



# # Step 3: Generate Ansible inventory
# cd ../ansible
# cat > dynamic_inventory.yml <<EOF
# all:
#   hosts:
#     ec2_instance:
#       ansible_host: $EC2_IP
# EOF

# # Step 4: Run Ansible with vars
# ansible-playbook -i dynamic_inventory.yml install_docker.yml
