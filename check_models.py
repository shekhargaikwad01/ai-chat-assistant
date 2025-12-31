# check_models.py

from openai import OpenAI

client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key="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")
models = client.models.list()
print([m.id for m in models.data])