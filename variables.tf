variable "name" {
  description = "Specifies the name of the swarm that is going to be built.  It is used for names and DNS names."
}

variable "managers" {
  description = "Number of managers in the swarm.  This should be an odd number otherwise there may be issues with raft consensus."
  default     = 3
}

variable "workers" {
  description = "Number of workers in the swarm."
  default     = 0
}

variable "vpc_id" {
  description = "The VPC that will contain the swarm."
}

variable "cloud_config_extra" {
  description = "Content added to the end of the cloud-config file."
  default     = ""
}

variable "exposed_security_group_ids" {
  description = "This is the security group ID that specifies the ports that would be exposed by the swarm for external access."
  type        = "list"
}

variable "s3_bucket_name" {
  description = "The S3 bucket name, if not specified it will be the DNS name with .terraform added to the end."
  default     = ""
}

variable "instance_type" {
  description = "EC2 instance type."
  default     = "t3.micro"
}

variable "volume_size" {
  description = "Size of root volume in gigabytes."
  default     = 8
}

variable "manager_subnet_segment_start" {
  description = "This is added to the index to represent the third segment of the IP address."
  default     = 10
}

variable "worker_subnet_segment_start" {
  description = "This is added to the index to represent the third segment of the IP address."
  default     = 110
}