from typing import Union
from ..node import Node
from .program_track_action import ProgramTrackAction, programTrackActionFragment
import json
from ...blocks_action_builder import BlocksActionBuilder

programTrackActionResponseFragment = (
    """
fragment ProgramTrackActionResponse on ProgramTrackActionResponse {
    id
    createdAt
    action {
        ...ProgramTrackAction
    }
    response
}
"""
    + programTrackActionFragment
)


class ProgramTrackActionResponse(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)

    @property
    def action(self):
        return ProgramTrackAction(self._data["action"], self._context)

    @property
    def data(self):
        return self._data["response"]

    @property
    def values(self):
        responses = self.data["steps"][0]["fields"]
        blocks = self.action.data["steps"][0]["action"]["blocks"]

        values = {}
        for index, block in enumerate(blocks):
            id = block.get("id")
            if id:
                values[id] = responses[index]

        return values

    async def _set_feedback(self, data, wait_for_feedback=True):
        if not self.action.waits_for_feedback:
            raise RuntimeError(
                "Can't set feedback for this response because its action does not wait for feedback."
            )

        pta = await self._context.client.create_program_track_action(data, wait_for_feedback)

        await self._context.client.update_program_track_action_response(self.id, pta.id)

        return pta

    async def set_feedback_with_data(
        self, data_json: str, wait_for_feedback=True
    ) -> ProgramTrackAction:
        data = json.loads(data_json.replace("\n", "\\n"))

        return await self._set_feedback(data, wait_for_feedback)

    async def set_feedback(
        self, title: str, blocks_action: Union[dict, BlocksActionBuilder], wait_for_feedback=True
    ) -> ProgramTrackAction:
        if isinstance(blocks_action, BlocksActionBuilder):
            blocks_action = blocks_action.build()

        data = {
            "type": "multiStep",
            "steps": [{"name": title, "action": blocks_action}],
        }

        return await self._set_feedback(data, wait_for_feedback)

    async def set_no_feedback(self):
        data = {"type": "multiStep", "steps": []}

        await self._set_feedback(data, False)
