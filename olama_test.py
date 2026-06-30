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
    The current a summary of news
  """

  return "there are no news"

def Talk(user_in) :



    system_prompt_ger = """Du bist ein Gesprächspartner.

    WICHTIGE REGELN:
    - Erwähne niemals Werkzeuge, deren Verwendung, Funktionen, APIs oder Systemfähigkeiten.
    - Erkläre niemals, warum ein Werkzeug verwendet wurde oder nicht.
    - Sage niemals, dass du keine Werkzeuge verwenden kannst.
    - Sprich niemals über Einschränkungen oder interne Abläufe.

    Wenn der Nutzer etwas Alltägliches sagt (z. B. Begrüßungen, Dank, Smalltalk):
    → Antworte natürlich, wie in einem menschlichen Gespräch.

    Wenn kein Werkzeug benötigt wird:
    → Antworte einfach ganz normal in verständlicher Sprache.

    Entscheide nur im Stillen, ob ein Werkzeug benötigt wird. Sprich nicht über diese Entscheidung."""

    messages = [    {
        "role": "system",
        "content": system_prompt_ger
    },{"role": "user", "content": user_in}]

    response = chat(model='llama3.1:8b', messages=messages, tools=[get_temperature,get_news])

    assistant_message = {
        "role": "assistant",
        "content": response.message.content or "",
        "tool_calls": response.message.tool_calls
    }

    messages.append(assistant_message)

    if response.message.tool_calls:
        for call in response.message.tool_calls:
            match call.function.name:
                case "get_temperature":
                    result = get_temperature(**call.function.arguments)
                case "get_news":
                    result = get_news()
                case _:
                    result = "wrong tool"

            messages.append({
                "role": "tool",
                "content": str(result)
            })

        final_response = chat(
            model='llama3.1:8b',
            messages=messages,
            tools=[get_temperature, get_news]
        )

        return final_response.message.content

    return response.message.content
