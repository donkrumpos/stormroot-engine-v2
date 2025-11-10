# Magic System - Features Backlog

## ✅ Completed (MVP)
- [x] Player stats (Intelligence → Max Mana)
- [x] Spell data system
- [x] Learn spells command
- [x] Cast command with mana cost
- [x] Mana curve (power scales with current mana)
- [x] Passive mana regeneration
- [x] Meditation (3x regen when still + sneaking)
- [x] Multiple spells (spark, fireball, lightning, meteor)
- [x] Spell cooldowns

## 🔥 High Priority (Core Mechanics)
- [ ] **Spell skill progression** - Spells level up with use, affecting damage/efficiency
- [ ] **Magic skill efficiency** - Higher skill = more damage per mana spent
- [ ] **Bind spells to hotbar** - Right-click casting instead of commands
- [ ] **Visual spell effects** - Particles scale with power/skill level
- [ ] **Sound effects** - Fix meditation sound, add spell-specific sounds

## 🎯 Medium Priority (Polish & Balance)
- [ ] **Meditation cooldown** - Prevent instant re-meditation after moving
- [ ] **Meditation reduces cooldowns** - Recovery tool for both mana + spell availability
- [ ] **Elemental resistances** - Targets resist damage types based on stats
- [ ] **Equipment bonuses** - Staves/wands/armor affect mana/regen/damage
- [ ] **Casting time** - Buildup before spell fires (interruptible)
- [ ] **Spell interruption** - Taking damage cancels casting

## 🌟 Advanced Features (Later)
- [ ] **Area of Effect spells** - Multiple targets
- [ ] **Projectile spells** - Physical travel time
- [ ] **Buff/Debuff spells** - Status effects
- [ ] **Channeled spells** - Continuous mana drain for sustained effects
- [ ] **Spell combinations** - Cast multiple elements for hybrid effects
- [ ] **Mana burn mechanics** - Casting at very low mana has consequences
- [ ] **Different magic schools** - Necromancy, Divine, Elemental specialization
- [ ] **Spell prerequisites** - Must learn basic before advanced

## 🎨 Immersion (No UI Philosophy)
- [ ] **Particle aura** - Visual mana state indicator around hands
- [ ] **Audio breathing** - Breathing sounds based on mana level
- [ ] **Physical feedback** - Movement speed affected by mana depletion
- [ ] **Spell visual degradation** - Weak spells look weaker (smaller particles, less sound)
- [ ] **Screen effects** - Subtle vision effects at low mana

## 🔧 Technical Improvements
- [ ] **Refactor into multiple files** when system grows large:
  - `magic_core.dsc` - damage calculation, spell execution
  - `magic_commands.dsc` - cast, learn, bind, unbind
  - `magic_mana.dsc` - regeneration, meditation
  - `magic_progression.dsc` - skill leveling, unlocks
- [ ] **Optimize tick rate** - Consider your old 5Hz game loop approach
- [ ] **Class system integration** - Non-mages shouldn't meditate

## 💡 Ideas to Explore
- [ ] Different meditation types (sitting vs standing)
- [ ] Mana potions/items
- [ ] Spell scrolls/books that teach spells
- [ ] Ritual casting (multiple players combine power)
- [ ] Environmental factors (casting in rain/night affects power)
- [ ] Mana wells/ley lines (location-based mana bonuses)

---

## Notes
- Keep MVP mindset: one feature at a time, fully tested before moving on
- Playtest core loop before adding complexity
- Remember: mana = fuel/stamina, skill = training/mastery
- Design philosophy: always castable, power scales with resources
