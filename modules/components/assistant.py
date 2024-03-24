from time import sleep
import os
import openai
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from openai.types.beta import Thread
from modules.components.execute_agent import execute_agent
from modules.components.stream_handler import EventHandler

class AiCanAssistant:
    ASSISTANT_NAME = "AiCanAsst"
    LLM_MODEL = "gpt-4-turbo-preview"

    def __init__(self, assistant_id: str = None, openai_key: str = None):
        self.assistant_id = assistant_id
        self.openai_key = openai_key

        self.assistant = openai.beta.assistants.retrieve(assistant_id=assistant_id)

        self.instructions = """Therapeutics Support Platform supporting the outcomes and everyday goals of People with Disabilities through AI powered activities adhered to their specific therapy plan. We bring to life their therapist’s expertise and specific plan to them from anywhere in the world. Please use the your retrieved files and thread files to answer the question, providing helpful and directional advice with respect to the question as it relates to your expertise in this field. Your answer should be detailed and specific, but must be grounded on actual facts and information.If the question does not relate to the user's information or Therapeutics Support, then please respond that your focus is supporting people with disabilities on Therapeutics."""

        self.context_file_ids = []
        self.openai_tools = [{"type": "retrieval"}, {"type": "code_interpreter"}]

        self.agent = None
        self.custom_tools = []

    def update(self):
        self.assistant = openai.beta.assistants.update(
            assistant_id=self.assistant_id,
            name="AiCanAsst",
            instructions=self.instructions,
            tools=self.openai_tools + self.openai_tools,
            model=AiCanAssistant.LLM_MODEL
        )

    """
    Method to initialize the assistant by uploading context files and updating the OpenAI assistant.
    """
    def initialise(self):
        self.upload_context_file(
            "./data/assistant-context.txt"
            )

        self.assistant = openai.beta.assistants.update(
            assistant_id=self.assistant_id,
            file_ids=self.context_file_ids,
        )

    def upload_context_file(self, file_name: str):
        file = self.add_file(file_name)
        self.context_file_ids.append(file.id)

    def add_file(self, file_name: str):
        file = openai.files.create(
            file=open(file_name, "rb"),
            purpose='assistants'
        )
        return file

    def create_thread(self) -> Thread:
        thread = openai.beta.threads.create()

        return thread
    
    def run_thread(self, thread: Thread):
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id
        )

        messages = []

        print(f"Waiting for run ({run.id}) to complete...")

        seconds = 0
        interval = 5
        while True:
            sleep(interval)
            seconds += interval
            print(f"Checking run ({run.id}) status... ({seconds} seconds so far)")
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.status == "completed":
                messages = openai.beta.threads.messages.list(
                    thread_id=thread.id
                )
                break

        return messages

    def refresh_agent(self):
        self.agent = OpenAIAssistantRunnable(assistant_id=self.assistant_id, as_agent=True)

    def run_agent(self, user_message: str, thread_id: str):
        return execute_agent(
            self.agent,
            self.custom_tools,
            {
                "content": user_message,
                "thread_id": thread_id
            }
        )

    def get_thread(thread_id: str):
        thread = openai.beta.threads.retrieve(
            thread_id=thread_id
        )
        return thread
    
    def read_thread(thread_id: str):
        messages = openai.beta.threads.messages.list(
            thread_id=thread_id
        )

        return messages

    def get_messages_count(thread_id: str) -> int:
        messages = openai.beta.threads.messages.list(
            thread_id=thread_id
        )
        print(messages.data)
        print(len(messages.data))
        return len(messages.data)

    def add_message(thread_id: str, role: str, content: str):
        new_msg = openai.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content
        )
        return new_msg

