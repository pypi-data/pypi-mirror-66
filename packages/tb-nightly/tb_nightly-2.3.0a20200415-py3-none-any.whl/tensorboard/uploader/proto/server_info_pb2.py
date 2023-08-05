# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/uploader/proto/server_info.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/uploader/proto/server_info.proto',
  package='tensorboard.service',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n,tensorboard/uploader/proto/server_info.proto\x12\x13tensorboard.service\"l\n\x11ServerInfoRequest\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x46\n\x14plugin_specification\x18\x02 \x01(\x0b\x32(.tensorboard.service.PluginSpecification\"\xb7\x02\n\x12ServerInfoResponse\x12\x39\n\rcompatibility\x18\x01 \x01(\x0b\x32\".tensorboard.service.Compatibility\x12\x32\n\napi_server\x18\x02 \x01(\x0b\x32\x1e.tensorboard.service.ApiServer\x12<\n\nurl_format\x18\x03 \x01(\x0b\x32(.tensorboard.service.ExperimentUrlFormat\x12:\n\x0eplugin_control\x18\x04 \x01(\x0b\x32\".tensorboard.service.PluginControl\x12\x38\n\rupload_limits\x18\x05 \x01(\x0b\x32!.tensorboard.service.UploadLimits\"\\\n\rCompatibility\x12:\n\x07verdict\x18\x01 \x01(\x0e\x32).tensorboard.service.CompatibilityVerdict\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\"\x1d\n\tApiServer\x12\x10\n\x08\x65ndpoint\x18\x01 \x01(\t\"?\n\x13\x45xperimentUrlFormat\x12\x10\n\x08template\x18\x01 \x01(\t\x12\x16\n\x0eid_placeholder\x18\x02 \x01(\t\"-\n\x13PluginSpecification\x12\x16\n\x0eupload_plugins\x18\x02 \x03(\t\"(\n\rPluginControl\x12\x17\n\x0f\x61llowed_plugins\x18\x01 \x03(\t\"%\n\x0cUploadLimits\x12\x15\n\rmax_blob_size\x18\x01 \x01(\x03*`\n\x14\x43ompatibilityVerdict\x12\x13\n\x0fVERDICT_UNKNOWN\x10\x00\x12\x0e\n\nVERDICT_OK\x10\x01\x12\x10\n\x0cVERDICT_WARN\x10\x02\x12\x11\n\rVERDICT_ERROR\x10\x03\x62\x06proto3')
)

_COMPATIBILITYVERDICT = _descriptor.EnumDescriptor(
  name='CompatibilityVerdict',
  full_name='tensorboard.service.CompatibilityVerdict',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VERDICT_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERDICT_OK', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERDICT_WARN', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERDICT_ERROR', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=811,
  serialized_end=907,
)
_sym_db.RegisterEnumDescriptor(_COMPATIBILITYVERDICT)

CompatibilityVerdict = enum_type_wrapper.EnumTypeWrapper(_COMPATIBILITYVERDICT)
VERDICT_UNKNOWN = 0
VERDICT_OK = 1
VERDICT_WARN = 2
VERDICT_ERROR = 3



_SERVERINFOREQUEST = _descriptor.Descriptor(
  name='ServerInfoRequest',
  full_name='tensorboard.service.ServerInfoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='tensorboard.service.ServerInfoRequest.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='plugin_specification', full_name='tensorboard.service.ServerInfoRequest.plugin_specification', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=177,
)


_SERVERINFORESPONSE = _descriptor.Descriptor(
  name='ServerInfoResponse',
  full_name='tensorboard.service.ServerInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='compatibility', full_name='tensorboard.service.ServerInfoResponse.compatibility', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='api_server', full_name='tensorboard.service.ServerInfoResponse.api_server', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url_format', full_name='tensorboard.service.ServerInfoResponse.url_format', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='plugin_control', full_name='tensorboard.service.ServerInfoResponse.plugin_control', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='upload_limits', full_name='tensorboard.service.ServerInfoResponse.upload_limits', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=491,
)


_COMPATIBILITY = _descriptor.Descriptor(
  name='Compatibility',
  full_name='tensorboard.service.Compatibility',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='verdict', full_name='tensorboard.service.Compatibility.verdict', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='details', full_name='tensorboard.service.Compatibility.details', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=493,
  serialized_end=585,
)


_APISERVER = _descriptor.Descriptor(
  name='ApiServer',
  full_name='tensorboard.service.ApiServer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='endpoint', full_name='tensorboard.service.ApiServer.endpoint', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=587,
  serialized_end=616,
)


