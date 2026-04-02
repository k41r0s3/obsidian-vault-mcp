# Use Cases

## Resume Builder

Keep your entire professional profile in a vault and generate tailored resumes on demand.

**Vault structure:**
```
Resume Builder/
├── profile.md         ← objective, background, target roles
├── experience.md      ← work history with full details
├── education.md       ← academic qualifications
├── skills.md          ← categorized skills & tools
├── projects.md        ← all projects with tags
└── certifications.md  ← certs, CTF rankings, awards
```

**Generate a tailored resume:**
```
Read all notes from my Resume Builder vault.
Here is the job description: [PASTE JD]

Generate a 1-page tailored resume:
- Rewrite objective to match this role
- Only include relevant skills and projects
- Prioritize matching experience bullet points
- Format: ATS-friendly, clean
- Output: Word document
```

**Update vault over time:**
```
"Append this new cert to certifications in Resume Builder: ..."
"Update only the ## KPMG section in my experience note with: ..."
"Search for 'Burp Suite' in Resume Builder"
```

---

## Personal Knowledge Base

```
"Search for everything about 'docker' in my Work Notes vault"
"Read my architecture note from Project X vault"
"Append today's standup to daily-log in Work Notes"
```

---

## Journaling

```
"Create a note called '2026-03-27' in my Journal vault with: ..."
"Read the last note I wrote in my Journal vault"
```

---

## Project Documentation

```
"Read the devlog from my Project X vault and summarize progress"
"Append this bug fix to the devlog in Project X: ..."
"Update only the ## Known Issues section in my devlog: ..."
```
