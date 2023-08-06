#!/usr/bin/env python

import argparse
import binascii
import os
import shutil
import sys
import time
import tqdm
from datetime import datetime
from tempfile import NamedTemporaryFile

import humanfriendly
from colorama import Fore

try:
    from . import common
except ImportError:
    import common


PARAMS = {}

PARAMS['this_script'] = common.get_script_name_from_filename(__file__)

MIN_BLOCK_SIZE = 512

DEFAULT_TOTALSIZE = "1.0GiB"
DEFAULT_FILESIZE = "100MiB"
DEFAULT_BLOCKSIZE = "16MiB"
DEFAULT_RETRIES = 20
DEFAULT_TIMEOUT = 5.0
DEFAULT_PREFIX = 'wipe_'
DEFAULT_SUFFIX = '.junk'
DEFAULT_PATTERN = None
DEFAULT_TGTDIR = '.'
DEFAULT_ERROR_DELAY = 0.25

COLORS = [
    Fore.BLACK,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
]


def setup_and_dispatch():
    ''' Handle args and call main tooling '''

    parser = argparse.ArgumentParser(
        description=common.format_title(PARAMS['this_script']),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--binary', action='store_true',
                        help='Decode numeric suffixed as binary (e.g., "1KB" = 1024)')
    parser.add_argument('--prefix', type=str, default=DEFAULT_PREFIX,
                        help='File prefix')
    parser.add_argument('--suffix', type=str, default=DEFAULT_SUFFIX,
                        help='File suffix / extension')
    parser.add_argument('--totalsize', type=str, default=str(DEFAULT_TOTALSIZE), metavar='SIZE',
                        help='Total size (up to free space on FS) or "FILL"')
    parser.add_argument('--filesize', type=str, default=str(DEFAULT_FILESIZE), metavar='SIZE',
                        help='File size (< max file size for FS)')
    parser.add_argument('--blocksize', type=str, default=str(DEFAULT_BLOCKSIZE), metavar='SIZE',
                        help='Block size (typ. << file size')
    parser.add_argument('--retries', type=int, default=DEFAULT_RETRIES, metavar='VAL',
                        help='Maximum retries on write fail')
    parser.add_argument('--timeout', type=float, default=DEFAULT_TIMEOUT, metavar='SECS',
                        help='Write timeout')
    parser.add_argument('--errdelay', type=float, default=DEFAULT_ERROR_DELAY, metavar='SECS',
                        help='Error retry delay')
    parser.add_argument('--pattern', type=str, default=DEFAULT_PATTERN,
                        help='Specify text/hex pattern to use ("xyz", "0x1DAB0"...)')
    parser.add_argument('--localtime', action='store_true',
                        help='Use local system time instead of UTC')
    parser.add_argument('--colorful', action='store_true',
                        help='Colorful output')
    parser.add_argument('--debug', action='store_true',
                        help='Debug mode')
    parser.add_argument('target_dir', nargs=argparse.REMAINDER,
                        help='Target path')
    try:
        args, extra_args = parser.parse_known_args()
    except BaseException as e:
        raise e

    print(common.format_title(PARAMS['this_script']))

    PARAMS['debug'] = args.debug
    PARAMS['colorful'] = args.colorful
    PARAMS['localtime'] = args.localtime
    PARAMS['binary'] = args.binary
    PARAMS['prefix'] = args.prefix
    PARAMS['suffix'] = args.suffix
    PARAMS['retries'] = int(args.retries)
    PARAMS['timeout'] = float(args.timeout)
    PARAMS['errdelay'] = float(args.errdelay)
    PARAMS['block_size'] = humanfriendly.parse_size(args.blocksize, binary=PARAMS['binary'])
    PARAMS['file_size'] = humanfriendly.parse_size(args.filesize, binary=PARAMS['binary'])

    if args.totalsize.lower() == "fill":
        PARAMS['total_size'] = 0
    else:
        PARAMS['total_size'] = humanfriendly.parse_size(args.totalsize, binary=PARAMS['binary'])

    if not args.pattern:
        # Default to random
        PARAMS['pattern'] = DEFAULT_PATTERN
    elif args.pattern.lower().startswith('0x'):
        # Hex pattern
        args.pattern = args.pattern[2:]
        if len(args.pattern) % 2:
            args.pattern = '0' + args.pattern
        PARAMS['pattern'] = binascii.unhexlify(args.pattern)
    else:
        # Text pattern
        PARAMS['pattern'] = args.pattern.encode('utf-8')

    if args.target_dir:
        PARAMS['tgtdir'] = args.target_dir[0]
    else:
        PARAMS['tgtdir'] = DEFAULT_TGTDIR

    if ((0 in [PARAMS['file_size'], PARAMS['block_size']])
       or (not (0 < len(args.target_dir) < 2))):
        parser.print_help(sys.stderr)
        sys.exit(0)

    print()
    pyfiller()


