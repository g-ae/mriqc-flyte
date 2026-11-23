import asyncio
import flyte
import numpy as np

env = flyte.TaskEnvironment(name="helloworld")


@env.task
def square(x: int) -> int:
    return x * x


@env.task
async def main(xs: list[int]) -> int:
    # launch this example by using:
    # flyte run --local examples/hello.py main --xs '[1, 2, 3]'
    # returns 14
    return sum([await square.aio(x) for x in xs])
