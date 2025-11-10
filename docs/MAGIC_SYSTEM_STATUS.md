# Magic System - Current Status & Next Steps

## ✅ What's Working (MVP Complete)

### Core Mechanics
- **Player Stats**: Intelligence determines max mana (INT × 2)
- **Mana System**: Depletes on cast, never blocks casting (always castable)
- **Mana Curve**: Damage scales with current mana using sqrt curve (100% mana = 100% damage, 10% mana = 32% damage)
- **Passive Regen**: 0.33 mana/second (20/min) using delta time (5 Hz tick rate)
- **Meditation**: Sneak + stand still = 3x regen (1 mana/sec = 60/min)
- **Spell Learning**: `/learn <spell>` command
- **Spell Preparation**: `/prepare <spell>` - up to 9 spells in quick-access slots
- **Spellbook**: Knowledge book item in offhand enables casting
- **Casting Method**: Empty hand + spellbook in offhand + right-click = cast spell from current hotbar slot
- **Cooldowns**: Per-spell cooldowns prevent spam
- **Multiple Spells**: Spark (2 mana, 3 dmg), Fireball (5 mana, 10 dmg), Lightning (8 mana, 15 dmg), Meteor (15 mana, 30 dmg)

### Files
- `magic_system.dsc` - Complete working implementation
- `spell_data.dsc` - Data-driven spell definitions
- `MAGIC_SYSTEM_TODO.md` - Feature backlog

## 🎯 Design Philosophy Established

1. **Magic comes from within** - Power is from the mage's attunement to leylines, not items
2. **Always castable** - Mana is fuel/stamina, not a gate. Low mana = weak spell, not blocked spell
3. **No UI philosophy** - Minimal HUD, diegetic feedback preferred
4. **Strategic resource management** - Players choose when to conserve vs expend mana
5. **Fast MVP, gradual complexity** - Build core loop first, add features incrementally

## 🔧 Technical Lessons Learned

### What Works
- Data-driven spell definitions in separate files
- Delta time events (5 Hz) for smooth updates without per-tick loops
- Event-driven casting detection (right-clicks)
- Simple flag-based spell preparation
- Sqrt curve for damage scaling feels natural

### What Didn't Work
- Hotbar transformation (too complex, event conflicts)
- `while true` loops (blocks event processing)
- `on player holds item` event (unreliable)
- Written book as spellbook (opens on right-click)
- Trying to detect number key presses directly

### Solution That Works
- Knowledge book in offhand (doesn't open)
- Empty hand casting (feels like concentration)
- Slot-based preparation (press 1-9 to select, right-click to cast)
- No visual transformation for MVP (add later as polish)

## 🚀 Immediate Next Steps

### High Priority
1. **Playtest the core loop** - Cast spells, manage mana, test feel
2. **Balance pass** - Adjust costs, cooldowns, damage values based on gameplay
3. **Visual feedback** - Add particle effects that scale with power
4. **Sound polish** - Fix meditation sound, add spell-specific sounds

### Quick Wins (30-60 min each)
- Spell skill progression (spells level up with use)
- Equipment bonuses (staves, robes affect mana/regen)
- More spell variety (AOE, buffs, utility)
- Casting time/buildup (interruptible casting)

### Longer Features
- Hotbar visual transformation (sigils appear when book equipped)
- Magic skill system (efficiency improvements)
- Elemental resistances
- Spell combinations

## 🐛 Known Issues

- Console spam from debug traces (harmless but annoying)
- Meditation cooldown needed (can game the system by moving briefly)
- No visual indicator of prepared spells (just have to remember)
- Spellbook can be lost (should be blessed/permanent)

## 📝 Design Questions for Next Session

1. **Class system integration** - Should non-mages be able to meditate? How to gate magic?
2. **Spell acquisition** - How should players learn spells? (NPCs, scrolls, quests?)
3. **Progression curve** - How fast should spells level up? Linear or exponential?
4. **Visual style** - Custom model data for sigils? Particle colors per element?
5. **Weapon integration** - How should enchanted weapons with embedded spells work?

## 🎨 Stormroot Integration Notes

The magic system aligns with Stormroot's core principles:
- **Ecological**: Mana as natural energy, meditation as attunement
- **Minimal UI**: No mana bars, feedback through gameplay feel
- **Symbolic weight**: Each spell type represents elemental forces
- **Interconnected**: Magic skill affects efficiency (planned)
- **Event-driven**: No tick loops, responds to player actions

Next phase should explore:
- Tying spells to elemental system (fire/water/earth/air)
- Leyline locations (environmental mana bonuses)
- Ritual casting (multiple players combine power)
- Seasonal/time-of-day effects on magic

## 💬 Prompt for Next Chat

"Continue building Stormroot's magic system. We have a working MVP with mana, spells, meditation, and slot-based casting. See MAGIC_SYSTEM_STATUS.md for current state. Ready to add [next feature from TODO] or playtest and refine what we have."