def pyfiller():
    free_space = shutil.disk_usage(PARAMS['tgtdir']).free
    selector = common.RandomSelector(COLORS)
    total_bytes_written = 0
    if PARAMS['total_size']:
        bytes_to_write = PARAMS['total_size']
    else:
        bytes_to_write = free_space
    while free_space and bytes_to_write > 0:
        if PARAMS['file_size'] > 0 and bytes_to_write > PARAMS['file_size']:
            file_size = PARAMS['file_size']
        else:
            file_size = bytes_to_write
        if PARAMS['localtime']:
            PARAMS['infix'] = datetime.utcnow().strftime('%Y%m%d-%H%M%S-%f')[:-3]
        else:
            PARAMS['infix'] = datetime.today().strftime('%Y%m%d-%H%M%S-%f')[:-3]
        PARAMS['bar_color'] = COLORS[selector.choose()] if PARAMS['colorful'] else Fore.RESET
        PARAMS['curr_retries'] = 0
        bytes_written = write_file(tgtdir=PARAMS['tgtdir'], file_size=file_size)
        total_bytes_written += bytes_written
        bytes_to_write -= bytes_written
        free_space = shutil.disk_usage(PARAMS['tgtdir']).free
    if bytes_to_write:
        note = ' ({} not written)'.format(humanfriendly.format_size(bytes_to_write, binary=PARAMS['binary']))
    else:
        note = ''
    print('Wrote {} bytes total{}'.format(
        humanfriendly.format_size(total_bytes_written, binary=PARAMS['binary']),
        note,
    ))
    if not free_space:
        print('Filesystem is full: {}'.format(PARAMS['tgtdir']))


def write_file(tgtdir, file_size):
    block_size = PARAMS['block_size']
    if PARAMS['binary']:
        unit_suffix = 'iB'
        unit_divisor = 1024
    else:
        unit_suffix = 'B'
        unit_divisor = 1000
    file_bytes_written = 0
    prev_offset = 0
    pattern_buffer = []
    with tqdm.tqdm(
        total=file_size,
        unit=unit_suffix,
        unit_scale=True,
        unit_divisor=unit_divisor,
        leave=True,
        initial=0,
        bar_format="{l_bar}%s{bar}%s{r_bar}" % (PARAMS['bar_color'], Fore.RESET),
    ) as pbar:
        with NamedTemporaryFile(
            mode='wb',
            dir=tgtdir,
            prefix=f"{PARAMS['prefix']}{PARAMS['infix']}__",
            suffix=PARAMS['suffix'],
            buffering=0,  # if -1, will not quite write the last part
            delete=False,
        ) as fp:
            bytes_remaining = file_size
            pbar.set_postfix(file=fp.name[-40:], refresh=False)
            pbar.refresh()
            while bytes_remaining > 0 and block_size > 0:
                t_start = time.time()
                bytes_to_write = bytes_remaining if bytes_remaining < block_size else block_size
                if PARAMS['pattern'] is DEFAULT_PATTERN:
                    pattern_buffer = os.urandom(bytes_to_write)
                else:
                    full_reps, part_reps = divmod(block_size, len(PARAMS['pattern']))
                    pattern_buffer = (PARAMS['pattern'][prev_offset:] + PARAMS['pattern'] * full_reps + PARAMS['pattern'][:part_reps])[:bytes_to_write]
                block_bytes_written = 0
                try:
                    block_bytes_written = fp.write(pattern_buffer[:bytes_to_write])
                except OSError:
                    time.sleep(PARAMS['errdelay'])
                    block_size = int(block_size // 2)
                    if block_size < MIN_BLOCK_SIZE:
                        block_size = 0
                bytes_remaining -= block_bytes_written
                file_bytes_written += block_bytes_written
                if PARAMS['pattern']:
                    prev_offset = file_bytes_written % len(PARAMS['pattern'])
                pbar.update(block_bytes_written)
                fp.flush()
                if time.time() - t_start > PARAMS['timeout']:
                    PARAMS['curr_retries'] += 1
                if PARAMS['curr_retries'] > PARAMS['retries']:
                    print()
                    print("Disk took too long (max retries exceeded) - aborting!")
                    print()
                    break

    return file_bytes_written


def main():
    try:
        setup_and_dispatch()
    except KeyboardInterrupt:
        print("Exiting...")
    sys.exit(0)


if __name__ == '__main__':
    # common.test_random_selector()
    main()
