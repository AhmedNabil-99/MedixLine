from django.db import models
from authentication.models import User

# Create your models here.

class Chat(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE , related_name="sender")
    reciever = models.ForeignKey(User , on_delete=models.CASCADE , related_name="reciever")
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"
    

    def __str__(self):
        return f"{self.sender} to {self.reciever} at {self.date}"
    

    @property
    def sender_profiles(self):
        sender_peofile = User.objects.get(user=self.sender)
        return sender_peofile
    
    @property
    def reciever_profiles(self):
        reciever_peofile = User.objects.get(user=self.reciever)
        return reciever_peofile