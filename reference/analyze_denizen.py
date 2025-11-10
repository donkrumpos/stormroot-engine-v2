#!/usr/bin/env python3
"""
Denizen Script Analysis Tool
Parses all .dsc files and extracts events, data keys, and call graphs
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class DenizenAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.events = []
        self.data_keys = []
        self.calls = []
        self.scripts = []

    def find_dsc_files(self):
        """Find all .dsc files recursively"""
        return list(self.root_dir.rglob("*.dsc"))

    def normalize_key(self, key):
        """Normalize flag/data key names"""
        key = key.strip()
        # Normalize common prefixes
        key = re.sub(r'^<player\.', 'player.', key)
        key = re.sub(r'^<server\.', 'server.', key)
        key = re.sub(r'^p\.', 'player.', key)
        key = re.sub(r'^s\.', 'server.', key)
        # Remove closing tags
        key = re.sub(r'>$', '', key)
        return key

    def parse_file(self, filepath):
        """Parse a single .dsc file"""
        rel_path = filepath.relative_to(self.root_dir)

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")
            return

        for line_num, line in enumerate(lines, 1):
            original_line = line
            line = line.rstrip()

            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue

            # Event handlers - looking for "on <event>:" or "after <event>:"
            event_match = re.match(r'^(\s*)(on|after)\s+(.+):\s*$', line, re.IGNORECASE)
            if event_match:
                indent = len(event_match.group(1))
                event_type = event_match.group(2)
                event_name = event_match.group(3).strip()
                self.events.append({
                    'file': str(rel_path),
                    'line': line_num,
                    'type': event_type,
                    'event': event_name,
                    'indent': indent
                })

            # Flag operations - player.flag, server.flag, etc.
            # Patterns: <player.flag[name]>, - flag player name, - adjust player flag:name
            flag_patterns = [
                r'<(player|server|npc)\.flag\[([^\]]+)\]>',
                r'-\s+flag\s+(player|server|npc)\s+([^\s:]+)',
                r'-\s+adjust\s+(player|server|npc)\s+flag:([^\s:]+)',
            ]

            for pattern in flag_patterns:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    scope = match.group(1).lower()
                    key_name = match.group(2)
                    full_key = f"{scope}.flag.{key_name}"
                    self.data_keys.append({
                        'file': str(rel_path),
                        'line': line_num,
                        'key': self.normalize_key(full_key),
                        'scope': scope,
                        'type': 'flag',
                        'context': line.strip()[:80]
                    })

            # YAML data operations
            yaml_patterns = [
                r'<yaml\[([^\]]+)\]\.read\[([^\]]+)\]>',
                r'-\s+yaml\s+set\s+([^\s:]+):([^\s]+)',
            ]

            for pattern in yaml_patterns:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    yaml_id = match.group(1)
                    yaml_key = match.group(2)
                    full_key = f"yaml.{yaml_id}.{yaml_key}"
                    self.data_keys.append({
                        'file': str(rel_path),
                        'line': line_num,
                        'key': full_key,
                        'scope': 'yaml',
                        'type': 'yaml',
                        'context': line.strip()[:80]
                    })

            # Run/inject/task calls
            call_patterns = [
                (r'-\s+run\s+([^\s]+)', 'run'),
                (r'-\s+inject\s+([^\s]+)', 'inject'),
                (r'-\s+task\s+([^\s]+)', 'task'),
            ]

            for pattern, call_type in call_patterns:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    target = match.group(1)
                    self.calls.append({
                        'file': str(rel_path),
                        'line': line_num,
                        'type': call_type,
                        'target': target,
                        'context': line.strip()[:80]
                    })

    def analyze_all(self):
        """Analyze all .dsc files"""
        files = self.find_dsc_files()
        print(f"Found {len(files)} .dsc files")

        for i, filepath in enumerate(files, 1):
            if i % 50 == 0:
                print(f"  Processed {i}/{len(files)} files...")
            self.parse_file(filepath)

        print(f"Extraction complete:")
        print(f"  - {len(self.events)} event handlers")
        print(f"  - {len(self.data_keys)} data key references")
        print(f"  - {len(self.calls)} run/inject/task calls")

        return {
            'events': self.events,
            'data_keys': self.data_keys,
            'calls': self.calls,
            'file_count': len(files)
        }

    def save_json(self, output_file):
        """Save analysis results to JSON"""
        data = {
            'events': self.events,
            'data_keys': self.data_keys,
            'calls': self.calls
        }
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved analysis to {output_file}")

if __name__ == "__main__":
    analyzer = DenizenAnalyzer(".")
    results = analyzer.analyze_all()
    analyzer.save_json("docs/analysis.json")
