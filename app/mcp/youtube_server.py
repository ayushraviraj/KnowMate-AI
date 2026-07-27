from mcp.server.fastmcp import FastMCP
from mcp.types import AnyUrl
from youtube_transcript_api import YouTubeTranscriptApi

mcp = FastMCP(
    "youtube-mcp-server",
    dependencies=["youtube-transcript-api"],
)


@mcp.tool()
def get_youtube_transcript(url: AnyUrl) -> str:
    """
    Get transcript for a YouTube video URL.
    """

    params = dict(url.query_params())

    if "v" not in params:
        raise ValueError("Invalid YouTube URL")

    video_id = params["v"]

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    full_text = " ".join(
        snippet.text for snippet in transcript
    )

    return full_text


if __name__ == "__main__":
    mcp.run()