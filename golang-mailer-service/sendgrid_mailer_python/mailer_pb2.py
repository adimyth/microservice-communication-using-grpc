# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mailer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0cmailer.proto\x12\x06mailer"_\n\x0fSendMailRequest\x12\x16\n\x0ereceiver_email\x18\x01 \x01(\t\x12\x15\n\rreceiver_name\x18\x02 \x01(\t\x12\x0f\n\x07subject\x18\x03 \x01(\t\x12\x0c\n\x04\x62ody\x18\x04 \x01(\t"#\n\x10SendMailResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32Q\n\rMailerService\x12@\n\tSendMails\x12\x17.mailer.SendMailRequest\x1a\x18.mailer.SendMailResponse"\x00\x42\x13Z\x11./sendgrid-mailerb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "mailer_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"Z\021./sendgrid-mailer"
    _SENDMAILREQUEST._serialized_start = 24
    _SENDMAILREQUEST._serialized_end = 119
    _SENDMAILRESPONSE._serialized_start = 121
    _SENDMAILRESPONSE._serialized_end = 156
    _MAILERSERVICE._serialized_start = 158
    _MAILERSERVICE._serialized_end = 239
# @@protoc_insertion_point(module_scope)