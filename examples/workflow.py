from stockwhisper.workflow import SqlWhisperWorkflow
from stockwhisper.actors import stock_actor

async def main():

    query_str = "Give me the last week of data for gold"
    # query_str = "What is the meaning of lifuru?"

    # FAILS
    # query_str = " Give me the average of the last 5 close prices for copper"

    w = SqlWhisperWorkflow(stock_actor)
    result = await w.run(query_str=query_str)
    print(result)

if __name__ == "__main__":

    import asyncio

    asyncio.run(main())

    # from llama_index.utils.workflow import draw_all_possible_flows
    # draw_all_possible_flows(MyWorkflow(stock_actor), filename="basic_workflow.html")
