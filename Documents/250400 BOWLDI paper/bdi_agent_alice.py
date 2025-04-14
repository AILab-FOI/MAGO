import asyncio
import spade
from spade_bdi.bdi import BDIAgent
from bowldi import BOWLDIConverter


async def main():
    a = BDIAgent("alice@localhost", "password", "empty.asl")

    await a.start()
    await asyncio.sleep(1)

    converter = BOWLDIConverter(input_data_path="onto_example.rdf",)
    converter.add_beliefs_to_agent(a.bdi_agent)

    a.bdi_agent.dump()

    await asyncio.sleep(1)
    await a.stop()


if __name__ == "__main__":
    spade.run(main())
