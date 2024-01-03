# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: log_labels.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10log_labels.proto\"R\n\x0e\x44ribblingLabel\x12\x14\n\x0cis_dribbling\x18\x01 \x01(\x08\x12\x10\n\x08robot_id\x18\x02 \x01(\r\x12\x18\n\x04team\x18\x03 \x01(\x0e\x32\n.TeamColor\"\x89\x01\n\x13\x42\x61llPossessionLabel\x12)\n\x05state\x18\x01 \x01(\x0e\x32\x1a.BallPossessionLabel.State\x12\x10\n\x08robot_id\x18\x02 \x01(\r\"5\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x11\n\rYELLOW_POSSES\x10\x01\x12\x0f\n\x0b\x42LUE_POSSES\x10\x02\"\x93\x01\n\x0cPassingLabel\x12\x13\n\x0bstart_frame\x18\x01 \x01(\x04\x12\x11\n\tend_frame\x18\x02 \x01(\x04\x12\x12\n\nsuccessful\x18\x03 \x01(\x08\x12\x11\n\tpasser_id\x18\x04 \x01(\r\x12\x1f\n\x0bpasser_team\x18\x05 \x01(\x0e\x32\n.TeamColor\x12\x13\n\x0breceiver_id\x18\x06 \x01(\r\"\x81\x01\n\rGoalShotLabel\x12\x13\n\x0bstart_frame\x18\x01 \x01(\x04\x12\x11\n\tend_frame\x18\x02 \x01(\x04\x12\x12\n\nsuccessful\x18\x03 \x01(\x08\x12\x12\n\nshooter_id\x18\x04 \x01(\r\x12 \n\x0cshooter_team\x18\x05 \x01(\x0e\x32\n.TeamColor\"\xba\x01\n\x06Labels\x12)\n\x10\x64ribbling_labels\x18\x01 \x03(\x0b\x32\x0f.DribblingLabel\x12\x34\n\x16\x62\x61ll_possession_labels\x18\x02 \x03(\x0b\x32\x14.BallPossessionLabel\x12%\n\x0epassing_labels\x18\x03 \x03(\x0b\x32\r.PassingLabel\x12(\n\x10goal_shot_labels\x18\x04 \x03(\x0b\x32\x0e.GoalShotLabel*)\n\tTeamColor\x12\x0e\n\nTeamYELLOW\x10\x00\x12\x0c\n\x08TeamBLUE\x10\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'log_labels_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TEAMCOLOR._serialized_start=715
  _TEAMCOLOR._serialized_end=756
  _DRIBBLINGLABEL._serialized_start=20
  _DRIBBLINGLABEL._serialized_end=102
  _BALLPOSSESSIONLABEL._serialized_start=105
  _BALLPOSSESSIONLABEL._serialized_end=242
  _BALLPOSSESSIONLABEL_STATE._serialized_start=189
  _BALLPOSSESSIONLABEL_STATE._serialized_end=242
  _PASSINGLABEL._serialized_start=245
  _PASSINGLABEL._serialized_end=392
  _GOALSHOTLABEL._serialized_start=395
  _GOALSHOTLABEL._serialized_end=524
  _LABELS._serialized_start=527
  _LABELS._serialized_end=713
# @@protoc_insertion_point(module_scope)
