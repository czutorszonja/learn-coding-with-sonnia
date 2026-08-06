# 06 — Modules: Reusable Blocks of Infrastructure

**← Back to [Lesson 05](05-terraform-resources-dependencies.md) · Next → [Lesson 07](07-terraform-provisioners.md)**

By now you've built config with resources, variables, and outputs. But as your infrastructure grows, `main.tf` gets long, and you find yourself copy-pasting the same VPC or the same app-server block into every project.

**Modules** fix that. A module is just a reusable, self-contained chunk of Terraform with its own inputs (variables) and outputs. Think of it as a **function for infrastructure**.

---

## 1. The Mental Model

```
        ┌───────────────────────────────┐
        │  MODULE: "web-app"            │
        │                               │
        │  input:  name, region, size   │  ← variables (like function args)
        │                               │
        │  contains: VPC + subnet +     │
        │            instance + SG      │  ← the reusable recipe
        │                               │
        │  output: url, public_ip       │  ← return values (like returns)
        └───────────────────────────────┘
```

Call a module from your root config the same way you'd call a function, passing in the variables it needs and reading back its outputs.

---

## 2. Root vs. Child Modules

- **Root module** = everything in your main project folder (the entry point you `apply`).
- **Child module** = a self-contained folder (often `modules/aws-vpc/`) you *call* from the root.

This is just nesting — every module is itself a full Terraform config of `variables.tf`, `main.tf`, `outputs.tf`.

---

## 3. Using a Module (Calling It)

Say you have a folder `modules/web-app/` containing a config that creates an app server. From your root `main.tf`:

```hcl
module "notes_app" {
  source = "./modules/web-app"   # local path (or a git/registry URL)

  app_name = "notes"
  region   = "eu-west-2"
  size     = "t3.micro"
}

# Use the module's outputs anywhere:
output "app_url" {
  value = module.notes_app.url
}
```

- `source` tells Terraform where the module lives — a local folder (`./modules/…`), a git repo, or the **Terraform Registry** (public, shared modules).
- `module.notes_app.<output>` reads values the module returns.

---

## 4. The Registry: Don't Reinvent the Wheel

The **Terraform Registry** (`registry.terraform.io`) has thousands of pre-built, versioned, community modules. To use one, just point `source` at it:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "notes-vpc"
  cidr = "10.0.0.0/16"
}
```

This is a huge time-saver for well-known patterns (VPCs, EKS clusters, S3 buckets with all the right bells and whistles). **Prefer a maintained module over hand-rolling** common infrastructure.

---

## 5. Good Module Design

- **One module = one concern.** A "web-app" module, a "database" module, a "networking" module. Don't make a "everything" module.
- **Expose the knobs it needs** via typed variables with good defaults; don't force every caller to set 30 values.
- **Return useful outputs** (URLs, ARNs, IDs) so callers can wire modules together.
- **Version your modules** (whether local via git tags or registry releases) so consumers get stable behaviour.
- **Keep secrets out** — a module shouldn't force secrets through variables that end up in state.

---

## 6. Modules + The Dependency Graph

Calling a module doesn't break ordering. The module's resources still reference each other, and the caller can depend on a module's output:

```hcl
module "database" {
  source = "./modules/database"
  ...
}

module "app_server" {
  source = "./modules/web-app"
  db_endpoint = module.database.endpoint   # app waits for the database module
}
```

Terraform builds one combined graph across all modules, so `app_server` is created after `database` resolves.

---

## 7. Real-World Scenario

**Scenario:** You run three services (notes, billing, auth) on AWS, each needing the same VPC + subnet + app-server pattern.

Without modules: copy the block three times, let them drift apart, patch three places.

With a `web-app` module: write it once, call it three times with different `app_name`. Fix a bug once in the module → all three updates on next `apply`.

---

## 8. Quick Recap

- **Module** = reusable chunk of config with inputs (variables) and outputs.
- **Root** module = your project; **child** modules = folders it calls.
- Call with `module "name" { source = ... }`, pass variables, read `module.name.output`.
- Use the **Registry** for common patterns; prefer maintained modules.
- Keep modules single-purpose, typed, versioned, and secret-free.

---

## 9. Your Turn

1. Refactor the VPC+subnet+instance stack from Lesson 05 into a `modules/web-app/` child module.
2. Call it from a new root `main.tf`, passing `app_name` and `size`.
3. Add an `output` that returns the instance's public IP from the module.
4. (Optional) Try a public Registry module, e.g. `terraform-aws-modules/vpc/aws`, in a scratch project.

Next up: when Terraform needs to run commands *inside* the resources it creates — provisioners. ⚙️
