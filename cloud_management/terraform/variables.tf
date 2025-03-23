variable "region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "availability_zone" {
  description = "Availability zone"
  default     = "us-east-1a"
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