_EXPERIMENTURLFORMAT = _descriptor.Descriptor(
  name='ExperimentUrlFormat',
  full_name='tensorboard.service.ExperimentUrlFormat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='template', full_name='tensorboard.service.ExperimentUrlFormat.template', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id_placeholder', full_name='tensorboard.service.ExperimentUrlFormat.id_placeholder', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=618,
  serialized_end=681,
)


_PLUGINSPECIFICATION = _descriptor.Descriptor(
  name='PluginSpecification',
  full_name='tensorboard.service.PluginSpecification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='upload_plugins', full_name='tensorboard.service.PluginSpecification.upload_plugins', index=0,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=683,
  serialized_end=728,
)


_PLUGINCONTROL = _descriptor.Descriptor(
  name='PluginControl',
  full_name='tensorboard.service.PluginControl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='allowed_plugins', full_name='tensorboard.service.PluginControl.allowed_plugins', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=730,
  serialized_end=770,
)


_UPLOADLIMITS = _descriptor.Descriptor(
  name='UploadLimits',
  full_name='tensorboard.service.UploadLimits',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_blob_size', full_name='tensorboard.service.UploadLimits.max_blob_size', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=772,
  serialized_end=809,
)

_SERVERINFOREQUEST.fields_by_name['plugin_specification'].message_type = _PLUGINSPECIFICATION
_SERVERINFORESPONSE.fields_by_name['compatibility'].message_type = _COMPATIBILITY
_SERVERINFORESPONSE.fields_by_name['api_server'].message_type = _APISERVER
_SERVERINFORESPONSE.fields_by_name['url_format'].message_type = _EXPERIMENTURLFORMAT
_SERVERINFORESPONSE.fields_by_name['plugin_control'].message_type = _PLUGINCONTROL
_SERVERINFORESPONSE.fields_by_name['upload_limits'].message_type = _UPLOADLIMITS
_COMPATIBILITY.fields_by_name['verdict'].enum_type = _COMPATIBILITYVERDICT
DESCRIPTOR.message_types_by_name['ServerInfoRequest'] = _SERVERINFOREQUEST
DESCRIPTOR.message_types_by_name['ServerInfoResponse'] = _SERVERINFORESPONSE
DESCRIPTOR.message_types_by_name['Compatibility'] = _COMPATIBILITY
DESCRIPTOR.message_types_by_name['ApiServer'] = _APISERVER
DESCRIPTOR.message_types_by_name['ExperimentUrlFormat'] = _EXPERIMENTURLFORMAT
DESCRIPTOR.message_types_by_name['PluginSpecification'] = _PLUGINSPECIFICATION
DESCRIPTOR.message_types_by_name['PluginControl'] = _PLUGINCONTROL
DESCRIPTOR.message_types_by_name['UploadLimits'] = _UPLOADLIMITS
DESCRIPTOR.enum_types_by_name['CompatibilityVerdict'] = _COMPATIBILITYVERDICT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServerInfoRequest = _reflection.GeneratedProtocolMessageType('ServerInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFOREQUEST,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ServerInfoRequest)
  })
_sym_db.RegisterMessage(ServerInfoRequest)

ServerInfoResponse = _reflection.GeneratedProtocolMessageType('ServerInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORESPONSE,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ServerInfoResponse)
  })
_sym_db.RegisterMessage(ServerInfoResponse)

Compatibility = _reflection.GeneratedProtocolMessageType('Compatibility', (_message.Message,), {
  'DESCRIPTOR' : _COMPATIBILITY,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.Compatibility)
  })
_sym_db.RegisterMessage(Compatibility)

ApiServer = _reflection.GeneratedProtocolMessageType('ApiServer', (_message.Message,), {
  'DESCRIPTOR' : _APISERVER,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ApiServer)
  })
_sym_db.RegisterMessage(ApiServer)

ExperimentUrlFormat = _reflection.GeneratedProtocolMessageType('ExperimentUrlFormat', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTURLFORMAT,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ExperimentUrlFormat)
  })
_sym_db.RegisterMessage(ExperimentUrlFormat)

PluginSpecification = _reflection.GeneratedProtocolMessageType('PluginSpecification', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINSPECIFICATION,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PluginSpecification)
  })
_sym_db.RegisterMessage(PluginSpecification)

PluginControl = _reflection.GeneratedProtocolMessageType('PluginControl', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINCONTROL,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PluginControl)
  })
_sym_db.RegisterMessage(PluginControl)

UploadLimits = _reflection.GeneratedProtocolMessageType('UploadLimits', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADLIMITS,
  '__module__' : 'tensorboard.uploader.proto.server_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.UploadLimits)
  })
_sym_db.RegisterMessage(UploadLimits)


# @@protoc_insertion_point(module_scope)
