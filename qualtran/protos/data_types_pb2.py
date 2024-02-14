# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data_types.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data_types.proto',
  package='qualtran',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10\x64\x61ta_types.proto\x12\x08qualtran\"\xd6\x02\n\x06QDType\x12\x15\n\x0b\x62itsize_int\x18\x01 \x01(\x03H\x00\x12\x16\n\x0c\x62itsize_expr\x18\x02 \x01(\tH\x00\x12\x1e\n\x04qbit\x18\x03 \x01(\x0b\x32\x0e.qualtran.QBitH\x01\x12\x1e\n\x04qany\x18\x04 \x01(\x0b\x32\x0e.qualtran.QAnyH\x01\x12\x1e\n\x04qint\x18\x05 \x01(\x0b\x32\x0e.qualtran.QIntH\x01\x12*\n\x0bq_ones_comp\x18\x06 \x01(\x0b\x32\x13.qualtran.QOnesCompH\x01\x12 \n\x05quint\x18\x07 \x01(\x0b\x32\x0f.qualtran.QUIntH\x01\x12/\n\rbounded_q_int\x18\x08 \x01(\x0b\x32\x16.qualtran.BoundedQUIntH\x01\x12&\n\x05q_fxp\x18\t \x01(\x0b\x32\x15.qualtran.QFixedPointH\x01\x42\t\n\x07\x62itsizeB\x0b\n\tdata_type\"\x06\n\x04QBit\"\x06\n\x04QAny\"\x06\n\x04QInt\"\x0b\n\tQOnesComp\"\x07\n\x05QUInt\"(\n\x0c\x42oundedQUInt\x12\x18\n\x10iteration_length\x18\x01 \x01(\x03\"/\n\x0bQFixedPoint\x12\x10\n\x08num_frac\x18\x01 \x01(\x03\x12\x0e\n\x06signed\x18\x02 \x01(\x08\x62\x06proto3'
)




