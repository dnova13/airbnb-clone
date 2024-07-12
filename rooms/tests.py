from django.test import TestCase
from . import models



# Create your tests here.
class RoomsTest(TestCase):    
    def test_room_data(self):
        model = models.Room
        rooms = model.objects.all()[:10]
        
        print(rooms)

        self.assertTrue(len(rooms) > 0, "queryset has no data.")
  