import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = (
    Path(__file__).resolve().parent / "youtube_server.py"
)


class YouTubeMCPClient:

    async def get_transcript(self, url: str) -> str:

        server = StdioServerParameters(
            command="python",
            args=[str(SERVER_PATH)],
        )

        async with stdio_client(server) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    "get_youtube_transcript",
                    {
                        "url": url,
                    },
                )

                if result.isError:
                    raise Exception(
                        result.content[0].text
                    )

                return result.structuredContent["result"]


youtube_client = YouTubeMCPClient()