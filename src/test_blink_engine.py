import time

from blink.blink_engine import BlinkEngine, BlinkEvent

engine = BlinkEngine()

print("===== Blink Engine Test =====")

# Eyes open
print(engine.update(0.30))

# Eyes close
print(engine.update(0.15))

time.sleep(0.2)

# Eyes open again
print(engine.update(0.30))

time.sleep(1)

# Eyes close again
print(engine.update(0.15))

time.sleep(1.2)

# Eyes open
print(engine.update(0.30))