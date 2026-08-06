# 02 — Installing Terraform and Your First Config

**← Back to [Lesson 01](01-terraform-intro.md) · Next → [Lesson 03](03-terraform-state.md)**

Time to get our hands dirty. By the end of this lesson you'll have Terraform installed and a real, working config that talks to a cloud provider.

---

## 1. Installing Terraform

### macOS
```bash
brew install terraform
```

### Windows (via Chocolatey)
```powershell
choco install terraform
```

### Linux (via the HashiCorp APT repo)
```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### Verify

```bash
terraform version
# Terraform v1.x.x
```

---

## 2. The Anatomy of a Terraform Config

Terraform reads files ending in `.tf`. A config is built from a few building blocks:

| Block | What it does |
|---|---|
| `terraform {}` | Global settings (required provider versions, backend, etc.) |
| `provider {}` | Which cloud/vendor to talk to and how |
| `resource {}` | One concrete thing to create (a bucket, a server, a database) |
| `data {}` | Read *existing* infrastructure (don't create, just look up) |
| `variable {}` | A knob you can set from outside the file |
| `output {}` | A value you want printed at the end (e.g. a URL) |

Let's look at each one with a real example.

---

## 3. Your First Config: An S3 Bucket

Create a new folder and a file called `main.tf`:

```bash
mkdir terraform-first && cd terraform-first
```

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

# Tell Terraform which cloud we're using and where
provider "aws" {
  region = "eu-west-2"   # London
}

# The actual thing we want to exist: an S3 bucket
resource "aws_s3_bucket" "learning" {
  bucket = "szonja-learning-bucket"
}
```

Read it out loud: *"There is an S3 bucket, named 'szonja-learning-bucket', in London."* That's the entire mental model of Terraform — you write sentences like that, and it makes them true.

---

## 4. init — Download the Providers

```bash
terraform init
```

```
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.x.x...
Terraform has been successfully initialized!
```

`init` reads the config, figures out which **providers** (cloud SDKs) it needs, downloads them, and sets up your working directory. It's the only step that touches the internet to grab tooling. Run it once per project (or after adding a new provider).

---

## 5. plan — Preview Without Changing Anything

```bash
terraform plan
```

```
Terraform used the selected providers to generate the following execution plan.

  # aws_s3_bucket.learning will be created
  + resource "aws_s3_bucket" "learning" {
      + bucket                          = "szonja-learning-bucket"
      + force_destroy                   = false
      ...
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

`plan` is **read-only** — it shows you exactly what Terraform *would* do, and asks nothing. This is your safety net: always `plan` before you `apply`. It catches typos, wrong names, and surprises while they're still free to fix.

---

## 6. apply — Make It Real

```bash
terraform apply
```

Terraform re-shows the plan, then asks:

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes
```

Type `yes`. Terraform reaches out to AWS and creates the bucket, printing what it did.

Once everything is created, you'll get any **outputs** at the bottom.

---

## 7. Inspecting What Exists: `state`

Everything Terraform creates is tracked. Look at the files in your folder now:

```
├── main.tf              # what you wrote (the recipe)
└── terraform.tfstate     # what exists (the record — DON'T hand-edit this!)
```

`terraform.tfstate` is Terraform's memory of what it created and how it maps to your config. Keep this file safe (more on that next lesson), and **never edit it by hand** — Terraform owns it.

### See it in action

You can query your state:

```bash
terraform show
```

You can also see the raw state with:

```bash
cat terraform.tfstate
```

(You'll notice it's JSON containing the bucket's real AWS id.)

---

## 8. destroy — Clean Up (So You Don't Get Billed)

Cloud resources Cost. Money. So get in the habit of tearing things down when you're done experimenting.

```bash
terraform destroy
```

Terraform shows a plan of everything it will delete, asks for `yes`, and removes the bucket. **This is the whole point** — one command, nothing left behind, no orphaned resources trickling into next month's bill.

---

## 9. Quick Recap

- Install with your package manager, verify with `terraform version`.
- Config lives in `*.tf` files; `provider` picks the cloud, `resource` creates things.
- **init** downloads providers → **plan** previews → **apply** makes it real → **destroy** tears down.
- `terraform.tfstate` records what exists; **never hand-edit it**.
- Always `plan` before `apply`, and `destroy` when you're done.

---

## 10. Your Turn

1. Install Terraform and confirm `terraform version` works.
2. Create `terraform-first/` with the S3 bucket config from this lesson.
3. Run `init`, then `plan` (no questions asked). What does it say it will create?
4. Run `apply` (answer `yes`). Did the bucket get created?
5. Run `destroy` (answer `yes`). Is anything left?

**Bonus:** Change the bucket name in `main.tf` and run `plan` again. Notice it says the bucket will be *replaced*, not modified — because an S3 bucket name can't change in place.

Next up: what happens to that state file when you're not alone — and why it's the most important file you'll protect. 🔐
