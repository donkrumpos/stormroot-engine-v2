#!/usr/bin/env python3
"""
Generate comprehensive documentation for the Denizen scripting system
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter

def load_analysis():
    """Load the analysis JSON file"""
    with open('docs/analysis.json', 'r') as f:
        return json.load(f)

def categorize_files():
    """Categorize all .dsc files by subsystem"""
    subsystems = defaultdict(list)

    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.dsc'):
                rel_path = os.path.relpath(os.path.join(root, file), '.')

                # Categorize based on path
                if 'skill_mechanics' in rel_path:
                    if 'mage_spells' in rel_path:
                        subsystems['Skills - Mage Spells'].append(rel_path)
                    elif 'prayer_spells' in rel_path:
                        subsystems['Skills - Prayer Spells'].append(rel_path)
                    elif 'song_spells' in rel_path:
                        subsystems['Skills - Song Spells'].append(rel_path)
                    elif 'specializations' in rel_path:
                        subsystems['Skills - Specializations'].append(rel_path)
                    elif 'natural_skills' in rel_path:
                        subsystems['Skills - Natural Skills'].append(rel_path)
                    elif 'debuffs' in rel_path or 'buffs' in rel_path:
                        subsystems['Skills - Status Effects'].append(rel_path)
                    else:
                        subsystems['Skills - Core Mechanics'].append(rel_path)
                elif 'npc' in rel_path:
                    subsystems['NPCs & Dialogue'].append(rel_path)
                elif 'creatures' in rel_path:
                    subsystems['Creatures & Mobs'].append(rel_path)
                elif 'items' in rel_path:
                    if 'weapon' in rel_path:
                        subsystems['Items - Weapons'].append(rel_path)
                    elif 'armor' in rel_path:
                        subsystems['Items - Armor'].append(rel_path)
                    elif 'currency' in rel_path:
                        subsystems['Economy - Currency Items'].append(rel_path)
                    else:
                        subsystems['Items - General'].append(rel_path)
                elif 'quest' in rel_path:
                    subsystems['Quests'].append(rel_path)
                elif 'region_specific' in rel_path:
                    subsystems['World & Regions'].append(rel_path)
                elif 'strongholds' in rel_path:
                    subsystems['Strongholds'].append(rel_path)
                elif 'dmodels' in rel_path:
                    subsystems['DModels (Visual)'].append(rel_path)
                elif rel_path in ['currency.dsc', 'equipment_handler.dsc']:
                    subsystems['Economy & Equipment'].append(rel_path)
                elif rel_path in ['reputation.dsc']:
                    subsystems['Reputation System'].append(rel_path)
                elif rel_path in ['first_spawn.dsc', 'general/world_loads.dsc']:
                    subsystems['Core - Server Lifecycle'].append(rel_path)
                elif rel_path in ['combat.dsc']:
                    subsystems['Combat System'].append(rel_path)
                else:
                    subsystems['Utilities & Misc'].append(rel_path)

    return dict(sorted(subsystems.items()))

def generate_system_map(data, subsystems):
    """Generate SYSTEM_MAP.md"""

    lines = [
        "# Denizen Scripting System Map",
        "",
        "**Generated:** Auto-analysis of 403+ .dsc files",
        "**Purpose:** High-level overview of the RPG system architecture",
        "",
        "---",
        "",
        "## Overview",
        "",
        "This is a **Minecraft RPG system** built on Denizen scripting. The codebase implements:",
        "- Custom skill/spell system (mage, prayer, song, specializations)",
        "- Economy with custom currency (copper/silver/gold/plat coins)",
        "- Equipment & inventory management",
        "- Combat mechanics with stats, attributes, debuffs",
        "- NPC dialogue & quest systems",
        "- Reputation & karma tracking",
        "- World regions & strongholds",
        "- Custom creature spawning with DModels",
        "",
        "---",
        "",
        "## Subsystems",
        ""
    ]

    # Build subsystem details
    for subsystem_name, files in subsystems.items():
        lines.append(f"### {subsystem_name}")
        lines.append("")
        lines.append(f"**Files:** {len(files)}")
        lines.append("")

        # Find events related to this subsystem
        subsystem_events = [e for e in data['events'] if any(f in e['file'] for f in files)]

        # Find calls
        subsystem_calls = [c for c in data['calls'] if any(f in c['file'] for f in files)]

        lines.append(f"**Event Handlers:** {len(subsystem_events)}")
        lines.append(f"**Script Calls:** {len(subsystem_calls)}")
        lines.append("")

        # Core files
        if len(files) <= 15:
            lines.append("**Core Scripts:**")
            for f in sorted(files)[:15]:
                lines.append(f"- `{f}`")
        else:
            lines.append("**Core Scripts:** (showing first 10)")
            for f in sorted(files)[:10]:
                lines.append(f"- `{f}`")
            lines.append(f"- _{len(files) - 10} more..._")

        lines.append("")

        # Key entry points
        if subsystem_events:
            entry_events = [e for e in subsystem_events if e['line'] < 50][:3]
            if entry_events:
                lines.append("**Entry Points:**")
                for evt in entry_events:
                    lines.append(f"- `{evt['event']}` in [{evt['file']}:{evt['line']}]({evt['file']}#L{evt['line']})")
                lines.append("")

        lines.append("---")
        lines.append("")

    # Cross-system dependencies
    lines.extend([
        "## Cross-System Dependencies",
        "",
        "### Critical Interconnections",
        "",
        "1. **game_loop.dsc** → All skill mechanics",
        "   - Runs 5x per second for all online players",
        "   - Executes `game_loop_task` which checks stamina, mana, buffs/debuffs",
        "   - Entry: `on delta time secondly` at [skill_mechanics/game_loop.dsc:5](skill_mechanics/game_loop.dsc#L5)",
        "",
        "2. **first_spawn.dsc** → Player initialization",
        "   - `on player logs in for the first time` → `give_starting_skills`",
        "   - Initializes stats, skills, attributes, reputation",
        "   - Entry: [first_spawn.dsc:5](first_spawn.dsc#L5)",
        "",
        "3. **equipment_handler.dsc** → Combat & Stats",
        "   - Manages armor/weapon equipping",
        "   - Affects combat damage calculations",
        "   - Links to currency system for item values",
        "",
        "4. **currency.dsc** → Economy & Items",
        "   - Custom coin system (copper/silver/gold/plat)",
        "   - Bank & purse inventories",
        "   - Used by NPCs, quests, shops",
        "",
        "5. **reputation.dsc** → World interactions",
        "   - Karma/fame system",
        "   - `on player kills entity` → reputation changes",
        "   - Affects NPC dialogue options",
        "",
        "---",
        "",
        "## Entry Points Summary",
        "",
        "### Server Startup",
        "- `on server prestart` in [general/world_loads.dsc:5](general/world_loads.dsc#L5)",
        "  - Creates custom worlds (rothigport_crypts, druvvenrog, underflame_abyss, etc.)",
        "",
        "### Player Join",
        "- `on player joins` in [first_spawn.dsc:16](first_spawn.dsc#L16)",
        "  - Sets permissions, teleports to spawn",
        "- `on player logs in for the first time` in [skill_mechanics/game_loop.dsc:19](skill_mechanics/game_loop.dsc#L19)",
        "  - Runs `give_starting_skills`",
        "",
        "### Game Loop (High Frequency)",
        "- `on delta time secondly` in [skill_mechanics/game_loop.dsc:5](skill_mechanics/game_loop.dsc#L5)",
        "  - Runs 5x per second per player",
        "  - **Performance critical** - any blocking operations here will lag the server",
        "",
        "---",
        "",
        "## Refactoring Recommendations",
        "",
        "### Potential Module Groupings",
        "",
        "1. **Core Player Systems**",
        "   - game_loop.dsc, first_spawn.dsc, equipment_handler.dsc, reputation.dsc",
        "   - High coupling, central to all features",
        "",
        "2. **Skills Module**",
        "   - All skill_mechanics/* (mage/prayer/song/specializations/natural)",
        "   - Already well-organized by directory",
        "",
        "3. **Economy Module**",
        "   - currency.dsc + items/currency/*",
        "   - Relatively independent, clear interface",
        "",
        "4. **Content Modules** (low coupling)",
        "   - NPCs, Quests, Regions, Strongholds",
        "   - Can be extracted/replaced easily",
        "",
        "5. **Combat Module**",
        "   - combat.dsc + debuffs + equipment_handler",
        "   - Medium coupling to stats/skills",
        "",
        "### High-Risk Refactor Areas",
        "",
        "- **game_loop.dsc**: Central nervous system - any changes affect everything",
        "- **Player flags/data**: Deeply embedded naming conventions throughout",
        "- **Equipment handler**: Tightly coupled to combat, stats, inventory UI",
        "",
        "---",
        "",
        f"**Total Scripts:** {len([f for files in subsystems.values() for f in files])}  ",
        f"**Total Subsystems:** {len(subsystems)}",
        ""
    ])

    with open('docs/SYSTEM_MAP.md', 'w') as f:
        f.write('\n'.join(lines))

    print("✓ Generated docs/SYSTEM_MAP.md")

def generate_data_keys(data):
    """Generate DATA_KEYS.md"""

    # Normalize and deduplicate keys
    key_info = defaultdict(lambda: {
        'type': set(),
        'scope': set(),
        'readers': set(),
        'writers': set(),
        'files': set(),
        'contexts': []
    })

    for entry in data['data_keys']:
        key = entry['key']
        key_info[key]['type'].add(entry['type'])
        key_info[key]['scope'].add(entry['scope'])
        key_info[key]['files'].add(entry['file'])

        # Determine if read or write
        context = entry['context'].lower()
        if 'read' in context or '<' in entry['context']:
            key_info[key]['readers'].add(entry['file'])
        if 'flag' in context or 'set' in context or 'yaml set' in context:
            key_info[key]['writers'].add(entry['file'])

        if len(key_info[key]['contexts']) < 3:
            key_info[key]['contexts'].append(entry['context'])

    lines = [
        "# Data Keys Index",
        "",
        "**Purpose:** Complete inventory of all flags, YAML keys, and persistent data structures.",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- **Total Unique Keys:** {len(key_info)}",
        f"- **Flag References:** {len([k for k in key_info if 'flag' in key_info[k]['type']])}",
        f"- **YAML References:** {len([k for k in key_info if 'yaml' in key_info[k]['type']])}",
        "",
        "---",
        ""
    ]

    # Group by domain
    domains = {
        'Player Skills': lambda k: k.startswith('player.flag.skill.'),
        'Player Stats': lambda k: k.startswith('player.flag.stat.'),
        'Player Reputation': lambda k: k.startswith('player.flag.reputation.'),
        'Player Class': lambda k: k.startswith('player.flag.class.'),
        'Player Score': lambda k: k.startswith('player.flag.score.'),
        'Player Equipment': lambda k: 'equipment' in k or 'weapon' in k or 'armor' in k,
        'Player Status': lambda k: 'status' in k or 'buff' in k or 'debuff' in k or 'hidden' in k or 'sprinting' in k,
        'Economy/Currency': lambda k: 'coin' in k or 'purse' in k or 'bank' in k or 'currency' in k,
        'Server Data': lambda k: k.startswith('server.') or k.startswith('yaml.'),
        'World/Region': lambda k: 'region' in k or 'world' in k or 'area' in k,
        'Quests': lambda k: 'quest' in k,
        'NPCs': lambda k: 'npc' in k,
        'Other': lambda k: True  # catch-all
    }

    for domain_name, predicate in domains.items():
        domain_keys = {k: v for k, v in key_info.items() if predicate(k)}

        if not domain_keys:
            continue

        lines.append(f"## {domain_name}")
        lines.append("")
        lines.append("| Key | Type | Scope | Readers | Writers | Notes |")
        lines.append("|-----|------|-------|---------|---------|-------|")

        for key in sorted(domain_keys.keys())[:50]:  # Limit to 50 per domain to avoid huge tables
            info = key_info[key]
            type_str = ', '.join(info['type'])
            scope_str = ', '.join(info['scope'])
            readers = len(info['readers'])
            writers = len(info['writers'])

            # Truncate key if too long
            display_key = key if len(key) < 40 else key[:37] + '...'

            # Sample context
            sample = info['contexts'][0] if info['contexts'] else ''
            sample = sample.replace('|', '\\|')[:40]

            lines.append(f"| `{display_key}` | {type_str} | {scope_str} | {readers} | {writers} | {sample} |")

        if len(domain_keys) > 50:
            lines.append(f"| ... | ... | ... | ... | ... | _{len(domain_keys) - 50} more keys in this domain_ |")

        lines.append("")

    # Warnings section
    lines.extend([
        "---",
        "",
        "## Warnings & Issues",
        "",
        "### Naming Inconsistencies",
        "",
    ])

    # Find potential duplicates (similar names)
    player_flags = [k for k in key_info if k.startswith('player.flag.')]
    flag_bases = defaultdict(list)
    for flag in player_flags:
        base = flag.replace('player.flag.', '').split('.')[0]
        flag_bases[base].append(flag)

    lines.append("**Flag Namespace Usage:**")
    for base, flags in sorted(flag_bases.items(), key=lambda x: -len(x[1]))[:10]:
        lines.append(f"- `{base}.*`: {len(flags)} flags")
    lines.append("")

    # Keys with many writers (potential race conditions)
    multi_writer_keys = [(k, len(v['writers'])) for k, v in key_info.items() if len(v['writers']) > 5]
    if multi_writer_keys:
        lines.append("### Keys with Many Writers (potential conflicts)")
        lines.append("")
        for key, count in sorted(multi_writer_keys, key=lambda x: -x[1])[:10]:
            lines.append(f"- `{key}`: {count} different files write to this")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Default Values & Initialization",
        "",
        "Most player flags are initialized in:",
        "- [skill_mechanics/game_loop.dsc](skill_mechanics/game_loop.dsc) - `give_starting_skills`",
        "  - Stats: `set_intial_stats_task`",
        "  - Skills: `set_initial_natural_skills_task`",
        "  - Attributes: `set_initial_attributes_task`",
        "  - Reputation: `set_initial_reputation_task`",
        "",
        "**Default patterns:**",
        "- Most skill levels default to `0`",
        "- Attribute levels default to `10`",
        "- Reputation karma/fame default to `1`",
        "",
    ])

    with open('docs/DATA_KEYS.md', 'w') as f:
        f.write('\n'.join(lines))

    print("✓ Generated docs/DATA_KEYS.md")

def generate_event_index(data):
    """Generate EVENT_INDEX.md"""

    lines = [
        "# Event Handler Index",
        "",
        f"**Total Event Handlers:** {len(data['events'])}",
        "",
        "---",
        "",
        "## Summary by Event Type",
        ""
    ]

    # Count event types
    event_types = Counter([e['event'] for e in data['events']])
    lines.append("| Event | Count | Files |")
    lines.append("|-------|-------|-------|")

    for event, count in event_types.most_common(20):
        files = len(set(e['file'] for e in data['events'] if e['event'] == event))
        lines.append(f"| `{event}` | {count} | {files} |")

    lines.extend([
        "",
        "---",
        "",
        "## High-Frequency Events (Performance Critical)",
        "",
        "These events run very frequently and should be optimized:",
        ""
    ])

    high_freq = [
        'delta time secondly',
        'player damages entity',
        'player damaged',
        'player clicks',
        'entity dies',
        'player moves'
    ]

    for evt_name in high_freq:
        handlers = [e for e in data['events'] if evt_name in e['event'].lower()]
        if handlers:
            lines.append(f"### `{evt_name}` ({len(handlers)} handlers)")
            lines.append("")
            for h in handlers:
                lines.append(f"- [{h['file']}:{h['line']}]({h['file']}#L{h['line']}) - `{h['event']}`")
            lines.append("")

    lines.extend([
        "---",
        "",
        "## Complete Event Index",
        "",
        "| File | Line | Event Type | Event Name |",
        "|------|------|------------|------------|"
    ])

    # Sort by file then line
    sorted_events = sorted(data['events'], key=lambda e: (e['file'], e['line']))

    for evt in sorted_events[:300]:  # Limit to 300 to keep file size reasonable
        file_link = f"[{evt['file']}:{evt['line']}]({evt['file']}#L{evt['line']})"
        evt_name = evt['event'][:60]  # Truncate long event names
        lines.append(f"| {file_link} | {evt['line']} | {evt['type']} | `{evt_name}` |")

    if len(sorted_events) > 300:
        lines.append(f"| ... | ... | ... | _{len(sorted_events) - 300} more events_ |")

    lines.append("")

    with open('docs/EVENT_INDEX.md', 'w') as f:
        f.write('\n'.join(lines))

    print("✓ Generated docs/EVENT_INDEX.md")

def generate_call_graph(data):
    """Generate CALL_GRAPH.md"""

    lines = [
        "# Call Graph & Script Dependencies",
        "",
        f"**Total Calls:** {len(data['calls'])}",
        "",
        "---",
        "",
        "## Summary",
        ""
    ]

    # Count call types
    call_types = Counter([c['type'] for c in data['calls']])
    lines.append("| Call Type | Count |")
    lines.append("|-----------|-------|")
    for call_type, count in call_types.items():
        lines.append(f"| `{call_type}` | {count} |")

    lines.append("")

    # Build call graph
    call_graph = defaultdict(lambda: {'calls': [], 'called_by': []})

    for call in data['calls']:
        caller = call['file']
        target = call['target']
        call_type = call['type']

        call_graph[caller]['calls'].append({
            'target': target,
            'type': call_type,
            'line': call['line']
        })
        call_graph[target]['called_by'].append({
            'caller': caller,
            'type': call_type,
            'line': call['line']
        })

    lines.extend([
        "---",
        "",
        "## Most Called Scripts",
        "",
        "Scripts that are frequently called by others:",
        "",
        "| Target Script | Times Called | Unique Callers |",
        "|---------------|--------------|----------------|"
    ])

    target_counts = defaultdict(int)
    target_callers = defaultdict(set)

    for call in data['calls']:
        target_counts[call['target']] += 1
        target_callers[call['target']].add(call['file'])

    for target, count in sorted(target_counts.items(), key=lambda x: -x[1])[:20]:
        unique_callers = len(target_callers[target])
        lines.append(f"| `{target}` | {count} | {unique_callers} |")

    lines.extend([
        "",
        "---",
        "",
        "## Scripts with Most Outbound Calls",
        "",
        "Scripts that call many other scripts (orchestrators):",
        "",
        "| Script | Outbound Calls | Unique Targets |",
        "|--------|----------------|----------------|"
    ])

    caller_counts = defaultdict(int)
    caller_targets = defaultdict(set)

    for call in data['calls']:
        caller_counts[call['file']] += 1
        caller_targets[call['file']].add(call['target'])

    for caller, count in sorted(caller_counts.items(), key=lambda x: -x[1])[:20]:
        unique_targets = len(caller_targets[caller])
        lines.append(f"| [{caller}]({caller}) | {count} | {unique_targets} |")

    lines.extend([
        "",
        "---",
        "",
        "## Call Chains by Subsystem",
        ""
    ])

    # Analyze call patterns within subsystems
    subsystems_of_interest = [
        ('skill_mechanics/game_loop.dsc', 'Game Loop'),
        ('first_spawn.dsc', 'Player Initialization'),
        ('currency.dsc', 'Economy System'),
        ('equipment_handler.dsc', 'Equipment System'),
        ('combat.dsc', 'Combat System')
    ]

    for script_file, subsystem_name in subsystems_of_interest:
        calls_from = [c for c in data['calls'] if c['file'] == script_file]

        if calls_from:
            lines.append(f"### {subsystem_name}")
            lines.append("")
            lines.append(f"**Source:** [{script_file}]({script_file})")
            lines.append("")
            lines.append("**Calls:**")

            for call in calls_from[:15]:
                lines.append(f"- `{call['type']}` → `{call['target']}` at line {call['line']}")

            if len(calls_from) > 15:
                lines.append(f"- _{len(calls_from) - 15} more calls..._")

            lines.append("")

    lines.extend([
        "---",
        "",
        "## Potential Issues",
        "",
        "### Circular Dependencies",
        "",
        "Scripts that call each other (potential infinite loops):",
        ""
    ])

    # Find circular calls
    circular = []
    for script_a in call_graph:
        for call in call_graph[script_a]['calls']:
            target = call['target']
            # Check if target calls back to script_a
            if any(c['target'] == script_a for c in call_graph.get(target, {}).get('calls', [])):
                if script_a < target:  # Avoid duplicates
                    circular.append((script_a, target))

    if circular:
        for a, b in circular[:10]:
            lines.append(f"- `{a}` ↔ `{b}`")
    else:
        lines.append("_No obvious circular dependencies detected (direct calls only)_")

    lines.append("")

    lines.extend([
        "### Deep Call Chains",
        "",
        "_Manual review recommended for:_",
        "- game_loop.dsc → game_loop_task → (multiple subsystems)",
        "- Any call chains deeper than 5 levels",
        "- Calls within high-frequency event handlers",
        "",
        "---",
        "",
        "## Call Graph Export",
        "",
        "For graph visualization, see `docs/analysis.json` which contains:",
        "- All calls with caller/target/line information",
        "- Can be imported into graph visualization tools",
        ""
    ])

    with open('docs/CALL_GRAPH.md', 'w') as f:
        f.write('\n'.join(lines))

    print("✓ Generated docs/CALL_GRAPH.md")

def main():
    print("Loading analysis data...")
    data = load_analysis()

    print("Categorizing files by subsystem...")
    subsystems = categorize_files()

    print("Generating documentation...")
    generate_system_map(data, subsystems)
    generate_data_keys(data)
    generate_event_index(data)
    generate_call_graph(data)

    print("\n" + "="*60)
    print("DOCUMENTATION GENERATION COMPLETE")
    print("="*60)
    print(f"\nTotal scripts scanned: {sum(len(files) for files in subsystems.values())}")
    print(f"Total event handlers: {len(data['events'])}")
    print(f"Total data keys indexed: {len(data['data_keys'])}")
    print(f"Total run/inject/task calls: {len(data['calls'])}")
    print(f"\nDocuments created:")
    print("  - docs/SYSTEM_MAP.md")
    print("  - docs/DATA_KEYS.md")
    print("  - docs/EVENT_INDEX.md")
    print("  - docs/CALL_GRAPH.md")
    print("\nReady for Stormroot mythic framework redesign!")

if __name__ == "__main__":
    main()
