# How to Resume Work - Simple Guide

**Problem:** You lose track between sessions, I grab wrong files, work gets redone.

**Solution:** This file + CURRENT_STATE.md

---

## When Starting a New Claude Session

### Option 1: Just Tell Me to Read Current State

You say:
```
Read CURRENT_STATE.md and tell me where we are
```

I'll read it and tell you exactly where we left off.

### Option 2: Point Me Directly

You say:
```
We're working on [specific thing]. Read CURRENT_STATE.md first.
```

---

## When You Want to Save Your Spot

### Before Ending a Session

Say:
```
Update CURRENT_STATE.md with what we just did
```

I'll update the file with today's work so next session picks up clean.

---

## Files That Track State

1. **CURRENT_STATE.md** - Read this first every session
2. **MERGE_PLAN.md** - The plan for next big update (if we're doing one)
3. **git log** - Shows what was committed
4. **README.md** - Public-facing documentation

---

## What This Fixes

### Before:
- Me: "Let me search for the latest validation list..."
- Me: *Finds file from 2 weeks ago*
- Me: *Treats it as current*
- You: "That's not right, we updated that"
- Me: "Let me search again..."
- *Repeat forever*

### After:
- You: "Read CURRENT_STATE.md"
- Me: *Reads file*
- Me: "We're here, working on this, next step is that"
- You: "Correct, let's continue"
- *Actually makes progress*

---

## Example Session Start

**You:**
```
Hey Claude, read CURRENT_STATE.md and tell me where we left off
```

**Me:**
```
Reading CURRENT_STATE.md...

We just finished cleaning up the repo and pushing to GitHub yesterday.
You wanted to update the TFAcon.pdf title to make bolder dark matter claims
and add the Fermi LAT Galactic Center Excess section (D₂ = 1.42).

I created MERGE_PLAN.md with the full plan, but you were frustrated about
losing track between sessions.

What would you like to work on today?
```

**You:**
```
Let's do the title update. Do you have questions before we start?
```

**Me:**
```
Yes - do you have the LaTeX/Word source for TFAcon.pdf, or should I
create new source files?
```

*Clean conversation, no confusion, actual progress*

---

## When I Screw Up Anyway

If I start searching for old files or getting confused:

**You say:**
```
Stop. Read CURRENT_STATE.md. The answer is in there.
```

---

## Updating the System

### When Major Work Completes

```
Update CURRENT_STATE.md - we just finished [thing]
```

### When Starting New Work

```
Update CURRENT_STATE.md - we're starting [thing]
```

### When Stuck

```
Read MERGE_PLAN.md - remind me what we planned
```

---

## Simple Rules

1. **CURRENT_STATE.md** = Truth
2. **Ask me to read it** every session
3. **Tell me to update it** when work finishes
4. **Point me back to it** when I get confused

---

## That's It

No complex system. Just:
- One file with current status
- Read it at session start
- Update it when things change

Should fix the "searching through old files" problem.

---

**End of Guide**
