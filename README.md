Multi‑Agent Lab (Governed, Identity‑Aware Multi‑Agent System)
A fully governed, identity‑aware, multi‑agent platform deployed via Terraform, bootstrapped with cloud‑init, secured with Tailscale, and orchestrated through Redis.
Each agent operates under strict RealAgentID identity and permission boundaries, ensuring safe, auditable, and policy‑enforced behavior.

This project demonstrates:

Infrastructure‑as‑Code (Terraform)

Zero‑touch provisioning (cloud‑init)

Zero‑trust networking (Tailscale)

Multi‑agent orchestration (Redis)

Identity‑based governance (RealAgentID)

Containerized execution (Docker Compose)

Architecture Overview
Code
Terraform → Azure VM → cloud-init → Docker Compose → Orchestrator → Agents
1. Terraform
Creates:

Resource group

Virtual network + subnet

Public IP

NIC

Ubuntu VM

cloud-init bootstrap

2. cloud-init
On first boot, the VM automatically:

Installs Docker

Installs docker-compose

Installs Tailscale

Clones this repository

Starts the entire multi-agent system

No manual configuration required.

3. Docker Compose
Defines:

Redis (message bus)

Orchestrator

Six agents

Shared RealAgentID config

4. Orchestrator
Central routing and governance layer:

Registers agents

Routes tasks

Enforces RealAgentID permissions

Blocks forbidden actions

Logs decisions

5. Agents
Each agent:

Loads its identity

Registers with orchestrator

Listens on its Redis queue

Verifies permissions

Executes tasks safely

Logs actions

Agents included:

Recon

Categorization

Analysis

Report

Guardrail

Learning

6. RealAgentID
Defines:

Agent identities

Allowed actions

Denied actions

Governance boundaries

7. Audit Logging
All agent actions are logged to:

Code
/var/log/realagentid/agent-actions.log
Repository Structure
Code
multi-agent-lab/
├── infra/
│   ├── main.tf
│   ├── vm.tf
│   ├── cloud-init/
│   │   └── init.yaml
│   └── realagentid/
│       └── agents.json
├── orchestrator/
│   └── app.py
├── agents/
│   ├── recon/
│   │   └── app.py
│   ├── categorization/
│   │   └── app.py
│   ├── analysis/
│   │   └── app.py
│   ├── report/
│   │   └── app.py
│   ├── guardrail/
│   │   └── app.py
│   └── learning/
│       └── app.py
├── realagentid/
│   └── logger.py
└── docker-compose.yml
How the System Works
Agent Registration
Each agent publishes:

Code
{"agent_id": "<name>"}
to the agent_register channel.

The orchestrator:

verifies identity

accepts or rejects the agent

Task Routing
Tasks are published to:

Code
task_queue
The orchestrator:

checks RealAgentID permissions

routes the task to queue:<agent_id>

blocks forbidden actions

Agent Execution
Each agent:

pulls tasks from its queue

verifies permissions

executes allowed actions

logs results

Audit Logging
Every action is logged with:

timestamp

agent_id

action

scope

status

details

Deployment Flow
terraform apply

Azure VM boots

cloud-init installs Docker, Tailscale, clones repo

docker compose up -d starts orchestrator + agents

Agents register

System becomes fully operational

Security Model
Zero‑Trust Networking
Tailscale provides:

encrypted access

no exposed ports

identity‑based access control

Identity‑Based Governance
RealAgentID enforces:

allowed actions

denied actions

agent‑specific boundaries

Auditability
Every action is logged for traceability.

Why This Project Matters
This platform demonstrates:

real infrastructure

real governance

real orchestration

real agent identity

real auditability

It’s not a toy — it’s a blueprint for safe, governed multi-agent systems.
