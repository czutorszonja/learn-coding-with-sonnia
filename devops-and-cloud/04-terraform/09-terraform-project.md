# 09 — Final Project: Notes API Infrastructure with Terraform

**← Back to [Lesson 08](08-terraform-workspaces-advanced.md)**

Welcome to the final project. Throughout this track you've built Docker containers, run Kubernetes, and deployed on AWS. Now we'll take everything from this Terraform course and do what Terraform does best: **define the entire Notes API infrastructure as code**, in a reusable, teardown-able, team-shareable way.

We'll create a small stack:
- An **S3 bucket** (for uploads)
- A **VPC** with a **subnet** (networking)
- A **security group** (firewall rules)
- An **EC2 instance** (the app server), bootstrapped via user-data
- **Outputs** to see what got created

By the end, you can spin this up for `dev`, tear it down, and rebuild it identically — the whole point of Infrastructure-as-Code.

---

## Architecture Overview

```
                 ┌───────────────────────────────┐
                 │         VPC 10.0.0.0/16        │
                 │                               │
                 │  ┌─────────────────────────┐  │
                 │  │   Subnet 10.0.1.0/24    │  │
                 │  │                         │  │
                 │  │  ┌───────────────────┐  │  │
                 │  │  │  Security Group    │  │  │
                 │  │  │  (port 22, 80)     │  │  │
                 │  │  └─────────┬─────────┘  │  │
                 │  │            │            │  │
                 │  │  ┌─────────▼─────────┐  │  │
                 │  │  │   EC2 instance    │  │  │
                 │  │  │  (web + user-data)│  │  │
                 │  │  └───────────────────┘  │  │
                 │  └─────────────────────────┘  │
                 └───────────────────────────────┘

    S3 bucket (szonja-notes-uploads)  ── uploads & files
```

---

## Step 0: Project Setup

```
mkdir tf-notes-project && cd tf-notes-project
```

We'll use variables, outputs, and a module to keep it clean and reusable.

---

## Step 1: Variables

```hcl
# variables.tf

variable "project_name" {
  type    = string
  default = "notes"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging or prod."
  }
  default = "dev"
}

variable "region" {
  type    = string
  default = "eu-west-2"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
```

---

## Step 2: Provider + Networking + Storage

```hcl
# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Storage — an S3 bucket for uploads (notice the workspace-suffixed name)
resource "aws_s3_bucket" "uploads" {
  bucket = "szonja-${var.project_name}-${terraform.workspace}"
  force_destroy = true
}

# Networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "app" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-west-2a"
}
```

---

## Step 3: Security Group (Firewall Rules)

```hcl
# sg.tf

resource "aws_security_group" "web" {
  name        = "notes-web-sg"
  description = "Allow SSH and web traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH from anywhere (demo only!)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
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
```

> ⚠️ **Security note:** Opening port 22 to `0.0.0.0/0` is fine for a throwaway demo, but **never** do it for real. For a production setup, restrict SSH to your own IP (e.g. `your-public-ip/32`) or use a bastion.

---

## Step 4: The App Server (with user-data, not a provisioner)

Remember Lesson 07 — we prefer `user_data` over a remote-exec provisioner for this:

```hcl
# instance.tf

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]   # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.app.id
  vpc_security_group_ids = [aws_security_group.web.id]
  associate_public_ip_address = true

  tags = {
    Name = "${var.project_name}-${terraform.workspace}"
  }

  user_data = <<-EOF
    #!/bin/bash
    sudo apt-get update -y
    sudo apt-get install -y nginx
    echo "<h1>Hello from Terraform :)</h1>" | sudo tee /var/www/html/index.html
    sudo systemctl enable nginx
  EOF
}
```

The data source always picks the current Ubuntu AMI, and the user-data runs at first boot — no fragile one-shot provisioners.

---

## Step 5: Outputs

```hcl
# outputs.tf

output "web_public_ip" {
  value = aws_instance.web.public_ip
}

output "web_url" {
  value = "http://${aws_instance.web.public_ip}"
}

output "bucket_name" {
  value = aws_s3_bucket.uploads.bucket
}
```

---

## Step 6: Run It

```bash
terraform init

# Create the dev workspace if you haven't already
terraform workspace select -or-create dev

terraform plan          # review before doing anything
terraform apply         # type yes
```

When apply finishes you'll see:

```
Outputs:

web_public_ip = "54.…"
web_url       = "http://54.…"
bucket_name   = "szonja-notes-dev"
```

Visit `web_url` in a browser — you should see **"Hello from Terraform :)"** served by nginx.

---

## Step 7: Environments & Teardown

Spin up `staging` the same way:

```bash
terraform workspace select -or-create staging
terraform apply -var="instance_type=t3.small" -var="environment=staging"
```

Identical infra, different workspace, different values. That's reproducibility.

And the moment you're done, clean up so nothing keeps billing you:

```bash
# Tear down the whole prod/current workspace
terraform destroy        # review, then type yes

# And remove the workspace
terraform workspace select default
terraform workspace delete staging
```

Because everything lives in `terraform.tfstate`, `destroy` removes the VPC, subnet, security group, instance, and bucket in the correct dependency order. **Nothing left behind.**

---

## Checklist — Did It All Land?

- [ ] `terraform init` ran without errors
- [ ] `workspace dev` created, `plan` clean, `apply` created VPC → subnet → SG → instance
- [ ] `web_url` loads "Hello from Terraform :)" over nginx
- [ ] A second workspace (`staging`) creates a separate, identical stack
- [ ] `terraform destroy` removes everything; `state list` shows nothing left

---

## Wrapping Up the Whole Terraform Course 🎉

If you've made it here, you can now:

- Explain **what Terraform is** and why IaC beats console-clicking (Lesson 1)
- **Init → plan → apply → destroy** an S3 bucket (Lesson 2)
- Protect and share **state** (Lesson 3)
- Make config **reusable** with variables and outputs (Lesson 4)
- Wire resources together and understand **dependency ordering** (Lesson 5)
- Package reusable chunks into **modules** (Lesson 6)
- Know when provisioners are (rarely) the right call (Lesson 7)
- Separate environments with **workspaces/data sources** (Lesson 8)

That's a genuinely valuable, hireable skill. Go build something real — and remember: `terraform destroy` before you sleep. 😄

**Next:** Check out the [Devops & Cloud Cheatsheet](../summary/cheatsheet.md) to keep it all fresh.
