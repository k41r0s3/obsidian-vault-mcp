# Use Cases

Practical examples of what you can do with vaultbridge once it's connected to Claude.

---

## Resume Builder

Keep your entire professional profile in an Obsidian vault and generate tailored resumes on demand.

**Vault structure:**
```
Resume Builder/
├── profile.md        ← objective, background, target roles
├── experience.md     ← work history
├── education.md      ← academic qualifications
├── skills.md         ← categorized skills & tools
├── projects.md       ← all projects with tags
└── certifications.md ← certs, awards, CTF rankings
```

**Workflow:**
1. Keep your vault files up to date as you gain experience
2. When applying for a role, paste the job description and say:

```
Read all notes from my Resume Builder vault.
Here is the job description: [JD]
Generate a tailored 1-page resume, highlighting only relevant skills and experience.
Output as a Word document.
```

Claude reads your vault, filters what's relevant to the JD, rewrites your objective, and generates the resume — in one shot.

**Updating your vault:**
```
"Append this new certification to my certifications note in Resume Builder:
## OSCP — Offensive Security, 2026"

"Update my experience note in Resume Builder — add this new role at the top:
## Security Analyst @ XYZ Corp (Jan 2026 – Present)
- ..."
```

---

## Personal Knowledge Base

Use vaultbridge as a natural language interface to any Obsidian vault.

```
"Search for everything related to 'docker' in my Work Notes vault"
"Read my meeting notes from last week in Personal Notes"
"Add this idea to my inbox note in Personal Notes: ..."
```

---

## Project Documentation

Keep project notes in Obsidian and let Claude help you write and update them.

```
"Read the architecture note from my Project X vault and summarize it"
"Append today's progress to the devlog note in Project X: ..."
```

---

## Daily Journaling

```
"Create a new note called '2026-03-27' in my Journal vault with today's entry: ..."
"Read my last 3 journal entries from my Journal vault"
```