_QDTYPE = _descriptor.Descriptor(
  name='QDType',
  full_name='qualtran.QDType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bitsize_int', full_name='qualtran.QDType.bitsize_int', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bitsize_expr', full_name='qualtran.QDType.bitsize_expr', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='qbit', full_name='qualtran.QDType.qbit', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='qany', full_name='qualtran.QDType.qany', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='qint', full_name='qualtran.QDType.qint', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='q_ones_comp', full_name='qualtran.QDType.q_ones_comp', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quint', full_name='qualtran.QDType.quint', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bounded_q_int', full_name='qualtran.QDType.bounded_q_int', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='q_fxp', full_name='qualtran.QDType.q_fxp', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
    _descriptor.OneofDescriptor(
      name='bitsize', full_name='qualtran.QDType.bitsize',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='data_type', full_name='qualtran.QDType.data_type',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=31,
  serialized_end=373,
)


_QBIT = _descriptor.Descriptor(
  name='QBit',
  full_name='qualtran.QBit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
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
  serialized_start=375,
  serialized_end=381,
)


_QANY = _descriptor.Descriptor(
  name='QAny',
  full_name='qualtran.QAny',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
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
  serialized_start=383,
  serialized_end=389,
)


_QINT = _descriptor.Descriptor(
  name='QInt',
  full_name='qualtran.QInt',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
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
  serialized_start=391,
  serialized_end=397,
)


_QONESCOMP = _descriptor.Descriptor(
  name='QOnesComp',
  full_name='qualtran.QOnesComp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
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
  serialized_start=399,
  serialized_end=410,
)


_QUINT = _descriptor.Descriptor(
  name='QUInt',
  full_name='qualtran.QUInt',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
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
  serialized_start=412,
  serialized_end=419,
)


_BOUNDEDQUINT = _descriptor.Descriptor(
  name='BoundedQUInt',
  full_name='qualtran.BoundedQUInt',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='iteration_length', full_name='qualtran.BoundedQUInt.iteration_length', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=421,
  serialized_end=461,
)


_QFIXEDPOINT = _descriptor.Descriptor(
  name='QFixedPoint',
  full_name='qualtran.QFixedPoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_frac', full_name='qualtran.QFixedPoint.num_frac', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signed', full_name='qualtran.QFixedPoint.signed', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=463,
  serialized_end=510,
)

_QDTYPE.fields_by_name['qbit'].message_type = _QBIT
_QDTYPE.fields_by_name['qany'].message_type = _QANY
_QDTYPE.fields_by_name['qint'].message_type = _QINT
_QDTYPE.fields_by_name['q_ones_comp'].message_type = _QONESCOMP
_QDTYPE.fields_by_name['quint'].message_type = _QUINT
_QDTYPE.fields_by_name['bounded_q_int'].message_type = _BOUNDEDQUINT
_QDTYPE.fields_by_name['q_fxp'].message_type = _QFIXEDPOINT
_QDTYPE.oneofs_by_name['bitsize'].fields.append(
  _QDTYPE.fields_by_name['bitsize_int'])
_QDTYPE.fields_by_name['bitsize_int'].containing_oneof = _QDTYPE.oneofs_by_name['bitsize']
_QDTYPE.oneofs_by_name['bitsize'].fields.append(
  _QDTYPE.fields_by_name['bitsize_expr'])
_QDTYPE.fields_by_name['bitsize_expr'].containing_oneof = _QDTYPE.oneofs_by_name['bitsize']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['qbit'])
_QDTYPE.fields_by_name['qbit'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['qany'])
_QDTYPE.fields_by_name['qany'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['qint'])
_QDTYPE.fields_by_name['qint'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['q_ones_comp'])
_QDTYPE.fields_by_name['q_ones_comp'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['quint'])
_QDTYPE.fields_by_name['quint'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['bounded_q_int'])
_QDTYPE.fields_by_name['bounded_q_int'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
_QDTYPE.oneofs_by_name['data_type'].fields.append(
  _QDTYPE.fields_by_name['q_fxp'])
_QDTYPE.fields_by_name['q_fxp'].containing_oneof = _QDTYPE.oneofs_by_name['data_type']
DESCRIPTOR.message_types_by_name['QDType'] = _QDTYPE
DESCRIPTOR.message_types_by_name['QBit'] = _QBIT
DESCRIPTOR.message_types_by_name['QAny'] = _QANY
DESCRIPTOR.message_types_by_name['QInt'] = _QINT
DESCRIPTOR.message_types_by_name['QOnesComp'] = _QONESCOMP
DESCRIPTOR.message_types_by_name['QUInt'] = _QUINT
DESCRIPTOR.message_types_by_name['BoundedQUInt'] = _BOUNDEDQUINT
DESCRIPTOR.message_types_by_name['QFixedPoint'] = _QFIXEDPOINT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QDType = _reflection.GeneratedProtocolMessageType('QDType', (_message.Message,), {
  'DESCRIPTOR' : _QDTYPE,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QDType)
  })
_sym_db.RegisterMessage(QDType)

QBit = _reflection.GeneratedProtocolMessageType('QBit', (_message.Message,), {
  'DESCRIPTOR' : _QBIT,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QBit)
  })
_sym_db.RegisterMessage(QBit)

QAny = _reflection.GeneratedProtocolMessageType('QAny', (_message.Message,), {
  'DESCRIPTOR' : _QANY,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QAny)
  })
_sym_db.RegisterMessage(QAny)

QInt = _reflection.GeneratedProtocolMessageType('QInt', (_message.Message,), {
  'DESCRIPTOR' : _QINT,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QInt)
  })
_sym_db.RegisterMessage(QInt)

QOnesComp = _reflection.GeneratedProtocolMessageType('QOnesComp', (_message.Message,), {
  'DESCRIPTOR' : _QONESCOMP,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QOnesComp)
  })
_sym_db.RegisterMessage(QOnesComp)

QUInt = _reflection.GeneratedProtocolMessageType('QUInt', (_message.Message,), {
  'DESCRIPTOR' : _QUINT,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QUInt)
  })
_sym_db.RegisterMessage(QUInt)

BoundedQUInt = _reflection.GeneratedProtocolMessageType('BoundedQUInt', (_message.Message,), {
  'DESCRIPTOR' : _BOUNDEDQUINT,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.BoundedQUInt)
  })
_sym_db.RegisterMessage(BoundedQUInt)

QFixedPoint = _reflection.GeneratedProtocolMessageType('QFixedPoint', (_message.Message,), {
  'DESCRIPTOR' : _QFIXEDPOINT,
  '__module__' : 'data_types_pb2'
  # @@protoc_insertion_point(class_scope:qualtran.QFixedPoint)
  })
_sym_db.RegisterMessage(QFixedPoint)


# @@protoc_insertion_point(module_scope)
