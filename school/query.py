from django.db import models
from django.db.models.query import QuerySet
from school.models import School

class SchoolHelper(object):

    query = QuerySet(model=School)
    
    def doesExists(self, name):
        self.name = name
        if self.query.filter(pk=name).exists():
            return True
        else:
            return False


if __name__ == '__main__':
    sh = SchoolHelper()
    print sh.doesExists('Yeo park')
    print sh.doesExists('Yeo parka')
