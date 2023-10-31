#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DSStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    @classmethod
    def setUpClass(cls) -> None:
        cls.storage = DBStorage()
        cls.storage.reload()

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        self.storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self) -> None:
        """Tests count method"""
        obs = [User(password="pwd1", email="one@mail.com"),
                    User(password='pwd2', email="two@mail.com"),
                    Amenity(name="WiFi")]
        for ob in obs:
            self.storage.new(ob)
        self.assertEqual(self.storage.count(User), 2)
        self.assertEqual(self.storage.count(Amenity), 1)
        self.assertEqual(self.storage.count(), 3)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self) -> None:
        """tests the get method"""
        user = User(password="pwd", email="one@mail.com")
        user.save()
        state = State(name='Kogi')
        state.save()
        city = City(state_id=state.id, name="Lokoja")
        city.save()
        self.assertEqual(user.password,
                         self.storage.get(User, user.id).password)
        self.assertEqual(city.state_id,
                         self.storage.get(City, city.id).state_id)
        self.assertEqual(state.name,
                         self.storage.get(State, state.id).name)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        amenity1 = Amenity(name='Internet')
        state1 = State(name='Abuja')
        self.storage.new(amenity1)
        self.storage.new(state1)
        objs = [amenity1, state1]
        for obj in objs:
            self.assertIs(obj, self.storage.get(obj.__class__, obj.id))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to db"""
        new_dict = {}
        user = User(email='me@hbnb.com', password='pwd')
        user.save()
        amenity1 = Amenity(name='Internet')
        amenity1.save()
        obs = [user, amenity1]
        for ob in obs:
            key = ob.__class__.__name__ + "." + ob.id
            new_dict[key] = ob
        self.storage.close()
        for ob in new_dict:
            self.assertIn(ob, self.storage.all())
