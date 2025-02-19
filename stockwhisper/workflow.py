from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow, step,
    Event,
)

from stockwhisper.actor import Actor
from stockwhisper.actors import stock_actor

class UserQueryIsValidEvent(Event):
    query_str: str

class UserQueryIsNotValidEvent(Event):
    reasoning_str: str

class TextToSqlEvent(Event):
    sql_str: str

class MyWorkflow(Workflow):

    def __init__(self, actor: Actor, timeout: int = 10, verbose: bool = False):
        super().__init__(timeout, verbose)
        self.actor = actor

    @step
    async def validate_user_query(self, ev: StartEvent) -> UserQueryIsValidEvent | UserQueryIsNotValidEvent:
        query_str = ev.query_str
        print(f"Validating user query: {query_str}...")
        validator = self.actor.validate_user_query(query_str)

        if validator.contains_valid_query:
            return UserQueryIsValidEvent(query_str=query_str)
        else:
            return UserQueryIsNotValidEvent(reasoning_str=validator.reasoning)

    @step
    async def invalid_user_query(self, ev: UserQueryIsNotValidEvent) -> StopEvent:
        print(f"Query Invalid: {ev.reasoning_str}")
        return StopEvent(result="Workflow complete with error.")

    @step
    async def convert_text_to_sql(self, ev: UserQueryIsValidEvent) -> TextToSqlEvent:
        print("Query valid, converting to sql...")
        query_str = ev.query_str
        sql_str = self.actor.generate_sql_query_with_context(query_str)
        return TextToSqlEvent(sql_str=sql_str)

    @step
    async def execute_sql_query(self, ev: TextToSqlEvent) -> StopEvent:
        sql_str = ev.sql_str
        print(f"SQL query: {sql_str}")
        df = self.actor.execute_sql_query(sql_str)
        print(df)
        return StopEvent(result="Workflow complete.")

async def main():

    query_str = "Give me the last week of data for gold"
    # query_str = "What is the meaning of lifuru?"

    w = MyWorkflow(stock_actor)
    result = await w.run(query_str=query_str)
    print(result)

if __name__ == "__main__":

    import asyncio

    asyncio.run(main())

    # from llama_index.utils.workflow import draw_all_possible_flows
    # draw_all_possible_flows(MyWorkflow(stock_actor), filename="basic_workflow.html")
