# gamesense
A Python library for use with SteelSeries GameSense 3.8.X+

## Installation

There are two different versions of this package. One supports normal synchronous function calls and the other support python's asynchronous functionality.

To install the sync version run:
```
pip install gamesense[sync]
```

To install the async version run:
```
pip install gamesense[async]
```

Or both:
```
pip install gamesense[sync,async]
```

## Usage
Relatively simple to use.

For synchronous usage:
```python
import gamesense

# Create a GameSense object instance to use
gs = gamesense.GameSense("SYNC_GAME", "Sync Game")

# Before you can register or send events, you must register your game
gs.register_game(icon_color_id=gamesense.GS_ICON_GOLD)

# Register an event (different than binding an event, see more info in the SteelSeries docs)
gs.register_event("DID_STUFF")

# Test out the event by sending the event
gs.send_event("DID_STUFF", {"value": 22})
```

For asynchronous usage:
```python
import asyncio
import gamesense

# For example purposes, need an event loop 
# Inside normal async functions, you'd just use await on the functions provided on AioGameSense
loop = asyncio.get_event_loop()

# Create a GameSense object instance to use
gs = gamesense.AioGameSense("ASYNC_GAME", "Async Game")

# Before you can register or send events, you must register your game
loop.run_until_complete(gs.register_game())

# Register an event (different than binding an event, see more info in the SteelSeries docs)
loop.run_until_complete(gs.register_event('DID_STUFF'))

# Test out the event by sending the event
loop.run_until_complete(gs.send_event("DID_STUFF", {"value": 23}))
```

The two examples do relatively the same thing. For more information about the SteelSeries GameSense API, see: https://github.com/SteelSeries/gamesense-sdk/tree/master/doc/api for more information. Things like binding handlers and such should be possible, but can be a bit complex. Commits are welcome for making such functionality easier.
