# 04 — Variables, Outputs, and Making Config Reusable

**← Back to [Lesson 03](03-terraform-state.md) · Next → [Lesson 05](05-terraform-resources-dependencies.md)**

So far you've hardcoded everything: bucket name, region, all inline in `main.tf`. That's fine for a playground, but the moment you want the same config for `dev` and `prod`, or want to reuse it without copy-pasting, you need **variables** and **outputs**.

---

## 1. Variables: Turn Knobs on Your Config

Instead of typing the bucket name every time, declare a **variable** and reference it:

```hcl
# variables.tf

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "szonja-learning-bucket"
}

variable "region" {
  type    = string
  default = "eu-west-2"
}
```

Then use them in `main.tf`:

```hcl
provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "learning" {
  bucket = var.bucket_name
}
```

Now the same config is usable anywhere — you just feed it different values.

---

## 2. Setting Values: Four Ways (Lowest to Highest Priority)

Terraform resolves a variable's value in this order:

1. **Default** in the variable block (fallback if nothing else sets it)
2. **`TF_VAR_` environment variables**, e.g. `TF_VAR_bucket_name="x"` (good for CI)
3. **`terraform.tfvars` file** (or `-var-file` flag) — the usual human way
4. **`-var` command-line flag** (highest priority, e.g. `terraform apply -var="bucket_name=foo"`)

Create a `terraform.tfvars` file:

```hcl
# terraform.tfvars
bucket_name = "szonja-prod-bucket"
region      = "us-east-1"
```

Now the *same* config, when pointed at a different `tfvars` file, produces a different environment:

```bash
terraform apply -var-file="envs/prod.tfvars"
terraform apply -var-file="envs/dev.tfvars"
```

Your recipe is written once; the environments are just different inputs. **That's the power.**

---

## 3. Types & Validation

Variables can be typed and validated so mistakes fail *before* they hit the cloud:

```hcl
variable "instance_count" {
  type    = number
  default = 1
}

variable "tags" {
  type = map(string)
  default = {
    env = "dev"
    team = "platform"
  }
}

variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}
```

Common types: `string`, `number`, `bool`, `list(string)`, `map(string)`, and `object({ ... })` for structured data.

---

## 4. Outputs: Hand Back the Results

After `apply`, you often want to know what got created — the bucket's URL, the server's IP. **Outputs** print those values and let other configs or scripts read them.

```hcl
# outputs.tf

output "bucket_arn" {
  value = aws_s3_bucket.learning.arn
}

output "bucket_url" {
  value = aws_s3_bucket.learning.bucket_regional_domain_name
}
```

After `terraform apply` you'll see:

```
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

bucket_arn = "arn:aws:s3:::szonja-learning-bucket"
bucket_url = "szonja-learning-bucket.s3.eu-west-2.amazonaws.com"
```

### Marking secrets as sensitive

```hcl
output "db_password" {
  value     = aws_db_instance.db.password
  sensitive = true   # hidden from plan/apply output
}
```

`sensitive = true` masks the value in the terminal. It's **not** encryption — just prevents casual shoulder-surfing — so keep real secrets out of state too.

---

## 5. A Useful Pattern: Locals

`locals {}` are like variables you compute *inside* the config — great for derived values you don't want to repeat:

```hcl
locals {
  name_prefix = "szonja-${var.environment}"
  full_bucket = "${local.name_prefix}-${var.bucket_name}"
}

resource "aws_s3_bucket" "learning" {
  bucket = local.full_bucket
}
```

Variables are inputs from the outside; **locals are internal helpers**. Use locals whenever you'd otherwise copy-paste an expression.

---

## 6. Real-World Scenario

**Scenario:** You support `dev` and `staging` for your notes API. They should be *identical* except names and region.

You write `main.tf` once using `var.` everywhere. You keep `envs/dev.tfvars` and `envs/staging.tfvars`. Deploying, promoting an environment, or spinning up a new one is just a different `.tfvars` file. Nobody copy-pastes a config and lets the two drift apart.

---

## 7. Quick Recap

- **Variables** (`variable {}`) turn hardcoded values into knobs.
- Set them via `default` < `TF_VAR_` < `terraform.tfvars` < `-var` flag.
- Type + `validation` catch mistakes early.
- **Outputs** (`output {}`) print results and share values with other configs.
- **Local** (`local.*`) for internal, derived values.
- Use `sensitive = true` on outputs hiding secrets.

---

## 8. Your Turn

1. Refactor last lesson's `main.tf` to use `variable` for the bucket name and region.
2. Create `dev.tfvars` and `staging.tfvars` with different bucket names.
3. Add an `output` for the bucket ARN. Apply and confirm it prints.
4. Add a `validation` so `environment` only accepts dev/staging/prod, then try a bad value and watch it fail.

Next up: how Terraform figures out what to create first when resources depend on each other. 🔗
