# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: node_debug_interface.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='node_debug_interface.proto',
  package='debug',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1anode_debug_interface.proto\x12\x05\x64\x65\x62ug\"\x17\n\x15GetNodeDetailsRequest\"\x7f\n\x16GetNodeDetailsResponse\x12\x37\n\x05stats\x18\x01 \x03(\x0b\x32(.debug.GetNodeDetailsResponse.StatsEntry\x1a,\n\nStatsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x12\n\x10GetEventsRequest\"1\n\x11GetEventsResponse\x12\x1c\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x0c.debug.Event\"6\n\x05\x45vent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x0c\n\x04json\x18\x03 \x01(\t2\xa7\x01\n\x12NodeDebugInterface\x12O\n\x0eGetNodeDetails\x12\x1c.debug.GetNodeDetailsRequest\x1a\x1d.debug.GetNodeDetailsResponse\"\x00\x12@\n\tGetEvents\x12\x17.debug.GetEventsRequest\x1a\x18.debug.GetEventsResponse\"\x00\x62\x06proto3'
)




_GETNODEDETAILSREQUEST = _descriptor.Descriptor(
  name='GetNodeDetailsRequest',
  full_name='debug.GetNodeDetailsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=37,
  serialized_end=60,
)


_GETNODEDETAILSRESPONSE_STATSENTRY = _descriptor.Descriptor(
  name='StatsEntry',
  full_name='debug.GetNodeDetailsResponse.StatsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='debug.GetNodeDetailsResponse.StatsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='debug.GetNodeDetailsResponse.StatsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=189,
)

_GETNODEDETAILSRESPONSE = _descriptor.Descriptor(
  name='GetNodeDetailsResponse',
  full_name='debug.GetNodeDetailsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stats', full_name='debug.GetNodeDetailsResponse.stats', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETNODEDETAILSRESPONSE_STATSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=189,
)


_GETEVENTSREQUEST = _descriptor.Descriptor(
  name='GetEventsRequest',
  full_name='debug.GetEventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=191,
  serialized_end=209,
)


_GETEVENTSRESPONSE = _descriptor.Descriptor(
  name='GetEventsResponse',
  full_name='debug.GetEventsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='events', full_name='debug.GetEventsResponse.events', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=211,
  serialized_end=260,
)


_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='debug.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='debug.Event.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='debug.Event.timestamp', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='json', full_name='debug.Event.json', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=262,
  serialized_end=316,
)

_GETNODEDETAILSRESPONSE_STATSENTRY.containing_type = _GETNODEDETAILSRESPONSE
_GETNODEDETAILSRESPONSE.fields_by_name['stats'].message_type = _GETNODEDETAILSRESPONSE_STATSENTRY
_GETEVENTSRESPONSE.fields_by_name['events'].message_type = _EVENT
DESCRIPTOR.message_types_by_name['GetNodeDetailsRequest'] = _GETNODEDETAILSREQUEST
DESCRIPTOR.message_types_by_name['GetNodeDetailsResponse'] = _GETNODEDETAILSRESPONSE
DESCRIPTOR.message_types_by_name['GetEventsRequest'] = _GETEVENTSREQUEST
DESCRIPTOR.message_types_by_name['GetEventsResponse'] = _GETEVENTSRESPONSE
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetNodeDetailsRequest = _reflection.GeneratedProtocolMessageType('GetNodeDetailsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETNODEDETAILSREQUEST,
  '__module__' : 'node_debug_interface_pb2'
  # @@protoc_insertion_point(class_scope:debug.GetNodeDetailsRequest)
  })
_sym_db.RegisterMessage(GetNodeDetailsRequest)

GetNodeDetailsResponse = _reflection.GeneratedProtocolMessageType('GetNodeDetailsResponse', (_message.Message,), {

  'StatsEntry' : _reflection.GeneratedProtocolMessageType('StatsEntry', (_message.Message,), {
    'DESCRIPTOR' : _GETNODEDETAILSRESPONSE_STATSENTRY,
    '__module__' : 'node_debug_interface_pb2'
    # @@protoc_insertion_point(class_scope:debug.GetNodeDetailsResponse.StatsEntry)
    })
  ,
  'DESCRIPTOR' : _GETNODEDETAILSRESPONSE,
  '__module__' : 'node_debug_interface_pb2'
  # @@protoc_insertion_point(class_scope:debug.GetNodeDetailsResponse)
  })
_sym_db.RegisterMessage(GetNodeDetailsResponse)
_sym_db.RegisterMessage(GetNodeDetailsResponse.StatsEntry)

GetEventsRequest = _reflection.GeneratedProtocolMessageType('GetEventsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETEVENTSREQUEST,
  '__module__' : 'node_debug_interface_pb2'
  # @@protoc_insertion_point(class_scope:debug.GetEventsRequest)
  })
_sym_db.RegisterMessage(GetEventsRequest)

GetEventsResponse = _reflection.GeneratedProtocolMessageType('GetEventsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETEVENTSRESPONSE,
  '__module__' : 'node_debug_interface_pb2'
  # @@protoc_insertion_point(class_scope:debug.GetEventsResponse)
  })
_sym_db.RegisterMessage(GetEventsResponse)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), {
  'DESCRIPTOR' : _EVENT,
  '__module__' : 'node_debug_interface_pb2'
  # @@protoc_insertion_point(class_scope:debug.Event)
  })
_sym_db.RegisterMessage(Event)


_GETNODEDETAILSRESPONSE_STATSENTRY._options = None

_NODEDEBUGINTERFACE = _descriptor.ServiceDescriptor(
  name='NodeDebugInterface',
  full_name='debug.NodeDebugInterface',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=319,
  serialized_end=486,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetNodeDetails',
    full_name='debug.NodeDebugInterface.GetNodeDetails',
    index=0,
    containing_service=None,
    input_type=_GETNODEDETAILSREQUEST,
    output_type=_GETNODEDETAILSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetEvents',
    full_name='debug.NodeDebugInterface.GetEvents',
    index=1,
    containing_service=None,
    input_type=_GETEVENTSREQUEST,
    output_type=_GETEVENTSRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_NODEDEBUGINTERFACE)

DESCRIPTOR.services_by_name['NodeDebugInterface'] = _NODEDEBUGINTERFACE

# @@protoc_insertion_point(module_scope)
