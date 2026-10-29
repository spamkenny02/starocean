"""Join absolute-frame routes at a checkpoint; no emulator execution is implied."""
from pathlib import Path
import argparse
import json


def validate(route):
    previous_end = 0
    for row in route:
        assert isinstance(row, list) and len(row) == 3, 'Expected [start, end, mask]'
        start, end, mask = row
        assert all(type(x) is int for x in row), 'Frame and mask values must be integers'
        assert 0 <= previous_end <= start < end and 0 <= mask <= 0xfff, row
        previous_end = end


def compose(prefix, continuation, checkpoint):
    validate(prefix)
    validate(continuation)
    assert continuation and continuation[0][0] == checkpoint, 'Continuation starts at another checkpoint'
    assert prefix and prefix[-1][1] >= checkpoint, 'Prefix does not reach checkpoint'
    result = [[start, min(end, checkpoint), mask] for start, end, mask in prefix if start < checkpoint]
    result.extend(continuation)
    validate(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prefix', type=Path)
    parser.add_argument('continuation', type=Path)
    parser.add_argument('--checkpoint', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    assert args.output.resolve() not in (args.prefix.resolve(), args.continuation.resolve()), 'Do not overwrite inputs'
    route = compose(json.loads(args.prefix.read_text()), json.loads(args.continuation.read_text()), args.checkpoint)
    args.output.write_text(json.dumps(route, indent=2) + '\n')
    print(f'{len(route)} intervals; end frame {route[-1][1]}; composition only, not a replay')
