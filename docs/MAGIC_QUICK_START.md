# Magic System - Quick Start Guide

## For Next Chat Session

### Context Files to Read
1. **MAGIC_SYSTEM_STATUS.md** - Current state, what's working, known issues
2. **MAGIC_DESIGN_DECISIONS.md** - Why we made the choices we did
3. **MAGIC_SYSTEM_TODO.md** - Feature backlog prioritized

### Working Files
- `magic_system.dsc` - Complete implementation (in conversation history)
- `spell_data.dsc` - Spell definitions (in conversation history)

### How to Resume

**If continuing from this chat:**
```
"I want to continue building the magic system. [Pick one:]
- Let's playtest what we have and refine it
- Add [feature from TODO] next
- I have feedback from testing: [describe]"
```

**If starting fresh chat:**
```
"Continue building Stormroot's magic system. We have a working MVP with:
- Mana system with curve-based damage scaling
- Spell preparation (9 quick-access slots)
- Spellbook casting (offhand book + empty hand + right-click)
- Meditation for faster regen
- 4 test spells with cooldowns

See uploaded MAGIC_SYSTEM_STATUS.md for full details.

Ready to: [choose one]
1. Playtest and balance existing mechanics
2. Add visual effects (particles, sounds)
3. Implement spell progression system
4. Build hotbar visual transformation
5. Other: [describe]"
```

### Test Sequence (To Verify System)

```bash
# In Minecraft:
/ex reload
/magicsetup
/learn fireball
/learn spark
/prepare fireball
/prepare spark
/spellbook

# Should now have knowledge book in offhand
# Press 1 (select slot 1 = fireball)
# Aim at mob, right-click with empty hand
# Should cast fireball

# Press 2 (select slot 2 = spark)
# Right-click again
# Should cast spark

# Meditate: Hold shift, stand still
# Should see "You begin to meditate..."
# Mana regens 3x faster

# Move while meditating
# Should see "You stop meditating."
```

### Common Issues & Fixes

**"Spell doesn't cast":**
- Is main hand empty?
- Is spellbook in offhand?
- Did you prepare the spell?
- Check console for errors

**"Can't learn spell":**
- Check spell_data.dsc loaded: `/ex script spell_data`
- Verify spell name matches exactly (lowercase)

**"Mana not regenerating":**
- Check delta time event running
- Look for errors in console
- Verify `/magicsetup` was run

**"Console spam":**
- Run `/ex debug false`
- Not breaking functionality, just noisy

### Development Principles

When adding features, remember:
1. **Playtest first** - Does current system feel good?
2. **One feature at a time** - Don't add 3 things at once
3. **MVP mentality** - Simplest version that works
4. **Ask before building** - Discuss approach before coding
5. **Scope discipline** - Resist feature creep

### Next Feature Decision Matrix

**If magic feels weak/boring:**
→ Add more spell variety or visual effects

**If combat is spammy:**
→ Add casting time/buildup mechanics

**If progression feels flat:**
→ Implement spell leveling system

**If resource management is trivial:**
→ Tune mana costs and regen rates

**If system is working well:**
→ Integrate with other Stormroot systems (elements, strongholds)

### Files You'll Need

From conversation history:
- Complete `magic_system.dsc` 
- Complete `spell_data.dsc`
- Working commands: magicsetup, learn, prepare, spellbook
- Working mana regen with meditation
- Working casting detection

From outputs folder:
- MAGIC_SYSTEM_STATUS.md
- MAGIC_DESIGN_DECISIONS.md  
- MAGIC_SYSTEM_TODO.md

### Project Context

This magic system is the first major mechanic for Stormroot Engine v2. Design principles:
- Ecological (mana as natural energy)
- Immersive (minimal UI)
- Modular (data-driven)
- Symbolic (elemental forces)
- Performant (event-driven)

Magic should eventually connect to:
- **Elements system** (elements_map.md) - Spell types
- **Strongholds** - Leyline nodes
- **Time/Season** - Environmental effects
- **Ritual casting** - Multi-player mechanics

### Pro Tips

- Use `/ex reload` after every script change
- Test incrementally (don't change 5 things then test)
- Keep conversation focused on ONE feature
- Reference design docs when making choices
- Git commit working states before experimenting
- Ask "does this serve the core vision?" before adding

### Success Metrics

You'll know the system is good when:
- Casting feels responsive and satisfying
- Mana management creates meaningful choices
- Players learn spell locations naturally (muscle memory)
- Low mana creates tension, not frustration
- Meditation timing is a tactical decision
- Different spells have distinct use cases
- System is extensible (easy to add spells)

---

**Ready to build!** 🔥⚡🌊
