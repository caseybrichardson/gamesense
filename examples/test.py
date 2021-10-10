import random
import time

import gamesense


def register_gamesense():
    gs = gamesense.GameSense("PYTEST", "PyTest")

    register_resp = gs.register_game(icon_color_id=gamesense.GS_ICON_GOLD)
    if not register_resp.success:
        print(register_resp.data)

    event_resp = gs.register_event("TEST1")
    if not event_resp.success:
        print(event_resp.data)

    event_resp = gs.register_event("TEST2")
    if not event_resp.success:
        print(event_resp.data)

    event_resp = gs.register_event("TEST3")
    if not event_resp.success:
        print(event_resp.data)

    event_resp = gs.register_event("TEST4")
    if not event_resp.success:
        print(event_resp.data)

    event_resp = gs.register_event("TEST5")
    if not event_resp.success:
        print(event_resp.data)

    return gs


def main():
    gs = register_gamesense()

    for i in range(10):
        time.sleep(1)
        e = gs.send_event(f'TEST{(i % 5) + 1}', {'value': i * 10, 'frame': {'r': random.randint(0, 10000)}})
        print(e.status_code, e.data)


if __name__ == '__main__':
    main()

