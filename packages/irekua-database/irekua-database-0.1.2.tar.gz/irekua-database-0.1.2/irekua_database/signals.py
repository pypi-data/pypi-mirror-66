from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def validate_model(sender, instance, raw=False, **kwargs):
    print('validating')
    try:
        app_label = instance._meta.app_label
    except AttributeError:
        return

    if app_label != 'database':
        return

    if not raw:
        instance.full_clean()
