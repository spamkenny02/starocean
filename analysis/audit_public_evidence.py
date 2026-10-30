"""Audit public metadata only. Does not decompress, run a ROM, or certify gameplay."""
from pathlib import Path
import argparse
import collections
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent
EVIDENCE = [
    'observed_fr.json', 'story_observed.json.gz', 'baird_variant_observed.json.gz',
    'chapter2_observed.json.gz', 'cool_observed.json.gz',
    'recovery_observed.json.gz', 'recovery_branch_observed.json.gz',
    'oct29_observed.json.gz',
    'oct30_maltos_observed.json.gz',
    'oct30_departure_observed.json.gz',
    'metox_observed.json.gz',
]


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def audit(root):
    catalog = read(root / 'catalog_extended.json.gz')
    by_key = {}
    for row in catalog:
        key = (row['cpu_bank'], row['cpu_address'])
        assert key not in by_key, ('duplicate catalog key', key)
        assert 0 < key[0] <= 255 and 0 <= key[1] <= 65535
        assert 0 <= row['source_file'] < 0x600000
        assert 0 < row['length'] <= 65536
        by_key[key] = row

    slots = read(root / 'lookup_slots.json.gz')
    table, slot_keys = {}, set()
    for bank, address, slot in slots:
        key = (bank, address)
        assert key in by_key and key not in slot_keys, ('invalid lookup key', key)
        assert 0 <= slot <= 65535 and slot not in table, ('duplicate/invalid slot', slot)
        slot_keys.add(key)
        table[slot] = key
    assert slot_keys == by_key.keys(), 'lookup manifest and catalog differ'
    max_probe = 0
    for slot, (bank, address) in table.items():
        distance = (slot - address) & 65535
        assert all(((address + step) & 65535) in table for step in range(distance)), (
            'lookup would trap before finding key', bank, address, slot)
        max_probe = max(max_probe, distance)

    backed, pcs, channels, files = set(), set(), set(), []
    listed_callsites = set(read(root / 'extended_callsites.json'))
    for name in EVIDENCE:
        path = root / name
        rows = read(path)
        keys = set()
        for row in rows:
            key = (row['cpu_bank'], row['cpu_address'])
            assert key in by_key, ('missing catalog entry', name, key)
            entry = by_key[key]
            assert entry['source_file'] == row['source_file'], ('physical source conflict', name, key)
            assert entry['length'] >= row['length'], ('insufficient length', name, key)
            assert entry['priority'] == 10, ('exported observation not classified observed', name, key)
            if 'fnv32' in row:
                assert len(row['fnv32']) == 8 and 0 <= int(row['fnv32'], 16) <= 0xffffffff
            if 'callsite_pc' in row:
                assert row['callsite_pc'] in listed_callsites, ('callsite missing from list', name, row['callsite_pc'])
                pcs.add(row['callsite_pc'])
            if 'channel' in row:
                channels.add(row['channel'])
            if 'count' in row:
                assert row['count'] > 0
            keys.add(key)
        backed.update(keys)
        files.append({'file': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'records': len(rows), 'unique_keys': len(keys)})

    observed = {key for key, row in by_key.items() if row['priority'] == 10}
    gap = [{'cpu_key': f'{bank:02X}:{address:04X}',
            'historical_provenance': by_key[(bank, address)]['method']}
           for bank, address in sorted(observed - backed)]
    return {
        'scope': 'Public metadata consistency only; no ROM, decompression or new gameplay validation',
        'catalog_keys': len(catalog), 'catalog_observed_keys': len(observed),
        'observed_keys_with_public_records': len(backed),
        'observed_keys_without_public_records': gap,
        'catalog_priority_counts': dict(sorted(collections.Counter(r['priority'] for r in catalog).items())),
        'lookup_slots': len(table), 'max_lookup_probe_distance': max_probe,
        'exported_callsite_count': len(pcs), 'listed_callsite_count': len(listed_callsites),
        'listed_callsites_without_exported_records': [f'{pc:06X}' for pc in sorted(listed_callsites - pcs)],
        'exported_channels': sorted(channels), 'evidence_files': files,
        'consistency_checks_passed': True,
        'caveats': [
            'Historical observed classifications without exported records are retained, not newly verified.',
            'Files can contain overlapping runs: their record/transfer counts must not be added as independent coverage.',
            'Hash syntax is checked; decompressed bytes cannot be checked without the exact source ROM.',
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT / 'public_evidence_audit.json')
    args = parser.parse_args()
    result = audit(args.root)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('evidence_files', 'caveats', 'observed_keys_without_public_records')}, indent=2))
    print('Historical observed keys without exported records:', len(result['observed_keys_without_public_records']))
