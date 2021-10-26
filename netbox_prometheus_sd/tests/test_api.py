from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from users.models import ObjectPermission

import json

from . import utils


class ApiEndpointTests(TestCase):
    """Test cases for ensuring API endpoint is working properly."""

    def setUp(self):

        self.client = APIClient()

        # Create test user and view permissions
        user = User.objects.create_user("username", "Pas$w0rd")
        obj_perm = ObjectPermission(name="test", actions=["view"])
        obj_perm.save()
        obj_perm.users.add(user)
        obj_perm.object_types.add(
            ContentType.objects.get(app_label="dcim", model="device")
        )
        obj_perm.object_types.add(
            ContentType.objects.get(app_label="ipam", model="ipaddress")
        )
        obj_perm.object_types.add(
            ContentType.objects.get(app_label="virtualization", model="virtualmachine")
        )
        self.client.force_authenticate(user)

    def test_device_endpoint(self):
        """Ensure device endpoint returns a valid response"""

        utils.build_device_full()

        resp = self.client.get("/api/plugins/prometheus-sd/devices/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.content)

        self.assertIsNotNone(data[0]["targets"])
        self.assertIsNotNone(data[0]["labels"])

    def test_virtual_machine_endpoint(self):
        """Ensure virtual machine endpoint returns a valid response"""

        utils.build_vm_full()

        resp = self.client.get("/api/plugins/prometheus-sd/virtual-machines/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.content)

        self.assertIsNotNone(data[0]["targets"])
        self.assertIsNotNone(data[0]["labels"])

    def test_ip_address_endpoint(self):
        """Ensure ip address endpoint returns a valid response"""

        utils.build_full_ip()

        resp = self.client.get("/api/plugins/prometheus-sd/ip-addresses/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.content)

        self.assertIsNotNone(data[0]["targets"])
        self.assertIsNotNone(data[0]["labels"])
