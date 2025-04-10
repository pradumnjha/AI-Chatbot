from botbuilder.core import ActivityHandler, TurnContext
from openai import OpenAI
import requests

class KnowledgeBot(ActivityHandler):
    def __init__(self, config):
        self.config = config
        self.openai = OpenAI(api_key=config.openai_api_key)

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text
        search_results = self.search_confluence(user_input)
        summary = self.query_openai(user_input, search_results)

        await turn_context.send_activity(summary)

    def search_confluence(self, query):
        url = f"https://YOUR_ORGANIZATIONAL_NAME.atlassian.net/wiki/rest/api/content/search?cql=text~\"{query}\""
        headers = {
            "Authorization": f"Basic {self.config.confluence_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return [f"{r['title']}: https://YOUR_ORGANIZATIONAL_NAME.atlassian.net/wiki{r['_links']['webui']}" for r in results]
        return ["No relevant Confluence results found."]

    def query_openai(self, question, results):
        context = "\n".join(results[:5])
        prompt = f"Using the following documentation context, answer the question:\n{context}\n\nQuestion: {question}"
        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an internal documentation assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
