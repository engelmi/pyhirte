from datetime import datetime
from collections import namedtuple

from dasbus.typing import Variant
import dasbus.connection as dbus
from dasbus.loop import EventLoop

from .const import HIRTE_DBUS_INTERFACE, HIRTE_OBJECT_PATH


class Hirte:

    def __init__(
        self
    ) -> None:
        super().__init__()
        self.bus = dbus.SystemMessageBus()
        self.manager = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            HIRTE_OBJECT_PATH
        )

    def Stop(
        self,
        nodeName,
        unitName
    ):
        self.action(
            "stop",
            nodeName,
            unitName
        )

    def Enable(
        self,
        nodeName,
        unitName
    ):
        self.action(
            "enable",
            nodeName,
            unitName
        )

    def Disable(
        self,
        nodeName,
        unitName
    ):
        self.action(
            "disable",
            nodeName,
            unitName
        )

    def Start(
        self,
        nodeName,
        unitName
    ):
        self.action(
            "start",
            nodeName,
            unitName
        )

    def action(
        self,
        operation,
        nodeName,
        unitName,
    ):
        manager = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            HIRTE_OBJECT_PATH
        )

        node_path = manager.GetNode(nodeName)
        node = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            node_path
        )

        loop = EventLoop()

        def job_removed(
            id,
            job_path,
            node_name,
            unit,
            result
        ):
            if job_path == my_job_path:
                run_time = (datetime.utcnow() - operation_time).total_seconds()
                run_time = "{:.1f}".format(run_time * 1000)
                print(f"{operation}ed {unit} on node {node_name}"
                      f" with result {result} in {run_time} msec")
                loop.quit()

        operation_time = datetime.utcnow()

        # Emitted each time a new job is dequeued or the underlying
        # systemd job finished.
        self.manager.JobRemoved.connect(job_removed)
        if operation == "start":
            my_job_path = node.StartUnit(unitName, "replace")
        elif operation == "stop":
            my_job_path = node.StopUnit(unitName, "replace")
        elif operation == "enable":
            my_job_path = node.EnableUnitFiles(unitName, False, False)
        elif operation == "disable":
            my_job_path = node.DisableUnitFiles(unitName, False, False)

        loop.run()

    def ListAllNodes(
        self,
    ):
        NodeInfo = namedtuple(
            "NodeInfo", [
                "name",
                "object_path",
                "status"]
        )

        nodes = self.manager.ListNodes()
        for node in nodes:
            info = NodeInfo(*node)
            print(f"Node: {info.name}, State: {info.status}")

    def SetCPUWeight(
        self,
        nodeName,
        unitName,
        value,
        persist=False
    ):
        # Don't persist change = True
        runtime = persist

        manager = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            HIRTE_OBJECT_PATH
        )

        node_path = manager.GetNode(nodeName)
        node = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            node_path
        )

        node.SetUnitProperties(
            unitName,
            runtime,
            [("CPUWeight", Variant("t", value))]
        )

    def CPUWeight(
        self,
        nodeName,
        unitName
    ):
        manager = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            HIRTE_OBJECT_PATH
        )

        node_path = manager.GetNode(nodeName)
        node = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            node_path
        )

        print(
            node.GetUnitProperty(
                unitName,
                "org.freedesktop.systemd1.Service",
                "CPUWeight"
            )
        )

    def ListActiveServices(
        self,
    ):
        NodeUnitInfo = namedtuple(
            "NodeUnitInfo", [
                "node",
                "name",
                "description",
                "load_state",
                "active_state",
                "sub_state",
                "follower",
                "object_path",
                "job_id",
                "job_type",
                "job_object_path"
            ]
        )

        units = self.manager.ListUnits()
        for u in units:
            info = NodeUnitInfo(*u)
            if info.active_state == "active" and \
                    info.name.endswith(".service"):
                print(f"Node: {info.node}, Unit: {info.name}")

    def ListNodeUnits(
        self,
        nodeName=None
    ):

        if nodeName is None:
            return namedtuple("UnitInfo", [])

        UnitInfo = namedtuple(
            "UnitInfo", [
                "name",
                "description",
                "load_state",
                "active_state",
                "sub_state",
                "follower",
                "object_path",
                "job_id",
                "job_type",
                "job_object_path"
            ]
        )

        node_path = self.manager.GetNode(nodeName)
        node = self.bus.get_proxy(
            HIRTE_DBUS_INTERFACE,
            node_path
        )

        units = node.ListUnits()
        for u in units:
            info = UnitInfo(*u)
            print(f"{info.name} - {info.description}")
