"""Check original-ROM DMA traces against an independent decompressor.

Only addresses, lengths, hashes and counters are exported, never ROM bytes.
This validates recorded transfers, not visual or complete scenario coverage.
"""
from pathlib import Path
import argparse
import collections
import ctypes as C
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SOURCE_SHA = 'a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd'


def validate(trace, source):
    meta = json.loads((trace.parent / 'run.json').read_text())
    assert meta['rom_sha256'] == SOURCE_SHA, 'Trace must identify the original French ROM'
    assert len(source) == 6291456 and hashlib.sha256(source).hexdigest() == SOURCE_SHA, 'Unexpected source ROM'
    records = collections.Counter()
    for line in trace.read_text().splitlines():
        fields = line.split(',')
        assert len(fields) == 7, 'Malformed trace record'
        bank, address, offset, length, fnv, pc, channel = fields
        row = (int(bank, 16), int(address, 16), int(offset), int(length), int(fnv, 16), int(pc, 16), int(channel))
        assert 0xc0 <= row[0] <= 0xff and 0 <= row[1] < 65536
        assert 0 <= row[2] < len(source) and 0 < row[3] <= 65536
        assert 0 <= row[4] <= 0xffffffff and 0 <= row[5] <= 0xffffff and 0 <= row[6] < 8
        records[row] += 1
    assert records, 'Empty trace is not a validation'
    lib = C.CDLL(str(ROOT / 'sdd1.so'))
    decode = getattr(lib, '_Z15SDD1_decompressPhS_i')
    decode.argtypes = [C.c_void_p, C.c_void_p, C.c_int]
    # Match the standalone validation's bounded read-ahead padding.
    rom_buffer = C.create_string_buffer(source + bytes(0x20000))
    output = C.create_string_buffer(65536)
    errors = []
    unique = {(r[2], r[3], r[4]) for r in records}
    for offset, length, expected in sorted(unique):
        decode(output, C.byref(rom_buffer, offset), length)
        actual = 2166136261
        for byte in output.raw[:length]:
            actual = ((actual ^ byte) * 16777619) & 0xffffffff
        if actual != expected:
            errors.append({'source_file': offset, 'length': length, 'expected_fnv32': f'{expected:08x}', 'actual_fnv32': f'{actual:08x}'})
    sources = collections.defaultdict(set)
    for bank, address, offset, *_ in records:
        sources[(bank << 16) | address].add(offset)
    conflicts = [{'key': f'{key:06x}', 'source_files': sorted(offsets)} for key, offsets in sorted(sources.items()) if len(offsets) > 1]
    return {
        'source_sha256': SOURCE_SHA,
        'trace_sha256': hashlib.sha256(trace.read_bytes()).hexdigest(),
        'frames': meta['frames'], 'start_frame': meta.get('start_frame', 0),
        'transfers': sum(records.values()), 'unique_records': len(records),
        'unique_cpu_keys': len(sources), 'independent_source_length_hash_checks': len(unique),
        'callsites': sorted({f'{r[5]:06x}' for r in records}),
        'channels': sorted({r[6] for r in records}),
        'decompression_errors': errors, 'physical_source_conflicts': conflicts,
        'checks_passed': not errors and not conflicts,
        'caveat': 'Recorded transfers only; no visual, SRAM, hardware or complete scenario validation.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', type=Path)
    parser.add_argument('--source', type=Path, default=ROOT.parent / 'upload/Star Ocean FR.smc')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.trace, args.source.read_bytes())
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    assert result['checks_passed'], 'Original DMA validation failed'
