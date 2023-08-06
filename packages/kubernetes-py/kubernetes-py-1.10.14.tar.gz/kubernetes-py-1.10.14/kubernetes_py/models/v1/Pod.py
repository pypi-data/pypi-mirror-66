#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes_py.models.unversioned.BaseModel import BaseModel
from kubernetes_py.models.v1.ObjectMeta import ObjectMeta
from kubernetes_py.models.v1.PodSpec import PodSpec
from kubernetes_py.models.v1.PodStatus import PodStatus
from kubernetes_py.utils import filter_model


class Pod(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_pod
    """

    def __init__(self, model=None):
        super(Pod, self).__init__()

        self.kind = "Pod"
        self.api_version = "v1"

        self.spec = PodSpec()
        self.status = PodStatus()

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        super(Pod, self).build_with_model(model)

        if "spec" in model:
            self.spec = PodSpec(model["spec"])
        if "status" in model:
            self.status = PodStatus(model["status"])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PodSpec):
            raise SyntaxError("Pod: spec: [ {0} ] is invalid.".format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, PodStatus):
            raise SyntaxError("Pod: status: [ {0} ] is invalid.".format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Pod, self).serialize()
        if self.spec is not None:
            data["spec"] = self.spec.serialize()
        if self.status is not None:
            data["status"] = self.status.serialize()
        return data
