from django.db import models

class DadosViagem(models.Model):
    unit_id = models.BigIntegerField()
    time_write = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    distance_traveled = models.DecimalField(max_digits=10, decimal_places=2)
    avg_speed = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_used = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        managed = False
        db_table = 'viagens'