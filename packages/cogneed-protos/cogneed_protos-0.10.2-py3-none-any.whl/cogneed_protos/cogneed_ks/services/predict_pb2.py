# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cogneed-protos/cogneed-ks/services/predict.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cogneed_protos.cogneed_ks.models import mfcc_audio_pb2 as cogneed__protos_dot_cogneed__ks_dot_models_dot_mfcc__audio__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cogneed-protos/cogneed-ks/services/predict.proto',
  package='ai.cogneed.cloud.speech.v1',
  syntax='proto3',
  serialized_options=_b('\n\032ai.cogneed.cloud.speech.v1P\001'),
  serialized_pb=_b('\n0cogneed-protos/cogneed-ks/services/predict.proto\x12\x1a\x61i.cogneed.cloud.speech.v1\x1a\x31\x63ogneed-protos/cogneed-ks/models/mfcc_audio.proto\"8\n\x12PredictionResponse\x12\x13\n\x0bprobability\x18\x01 \x01(\x01\x12\r\n\x05label\x18\x02 \x01(\t\"_\n\x11PredictionRequest\x12\x39\n\nmfcc_audio\x18\x01 \x01(\x0b\x32%.ai.cogneed.cloud.speech.v1.MfccAudio\x12\x0f\n\x07version\x18\x02 \x01(\x03\x32z\n\x0ePredictService\x12h\n\x07predict\x12-.ai.cogneed.cloud.speech.v1.PredictionRequest\x1a..ai.cogneed.cloud.speech.v1.PredictionResponseB\x1e\n\x1a\x61i.cogneed.cloud.speech.v1P\x01\x62\x06proto3')
  ,
  dependencies=[cogneed__protos_dot_cogneed__ks_dot_models_dot_mfcc__audio__pb2.DESCRIPTOR,])




_PREDICTIONRESPONSE = _descriptor.Descriptor(
  name='PredictionResponse',
  full_name='ai.cogneed.cloud.speech.v1.PredictionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='probability', full_name='ai.cogneed.cloud.speech.v1.PredictionResponse.probability', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='ai.cogneed.cloud.speech.v1.PredictionResponse.label', index=1,
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
  serialized_start=131,
  serialized_end=187,
)


_PREDICTIONREQUEST = _descriptor.Descriptor(
  name='PredictionRequest',
  full_name='ai.cogneed.cloud.speech.v1.PredictionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mfcc_audio', full_name='ai.cogneed.cloud.speech.v1.PredictionRequest.mfcc_audio', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='ai.cogneed.cloud.speech.v1.PredictionRequest.version', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=189,
  serialized_end=284,
)

_PREDICTIONREQUEST.fields_by_name['mfcc_audio'].message_type = cogneed__protos_dot_cogneed__ks_dot_models_dot_mfcc__audio__pb2._MFCCAUDIO
DESCRIPTOR.message_types_by_name['PredictionResponse'] = _PREDICTIONRESPONSE
DESCRIPTOR.message_types_by_name['PredictionRequest'] = _PREDICTIONREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PredictionResponse = _reflection.GeneratedProtocolMessageType('PredictionResponse', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTIONRESPONSE,
  __module__ = 'cogneed_protos.cogneed_ks.services.predict_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.cloud.speech.v1.PredictionResponse)
  ))
_sym_db.RegisterMessage(PredictionResponse)

PredictionRequest = _reflection.GeneratedProtocolMessageType('PredictionRequest', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTIONREQUEST,
  __module__ = 'cogneed_protos.cogneed_ks.services.predict_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.cloud.speech.v1.PredictionRequest)
  ))
_sym_db.RegisterMessage(PredictionRequest)


DESCRIPTOR._options = None

_PREDICTSERVICE = _descriptor.ServiceDescriptor(
  name='PredictService',
  full_name='ai.cogneed.cloud.speech.v1.PredictService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=286,
  serialized_end=408,
  methods=[
  _descriptor.MethodDescriptor(
    name='predict',
    full_name='ai.cogneed.cloud.speech.v1.PredictService.predict',
    index=0,
    containing_service=None,
    input_type=_PREDICTIONREQUEST,
    output_type=_PREDICTIONRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PREDICTSERVICE)

DESCRIPTOR.services_by_name['PredictService'] = _PREDICTSERVICE

# @@protoc_insertion_point(module_scope)
