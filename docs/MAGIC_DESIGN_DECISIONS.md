# Magic System Design Decisions

## Core Philosophy: Internal Power

**Decision**: Magic comes from within the mage, not external items.

**Rationale**: 
- Fits lore: mages are "attuned to Deluvia's leylines"
- Differentiates from item-based systems (wands, staves as primary)
- Makes magic feel like concentration and knowledge, not equipment
- Allows strategic choice: carry tools OR cast spells (empty hands required)

**Implementation**: 
- Empty main hand required for casting (concentration)
- Spellbook in offhand (represents knowledge, not power source)
- Weapons can be enchanted with spells as rare hybrid items (later)

---

## Mana as Fuel, Not Gate

**Decision**: Spells always castable regardless of mana. Power scales with available mana.

**Rationale**:
- More realistic: exhausted person can still act, just weakly
- Emergent gameplay: desperate low-mana casts vs waiting for full power
- Removes binary frustration of "can't cast"
- Creates risk/reward: cast now weakly or meditate and cast strong?

**Implementation**:
- Damage = base_damage × sqrt(current_mana / max_mana)
- Square root curve provides good feel: 
  - 100% mana = 100% damage
  - 25% mana = 50% damage
  - 1% mana = 10% damage
- Never truly zero, always some effect

**Rejected Alternatives**:
- Hard mana gates (too D&D-like, binary frustration)
- Linear scaling (too punishing at low mana)
- No mana system (wanted resource management strategy)

---

## Preparation System (D&D-Inspired)

**Decision**: Players prepare 9 spells for quick access, can know unlimited total spells.

**Rationale**:
- Strategic loadout choices (which 9 for this adventure?)
- Prevents choice paralysis (unlimited spells in combat)
- Fits lore: "studying up spells ahead of time"
- Uses Minecraft's 9 hotbar slots naturally
- Commands for 10+ spells = advanced invocations

**Implementation**:
- `/learn <spell>` - Adds to total knowledge
- `/prepare <spell>` - Assigns to next available slot (1-9)
- Hotbar slots 1-9 map to prepared spells
- `/cast <spell>` works for any known spell (slower, deliberate)

**Future Enhancement**: GUI for dragging spells into prepare slots

---

## Casting Mechanics: Simplicity Over Flash

**Decision**: Empty hand + spellbook in offhand + right-click = cast from current slot.

**What We Tried**:
1. Hotbar transformation (sigils replace items) - TOO COMPLEX
2. Right-click sigil items - Event conflicts
3. Detect number key presses - Unreliable event
4. Cycling through spells - Clunky UX

