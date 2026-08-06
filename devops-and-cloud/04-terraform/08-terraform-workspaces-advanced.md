# 08 — Workspaces, Data Sources, and Advanced Commands

**← Back to [Lesson 07](07-terraform-provisioners.md) · Next → [Lesson 09](09-terraform-project.md)**

You've got a reusable config with variables, outputs, modules. Now let's level up: separating environments cleanly, reading *existing* infrastructure, and a few commands that keep you out of trouble.

---

## 1. Workspaces: One Config, Many Environments

A **workspace** is a separate state instance for the same config. The classic use: `dev`, `staging`, `prod` created from one set of `.tf` files.

```bash
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
terraform apply
terraform workspace select prod
terraform apply
```

Each workspace gets its **own** `terraform.tfstate`, so you can `apply` in `dev` without touching `prod`. Reference the current workspace in your config:

```hcl
resource "aws_s3_bucket" "app" {
  bucket = "szonja-${terraform.workspace}-bucket"
}
```

> **How to choose:** Workspaces are great for quick, lightweight environment separation of the *same* code. But many teams prefer separate configs/repos per environment (using different tfvars) because it lets environments drift in *code* too, not just state. Both are valid; pick one and be consistent.

---

## 2. Data Sources: Read What Already Exists

Sometimes you don't want to *create* something — you want to *use* something that already exists, like the latest Ubuntu AMI or an existing VPC. That's what **data sources** are for.

```hcl
# Get the latest Ubuntu AMI owned by Canonical
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id   # ← read from the data source
  instance_type = "t3.micro"
}
```

- `data "aws_ami" "ubuntu"` *looks up* the AMI instead of creating it.
- You reference it as `data.aws_ami.ubuntu.id`, same pattern as arguments.
- `data` blocks run a **read** at plan time; they create nothing.

**When are data sources useful?** Picking the current base image, discovering an existing subnet/VPC by tag, reading an existing IAM role name — any time you need info Terraform didn't create.

---

## 3. The Handy "Almost" Command: `terraform validate` and `fmt`

- `terraform fmt` — auto-formats your `.tf` files to the canonical style.
- `terraform validate` — checks config for syntax and internal consistency *without* contacting the cloud or reading state.

```bash
terraform fmt
terraform validate
# Success! The configuration is valid.
```

Run these before `apply` (and in CI) to catch obvious errors early and keep code uniform.

---

## 4. More Lifecycle Commands

### Refresh the state to match reality

```bash
terraform refresh
```

Updates `terraform.tfstate` with the current real-world state of your resources (things changed outside Terraform). Usually you don't run this directly — `plan`/`apply` refresh automatically — but it's good to know it exists.

### Lock / unlock state

Remote state uses locks to stop two `apply`s racing:

```bash
terraform force-unlock <LOCK_ID>
```

Only use this if a run crashed and left a stale lock you're sure is orphaned. Forcing an active lock can corrupt state — treat it as a last resort.

---

## 5. `terraform import`: Bring Existing Infra Under Management

Forgot to use Terraform from the start, and now you have resources created manually in the console? You can **import** them:

```bash
terraform import aws_s3_bucket.learning szonja-existing-bucket
```

You must first write the matching `resource` block in your config. After import, Terraform manages that previously hand-created bucket just like any other — you can now `plan`, `apply`, and eventually `destroy` it.

---

## 6. Real-World Scenario

**Scenario:** You run `dev` and `prod` for your notes API from one config.

- **Workspaces** keep two separate states for the same code.
- A **data source** always fetches the latest Ubuntu AMI rather than hardcoding an ID.
- **`fmt` + `validate`** run in CI before any apply, catching bad config cheaply.
- Any legacy resource gets **imported** so it's fully under Terraform control.

---

## 7. Quick Recap

- **Workspaces** = separate states for the same config (dev/prod separation).
- **Data sources** (`data "…"`) read existing infrastructure instead of creating it.
- **`terraform fmt`** formats; **`terraform validate`** sanity-checks config offline.
- **`terraform refresh`** reconciles state with reality.
- **`terraform import`** adopts existing manually-created resources.
- `force-unlock` only for genuinely orphaned locks.

---

## 8. Your Turn

1. Create `dev` and `prod` workspaces and confirm each has its own state (`terraform show` differs).
2. Replace a hardcoded AMI id in your config with a `data "aws_ami"` source, then `plan`.
3. Run `terraform fmt` and describe what it changed (if anything).
4. (Challenge) Create a bucket in the AWS console manually, then `terraform import` it. What's the immediate benefit?

Next up: putting it all together in a final project. 🏗️
