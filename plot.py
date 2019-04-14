import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import argparse

def plot_range(s):
    try:
        start, end = map(int, s.split(','))
        return (start, end)
    except Exception as e:
        raise argparse.ArgumentTypeError("Plot range must be in format (int,int)")


parser = argparse.ArgumentParser()
parser.add_argument('--limit', '-limit', '-l', type=int, help="Plot limit.", default=10)
parser.add_argument('--mouse', '-mouse', '-m', help="Show mouse data instead of key data.", required=False, action='store_true')
parser.add_argument('--order', '-o', type=str, help="Results order (DESC|ASC)", default="DESC", choices=['ASC', 'DESC'])
parser.add_argument('--range', '-r', type=plot_range, help="Plot range.")
# Too much work, don't really need it
# parser.add_argument('--include-mouse', '-incude-mouse', '-i', help="Include mouse data with keyboard data.", required=False, action='store_true')
args = parser.parse_args()

with sqlite3.connect('keydata.db') as conn:
    c = conn.cursor()
    c.execute(f"""
        SELECT * FROM  {"mouseclicks" if args.mouse else "keypresses"} 
        ORDER BY {"times_" + ("clicked" if args.mouse else "pressed")} {args.order} {f"LIMIT {args.limit}" if not args.range else ""}
    """)
    click_data = c.fetchall()
    keys = [k[0] for k in click_data]
    clicks = [k[1 if args.mouse else 2] for k in click_data]

    if args.range:
        keys = keys[args.range[0]:args.range[1]]
        clicks = clicks[args.range[0]:args.range[1]]

    y_pos = np.arange(len(keys))

    plt.bar(y_pos, clicks, align='center')
    plt.xticks(y_pos, keys)
    plt.ylabel('Clicks' if args.mouse else 'Presses')
    plt.title(f'{"Mouse" if args.mouse else "Key"} usage data')
    plt.show()

# Old unnecessary stuff that I'm scared to remove in case what's above fails for some reason

# if args.mouse:
#     with sqlite3.connect('keydata.db') as conn:
#         c = conn.cursor()
#         c.execute(f'SELECT * FROM mouseclicks ORDER BY times_clicked {args.order} {f"LIMIT {args.limit}" if not args.range else ""}')
#         click_data = c.fetchall()
#         keys = [k[0] for k in click_data]
#         clicks = [k[1] for k in click_data]

#         if args.range:
#             keys = keys[args.range[0]:args.range[1]]
#             clicks = clicks[args.range[0]:args.range[1]]

#         y_pos = np.arange(len(keys))

#         plt.bar(y_pos, clicks, align='center')
#         plt.xticks(y_pos, keys)
#         plt.ylabel('Clicks')
#         plt.title('Mouse usage data')
#         plt.show()
# else:
#     with sqlite3.connect('keydata.db') as conn:
#         c = conn.cursor()
#         c.execute(f'SELECT * FROM keypresses ORDER BY times_pressed {args.order} {f"LIMIT {args.limit}" if not args.range else ""}')
#         key_data = c.fetchall()
#         keys = [k[0] for k in key_data]
#         presses = [k[2] for k in key_data]

#         if args.range:
#             keys = keys[args.range[0]:args.range[1]]
#             presses = presses[args.range[0]:args.range[1]]

#         y_pos = np.arange(len(keys))

#         plt.bar(y_pos, presses, align='center')
#         plt.xticks(y_pos, keys)
#         plt.ylabel('Presses')
#         plt.title('Key usage data')
#         plt.show()
