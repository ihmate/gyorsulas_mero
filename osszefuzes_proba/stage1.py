from shared_memory_dict import SharedMemoryDict
from time import sleep

smd_config = SharedMemoryDict(name='config', size=1024)

def funkcio():
    smd_config["status"] = 0

    while True:
        smd_config["status"] += 1
        sleep(1)

if __name__ == "__main__":
    funkcio()