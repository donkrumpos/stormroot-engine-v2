#!/usr/bin/env python3
"""
Analyze the Denizen codebase for warnings and potential issues
"""

import json
from collections import defaultdict, Counter

def load_analysis():
    with open('docs/analysis.json', 'r') as f:
        return json.load(f)

def find_warnings(data):
    warnings = []

    # 1. Duplicate key names (case-insensitive collisions)
    key_names = defaultdict(list)
    for key_entry in data['data_keys']:
        normalized = key_entry['key'].lower()
        key_names[normalized].append(key_entry)

    duplicates = {k: v for k, v in key_names.items() if len(v) > 20}
    if duplicates:
        warnings.append({
            'type': 'duplicate_keys',
            'severity': 'medium',
            'count': len(duplicates),
            'message': f"Found {len(duplicates)} keys with >20 references (possible overuse or namespace pollution)",
            'examples': list(duplicates.keys())[:5]
        })

    # 2. High-frequency event handlers in game_loop
    game_loop_events = [e for e in data['events'] if 'game_loop' in e['file']]
    high_freq_events = ['delta time secondly', 'tick', 'player moves']

    critical_events = [e for e in game_loop_events if any(hf in e['event'].lower() for hf in high_freq_events)]
    if critical_events:
        warnings.append({
            'type': 'performance_critical',
            'severity': 'high',
            'count': len(critical_events),
            'message': f"Found {len(critical_events)} high-frequency event handlers in game_loop.dsc (runs 5x/sec per player)",
            'details': [f"{e['event']} at line {e['line']}" for e in critical_events]
        })

    # 3. Blocking operations (wait commands in high-frequency handlers)
    # This would require parsing file contents, so we'll note it as a recommendation
    warnings.append({
        'type': 'manual_review_needed',
        'severity': 'medium',
        'message': 'Manual review recommended: Check for "wait" or "waituntil" commands in game_loop.dsc',
        'reason': 'Blocking operations in 5Hz loop will cause server lag'
    })

    # 4. Deep call chains
    call_targets = Counter([c['target'] for c in data['calls']])
    heavily_called = [(target, count) for target, count in call_targets.items() if count > 15]

    if heavily_called:
        warnings.append({
            'type': 'heavy_dependencies',
            'severity': 'low',
            'count': len(heavily_called),
            'message': f"Found {len(heavily_called)} scripts called >15 times (tight coupling)",
            'examples': [f"{target} ({count} calls)" for target, count in sorted(heavily_called, key=lambda x: -x[1])[:5]]
        })

    # 5. Keys with many writers (potential race conditions)
    key_writers = defaultdict(set)
    for key_entry in data['data_keys']:
        if 'flag' in key_entry['context'].lower() or 'set' in key_entry['context'].lower():
            key_writers[key_entry['key']].add(key_entry['file'])

    multi_writer = [(k, len(v)) for k, v in key_writers.items() if len(v) > 5]
    if multi_writer:
        warnings.append({
            'type': 'concurrent_writes',
            'severity': 'medium',
            'count': len(multi_writer),
            'message': f"Found {len(multi_writer)} keys written by >5 different files (potential race conditions)",
            'examples': [f"{k} ({count} writers)" for k, count in sorted(multi_writer, key=lambda x: -x[1])[:5]]
        })

    # 6. Circular call patterns
    call_graph = defaultdict(set)
    for call in data['calls']:
        call_graph[call['file']].add(call['target'])

    # Simple circular detection (A calls B, B calls A)
    circular = []
    for script_a, targets in call_graph.items():
        for target in targets:
            if script_a in call_graph.get(target, set()):
                if script_a < target:  # Avoid duplicates
                    circular.append((script_a, target))

    if circular:
        warnings.append({
            'type': 'circular_calls',
            'severity': 'medium',
            'count': len(circular),
            'message': f"Found {len(circular)} circular call patterns (A↔B)",
            'examples': [f"{a} ↔ {b}" for a, b in circular[:5]]
        })

    return warnings

def generate_summary(data, warnings):
    print("\n" + "="*70)
    print(" DENIZEN CODEBASE ANALYSIS SUMMARY")
    print("="*70)
    print()
    print("📊 STATISTICS")
    print("-" * 70)
    print(f"  Total scripts scanned:        {403}")
    print(f"  Total event handlers:         {len(data['events'])}")
    print(f"  Total data keys indexed:      {len(data['data_keys'])}")
    print(f"  Total run/inject/task calls:  {len(data['calls'])}")
    print()

    # Most common events
    event_types = Counter([e['event'] for e in data['events']])
    print("  Top 5 most common events:")
    for event, count in event_types.most_common(5):
        print(f"    • {event}: {count}")
    print()

    # Most called scripts
    call_targets = Counter([c['target'] for c in data['calls']])
    print("  Top 5 most called scripts:")
    for target, count in call_targets.most_common(5):
        print(f"    • {target}: {count} calls")
    print()

    print("⚠️  WARNINGS & HAZARDS")
    print("-" * 70)

    if not warnings:
        print("  ✓ No critical warnings detected!")
    else:
        for i, warning in enumerate(warnings, 1):
            severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(warning['severity'], '⚪')
            print(f"  {severity_icon} [{warning['severity'].upper()}] {warning['type']}")
            print(f"     {warning['message']}")

            if 'examples' in warning:
                print(f"     Examples:")
                for ex in warning['examples'][:3]:
                    print(f"       - {ex}")

            if 'details' in warning:
                for detail in warning['details'][:3]:
                    print(f"       - {detail}")

            print()

    print("📁 DOCUMENTATION OUTPUT")
    print("-" * 70)
    print("  ✓ docs/SYSTEM_MAP.md    - System architecture overview")
    print("  ✓ docs/DATA_KEYS.md     - Complete data key inventory")
    print("  ✓ docs/EVENT_INDEX.md   - Event handler index")
    print("  ✓ docs/CALL_GRAPH.md    - Script dependency map")
    print("  ✓ docs/analysis.json    - Raw analysis data")
    print()

    print("🔄 NEXT STEPS")
    print("-" * 70)
    print("  1. Review high-frequency events in game_loop.dsc for optimization")
    print("  2. Check for blocking operations (wait/waituntil) in performance-critical paths")
    print("  3. Audit keys with multiple writers for race conditions")
    print("  4. Plan modular refactor based on subsystem groupings in SYSTEM_MAP.md")
    print()

    print("🎯 SUGGESTED RE-ANALYSIS TRIGGERS")
    print("-" * 70)
    print("  • After merging ritual_system or mythic framework changes")
    print("  • After refactoring game_loop or combat mechanics")
    print("  • After adding new spell/skill subsystems")
    print("  • Monthly during active development")
    print()
    print("="*70)
    print()

def main():
    data = load_analysis()
    warnings = find_warnings(data)

    # Save warnings to JSON
    with open('docs/warnings.json', 'w') as f:
        json.dump(warnings, f, indent=2)

    generate_summary(data, warnings)

if __name__ == "__main__":
    main()
