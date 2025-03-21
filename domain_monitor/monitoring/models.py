from django.db import models

class Domain(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
  
    def __str__(self):
        return self.name

class DomainStatus(models.Model):
    domain = models.OneToOneField(Domain, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default='OK')
    expiration_date = models.DateTimeField('expiration date', null=True)
    registrar = models.CharField(max_length=200, null=True)
    response_code = models.IntegerField(null=True)
    response_time = models.FloatField(null=True)
    
    def __str__(self):
        return self.status

class DomainHistory(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    date = models.DateTimeField('date')
    status = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.domain} - {self.date} - {self.status}"
