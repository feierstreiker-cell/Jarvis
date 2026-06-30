from ollama import chat



def get_temperature(city: str) -> str:
  """Get the current temperature for a city

  Args:
    city: The name of the city

  Returns:
    The current temperature for the city
  """
  temperatures = {
    "New York": "22°C",
    "London": "15°C",
    "Tokyo": "18°C",
  }
  return temperatures.get(city, "Unknown")

def get_news() -> str:
  """Get relevant news

  Returns:
    The current a summury of news
  """

  return "there are no news"

def Talk(user_in) :
    messages = [    {
        "role": "system",
        "content": (
            "You are Jarvis, a helpful offline voice assistant."

            "Your responses will be read aloud by a text-to-speech engine."

            """Always:
            - Speak naturally as if talking to a person.
            - Avoid markdown, bullet points, and numbered lists unless requested.
            - Avoid mentioning formatting.
            - Keep responses concise unless asked for more detail.
            - When using tools, never mention the tool itself. Simply explain the result naturally.
            - If you don't know something, say so honestly."""

        )
    },{"role": "user", "content": user_in}]

    response = chat(model='llama3.1:8b', messages=messages, tools=[get_temperature,get_news])

    print(response.message)

    messages.append(response.message)
    if response.message.tool_calls:
    # only recommended for models which only return a single tool call
        for call in response.message.tool_calls:
            match call.function.name:
                case "get_temperature":
                    result = get_temperature(**call.function.arguments)
                case "get_news":
                    result = get_news()
                case _:
                    result = "wrong tool"

            messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

    final_response = chat(model='llama3.1:8b', messages=messages)
    return final_response.message.content


res = Talk("wie viel grad sind es in New York? und gibt es gerade nachrichten")
print(res)
