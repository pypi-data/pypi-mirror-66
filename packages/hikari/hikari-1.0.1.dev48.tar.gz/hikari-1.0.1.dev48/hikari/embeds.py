#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Components and entities that are used to describe message embeds on Discord."""
__all__ = [
    "Embed",
    "EmbedThumbnail",
    "EmbedVideo",
    "EmbedImage",
    "EmbedProvider",
    "EmbedAuthor",
    "EmbedFooter",
    "EmbedField",
]

import datetime
import typing

import attr

import hikari.internal.conversions
from hikari import colors
from hikari import entities
from hikari.internal import marshaller


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedFooter(entities.HikariEntity, entities.Deserializable, entities.Serializable):
    """Represents an embed footer."""

    #: The footer text.
    #:
    #: :type: :obj:`str`
    text: str = marshaller.attrib(deserializer=str, serializer=str)

    #: The URL of the footer icon.
    #:
    #: :type: :obj:`str`, optional
    icon_url: typing.Optional[str] = marshaller.attrib(
        deserializer=str, serializer=str, if_undefined=None, default=None
    )

    #: The proxied URL of the footer icon.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`str`, optional
    proxy_icon_url: typing.Optional[str] = marshaller.attrib(
        deserializer=str, transient=True, if_undefined=None, default=None
    )


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedImage(entities.HikariEntity, entities.Deserializable, entities.Serializable):
    """Represents an embed image."""

    #: The URL of the image.
    #:
    #: :type: :obj:`str`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, serializer=str, if_undefined=None, default=None)

    #: The proxied URL of the image.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`str`, optional
    proxy_url: typing.Optional[str] = marshaller.attrib(
        deserializer=str, transient=True, if_undefined=None, default=None
    )

    #: The height of the image.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`int`, optional
    height: typing.Optional[int] = marshaller.attrib(deserializer=int, transient=True, if_undefined=None, default=None)

    #: The width of the image.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`int`, optional
    width: typing.Optional[int] = marshaller.attrib(deserializer=int, transient=True, if_undefined=None, default=None)


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedThumbnail(entities.HikariEntity, entities.Deserializable, entities.Serializable):
    """Represents an embed thumbnail."""

    #: The URL of the thumbnail.
    #:
    #: :type: :obj:`str`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, serializer=str, if_undefined=None, default=None)

    #: The proxied URL of the thumbnail.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`str`, optional
    proxy_url: typing.Optional[str] = marshaller.attrib(
        deserializer=str, transient=True, if_undefined=None, default=None
    )

    #: The height of the thumbnail.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`int`, optional
    height: typing.Optional[int] = marshaller.attrib(deserializer=int, transient=True, if_undefined=None, default=None)

    #: The width of the thumbnail.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`int`, optional
    width: typing.Optional[int] = marshaller.attrib(deserializer=int, transient=True, if_undefined=None, default=None)


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedVideo(entities.HikariEntity, entities.Deserializable):
    """Represents an embed video.

    Note
    ----
    This embed attached object cannot be sent by bots or webhooks while sending
    an embed and therefore shouldn't be initiated like the other embed objects.
    """

    #: The URL of the video.
    #:
    #: :type: :obj:`str`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The height of the video.
    #:
    #: :type: :obj:`int`, optional
    height: typing.Optional[int] = marshaller.attrib(deserializer=int, if_undefined=None)

    #: The width of the video.
    #:
    #: :type: :obj:`int`, optional
    width: typing.Optional[int] = marshaller.attrib(deserializer=int, if_undefined=None)


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedProvider(entities.HikariEntity, entities.Deserializable):
    """Represents an embed provider.

    Note
    ----
    This embed attached object cannot be sent by bots or webhooks while sending
    an embed and therefore shouldn't be initiated like the other embed objects.
    """

    #: The name of the provider.
    #:
    #: :type: :obj:`str`, optional
    name: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The URL of the provider.
    #:
    #: :type: :obj:`str`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None, if_none=None)


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedAuthor(entities.HikariEntity, entities.Deserializable, entities.Serializable):
    """Represents an embed author."""

    #: The name of the author.
    #:
    #: :type: :obj:`str`, optional
    name: typing.Optional[str] = marshaller.attrib(deserializer=str, serializer=str, if_undefined=None, default=None)

    #: The URL of the author.
    #:
    #: :type: :obj:`str`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, serializer=str, if_undefined=None, default=None)

    #: The URL of the author icon.
    #:
    #: :type: :obj:`str`, optional
    icon_url: typing.Optional[str] = marshaller.attrib(
        deserializer=str, serializer=str, if_undefined=None, default=None
    )

    #: The proxied URL of the author icon.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`str`, optional
    proxy_icon_url: typing.Optional[str] = marshaller.attrib(
        deserializer=str, transient=True, if_undefined=None, default=None
    )


