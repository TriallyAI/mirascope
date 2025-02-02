import asyncio

from mirascope.core import BaseTool, openai, prompt_template


class FormatBook(BaseTool):
    title: str
    author: str

    async def call(self) -> str:
        # Simulating an async API call
        await asyncio.sleep(1)
        return f"{self.title} by {self.author}"


@openai.call(model="gpt-4o-mini", tools=[FormatBook])
@prompt_template("Recommend a {genre} book")
async def recommend_book(genre: str): ...


async def main():
    response = await recommend_book("fantasy")
    if isinstance((tool := response.tool), FormatBook):
        output = await tool.call()
        print(output)
    else:
        print(response.content)


asyncio.run(main())
