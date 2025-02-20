from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow, step,
    Event,
)

from sqlwhisper.actor import Actor

class UserQueryIsValidEvent(Event):
    query_str: str

class UserQueryIsNotValidEvent(Event):
    reasoning_str: str

class TextToSqlEvent(Event):
    sql_str: str

class SqlWhisperWorkflow(Workflow):

    def __init__(self, actor: Actor, timeout: int = 10, verbose: bool = False):
        super().__init__(timeout, verbose)
        self.actor = actor

    @step
    async def validate_user_query(self, ev: StartEvent) -> UserQueryIsValidEvent | UserQueryIsNotValidEvent:
        query_str = ev.query_str
        print(f"Validating user query:\n\n {query_str}...\n")
        validator = self.actor.validate_user_query(query_str)

        if validator.contains_valid_query:
            return UserQueryIsValidEvent(query_str=query_str)
        else:
            return UserQueryIsNotValidEvent(reasoning_str=validator.reasoning)

    @step
    async def invalid_user_query(self, ev: UserQueryIsNotValidEvent) -> StopEvent:
        print(f"Query Invalid: \n\n{ev.reasoning_str}\n\n")
        return StopEvent(result="Workflow complete with error.")

    @step
    async def convert_text_to_sql(self, ev: UserQueryIsValidEvent) -> TextToSqlEvent:
        print("Query valid, converting to sql...\n")
        query_str = ev.query_str
        sql_str = self.actor.generate_sql_query(query_str)
        return TextToSqlEvent(sql_str=sql_str)

    @step
    async def execute_sql_query(self, ev: TextToSqlEvent) -> StopEvent:
        sql_str = ev.sql_str
        print(f"SQL query: \n\n{sql_str}\n")
        df = self.actor.execute_sql_query(sql_str)
        print(f"{df}\n")
        return StopEvent(result="Workflow complete.")