@marshaller.marshallable()
@attr.s(slots=True)
class EmbedField(entities.HikariEntity, entities.Deserializable, entities.Serializable):
    """Represents a field in a embed."""

    #: The name of the field.
    #:
    #: :type: :obj:`str`
    name: str = marshaller.attrib(deserializer=str, serializer=str)

    #: The value of the field.
    #:
    #: :type: :obj:`str`
    value: str = marshaller.attrib(deserializer=str, serializer=str)

    #: Whether the field should display inline. Defaults to :obj:`False`.
    #:
    #: :type: :obj:`bool`
    is_inline: bool = marshaller.attrib(
        raw_name="inline", deserializer=bool, serializer=bool, if_undefined=False, default=True
    )


@marshaller.marshallable()
@attr.s(slots=True)
class Embed(entities.HikariEntity, entities.Deserializable, entities.Serializable):
    """Represents an embed."""

    #: The title of the embed.
    #:
    #: :type: :obj:`str`, optional
    title: typing.Optional[str] = marshaller.attrib(deserializer=str, serializer=str, if_undefined=None, default=None)

    #: The description of the embed.
    #:
    #: :type: :obj:`str`, optional
    description: typing.Optional[str] = marshaller.attrib(
        deserializer=str, serializer=str, if_undefined=None, default=None
    )

    #: The URL of the embed.
    #:
    #: :type: :obj:`str`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, serializer=str, if_undefined=None, default=None)

    #: The timestamp of the embed.
    #:
    #: :type: :obj:`datetime.datetime`, optional
    timestamp: typing.Optional[datetime.datetime] = marshaller.attrib(
        deserializer=hikari.internal.conversions.parse_iso_8601_ts,
        serializer=lambda timestamp: timestamp.replace(tzinfo=datetime.timezone.utc).isoformat(),
        if_undefined=None,
        default=None,
    )

    color: typing.Optional[colors.Color] = marshaller.attrib(
        deserializer=colors.Color, serializer=int, if_undefined=None, default=None
    )

    #: The footer of the embed.
    #:
    #: :type: :obj:`EmbedFooter`, optional
    footer: typing.Optional[EmbedFooter] = marshaller.attrib(
        deserializer=EmbedFooter.deserialize, serializer=EmbedFooter.serialize, if_undefined=None, default=None
    )

    #: The image of the embed.
    #:
    #: :type: :obj:`EmbedImage`, optional
    image: typing.Optional[EmbedImage] = marshaller.attrib(
        deserializer=EmbedImage.deserialize, serializer=EmbedImage.serialize, if_undefined=None, default=None
    )

    #: The thumbnail of the embed.
    #:
    #: :type: :obj:`EmbedThumbnail`, optional
    thumbnail: typing.Optional[EmbedThumbnail] = marshaller.attrib(
        deserializer=EmbedThumbnail.deserialize, serializer=EmbedThumbnail.serialize, if_undefined=None, default=None
    )

    #: The video of the embed.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`EmbedVideo`, optional
    video: typing.Optional[EmbedVideo] = marshaller.attrib(
        deserializer=EmbedVideo.deserialize, transient=True, if_undefined=None, default=None,
    )

    #: The provider of the embed.
    #:
    #: Note
    #: ----
    #: This field cannot be set by bots or webhooks while sending an embed and
    #: will be ignored during serialization.
    #:
    #:
    #: :type: :obj:`EmbedProvider`, optional
    provider: typing.Optional[EmbedProvider] = marshaller.attrib(
        deserializer=EmbedProvider.deserialize, transient=True, if_undefined=None, default=None
    )

    #: The author of the embed.
    #:
    #: :type: :obj:`EmbedAuthor`, optional
    author: typing.Optional[EmbedAuthor] = marshaller.attrib(
        deserializer=EmbedAuthor.deserialize, serializer=EmbedAuthor.serialize, if_undefined=None, default=None
    )

    #: The fields of the embed.
    #:
    #: :type: :obj:`typing.Sequence` [ :obj:`EmbedField` ], optional
    fields: typing.Optional[typing.Sequence[EmbedField]] = marshaller.attrib(
        deserializer=lambda fields: [EmbedField.deserialize(f) for f in fields],
        serializer=lambda fields: [f.serialize() for f in fields],
        if_undefined=None,
        default=None,
    )
