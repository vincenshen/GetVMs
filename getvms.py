# -*- coding:utf-8 -*-

"""
Python program for listing the vms on an ESX / vCenter host
"""

import atexit
import base64

from pyVim import connect
from pyVmomi import vim
import ssl


ssl._create_default_https_context = ssl._create_unverified_context


def get_vm_name(vm_container):
    """
    produce vm name
    """
    for child in vm_container:
        if child.summary.runtime.powerState == "poweredOn":
            yield child.summary.config.name


def write_vm_tofile(vm_container, vc_server):
    """
    write vm name and vc ip to txt file
    """
    vm_yield = get_vm_name(vm_container)
    f1 = open("vm_sched_1.list", "a")
    f2 = open("vm_sched_2.list", "a")

    try:
        while True:
            f1.write("%s,%s\n" % (vm_yield.__next__(), vc_server))
            f2.write("%s,%s\n" % (vm_yield.__next__(), vc_server))
    except StopIteration:
        print("%s vm get complete!" % vc_server)
    f1.close()
    f2.close()


def main(vc):
    """
    Simple command-line program for listing the virtual machines on a system.
    """
    service_instance = connect.SmartConnect(host=vc,
                                            user="administrator@vsphere.local",
                                            pwd=base64.decodebytes(b'VkdDbG9jYWxhZG1pbkAyMDEy\n').decode(),
                                            port=443)

    atexit.register(connect.Disconnect, service_instance)

    content = service_instance.RetrieveContent()

    container = content.rootFolder  # starting point to look into
    view_type = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    container_view = content.viewManager.CreateContainerView(
        container, view_type, recursive)

    children = container_view.view

    write_vm_tofile(children, vc_server)


if __name__ == "__main__":

    vc_server_list = ["10.120.137.37"]
    for vc_server in vc_server_list:
        main(vc_server)
