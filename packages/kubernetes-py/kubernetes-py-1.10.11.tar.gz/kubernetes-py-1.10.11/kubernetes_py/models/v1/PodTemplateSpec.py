#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes_py.models.v1.ObjectMeta import ObjectMeta
from kubernetes_py.models.v1.PodSpec import PodSpec


class PodTemplateSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podtemplatespec
    """

    def __init__(self, model=None):
        super(PodTemplateSpec, self).__init__()

        self._metadata = ObjectMeta()
        self._spec = PodSpec()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if "metadata" in model:
            self.metadata = ObjectMeta(model["metadata"])
        if "spec" in model:
            self.spec = PodSpec(model["spec"])

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata=None):
        if not isinstance(metadata, ObjectMeta):
            raise SyntaxError("PodTemplateSpec: metadata: [ {0} ] is invalid".format(metadata))
        self._metadata = metadata

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PodSpec):
            raise SyntaxError("PodTemplateSpec: spec: [ {0} ] is invalid".format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.metadata is not None:
            data["metadata"] = self.metadata.serialize()
        if self.spec is not None:
            data["spec"] = self.spec.serialize()
        return data
