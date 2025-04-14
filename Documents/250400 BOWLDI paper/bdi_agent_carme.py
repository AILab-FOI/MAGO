import asyncio
import spade
from spade_bdi.bdi import BDIAgent
from bowldi import BOWLDIConverter


async def main():
    a = BDIAgent("carme@localhost", "password", "output.asl")

    await a.start()
    await asyncio.sleep(1)

    converter = BOWLDIConverter()
    converter.convert_agent_beliefs_to_ontology(
        a.bdi_agent, "onto_carme.owl")

    await asyncio.sleep(1)
    await a.stop()


if __name__ == "__main__":
    spade.run(main())
