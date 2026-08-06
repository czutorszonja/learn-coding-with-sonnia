# 03 — State: The File That Remembers Everything

**← Back to [Lesson 02](02-terraform-first-steps.md) · Next → [Lesson 04](04-terraform-variables.md)**

Last lesson you created an S3 bucket and Terraform "remembered" it in `terraform.tfstate`. That file is the heart of Terraform — and the thing beginners most often get wrong. This lesson is about understanding, protecting, and sharing it.

---

## 1. The Mental Model

Think of **state** as a **shopping list that Terraform itself keeps updated**.

```
main.tf                     terraform.tfstate
(what you WANT)             (what actually EXISTS)
"1 S3 bucket"      ──────▶  bucket "szonja-learning-bucket" = aws_…f3k2j1
"1 EC2 instance"   ──────▶  instance "web-server" = i-0abcd1234
```

When you run `plan`, Terraform does the comparison:

> Desired (−) Reality = the change needed.

- Want a bucket but none exists → **create it**
- Bucket exists but config changed → **update it**
- Bucket exists but removed from config → **delete it** (that's why `destroy` works!)

Without state, Terraform would have no idea which resources it manages vs. which were created some other way. It literally cannot function without it.

---

## 2. Why Hand-Editing State Is Dangerous

`terraform.tfstate` looks like ordinary JSON you could tweak. **Don't.**

- Terraform maps config blocks to real cloud resources **by this file**, using internal IDs.
- Editing it can make Terraform think a resource is something it isn't — leading to accidental **deletion** or **recreation** of real infrastructure.
- If you corrupt it and Terraform loses track, your cloud resources become **orphaned**: still running, still costing money, but invisible to Terraform.

Rule of thumb: **the `.tf` files are for you to edit; the `.tfstate` is for Terraform.** You read it to understand, you never write to it.

---

## 3. The Big Problem: State Lives on Your Laptop

Here's the catch. So far, `terraform.tfstate` sits in your project folder, on your machine. That's fine when you're the only one.

But the moment you collaborate:

- **Two people** each have their own state → they fight over the same resources and overwrite each other.
- **A CI/CD pipeline** runs `apply` from a server → which state does it use?
- **You lose your laptop** → you lose the state → you orphan every resource you ever created.

**Local state doesn't scale.** The fix is **remote state**.

---

## 4. Remote State: One Source of Truth

Store state in a shared, lock-protected location — most commonly an **S3 bucket** (with DynamoDB for a lock, a detail we can mention later).

```hcl
# backend.tf

terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "notes-app/terraform.tfstate"
    region = "eu-west-2"
  }
}
```

Now every collaborator, and every CI pipeline, loads and updates the **same** state file. Two people can't silently desync, and `terraform` gets an automatic **lock** so two runs don't clobber each other.

> **Important:** The `backend` block changes how state is *stored*, not what resources you *create*. The S3 state bucket is special infrastructure you set up once, **outside** your normal config (or Terraform would try to delete the thing holding its own memory).

---

## 5. Never Put Secrets in State

The state file contains real-world attribute values, and some of those can be sensitive — database endpoints, ARNs, sometimes even secrets if a resource stores them in its attributes.

Treat `terraform.tfstate` like a **credentials file**:

- Set `sensitive = true` on outputs that hold secrets so `plan`/`apply` **mask** them.
- **Never** commit state to a public git repo.
- Add `*.tfstate*` to `.gitignore` in your own projects.

---

## 6. Commands Around State

Get comfortable with these:

```bash
terraform state list                    # list every resource Terraform knows about
terraform state show aws_s3_bucket.x    # details of one resource
terraform state mv old.name new.name    # rename a resource in state (renaming in .tf alone would destroy+recreate)
terraform state rm aws_s3_bucket.x      # tell Terraform to STOP managing it (resource stays in cloud!)
```

The last one is subtle and powerful: `state rm` **un-tracks** a resource without deleting it from the cloud. Useful when a resource should now be managed by a different tool or team.

---

## 7. What NOT to Do

| Don't | Why |
|---|---|
| Hand-edit `terraform.tfstate` | Breaks Terraform's mapping → accidental delete/recreate |
| Commit state to a public repo | It contains real resource IDs and possibly secrets |
| Keep state only on your laptop | Loss = orphaned resources; team = desync |
| `rm` resources from the cloud directly, bypassing Terraform | State and reality drift → Terraform will try to re-create them |

---

## 8. Real-World Analogy

Imagine state as a **warehouse inventory ledger**.

Your `.tf` files say *"the warehouse should contain these items."* The ledger (`tfstate`) says *"here's where each item physically is."* If you tear out a page of the ledger but the item is still physically in the warehouse — you've lost track of it. It's still there, still costing rent, but now nobody can find or clean it up.

**Remote state** = a shared, master ledger in the office that everyone reads and updates, locked while someone's editing it.

---

## 9. Quick Recap

- **State** = Terraform's record of what exists; it's how `plan` knows what to change.
- **Never hand-edit it** — you can orphan or accidentally destroy real resources.
- **Use remote state** (e.g. S3) for teams, CI, and disaster recovery.
- **Protect it like credentials** — secrets can live in its attributes.
- `state list` / `state show` / `state mv` / `state rm` are your inspection + admin tools.

---

## 10. Your Turn

1. From last lesson's folder, run `terraform show`. What does it know about?
2. Look at `terraform.tfstate` as JSON. Can you spot the bucket's real AWS id?
3. Add `*.tfstate*` to a `.gitignore`. Why would you want that?
4. (Optional/challenge) Create a second, throwaway S3 bucket resource in a `scratch.tf`, apply it, then `terraform state rm` it. Confirm with `terraform state list` that Terraform no longer tracks it — then delete the bucket manually in the AWS console. What did you just demonstrate?

Next up: stop hardcoding values — variables make your config reusable. 🔧
