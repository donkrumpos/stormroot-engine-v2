# Stormroot Engine v2 - Magic System

## Project Overview

This is a Minecraft MMORPG using Denizen scripting to create custom game mechanics. The project emphasizes **immersion, modularity, and ecological design** - replacing traditional fantasy tropes with Miyazaki-style animism and natural interconnected systems.

## Current Focus: Magic System (MVP Complete)

We've built a working magic system with:
- Mana-based spellcasting (INT × 2 = max mana)
- Damage scaling with mana curve (sqrt function)
- Meditation mechanics (3x regen when still + sneaking)
- Slot-based spell preparation (9 quick-access spells)
- Spellbook item (offhand) enables casting
- Empty hand + right-click = cast spell
- 4 test spells with cooldowns

**Status:** Working MVP, ready for playtesting/iteration

## File Structure

```
/docs/
  MAGIC_SYSTEM_STATUS.md      - Current state, what's working, known issues
  MAGIC_DESIGN_DECISIONS.md   - Architecture rationale and philosophy
  MAGIC_QUICK_START.md        - How to resume development
  MAGIC_SYSTEM_TODO.md        - Feature backlog prioritized

/scripts/ (Denizen scripts - typically in server/plugins/Denizen/scripts/)
  magic_system.dsc            - Main implementation (see conversation history)
  spell_data.dsc              - Data-driven spell definitions
  
/reference/
  Events___Denizen_Meta_Documentation.html  - Denizen event reference
  Stormroot_Engine_v2___DESIGN_DECISIONS.md - Core project philosophy
  elements_map.md             - Elemental system design
```

## Key Design Principles

1. **Elegance** - Minimal code expressing deep systems
2. **Immersion** - Low-UI, diegetic feedback, natural metaphors
3. **Modularity** - Data-driven YAML schemas, small composable tasks
4. **Lore Coherence** - Every mechanic has symbolic weight
5. **Performance** - Event-driven logic, no per-tick loops

### Magic System Specific

- **Magic from within** - Power from mage's attunement, not items
- **Always castable** - Mana = fuel/stamina, not gate (low mana = weak spell)
- **No UI philosophy** - Minimal HUD, feedback through gameplay feel
- **Strategic** - Resource management, preparation choices matter
- **Fast MVP** - Core loop first, gradual complexity

## Technology Stack

- **Platform:** Minecraft (Spigot/Paper server)
- **Scripting:** Denizen (YAML-based scripting language)
- **Version Control:** Git
- **Documentation:** Markdown

## Denizen Quick Reference

### Script Types
- `command` - Player commands (/cast, /learn)
- `task` - Reusable logic blocks
- `world` - Event listeners
- `data` - Configuration/definitions
- `procedure` - Functions that return values
- `item` - Custom item definitions

### Common Patterns
```yaml
# Command
command_name:
    type: command
    name: commandname
    description: What it does
    script:
    - narrate "Hello!"

# World Event
event_handler:
    type: world
    events:
        on player right clicks:
        - narrate "Clicked!"

# Task
task_name:
    type: task
    definitions: arg1|arg2
    script:
    - narrate <[arg1]>
```

### Key Tags
- `<player>` - Current player
- `<context.X>` - Event-specific data
- `<player.flag[name]>` - Persistent player data
- `<script[name].data_key[path]>` - Read data files
- `<player.item_in_hand>` - What player holds
- `<player.item_in_offhand>` - Offhand item
- `<player.target>` - What player looks at

## Common Tasks

### Testing Changes
```bash
# In Minecraft console or as OP player:
/ex reload          # Reload all scripts
/ex run <script>    # Run a specific task

# Test magic system:
/magicsetup        # Initialize player stats
/learn fireball    # Learn a spell
/prepare fireball  # Prepare for slot 1
/spellbook         # Get spellbook in offhand
# Press 1, right-click with empty hand
```

