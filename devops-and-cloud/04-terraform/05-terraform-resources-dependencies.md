# 05 — Resources, Dependencies, and Ordering

**← Back to [Lesson 04](04-terraform-variables.md) · Next → [Lesson 06](06-terraform-modules.md)**

You've created a resource. But real infrastructure has many resources that depend on each other — a server needs its network first, a database needs its subnet, an API needs its security group. How does Terraform know what to create first?

The satisfying answer: **you don't have to tell it.** Terraform figures out the order automatically by reading the dependencies between resources.

---

## 1. The Mental Model

Think of your config as a **dependency graph**, not a to-do list.

```
        ┌─────────────────────────┐
        │  aws_vpc "main"         │
        └────────────┬────────────┘
                     │ depends on
        ┌────────────▼────────────┐
        │  aws_subnet "app"       │
        └────────────┬────────────┘
                     │ depends on
        ┌────────────▼────────────┐
        │  aws_instance "web"     │
        └─────────────────────────┘
```

A subnet **references** the VPC. An instance **references** the subnet. Terraform walks these references and creates things in dependency order — VPC first, then subnet, then instance. You never hand-write the sequence.

---

## 2. Implicit Dependencies (the common case)

When one resource references another, the dependency is **implicit** — Terraform sees it and orders correctly.

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "app" {
  vpc_id     = aws_vpc.main.id        # ← reference = implicit dependency
  cidr_block = "10.0.1.0/24"
}

resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.app.id   # ← reference = implicit dependency
}
```

Here `aws_vpc.main.id` and `aws_subnet.app.id` create the graph. Terraform creates the VPC first, then the subnet, then the instance — and tears them down in the **reverse** order (instance, subnet, VPC) when you `destroy`.

---

## 3. The Attribute-Reference Pattern

That `aws_vpc.main.id` is called an **attribute reference**. The general shape is:

```hcl
<resource_type>.<resource_name>.<attribute>
# e.g.      aws_s3_bucket.learning.arn
#                aws_instance.web.public_ip
```

You'll use this constantly: passing one resource's output (like a VPC id or a bucket ARN) into another resource's config. It's how you wire a whole stack together.

---

## 4. Explicit Dependencies (when references aren't enough)

Sometimes two resources are related but you *don't* reference one from the other's config — say, a side-effect relationship where Terraform can't see the link by itself.

Use `depends_on` to force the order:

```hcl
resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.ecs_role.name
  policy_arn = aws_iam_policy.task_policy.arn
}

resource "aws_ecs_cluster" "cluster" {
  name = "notes-cluster"
  depends_on = [aws_iam_role_policy_attachment.attach]
}
```

`depends_on` takes a **list** of references. Use it sparingly — only when Terraform genuinely can't infer the dependency. Over-using it makes the graph rigid and slower to plan.

---

## 5. What Happens When a Dependency Changes

Say you change the VPC's CIDR block. Terraform must update the VPC, which forces the subnet, which forces the instance. In the plan you'll see the **chain**:

```
  # aws_vpc.main will be updated in-place
  # aws_subnet.app must be replaced       (depends on vpc)
  # aws_instance.web must be replaced     (depends on subnet)
```

Some resources can be updated in place (`~` in plan output); others must be **replaced** (`-/+`), which means destroy-then-recreate. That's why changing a closely-coupled thing can ripple. Same reason an S3 bucket name change earlier meant replacement instead of update.

---

## 6. Real-World Scenario

**Scenario:** You deploy a small Notes API — a VPC, a subnet, a database, and an app server.

```
VPC → subnet → security group
         │         │
         └────┐    │
              ▼    ▼
            database   app server
```

You write each resource referencing the ones it needs. Terraform draws the graph, builds in the right order, and because the database's security group is referenced by the app server (and vice-versa), it wires them up correctly without a single hand-written step.

---

## 7. Quick Recap

- Terraform builds a **dependency graph** from resource references automatically.
- **Implicit dependency** = one resource references another's attributes.
- Attribute references look like `resource_type.resource_name.attribute`.
- **Explicit `depends_on`** forces order when references can't express it — use sparingly.
- Order matters for **replacements**: changing a parent often forces its children to rebuild.
- Terraform destroys in the **reverse** order it created.

---

## 8. Your Turn

1. Write a VPC + subnet + instance stack like the one above, referencing `aws_vpc.main.id` in the subnet.
2. Run `plan`. Notice it orders VPC → subnet → instance without you asking.
3. Add an `output` for `aws_instance.web.public_ip`. Apply and confirm.
4. Simulate a rippling change: edit the VPC CIDR block and `plan` again. Which resources get *replaced*?

Next up: pack reusable chunks of infrastructure into **modules** so you can share and reuse them. 🧩
