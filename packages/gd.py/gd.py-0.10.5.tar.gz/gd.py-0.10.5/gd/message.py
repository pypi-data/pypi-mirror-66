from .typing import Client, Message, Optional, Union

from .abstractentity import AbstractEntity
from .abstractuser import AbstractUser

from .utils.enums import MessageOrRequestType
from .utils.indexer import Index
from .utils.parser import ExtDict
from .utils.text_tools import make_repr
from .utils.crypto.coders import Coder


class Message(AbstractEntity):
    """Class that represents private messages in Geometry Dash.
    This class is derived from :class:`.AbstractEntity`.
    """

    SCHEMA = "Re: {msg.subject}"

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self._body = options.pop("body", "")

    def __repr__(self) -> str:
        info = {"author": self.author, "id": self.id, "is_read": self.is_read()}
        return make_repr(self, info)

    def __str__(self) -> str:
        return str(self.subject)

    @classmethod
    def from_data(
        cls, data: ExtDict, user_2: Union[ExtDict, AbstractUser], client: Client
    ) -> Message:
        user_1 = AbstractUser(
            name=data.get(Index.MESSAGE_SENDER_NAME, "unknown"),
            id=data.getcast(Index.MESSAGE_SENDER_ID, 0, int),
            account_id=data.getcast(Index.MESSAGE_SENDER_ACCOUNT_ID, 0, int),
            client=client,
        )
        if isinstance(user_2, ExtDict):
            user_2 = AbstractUser(**user_2, client=client)

        indicator = data.getcast(Index.MESSAGE_INDICATOR, 0, int)
        is_normal = indicator ^ 1

        subject = Coder.do_base64(
            data.get(Index.MESSAGE_SUBJECT, ""), encode=False, errors="replace"
        )

        return Message(
            id=data.getcast(Index.MESSAGE_ID, 0, int),
            timestamp=data.get(Index.MESSAGE_TIMESTAMP, "unknown"),
            subject=subject,
            is_read=bool(data.getcast(Index.MESSAGE_IS_READ, 0, int)),
            author=(user_1 if is_normal else user_2),
            recipient=(user_2 if is_normal else user_1),
            type=indicator,
            client=client,
        )

    @property
    def author(self) -> AbstractUser:
        """:class:`.AbstractUser`: An author of the message."""
        return self.options.get("author", AbstractUser(client=self.client))

    @property
    def recipient(self) -> AbstractUser:
        """:class:`.AbstractUser`: A recipient of the message."""
        return self.options.get("recipient", AbstractUser(client=self.client))

    @property
    def subject(self) -> str:
        """:class:`str`: A subject of the message, as string."""
        return self.options.get("subject", "")

    @property
    def timestamp(self) -> str:
        """:class:`str`: A human-readable string representing how long ago message was created."""
        return self.options.get("timestamp", "unknown")

    @property
    def type(self) -> MessageOrRequestType:
        """:class:`.MessageOrRequestType`: Whether a message is sent or inbox."""
        return MessageOrRequestType.from_value(self.options.get("type", 0))

    @property
    def body(self) -> Optional[str]:
        """Optional[:class:`str`]: A body of the message. Requires :meth:`.Message.read`."""
        return self._body

    @body.setter
    def body(self, body: str) -> None:
        """Set ``self.body`` to ``body``."""
        self._body = body

    def is_read(self) -> bool:
        """:class:`bool`: Indicates whether message is read or not."""
        return bool(self.options.get("is_read"))

    async def read(self) -> str:
        """|coro|

        Read a message. Set the body of the message to the content.

        Returns
        -------
        :class:`str`
            The content of the message.
        """
        return await self.client.read_message(self)

    async def reply(self, content: str, schema: Optional[str] = None) -> None:
        """|coro|

        Reply to the message. Format the subject according to schema.

        Schema format can only contain ``{msg.attr}`` elements.

        Content also allows schema format.

        Example:

        .. code-block:: python3

            await message.reply(
                content='Replying to message by {msg.author.name}.'
                schema='Re: {msg.subject} ({msg.rating})'
            )
        """
        if schema is None:
            schema = self.SCHEMA

        content, subject = content.format(msg=self), schema.format(msg=self)

        return await self.author.send(subject, content)

    async def delete(self) -> None:
        """|coro|

        Delete a message.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to delete a message.
        """
        await self.client.delete_message(self)
