import asyncio
import time
import spade
from spade_bdi.bdi import BDIAgent

async def main():
    a = BDIAgent("BasicAgent_BDI@localhost", "SPADE", "output.asl")

    await a.start()

    await asyncio.sleep(1)

    a.bdi.print_beliefs()

    time.sleep(1)

    await a.stop()

if __name__ == "__main__":
    spade.run(main())

