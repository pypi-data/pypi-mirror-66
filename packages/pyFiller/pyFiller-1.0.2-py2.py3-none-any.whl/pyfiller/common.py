"""

"""

import errno
import os
import random
import sys
from collections import Counter, deque, OrderedDict
try:
    from . import __config__ as config
except ImportError:
    import __config__ as config


class RandomSelector:
    def __init__(self, items):
        if isinstance(items, (int, float)):
            self.num_items = int(items)
        else:
            self.num_items = len(items)
        self.count = Counter()
        self.prev = deque()
        self.curr = list(range(self.num_items))

    def choose(self):
        if len(self.prev) > self.num_items // 2:
            self.curr.append(self.prev.popleft())
        selection = random.choice(self.curr)
        self.count[selection] += 1
        self.curr.remove(selection)
        self.prev.append(selection)
        return selection

    def get_stats(self):
        return self.count


def test_random_selector():
    import tqdm
    from colorama import Fore
    COLORS = [
        Fore.WHITE,
        Fore.RED,
        Fore.BLUE,
        Fore.GREEN,
    ]

    cnt = 0
    while True:
        r = RandomSelector(len(COLORS))
        for i in range(len(COLORS) * 100):
            x = r.choose()
            for i in tqdm.trange(int(1e6), unit='B', unit_scale=True, unit_divisor=1000, bar_format="{l_bar}%s{bar}%s{r_bar}" % (COLORS[x], Fore.RESET)):
                pass
        x = r.get_stats()
        if len(set(x.values())) == 1:
            print(cnt, x)
            break
        cnt += 1


def get_script_name_from_filename(filename):
    basename = os.path.splitext(os.path.basename(filename))[0]
    return config.CONSOLE_SCRIPTS[basename]['scriptname']


def format_title(this_script):
    return '{} v{} - {}'.format(this_script, config.VERSION, config.DESCRIPTION)


def get_basenames(requirements):
    return list(OrderedDict.fromkeys([os.path.splitext(r)[0] for r in requirements]))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def exit_with_error(error_text, error_code=1, parser=None):
    print(error_text, file=sys.stderr)
    print(file=sys.stderr)
    if parser:
        parser.print_help(sys.stderr)
    sys.exit(error_code)
