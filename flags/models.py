from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class FlagState(models.Model):
    name = models.CharField(max_length=64)
    condition = models.CharField(max_length=64, default='boolean')
    value = models.CharField(max_length=127, default='True')

    class Meta:
        app_label = 'flags'
        unique_together = ('name', 'condition', 'value')

    def __str__(self):
        return "{name} is enabled when {condition} is {value}".format(
            name=self.name, condition=self.condition, value=self.value)


@receiver(post_save, sender=FlagState)
@receiver(post_delete, sender=FlagState)
def invalidate_cached_flag_conditions(sender, instance, **kwargs):
    cache.delete('flags_conditions_' + instance.name)