**What Worked**:
- Select slot (1-9) to choose spell
- Right-click with empty hand to cast
- Spellbook in offhand enables system
- Knowledge book (doesn't open like written book)

**Rationale**:
- Leverages Minecraft's existing hotbar muscle memory
- Fast combat: press number, right-click, boom
- No complex inventory swapping
- Clear enable/disable: equip/unequip book
- Offhand is underutilized in vanilla

**Trade-offs**:
- No visual spell indicators on hotbar (MVP - add later)
- Requires empty hand (can't cast while holding torch)
- Must remember which slot = which spell (later: action bar display)

---

## Meditation: Risk vs Reward

**Decision**: Stand still + sneak = 3x mana regen. Movement breaks meditation.

**Rationale**:
- Tactical choice: safety vs speed
- Feels like concentration (standing still)
- Uses sneak (underutilized mechanic)
- Vulnerable while meditating (can't move)
- Location-based decision: "Is it safe to meditate here?"

**Implementation**:
- Normal regen: 0.33 mana/sec (20/min)
- Meditation regen: 1.0 mana/sec (60/min)
- Tracks location each tick, breaks if moved
- 5 Hz check rate (responsive but not tick-heavy)

**Future Enhancement**: 
- Meditation skill affects regen multiplier
- Cooldown after breaking (prevent gaming system)
- Visual effects (particles, posture change)

---

## No UI Philosophy

**Decision**: Minimize HUD elements. Feedback through gameplay feel.

**Rationale**:
- Stormroot principle: diegetic, immersive
- "In real life, you don't see a mana bar"
- Forces player awareness and estimation
- More atmospheric, less gamey

**Current Feedback Methods**:
- Chat messages (temporary MVP approach)
- Damage numbers show effectiveness
- Spell sound/visuals scale with power
- Failure states feel different (weak fizzle vs strong blast)

**Planned Feedback (Non-UI)**:
- Particle aura around hands (fades with low mana)
- Breathing sounds (heavier when exhausted)
- Screen effects (slight blur/darkness at very low mana)
- Movement slowdown at critical mana
- Spell visuals shrink/fade when weak

**Where UI May Be Needed**:
- Action bar for current spell name (minimal, contextual)
- Boss bar for major buffs/debuffs (optional toggle)
- Spell preparation GUI (out-of-combat, acceptable)

---

## Event-Driven, Not Tick-Based

**Decision**: Use `delta time secondly` + events, avoid `while true` loops.

**Rationale**:
- Performance: 5 Hz is sufficient for mana regen
- Responsiveness: Events fire instantly on player action
- Stability: Loops can block event processing
- Maintainability: Event-driven is easier to debug

**Implementation**:
- Mana regen: `delta time secondly` running 5x per second
- Casting: `on player right clicks` event
- Meditation: Location check per mana tick (5 Hz)
- Cooldowns: Denizen's auto-expiring flags

**Lessons Learned**:
- `while true` caused event blocking (bad)
- Per-tick loops are overkill for most mechanics
- 5 Hz hits sweet spot: responsive + performant

---

## Data-Driven Spell Definitions

**Decision**: All spell properties in external YAML data file.

**Rationale**:
- Non-coders can balance spells
- Easy to add new spells without touching logic
- Centralized spell database
- Version control friendly
- Modding support

**Spell Schema**:
```yaml
spell_name:
    mana_cost: number
    base_damage: number
    damage_type: string
    display_name: string
    cooldown: seconds
```

**Future Additions**:
- Range, AOE, duration
- Prerequisites, difficulty
- Particle/sound effects
- Target type (single/aoe/self/linear)
- Damage type percentages (70% fire, 30% energy)

---

## Cooldowns: Prevent Spam, Enable Strategy

**Decision**: Individual cooldowns per spell, not global cooldown.

**Rationale**:
- Spell identity (spark = spammable, meteor = rare)
- Encourages spell variety in combat
- No "optimal rotation" - situational choices
- Balances powerful spells (high cost + long cooldown)

**Implementation**:
- Stored as expiring flags
- Checked before cast, refuse if active
- Display time remaining
- Independent per spell

**Balance Targets**:
- Cheap spells: 0.5-2s cooldown
- Medium spells: 2-4s cooldown
- Expensive spells: 4-8s cooldown
- Ultimate spells: 30-60s cooldown

---

## MVP Philosophy: Fast Core, Gradual Complexity

**Decision**: Build working core first, add features incrementally.

**Rationale**:
- Validate core loop before expanding
- Avoid scope creep paralysis
- Get playtesting feedback early
- Each feature builds on stable foundation
- Easy to identify what's fun vs what's bloat

**MVP Scope**:
- ✅ Mana system
- ✅ 4 spells with variety
- ✅ Preparation/casting
- ✅ Cooldowns
- ✅ Meditation

**Deferred to Post-MVP**:
- Visual hotbar transformation
- Skill progression
- Equipment bonuses
- Particle effects
- Sound polish
- Elemental system integration

**Next Session Priority**:
1. Playtest existing mechanics
2. Balance pass on costs/cooldowns
3. Add ONE new feature from backlog
4. Iterate based on feel

---

## Design Questions Still Open

1. **Spell Acquisition**: Buy from NPCs? Find scrolls? Quest rewards? Skill points?
2. **Class Gating**: Should warriors be able to meditate? How to prevent?
3. **Progression Rate**: How fast should spell mastery increase?
4. **Visual Language**: What should high-level magic look like vs low-level?
5. **Ritual Magic**: How should multi-player combined casting work?
6. **Environmental Magic**: Leylines, time of day, weather effects?
7. **Spell Schools**: Should spells be organized by element/discipline?
8. **Failure States**: Should low skill cause backfires? Fizzles?

---

## Integration with Stormroot

**Alignment with Core Principles**:

**Elegance**: 
- Mana curve in one line: `sqrt(current/max)`
- Preparation system uses native hotbar
- Event-driven, not loop-heavy

**Immersion**:
- No mana bars
- Magic from within, not items
- Meditation requires vulnerability
- Empty hands = concentration

**Modularity**:
- Data-driven spell definitions
- Reusable cast_spell_task
- Separate files for data vs logic
- Easy to extend with new spells

**Lore Coherence**:
- Leyline attunement (mana source)
- Knowledge-based (spellbook = study)
- Preparation = memorization
- Power scales with resources

**Performance**:
- 5 Hz tick rate
- Event-driven casting
- No per-tick loops
- Flag-based cooldowns

**Next Phase Connection**:
- Elements system: Tie spell types to elements.yml
- Strongholds: Leyline nodes provide mana bonuses
- Ecology: Seasonal magic power fluctuations
- Ritual: Multi-player spell combinations
