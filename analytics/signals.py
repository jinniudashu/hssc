from django.dispatch import Signal

object_viewed_signal = Signal(providing_args=['instance', 'request'])

# object_viewed_signal.send(instance.__class__, instance=instance, request=request)