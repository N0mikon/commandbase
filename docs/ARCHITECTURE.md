# Architecture

Visual guide to how commandbase's 8 plugins, 46 skills, 8 agents, and 1 hook connect.

## System Diagrams

| Diagram | What it shows |
|---------|--------------|
| [Plugin Dependencies](plugin-dependencies.md) | How the 8 plugins relate and what each exports |
| [BRDSPI Pipeline](brdspi-pipeline.md) | The six-phase artifact chain all domain plugins share |
| [Hook Timeline](hook-timeline.md) | When each hook fires during a conversation |

## Domain Workflows

Each domain plugin follows the same BRDSPI pattern adapted to its context. These pages show the specific skills, agents, and extras for each domain.

| Workflow | Skills | Agents | Extras |
|----------|:------:|:------:|--------|
| [Code Workflow](code-workflow.md) | 8 | 3 | /debugging-code, /starting-refactors |
| [Vault Workflow](vault-workflow.md) | 8 | 0 | /importing-vault, /starting-vault |
| [Services Workflow](services-workflow.md) | 6 | 0 | Straight BRDSPI, no extras |
