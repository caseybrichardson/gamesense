# gamesense-python-sdk
A Python SDK for use with SteelSeries GameSense 3.8.X+

## Installation
The only remote dependency is requests. Install that with pip.

## Usage
Relatively simple to use.

```python
# Create a GameSense object instance to use
gs = GameSense("PYTHON_SDK", "Python SDK")

# Before you can register or send events, you must register your game
gs.register_game(icon_color_id=GS_ICON_GOLD)

# Register an event (different than binding an event, see more info in the SteelSeries docs)
gs.register_event("DID_STUFF")

# Test out the event by sending the event
gs.send_event("DID_STUFF", {"value": 22})
```

## Todo (at the moment)
* Support more of the endpoints with nice API wrappers for minimal interaction/message building (main endpoint being `/bind_game_event`)
* Cleanup the constants declared in the module

## License
MIT License

Copyright (c) 2016 Casey Richardson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
