provider "aws" {
  region  = var.region 
}

# Get the default VPC
data "aws_vpc" "default" {
  default = true
}

# Get the default subnet in the default VPC
data "aws_subnet" "default" {
  vpc_id = data.aws_vpc.default.id
  availability_zone = var.availability_zone
}

# Create a security group to allow HTTP & SSH access
resource "aws_security_group" "allow_web_sg" {
  name        = "allow_web_sg_traffic"
  description = "Allow web traffic (HTTP) and SSH"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch an EC2 instance in the default VPC
resource "aws_instance" "web_server" {
  ami                    = var.ami_id  # Ubuntu 22.04 AMI for us-east-1
  instance_type          = var.instance_type
  subnet_id              = data.aws_subnet.default.id
  security_groups        = [aws_security_group.allow_web_sg.id]
  associate_public_ip_address = true
  key_name               = var.key_name  # Replace with your key pair name

  user_data = <<-EOF
                #!/bin/bash
                sudo apt update -y
                sudo apt install -y docker.io
                sudo systemctl enable docker
                sudo systemctl start docker

                # Add ubuntu user to docker group to run without sudo
                sudo usermod -aG docker ubuntu

              EOF

  tags = {
    Name = "WebServer"
  }
}


