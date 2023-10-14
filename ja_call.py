''' ja_call.py JAのコールサインかどうかを判定する。 '''

import re

# JA Callsignの正規表現パターン
# 1文字目: Jか7
# 2文字目: AからS
# 3文字目: 数字0-9
# 4文字目以降: 文字A-Z
JA_PATTERN = '[J|7][A-S][0-9][A-Z]'


def is_ja_call(callsign):
    ''' JA callsign check returns boolean '''
    callsign = callsign.upper()
    pattern = re.compile(JA_PATTERN)
    pa = pattern.search(callsign)
    # print(pa.span(), pa.start(), pa.end())
    if pa is None:
        result = False
    else:
        result = True

    return result


def main():
    ''' main func for test purpose '''
    call = 'JS2IIU'
    print(is_ja_call(call))


if __name__ == '__main__':
    main()
