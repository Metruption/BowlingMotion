# Bowling Motion

Motion controlled bowling with android phones

### Dependencies:
* **Python3:** https://www.python.org/
* **PyGame:** https://www.pygame.org/
* **paho-mqtt:** https://eclipse.org/paho/clients/python/
* **scipy:** https://www.scipy.org/

**Resolving the dependencies:**
```bash
pip install Pygame paho-mqtt numpy matplotlib
```

### Known issues:
* Only supports one game to be played worldwide at a time. If two people have the game client open and one throws the ball then both clients will receive the throw.