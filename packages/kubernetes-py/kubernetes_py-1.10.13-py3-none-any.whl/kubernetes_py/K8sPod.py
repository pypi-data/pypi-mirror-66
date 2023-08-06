#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

from kubernetes_py import K8sConfig
from kubernetes_py.K8sContainer import K8sContainer
from kubernetes_py.K8sExceptions import NotFoundException, TimedOutException
from kubernetes_py.K8sObject import K8sObject
from kubernetes_py.models.v1.Pod import Pod
from kubernetes_py.models.v1.PodStatus import PodStatus
from kubernetes_py.models.v1.Probe import Probe
from kubernetes_py.utils import is_valid_dict, is_valid_string, is_valid_list
from kubernetes_py.models.v1.Toleration import Toleration
from kubernetes_py.models.unversioned.BaseUrls import BaseUrls


class K8sPod(K8sObject):

    POD_READY_TIMEOUT_SECONDS = 120

    def __init__(self, config=None, name=None):
        super(K8sPod, self).__init__(config=config, obj_type="Pod", name=name)
        if self.config.pull_secret is not None:
            self.add_image_pull_secrets(self.config.pull_secret)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sPod, self).create()
        self.get()
        self._wait_for_readiness()
        return self

    def update(self):
        super(K8sPod, self).update()
        self.get()
        self._wait_for_readiness()
        return self

    def list(self, pattern=None, labels=None):
        ls = super(K8sPod, self).list(labels=labels)
        pods = list(map(lambda pod: Pod(pod), ls))
        if pattern is not None:
            pods = list(filter(lambda pod: pattern in pod.name, pods))
        k8s = list()
        for x in pods:
            p = K8sPod(config=self.config, name=x.name).from_model(m=x)
            k8s.append(p)
        return k8s

    # -------------------------------------------------------------------------------------  wait

    def _wait_for_readiness(self):
        start_time = time.time()
        while not self.is_ready():
            time.sleep(0.2)
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.POD_READY_TIMEOUT_SECONDS:
                raise TimedOutException("Timed out on Pod readiness: [ {0} ]".format(self.name))

    # -------------------------------------------------------------------------------------  add

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError("K8sPod.add_container() container: [ {0} ] is invalid.".format(container))

        containers = self.model.spec.containers
        if container not in containers:
            containers.append(container.model)
            self.model.spec.containers = containers
        return self

    def add_image_pull_secrets(self, secrets=None):
        self.model.spec.add_image_pull_secrets(secrets)
        return self

    def add_volume(self, volume=None):
        volumes = self.model.spec.volumes
        if volume not in volumes:
            volumes.append(volume.model)
        self.model.spec.volumes = volumes
        return self

    def add_toleration(self, key=None, value=None, effect=None):
        exists = False
        for tol in self.tolerations:
            if tol.key == key and tol.value == value and tol.effect == effect:
                exists = True
        if not exists:
            tol = Toleration()
            tol.key = key
            tol.value = value
            tol.effect = effect
            self.tolerations.append(tol)
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_node_name(self):
        self.model.spec.node_name = None
        return self

    def del_toleration(self, key=None, value=None, effect=None):
        remaining_tolerations = []
        for tol in self.tolerations:
            if tol.key != key and tol.value != value and tol.effect != effect:
                remaining_tolerations.append(tol)
        if self.tolerations != remaining_tolerations:
            self.tolerations = remaining_tolerations
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Pod(self.get_model())
        return self

    # ------------------------------------------------------------------------------------- polling readiness

    def is_ready(self):
        self.get()
        if self.status is not None and isinstance(self.status, PodStatus):
            pod_phase = self.status.phase
            conditions = self.status.conditions
            conditions_ok = 0
            for cond in conditions:
                if cond.status == "True":
                    conditions_ok += 1
            if pod_phase == "Running" and len(conditions) == conditions_ok:
                return True
        return False

    # ------------------------------------------------------------------------------------- logs

    def get_log(self, container=None):
        url = "{base}/{name}/log".format(base=self.base_url, name=self.name)
        if container:
            url = "{url}?container={container}".format(url=url, container=container)

        state = self.request(method="GET", url=url)
        if not state.get("success"):
            status = state.get("status", "")
            reason = state.get("data", dict()).get("message", None)
            message = "K8sPod: GET [ {0}:{1} ] failed: HTTP {2} : {3} ".format(self.obj_type, self.name, status, reason)
            raise NotFoundException(message)

        if "data" in state and state.get("data") is not None:
            logs = state.get("data").splitlines()
            return logs
        return ""

    # ------------------------------------------------------------------------------------- metrics

    def get_metrics(self):
        bu = BaseUrls(api=self.config.version, namespace=self.config.namespace)
        base_url = bu.get_base_url(object_type="PodMetrics")
        url = "{base}/{name}".format(base=base_url, name=self.name)

        state = self.request(method="GET", url=url)
        if not state.get("success"):
            status = state.get("status", "")
            reason = state.get("data", dict()).get("message", None)
            message = "K8sPod: GET [ {0}:{1} ] failed: HTTP {2} : {3} ".format(self.obj_type, self.name, status, reason)
            raise NotFoundException(message)

        if "data" in state and state.get("data") is not None:
            return state.get("data")
        return ""

    # ------------------------------------------------------------------------------------- set

    def set_container_image(self, name=None, image=None):
        containers = []
        for c in self.model.spec.containers:
            if c.name == name:
                c.image = image
            containers.append(c)
        self.model.spec.containers = containers
        return self

    # ------------------------------------------------------------------------------------- activeDeadline

    @property
    def active_deadline(self):
        return self.model.spec.active_deadline_seconds

    @active_deadline.setter
    def active_deadline(self, secs=None):
        self.model.spec.active_deadline_seconds = secs

    # ------------------------------------------------------------------------------------- automountServiceAccountToken

    @property
    def automount_service_account_token(self):
        return self.model.spec.automount_service_account_token

    @automount_service_account_token.setter
    def automount_service_account_token(self, automount=None):
        self.model.spec.automount_service_account_token = automount

    # ------------------------------------------------------------------------------------- containers

    @property
    def containers(self):
        _list = []
        for c in self.model.spec.containers:
            k8scontainer = K8sContainer(name=c.name, image=c.image)
            k8scontainer.model = c
            _list.append(k8scontainer)
        return _list

    @containers.setter
    def containers(self, containers=None):
        if not is_valid_list(containers, K8sContainer):
            self.model.spec.containers = [x.model for x in containers]

    # ------------------------------------------------------------------------------------- dnsPolicy

    @property
    def dns_policy(self):
        return self.model.spec.dns_policy

    @dns_policy.setter
    def dns_policy(self, policy=None):
        self.model.spec.dns_policy = policy

    # ------------------------------------------------------------------------------------- generateName

    @property
    def generate_name(self):
        return self.model.metadata.generate_name

    @generate_name.setter
    def generate_name(self, name=None):
        self.model.metadata.generate_name = name

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self.model.metadata.namespace

    @namespace.setter
    def namespace(self, nspace=None):
        self.model.metadata.namespace = nspace

    # ------------------------------------------------------------------------------------- nodeName

    @property
    def node_name(self):
        return self.model.spec.node_name

    @node_name.setter
    def node_name(self, name=None):
        self.model.spec.node_name = name

    # ------------------------------------------------------------------------------------- nodeSelector

    @property
    def node_selector(self):
        return self.model.spec.node_selector

    @node_selector.setter
    def node_selector(self, selector=None):
        self.model.spec.node_selector = selector

    # -------------------------------------------------------------------------------------  livenessProbes

    @property
    def liveness_probes(self):
        data = {}
        containers = self.model.spec.containers
        for c in containers:
            if c.liveness_probe is not None:
                data[c.name] = c.liveness_probe
        return data

    @liveness_probes.setter
    def liveness_probes(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError("K8sPod: liveness_probes: [ {} ] is invalid.".format(tup))

        c_name, probe = tup
        container_names = [c.name for c in self.model.spec.containers]
        if c_name not in container_names:
            raise SyntaxError("K8sPod: liveness_probes: container [ {} ] not found.".format(c_name))
        if not isinstance(probe, Probe):
            raise SyntaxError("K8sPod: liveness_probe: probe: [ {} ] is invalid.".format(probe))

        containers = []
        for c in self.model.spec.containers:
            if c.name == c_name:
                c.liveness_probe = probe
            containers.append(c)
        self.model.spec.template.spec.containers = containers

    # -------------------------------------------------------------------------------------  readinessProbes

    @property
    def readiness_probes(self):
        data = {}
        containers = self.model.spec.containers
        for c in containers:
            if c.readiness_probe is not None:
                data[c.name] = c.readiness_probe
        return data

    @readiness_probes.setter
    def readiness_probes(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError("K8sPod: readiness_probes: [ {} ] is invalid.".format(tup))

        c_name, probe = tup
        container_names = [c.name for c in self.model.spec.template.spec.containers]
        if c_name not in container_names:
            raise SyntaxError("K8sPod: readiness_probes: container [ {} ] not found.".format(c_name))
        if not isinstance(probe, Probe):
            raise SyntaxError("K8sPod: readiness_probes: probe: [ {} ] is invalid.".format(probe))

        containers = []
        for c in self.model.spec.template.spec.containers:
            if c.name == c_name:
                c.readiness_probe = probe
            containers.append(c)
        self.model.spec.template.spec.containers = containers

    # ------------------------------------------------------------------------------------- restartPolicy

    @property
    def restart_policy(self):
        return self.model.spec.restart_policy

    @restart_policy.setter
    def restart_policy(self, policy=None):
        self.model.spec.restart_policy = policy

    # ------------------------------------------------------------------------------------- serviceAccountName

    @property
    def service_account_name(self):
        return self.model.spec.service_account_name

    @service_account_name.setter
    def service_account_name(self, name=None):
        self.model.spec.service_account_name = name

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        self.get()
        return self.model.status

    @status.setter
    def status(self, status=None):
        self.model.status = status

    # ------------------------------------------------------------------------------------- terminationGracePeriod

    @property
    def termination_grace_period(self):
        return self.model.spec.termination_grace_period_seconds

    @termination_grace_period.setter
    def termination_grace_period(self, secs=None):
        self.model.spec.termination_grace_period_seconds = secs

    # ------------------------------------------------------------------------------------- volumes

    @property
    def volumes(self):
        return self.model.spec.volumes

    @volumes.setter
    def volumes(self, v=None):
        self.model.spec.volumes = v

    # -------------------------------------------------------------------------------------  start time

    @property
    def start_time(self):
        return self.model.status.start_time

    @start_time.setter
    def start_time(self, t=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  phase

    @property
    def phase(self):
        return self.model.status.phase

    @phase.setter
    def phase(self, p=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  affinity

    @property
    def affinity(self):
        return self.model.spec.affinity

    @affinity.setter
    def affinity(self, a):
        self.model.spec.affinity = a

    # -------------------------------------------------------------------------------------  tolerations

    @property
    def tolerations(self):
        return self.model.spec.tolerations

    @tolerations.setter
    def tolerations(self, t=None):
        self.model.spec.tolerations = t

    # -------------------------------------------------------------------------------------  host_ip

    @property
    def host_ip(self):
        return self.model.status.host_ip

    @host_ip.setter
    def host_ip(self, ip=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  pod_ip

    @property
    def pod_ip(self):
        return self.model.status.pod_ip

    @pod_ip.setter
    def pod_ip(self, ip=None):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------- filtering

    @classmethod
    def get_by_name(cls, config=None, name=None, name_label="name"):
        if not is_valid_string(name):
            raise SyntaxError("K8sPod.get_by_name(): name: [ {0} ] is invalid.".format(name))
        return cls.get_by_labels(config=config, labels={name_label: name,})

    @staticmethod
    def get_by_labels(config=None, labels=None):
        if config is None:
            config = K8sConfig()
        if not is_valid_dict(labels):
            raise SyntaxError("K8sPod.get_by_labels(): labels: [ {} ] is invalid.".format(labels))

        pods = K8sPod(config=config, name="whatever").list(labels=labels)

        return pods

    @staticmethod
    def get_by_pod_ip(config=None, ip=None, labels=None):
        if config is None:
            config = K8sConfig()
        if not is_valid_string(ip):
            raise SyntaxError("K8sPod.get_by_pod_ip(): ip: [ {0} ] is invalid.".format(ip))

        found = None
        pods = K8sPod(config=config, name="throwaway").list(labels=labels)

        for pod in pods:
            try:
                assert isinstance(pod, K8sPod)
                if pod.pod_ip == ip:
                    found = pod
                    break
            except NotFoundException:
                pass
        return found
