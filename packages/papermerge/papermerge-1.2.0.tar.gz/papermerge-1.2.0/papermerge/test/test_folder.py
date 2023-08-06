from pathlib import Path

from django.test import TestCase
from papermerge.core.models import (
    Folder,
)

from papermerge.test.utils import create_root_user

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestFolder(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_delete_parent_deletes_nested_folder_as_well(self):
        """
        If folder C is child of folder P, then when
        deleting P - C will be deleted as well
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )

        Folder.objects.create(
            title="C",
            user=self.user,
            parent=p
        )

        p = Folder.objects.get(title="P")
        self.assertEqual(p.get_children().count(), 1)

        Folder.objects.get(title="P").delete()

        with self.assertRaises(Folder.DoesNotExist):
            Folder.objects.get(title="C")

    def test_delete_nested_folder_does_not_delete_parent(self):
        """
        If folder C is child of folder P, then when
        deleting C - P should not be deleted
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )

        Folder.objects.create(
            title="C",
            user=self.user,
            parent=p
        )

        p = Folder.objects.get(title="P")
        self.assertEqual(p.get_children().count(), 1)

        Folder.objects.get(title="C").delete()

        try:
            Folder.objects.get(title="P")
        except Folder.DoesNotExist:
            self.fail(
                "Parent folder was deleted when child"
                " deletion only was intended"
            )