### Debugging
```bash
/ex debug true     # Enable debug output (VERY verbose)
/ex debug false    # Disable debug output
/ex flag player    # View all player flags
/ex narrate <tag>  # Test a tag evaluation
```

### Adding a New Spell

1. Edit `spell_data.dsc`:
```yaml
new_spell:
    mana_cost: 10
    base_damage: 20
    damage_type: fire
    display_name: "New Spell"
    cooldown: 3.0
```

2. Reload: `/ex reload`
3. Test: `/learn new_spell` → `/prepare new_spell`

## Known Issues

- Console spam from debug traces (harmless, run `/ex debug false`)
- Meditation can be gamed by brief movement (needs cooldown)
- No visual spell indicators on hotbar (MVP - polish later)
- Spellbook can be lost (should be blessed/permanent)

## Development Workflow

1. **Read status docs** - Understand current state
2. **Choose ONE feature** - From TODO.md, don't add multiple
3. **Discuss approach** - Before coding, ask about design
4. **Test incrementally** - Change one thing, test, repeat
5. **Update docs** - Keep STATUS.md current
6. **Git commit** - Working states before experimenting

## Anti-Patterns to Avoid

❌ `while true` loops - Blocks event processing  
❌ Per-tick updates - Use `delta time` instead  
❌ Hardcoded values - Use data files  
❌ Multiple features at once - MVP mentality  
❌ Copying old complex code - Simplify for MVP  
❌ UI-heavy feedback - Prefer diegetic methods  

## What We Tried That Didn't Work

- Hotbar transformation (complex event conflicts)
- `on player holds item` event (unreliable)
- `while true` mana regen loop (blocked events)
- Written book as spellbook (opens on right-click)
- Detecting number key presses directly (no reliable event)

## What Works Well

- Knowledge book in offhand (doesn't open)
- Empty hand casting (feels like concentration)
- Delta time events (5 Hz for smooth updates)
- Right-click detection with item flags
- Slot-based preparation (natural hotbar use)
- Sqrt curve for damage scaling (good feel)

## Next Steps (Priority Order)

1. **Playtest & Balance** - Tune costs, cooldowns, damage
2. **Visual Effects** - Particles that scale with power
3. **Sound Polish** - Fix meditation sound, add spell sounds
4. **Spell Progression** - Spells level up with use
5. **Equipment Bonuses** - Staves/robes affect stats

See MAGIC_SYSTEM_TODO.md for complete backlog.

## Integration Points (Future)

- **Elements System** - Tie spells to elements.yml (fire/water/earth/air)
- **Strongholds** - Leyline nodes provide mana bonuses
- **Time/Season** - Environmental magic effects
- **Ritual Casting** - Multi-player spell combinations
- **Class System** - Gate magic to specific classes

## Questions for Design Decisions

- How should players learn new spells? (NPCs, scrolls, quests?)
- Should non-mages be able to meditate?
- How fast should spell mastery progress?
- What should high-level magic look like visually?
- How do enchanted weapons with spells work?

## Getting Help

**Read first:**
1. MAGIC_SYSTEM_STATUS.md - Current state
2. MAGIC_DESIGN_DECISIONS.md - Why we made choices
3. This file - How to work with project

**When stuck:**
- Check Events documentation for correct event syntax
- Reference old working code for patterns
- Ask about approach before implementing
- Test one change at a time

## Success Criteria

Magic system is good when:
✅ Casting feels responsive and satisfying  
✅ Mana management creates meaningful choices  
✅ Players learn slot locations naturally  
✅ Low mana = tension, not frustration  
✅ Meditation timing is tactical  
✅ Different spells have distinct use cases  
✅ Easy to add new spells (data-driven)  

---

**Philosophy:** Build mythic, ecological RPG systems that feel hand-crafted and alive. Magic isn't D&D mechanics - it's attunement to natural forces. Every system should have symbolic weight and interconnect with the world.

**Approach:** Elegant, minimal code. Immersive feedback. Event-driven performance. One feature at a time. Always ask: "Does this serve the core vision?"
