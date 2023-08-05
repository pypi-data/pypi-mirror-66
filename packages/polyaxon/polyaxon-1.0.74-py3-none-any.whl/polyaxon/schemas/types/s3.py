#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import polyaxon_sdk

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class S3TypeSchema(BaseCamelSchema):
    bucket = RefOrObject(fields.Str(allow_none=True))
    key = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1S3Type


class V1S3Type(BaseConfig, polyaxon_sdk.V1S3Type):
    IDENTIFIER = "s3"
    SCHEMA = S3TypeSchema
    REDUCED_ATTRIBUTES = ["bucket", "key"]
