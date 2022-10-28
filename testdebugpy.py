# addon version 2.0.0 +

import signal
import debugpy
import os

debugpy.listen(("0.0.0.0", 5679))
print("debugpy version is: " + debugpy.__version__)
print("Waiting")
debugpy.wait_for_client()

print("Connected")
# pid = os.getpid()
# print("PID: ", pid)
# print("Killed")
# os.kill(pid, signal.SIGTERM)
input('Press Enter to Exit')