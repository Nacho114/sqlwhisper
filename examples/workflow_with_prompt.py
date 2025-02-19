from stockwhisper.workflow import SqlWhisperWorkflow
from stockwhisper.actors import stock_actor

async def main():

    query_str = input("Enter query:")

    w = SqlWhisperWorkflow(stock_actor)
    result = await w.run(query_str=query_str)
    print(result)

if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
