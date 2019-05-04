import unittest
import os
from Model.tasklistmodel import TaskListModel, DBConnectionShelve


class ModelTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tearDown()     # Make sure files are deleted
        self.model = TaskListModel(DBConnectionShelve(), './testdata/test')
        self.model.add_task_to_db('task 1')
        self.model.add_subtask_to_db(self.model.tasks["task 1"], "subtask 1 1")
        self.model.add_subtask_to_db(self.model.tasks["task 1"], "subtask 1 2")
        self.model.add_subtask_to_db(self.model.tasks["task 1"], "subtask 1 3")
        self.model.add_task_to_db('task 2')
        self.model.add_subtask_to_db(self.model.tasks["task 2"], "subtask 2 1")
        self.model.add_subtask_to_db(self.model.tasks["task 2"], "subtask 2 2")
        self.model.add_subtask_to_db(self.model.tasks["task 2"], "subtask 2 3")
        self.model.add_task_to_db('task 3')
        self.model.add_subtask_to_db(self.model.tasks["task 3"], "subtask 3 1")
        self.model.add_task_to_db('task 4')
        self.model.add_subtask_to_db(self.model.tasks["task 3"], "subtask 3 2")
        self.model.add_subtask_to_db(self.model.tasks["task 4"], "subtask 4 1")
        self.model.add_subtask_to_db(self.model.tasks["task 4"], "subtask 4 2")
        self.model.add_subtask_to_db(self.model.tasks["task 4"], "subtask 4 3")


    def test_db_extsis(self):
        self.assertIsNotNone(self.model.db, "Database not initilized")
        self.assertIsInstance(self.model.dbconnectiontype, DBConnectionShelve)

    def test_sequences(self):
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1"].sequence, 1)
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 2"].sequence, 2)
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 3"].sequence, 3)
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 1"].sequence, 1)
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 2"].sequence, 2)
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 3"].sequence, 3)
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 1"].sequence, 1)
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 2"].sequence, 2)
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 1"].sequence, 1)
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 2"].sequence, 2)
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 3"].sequence, 3)

    def test_sorted_list(self):
        self.assertEqual(self.model.tasks.items_sorted[0].description, "task 1")
        self.assertEqual(self.model.tasks["task 1"].subtasks.items_sorted[0].description, "subtask 1 1")
        self.assertEqual(self.model.tasks["task 1"].subtasks.items_sorted[1].description, "subtask 1 2")
        self.assertEqual(self.model.tasks["task 1"].subtasks.items_sorted[2].description, "subtask 1 3")

        self.assertEqual(self.model.tasks.items_sorted[1].description, "task 2")
        self.assertEqual(self.model.tasks["task 2"].subtasks.items_sorted[0].description, "subtask 2 1")
        self.assertEqual(self.model.tasks["task 2"].subtasks.items_sorted[1].description, "subtask 2 2")
        self.assertEqual(self.model.tasks["task 2"].subtasks.items_sorted[2].description, "subtask 2 3")

        self.assertEqual(self.model.tasks.items_sorted[2].description, "task 3")
        self.assertEqual(self.model.tasks["task 3"].subtasks.items_sorted[0].description, "subtask 3 1")
        self.assertEqual(self.model.tasks["task 3"].subtasks.items_sorted[1].description, "subtask 3 2")

        self.assertEqual(self.model.tasks.items_sorted[3].description, "task 4")
        self.assertEqual(self.model.tasks["task 4"].subtasks.items_sorted[0].description, "subtask 4 1")
        self.assertEqual(self.model.tasks["task 4"].subtasks.items_sorted[1].description, "subtask 4 2")
        self.assertEqual(self.model.tasks["task 4"].subtasks.items_sorted[2].description, "subtask 4 3")

    def test_content(self):
        # testing tasks
        self.assertEqual(self.model.tasks["task 1"].description, "task 1")
        self.assertEqual(self.model.tasks["task 2"].description, "task 2")
        self.assertEqual(self.model.tasks["task 3"].description, "task 3")
        self.assertEqual(self.model.tasks["task 4"].description, "task 4")
        # testing subtasks
        # 1
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1"].description, "subtask 1 1")
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 2"].description, "subtask 1 2")
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 3"].description, "subtask 1 3")
        # 2
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 1"].description, "subtask 2 1")
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 2"].description, "subtask 2 2")
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 3"].description, "subtask 2 3")
        # 3
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 1"].description, "subtask 3 1")
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 2"].description, "subtask 3 2")
        # 4
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 1"].description, "subtask 4 1")
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 2"].description, "subtask 4 2")
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 3"].description, "subtask 4 3")

    def test_length(self):
        self.assertEqual(len(self.model.tasks), 4)

        self.assertEqual(len(self.model.tasks["task 1"].subtasks), 3)
        # add an item to the subtask
        self.model.add_subtask_to_db(self.model.tasks["task 1"], "subtask 1 4")
        self.assertEqual(len(self.model.tasks["task 1"].subtasks), 4)
        self.assertEqual(len(self.model.tasks.items_sorted[0].subtasks), 4)
        self.assertEqual(len(self.model.tasks["task 2"].subtasks), 3)
        self.assertEqual(len(self.model.tasks.items_sorted[1].subtasks), 3)
        self.assertEqual(len(self.model.tasks["task 3"].subtasks), 2)
        self.assertEqual(len(self.model.tasks.items_sorted[2].subtasks), 2)
        self.assertEqual(len(self.model.tasks["task 4"].subtasks), 3)
        self.assertEqual(len(self.model.tasks.items_sorted[3].subtasks), 3)

    def test_task_deletion(self):
        self.model.remove_task_from_db("task 1")
        self.assertEqual(len(self.model.tasks), 3)
        with self.assertRaises(KeyError):
            self.model.db["task 1"]
            self.model.tasks["task 1"]
        self.assertEqual(self.model.tasks["task 2"].sequence, 1)
        self.assertEqual(self.model.tasks["task 3"].sequence, 2)
        self.assertEqual(self.model.tasks["task 4"].sequence, 3)
        self.assertEqual(self.model.tasks.items_sorted[0].description, "task 2")
        self.assertEqual(self.model.tasks.items_sorted[1].description, "task 3")
        self.assertEqual(self.model.tasks.items_sorted[2].description, "task 4")
        # last task removal
        self.model.remove_task_from_db("task 4")
        self.assertEqual(len(self.model.tasks), 2)
        with self.assertRaises(KeyError):
            self.model.db["task 4"]
            self.model.tasks["task 4"]
        self.assertEqual(self.model.tasks["task 2"].sequence, 1)
        self.assertEqual(self.model.tasks["task 3"].sequence, 2)
        self.assertEqual(self.model.tasks.items_sorted[0].description, "task 2")
        self.assertEqual(self.model.tasks.items_sorted[1].description, "task 3")
        with self.assertRaises(IndexError):
            self.model.tasks.items_sorted[2]
        # middle task removal
        self.model.add_task_to_db('task 4')
        self.model.add_task_to_db('task 5')
        self.assertEqual(len(self.model.tasks), 4)
        self.model.remove_task_from_db("task 3")
        self.assertEqual(len(self.model.tasks), 3)
        with self.assertRaises(KeyError):
            self.model.db["task 3"]
            self.model.tasks["task 3"]
        self.assertEqual(self.model.tasks["task 2"].sequence, 1)
        self.assertEqual(self.model.tasks["task 4"].sequence, 2)
        self.assertEqual(self.model.tasks["task 5"].sequence, 3)
        self.assertEqual(self.model.tasks.items_sorted[0].description, "task 2")
        self.assertEqual(self.model.tasks.items_sorted[1].description, "task 4")
        self.assertEqual(self.model.tasks.items_sorted[2].description, "task 5")

    # TODO add tests for soted_items
    def test_subtask_deletion(self):
        self.model.remove_subtask_from_db("task 1", "subtask 1 2")
        # test length
        self.assertEqual(len(self.model.tasks["task 1"].subtasks), 2)
        # test presence
        with self.assertRaises(KeyError):
            self.model.tasks["task 1"].subtasks["subtask 1 2"]
            self.model.db["task 1"]["subtask 1 2"]
        # test sequence
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1"].sequence, 1)
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 3"].sequence, 2)
        # delete first item
        self.model.remove_subtask_from_db("task 2", "subtask 2 1")
        # test length
        self.assertEqual(len(self.model.tasks["task 2"].subtasks), 2)
        # test presence
        with self.assertRaises(KeyError):
            self.model.tasks["task 2"].subtasks["subtask 2 1"]
            self.model.db["task 2"]["subtask 2 1"]
        # test sequence
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 2"].sequence, 1)
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 3"].sequence, 2)

        # delete last item
        self.model.remove_subtask_from_db("task 4", "subtask 4 3")
        # test length
        self.assertEqual(len(self.model.tasks["task 4"].subtasks), 2)
        # test presence
        with self.assertRaises(KeyError):
            self.model.tasks["task 4"].subtasks["subtask 4 3"]
            self.model.db["task 4"]["subtask 4 3"]
        # test sequence
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 1"].sequence, 1)
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 2"].sequence, 2)

    # TODO add tests for soted_items
    def test_modify_task(self):
        self.model.modify_task_in_db("task 1", "task 1 +", True)
        with self.assertRaises(KeyError):
            self.model.tasks["task 1"]
            self.model.db["task 1"]
        self.assertEqual(self.model.tasks["task 1 +"].completed, True)
        self.assertEqual(self.model.db["task 1 +"]["completed"], True)
        self.model.modify_task_in_db("task 1 +", "task 1", True)
        with self.assertRaises(KeyError):
            self.model.tasks["task 1 +"]
            self.model.db["task 1 +"]
        self.assertEqual(self.model.tasks["task 1"].completed, True)
        self.assertEqual(self.model.db["task 1"]["completed"], True)
        self.model.modify_task_in_db("task 1", completed=False)
        self.model.modify_task_in_db("task 1", "task 2", True)
        self.assertIsInstance(self.model.db["task 1"], dict)
        self.assertIsInstance(self.model.db["task 2"], dict)
        self.assertEqual(self.model.db["task 1"]["completed"], False)
        self.assertEqual(self.model.db["task 2"]["completed"], False)
        # modfiy selected
        self.model.modify_task_in_db("task 4", selected=True)
        self.assertEqual(self.model.db["task 4"]["selected"], True)
        self.assertEqual(self.model.tasks["task 4"].selected, True)
        self.model.modify_task_in_db("task 4", selected=False)
        self.assertEqual(self.model.db["task 4"]["selected"], False)
        self.assertEqual(self.model.tasks["task 4"].selected, False)

    # TODO add tests for soted_items
    def test_modify_subtask(self):
        self.model.modify_subtask_in_db("task 1", "subtask 1 1", "subtask 1 1 +", True, True)
        with self.assertRaises(KeyError):
            self.model.db["task 1"]["subtask 1 1"]
            self.model.tasks["task 1"].subtasks["subtask 1 1"]
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1 +"].description, "subtask 1 1 +")
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1 +"].sequence, 1)
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1 +"].completed, True)
        self.assertEqual(self.model.tasks["task 1"].subtasks["subtask 1 1 +"].selected, True)
        self.assertEqual(self.model.db["task 1"]["subtask 1 1 +"]["description"], "subtask 1 1 +")
        self.assertEqual(self.model.db["task 1"]["subtask 1 1 +"]["sequence"], 1)
        self.assertEqual(self.model.db["task 1"]["subtask 1 1 +"]["completed"], True)
        self.assertEqual(self.model.db["task 1"]["subtask 1 1 +"]["selected"], True)
        # other subtask
        self.model.modify_subtask_in_db("task 2", "subtask 2 2", "subtask 2 2 +", True)
        with self.assertRaises(KeyError):
            self.model.db["task 2"]["subtask 2 2"]
            self.model.tasks["task 2"].subtasks["subtask 2 2"]
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 2 +"].description, "subtask 2 2 +")
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 2 +"].sequence, 2)
        self.assertEqual(self.model.tasks["task 2"].subtasks["subtask 2 2 +"].completed, True)
        self.assertEqual(self.model.db["task 2"]["subtask 2 2 +"]["description"], "subtask 2 2 +")
        self.assertEqual(self.model.db["task 2"]["subtask 2 2 +"]["sequence"], 2)
        self.assertEqual(self.model.db["task 2"]["subtask 2 2 +"]["completed"], True)
        # update only description
        self.model.modify_subtask_in_db("task 3", "subtask 3 1", "subtask 3 1 +")
        with self.assertRaises(KeyError):
            self.model.db["task 3"]["subtask 3 1"]
            self.model.tasks["task 3"].subtasks["subtask 3 1"]
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 1 +"].description, "subtask 3 1 +")
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 1 +"].sequence, 1)
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 1 +"].completed, False)
        self.assertEqual(self.model.db["task 3"]["subtask 3 1 +"]["description"], "subtask 3 1 +")
        self.assertEqual(self.model.db["task 3"]["subtask 3 1 +"]["sequence"], 1)
        self.assertEqual(self.model.db["task 3"]["subtask 3 1 +"]["completed"], False)
        # update only completion
        self.model.modify_subtask_in_db("task 3", "subtask 3 2", completed=True)
        self.assertIsInstance(self.model.db["task 3"]["subtask 3 2"], dict)
        self.assertIn("subtask 3 2", self.model.tasks["task 3"].subtasks.items)
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 2"].description, "subtask 3 2")
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 2"].sequence, 2)
        self.assertEqual(self.model.tasks["task 3"].subtasks["subtask 3 2"].completed, True)
        self.assertEqual(self.model.db["task 3"]["subtask 3 2"]["description"], "subtask 3 2")
        self.assertEqual(self.model.db["task 3"]["subtask 3 2"]["sequence"], 2)
        self.assertEqual(self.model.db["task 3"]["subtask 3 2"]["completed"], True)
        # update selected
        self.model.modify_subtask_in_db("task 4", "subtask 4 1", selected=True)
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 1"].selected, True)
        self.assertEqual(self.model.db["task 4"]["subtask 4 1"]["selected"], True)
        self.model.modify_subtask_in_db("task 4", "subtask 4 1", selected=False)
        self.assertEqual(self.model.tasks["task 4"].subtasks["subtask 4 1"].selected, False)
        self.assertEqual(self.model.db["task 4"]["subtask 4 1"]["selected"], False)


    def tearDown(self) -> None:
        for root, _, files in os.walk("./testdata"):
            for file in files:
                os.remove(os.path.join(root, file))


if __name__ == "__main__":
    unittest.main(verbosity=2)
