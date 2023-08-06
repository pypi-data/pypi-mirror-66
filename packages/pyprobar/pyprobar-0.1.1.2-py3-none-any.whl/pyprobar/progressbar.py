import sys
import time, datetime
from datetime import timedelta
import abc
import random
from colorama import Fore
from .cursor import Cursor
cursor = Cursor()

class Progress(metaclass=abc.ABCMeta):
    unit_percent = 0.034
    total_space = 30

    @abc.abstractmethod
    def currentProgress(self):
        pass

    @abc.abstractmethod
    def appearance(self):
        pass

    @abc.abstractmethod
    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""

    @staticmethod
    def get_color(N_color, update=True, COLOR=[0]):
        """Choice random n colors"""
        if update == True or COLOR[0] == 0:
            color_list = ['CYAN', 'GREEN', 'RED', 'YELLOW', 'RESET', \
                          'LIGHTGREEN_EX', 'LIGHTRED_EX', \
                          'LIGHTYELLOW_EX', 'LIGHTBLACK_EX', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX']
            # 'LIGHTMAGENTA_EX', 'MAGENTA', 'BLUE',

            color = [Fore.LIGHTCYAN_EX]  # Manually specify the first color
            for i in range(N_color - 2):
                color.append(eval("Fore." + random.choice(color_list)))
            color.append(Fore.LIGHTBLUE_EX)  # and the last color
            COLOR[0] = color

            return COLOR[0]
        else:
            return COLOR[0]

class IntegProgress(Progress):
    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""
        n_sign1, mod_sign1 = divmod(percent, self.unit_percent)
        N1 = int(n_sign1)
        sign1 = symbol_1 * N1
        N0 = int((mod_sign1 / self.unit_percent) * (self.total_space - N1))

        sign0 = symbol_2 * N0
        SIGN = '|' + sign1 + sign0 + (self.total_space - N1 - N0 - 1) * ' ' + '|'
        return SIGN, N1

    def currentProgress(self, percent, t0, terminal):
        cost_time = time.time() - t0
        total_time = cost_time / percent
        PERCENT = percent * 100

        remain_time = int(total_time - cost_time)
        remain_time = datetime.timedelta(seconds=remain_time)
        total_time = timedelta(seconds=int(total_time))
        cost_time = datetime.timedelta(seconds=int(cost_time))

        _PERCENT = f"{PERCENT: >6.2f}%"
        _COST = f" {cost_time}|{total_time} "
        _REMAIN = f" {remain_time}|{total_time} "
        _ETC = f" ETC: {(datetime.datetime.now() + remain_time).strftime('%m-%d %H:%M:%S')}"
        return _PERCENT, _REMAIN , _ETC

    def appearance(self, idx, total_steps, symbol_1, symbol_2, t0, terminal):
        counts = idx + 1
        percent = counts / total_steps
        PERCENT = percent * 100
        if idx == 0:
            print(f"\r{0:.2f}% \t  {0:.1f}|{float('inf'):.1f}s{cursor.EraseLine(0)}", end='', flush=True)
            self.d_percent = 0.01
        else:
            if PERCENT >= self.d_percent:
                self.d_percent += 0.01
                SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
                _PERCENT, _REMAIN , _ETC = self.currentProgress(percent, t0, terminal)
                print('\r' + Fore.CYAN + f"{_PERCENT}" + Fore.LIGHTBLACK_EX + SIGN + \
                      Fore.LIGHTGREEN_EX + _REMAIN + Fore.LIGHTBLUE_EX + _ETC + Fore.RESET + cursor.EraseLine(0), end='',
                      flush=True)
        if counts == total_steps:
            print('\n')



class probar(IntegProgress):
    """Simple progress bar display, to instead of tqdm.
    """

    def __init__(self, iterable, total_steps=None, symbol_1="█", symbol_2='>', terminal=False):
        self.iterable = iterable
        self.t0 = time.time()
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.terminal = terminal

        if hasattr(iterable, '__len__'):
            self.total_steps = len(iterable)
        else:
            self.total_steps = total_steps
            if self.total_steps == None:
                raise ValueError(f'{iterable} has no __len__ attr, use total_steps param')

    def __iter__(self):
        for idx, i in enumerate(self.iterable):
            self.appearance(idx, self.total_steps, self.symbol_1, self.symbol_2, self.t0, self.terminal)
            yield idx, i


class SepaProgress(Progress):
    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""
        n_sign1, mod_sign1 = divmod(percent, self.unit_percent)
        N1 = int(n_sign1)
        sign1 = symbol_1 * N1
        N0 = int((mod_sign1 / self.unit_percent) * (self.total_space - N1))

        sign0 = symbol_2 * N0
        SIGN = '|' + sign1 + sign0 + (self.total_space - N1 - N0 - 1) * ' ' + '|'
        return SIGN, N1

    def currentProgress(self):
        pass
    def appearance(self):
        pass

sepabar = SepaProgress()

def bar(index, total_size, color='constant_random', symbol_1="█", symbol_2='>', teminal=True):
    """Simple progress bar display, to instead of tqdm.
    :arg color: options  'constant_random', 'update_random', 'reset'
    """
    
    global first_time, flag_update_color, COLOR
    _index = index + 1
    if index == 0:
        first_time = time.time()
        flag_update_color = None
        index = 1

    _percent = index/(total_size) # for time
    percent = (_index)/total_size # for bar
    cost_time = time.time() - first_time

    total_time = cost_time/_percent
    # remain_time = int(total_time - cost_time)
    remain_time = int(total_time * (1-percent))
    remain_time = timedelta(seconds=remain_time)
    total_time = timedelta(seconds=int(total_time))
    ETC_1 = f"{remain_time}|{total_time} "
    ETC_2 = f"ETC: {(datetime.datetime.now() + remain_time).strftime('%m-%d %H:%M:%S')}"

    SIGN, N1 = sepabar.current_bar(percent, symbol_1, symbol_2)

    if color == "update_random":
        if flag_update_color != N1:
            flag_update_color = N1
            COLOR = sepabar.get_color(N_color=4, update=True)
            [color1, color2, color3, color4] = COLOR
        else:
            [color1, color2, color3, color4] = COLOR

        print(color1 + f"\r{percent * 100: >6.2f}% ", color2 + SIGN, color3 + f"{ETC_1}", color4 + f"{ETC_2}",
              Fore.RESET+cursor.EraseLine(0), end='',flush=True)
    elif color == 'constant_random':
        [color1, color2, color3, color4] = get_color(N_color=4, update=False)
        print(f"\r{color1}{percent * 100: >6.2f}% {color2}{SIGN}{color3}{ETC_1}{color4}{ETC_2} {Fore.RESET}{cursor.EraseLine(0)}",
              end='', flush=True)
    elif color == 'reset':

        print(f"\r{percent * 100: >6.2f}% "+ SIGN + f"{ETC_1} {ETC_2}{cursor.EraseLine(0)}", end='', flush=True)
    else:
        raise ValueError("Invalid input!")

    if _index == total_size:
        print('\n')




