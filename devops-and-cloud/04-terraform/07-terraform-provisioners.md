# 07 — Provisioners: Running Commands Inside Your Infra

**← Back to [Lesson 06](06-terraform-modules.md) · Next → [Lesson 08](08-terraform-workspaces-advanced.md)**

So far, Terraform has only *created* cloud resources — buckets, networks, servers. But sometimes you need to run a command *inside* a freshly created machine: install a package, clone a repo, bootstrap an app.

**Provisioners** let Terraform run those commands. They're the most dangerous tool in Terraform — useful, but easy to misuse. Let's learn them properly, and learn when *not* to.

---

## 1. The Mental Model

Terraform is *declarative* and idempotent: "make this true." Provisioners are different — they run **one-shot imperative commands** at a specific moment. They're the **imperative bolt-on** to an otherwise declarative tool.

```
apply
 └─ create aws_instance (resource created)
 └─ provisioner: run `apt install nginx` inside it   ← one-off command
 └─ provisioner: run `./deploy.sh` inside it
```

The provisioner fires at a point in time (usually right after creation) and does something. Once. It doesn't keep watch over that thing afterwards.

---

## 2. The Two Types You'll Meet

### file — copy files onto a machine

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  provisioner "file" {
    source      = "app.conf"
    destination = "/home/ubuntu/app.conf"
  }
}
```

### remote-exec — run commands over SSH

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl start nginx",
    ]
  }
}
```

There's also `local-exec` (runs on *your* machine, not the server) — handy for triggering local scripts after a deploy.

---

## 3. The Big Problem: Ordering & Failure

Because a provisioner runs once, it can't repair *later* drift. Consider:

```hcl
# Run #1: instance created, nginx installed → success
terraform apply

# A month passes. Someone (or a patch) stops nginx.

# Run #2: nothing to change → apply does NOTHING
terraform apply   # nginx stays stopped; provisioner never re-runs
```

Provisioners are **not a management loop**. They don't keep nginx running; they just (try to) install it once. The running service is a separate concern — exactly what a config-management tool (Ansible, Chef) or a container image does better.

---

## 4. The Terraform Guidance (Important!)

Terraform's own maintainers recommend **avoiding** provisioners whenever possible. Why?

- **Not idempotent** — re-running doesn't re-run them; failures leave half-done installs.
- **Not declarative** — you can't see the "desired state" in the config the same way.
- **Hard to debug** — errors inside a script are opaque to Terraform's plan/destroy lifecycle.

---

## 5. Better Alternatives (the "right" way)

Instead of `remote-exec` to install software on a raw server, prefer:

| Goal | Better tool |
|---|---|
| Package an app + its runtime | **Docker image** (you did this in the Docker track ☝️) |
| Pre-bake a server's software | **Custom AMI** (build the image once, launch it many times) |
| Configure/keep a server healthy over time | **Config management** (Ansible, Chef, Puppet) — separate concern |
| Bootstrap downloads at launch | **User data scripts** (cloud-init) — not provisioners |

```hcl
# Better: a user-data script baked in at launch
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  user_data = <<-EOF
    #!/bin/bash
    sudo apt-get install -y nginx
    sudo systemctl start nginx
  EOF
}
```

`user_data` runs automatically at first boot and rebuilds cleanly if the instance is recreated — closer to the declarative spirit.

---

## 6. Provisioners as "Destroy" Cleanup

Provisioners can also run when a resource is *destroyed*:

```hcl
provisioner "local-exec" {
  when    = destroy
  command = "aws s3 rb s3://${self.id} --force"
}
```

Useful for cleanup side-effects that Terraform can't express as a resource. But again — keep it minimal and beware of destroy-time failure leaving things half-cleaned.

---

## 7. Real-World Scenario

**Scenario:** You need a quick throwaway EC2 to run a one-off test that clones a repo and runs it.

A `remote-exec` provisioner that clones + runs at create-time is *fine* for a scratch instance you'll `destroy` right after. But for anything long-lived (a production web server, a database), baking a Docker image or an AMI is the robust choice.

**Rule:** provisioners = fine for bootstrap/throwaway; avoid for anything that must stay converging.

---

## 8. Quick Recap

- **Provisioners** = one-shot imperative commands (`file`, `remote-exec`, `local-exec`) run at a point in time.
- **Idempotency problem** — they don't re-run or repair drift; they install once.
- Terraform **recommends avoiding them** for anything long-lived.
- Prefer **Docker images, custom AMIs, and user-data** for reproducible software setup.
- Keep provisioners for throwaway bootstrap or destroy-time cleanup.

---

## 9. Your Turn

1. Add a `remote-exec` provisioner to a scratch instance that installs nginx.
2. Apply it, then re-apply. Observe that the provisioner does *not* run again.
3. Rebuild the same setup using `user_data` instead. Which feels more declarative?
4. Reflect: if you had to keep a production app installed and healthy, why would a provisioner be the wrong tool?

Next up: environments and advanced commands — workspaces and data sources. 🛠️
