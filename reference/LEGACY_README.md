# Legacy Code Reference

This folder contains working code from 3 years ago. **DO NOT USE DIRECTLY.**

These files are preserved for:
- Pattern reference (event handling, bind system)
- Solutions to problems we might encounter again
- Understanding what worked in production
- Historical context

## What's Here

- `magic_handler_legacy.dsc` - Original spell binding/casting system
- `game_loop_legacy.dsc` - 5Hz game loop with mana/meditation
- `spells_data_legacy.dsc` - Full spell database with all properties

## What to Use Instead

See `/scripts/magic_system.dsc` for current clean implementation.

## When to Reference This

✅ "How did I handle X before?"
✅ "What event did I use for Y?"
✅ "How did the bind system work?"

❌ Don't copy/paste large chunks
❌ Don't use as starting point (it's complex)
❌ Current code is intentionally simpler
```

**Why this helps:**
- ✅ Claude Code can reference specific patterns when you say "check how I did bind system in legacy code"
- ✅ Clearly separated (won't accidentally use old code)
- ✅ Historical wisdom preserved
- ✅ Good for "I know I solved this before..."
- ✅ Shows evolution of your thinking

**Update CLAUDE.md to mention it:**

Add to the File Structure section:
```
/reference/
  magic_handler_legacy.dsc  - OLD working implementation (DO NOT USE DIRECTLY)
  LEGACY_README.md          - Explains legacy code purpose