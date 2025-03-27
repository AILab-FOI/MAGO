import spade


class DummyAgent(spade.agent.Agent):
    async def setup(self):
        print("Hello, world! I'm agent {}".format(str(self.jid)))


async def main():
    dummy = DummyAgent("alice@localhost", "password")
    await dummy.start()


if __name__ == "__main__":
    spade.run(main())
