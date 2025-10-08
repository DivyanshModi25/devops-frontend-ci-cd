variable "region" {
  description = "AWS Region"
  default     = "ap-south-1"
}

variable "availability_zone" {
  description = "Availability zone"
  default     = "ap-south-1a"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for Ubuntu 22.04"
}

variable "key_name" {
  description = "SSH Key Pair name for EC2"
}


variable "profile" {
  description = "aws account with which i need to connect"
}