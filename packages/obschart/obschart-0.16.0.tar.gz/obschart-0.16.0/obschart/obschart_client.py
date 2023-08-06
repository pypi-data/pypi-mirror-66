from .obschart_api_transport import ObschartApiTransport
from .api.nodes import ProgramTrackActionResponse
from typing import Optional, Union, Any, Callable
from .blocks_action_builder import BlocksActionBuilder
from typing import Awaitable
import asyncio
from .gql import GqlClient
from .api import ObschartApiClient
import io
import logging

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

OnResponseCallback = Callable[[ProgramTrackActionResponse], Awaitable[None]]

log = logging.getLogger(__name__)


class ObschartClient(ObschartApiClient):
    _transport: ObschartApiTransport

    def __init__(
        self,
        authentication_token: Optional[str] = None,
        api_url: Optional[str] = "https://api.obschart.com/",
    ):

        self._transport = ObschartApiTransport(api_url)
        gql_client = GqlClient(transport=self._transport)
        super().__init__(gql_client=gql_client)

        if authentication_token:
            self.set_authentication_token(authentication_token)

    def set_authentication_token(self, authentication_token: str):
        self._transport._client.headers["Authorization"] = f"Bearer {authentication_token}"

    async def login(self, email: str, password: str):
        authentication_token, session = await self.create_session(email, password)
        self.set_authentication_token(authentication_token)
        return session

    def on_response(self, on_response_callback: OnResponseCallback):
        async def main() -> Any:
            while True:
                responses = await self.poll_program_track_action_responses(
                    {"applicationId": {"eq": "me"}}
                )

                for response in responses:

                    async def task():
                        try:
                            log.debug("Handling response...")
                            await on_response_callback(response)
                            log.debug("Response handled")
                        except:
                            log.exception("Could not handle response: %s", response)

                    asyncio.ensure_future(task())

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        # https://stackoverflow.com/a/37345564/11225752
        # loop.run_until_complete(asyncio.Task.all_tasks())

    def build_feedback_data(self):
        return BlocksActionBuilder()

    def create_image(self, image_like: Union[plt.Figure, str, Any]):
        if isinstance(image_like, str):
            file_path = image_like
            image = open(file_path, "rb")
        elif plt and isinstance(image_like, plt.Figure):
            figure = image_like

            buffer = io.BytesIO()
            figure.savefig(buffer, format="png")
            buffer.seek(0)

            image = buffer
        else:
            image = image_like

        return super().create_image(image)
