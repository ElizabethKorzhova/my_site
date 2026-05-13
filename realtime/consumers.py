"""This module provides consumers for realtime online counter and push notifications."""
import json
from typing import Any, ClassVar, Dict

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class RealtimeConsumer(AsyncWebsocketConsumer):
    """Represents WebSocket consumer for online users counter and push notifications."""
    group_name: ClassVar[str] = "realtime"
    online_users_count: ClassVar[int] = 0

    async def connect(self) -> None:
        """Handles WebSocket connection."""
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        RealtimeConsumer.online_users_count += 1
        await self.broadcast_online_count()

    async def disconnect(self, close_code: int) -> None:
        """Handles WebSocket disconnection."""
        RealtimeConsumer.online_users_count = max(
            0,
            RealtimeConsumer.online_users_count - 1,
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.broadcast_online_count()

    async def receive(self,
                      text_data: str | None = None,
                      bytes_data: bytes | None = None) -> None:
        """Receives message from client."""
        if text_data is None:
            return

        data: dict[str, Any] = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "notification":
            await self.handle_notification(data)

    async def handle_notification(self, data: Dict[str, Any]) -> None:
        """Handles push notification from client."""
        user = self.scope["user"]

        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.send_json(
                {
                    "type": "error",
                    "message": "Guests cannot send messages.",
                }
            )
            return

        message = str(data.get("message", "")).strip()

        if not message:
            await self.send_json(
                {
                    "type": "error",
                    "message": "Message cannot be empty.",
                }
            )
            return

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "push_notification",
                "message": message,
                "username": user.username,
            },
        )

    async def broadcast_online_count(self) -> None:
        """Broadcast current online users count to all clients."""
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "online_count",
                "count": RealtimeConsumer.online_users_count,
            },
        )

    async def online_count(self, event: Dict[str, Any]) -> None:
        """Sends online counter update to WebSocket client."""
        await self.send_json(
            {
                "type": "online_count",
                "count": event["count"],
            }
        )

    async def push_notification(self, event: Dict[str, Any]) -> None:
        """Sends push notification to WebSocket client."""
        await self.send_json(
            {
                "type": "notification",
                "message": event["message"],
                "username": event["username"],
            }
        )

    async def send_json(self, content: Dict[str, Any]) -> None:
        """Sends JSON data to WebSocket client."""
        await self.send(text_data=json.dumps(content))