from django.dispatch import Signal


operand_finished = Signal(providing_args=['pid', 'ocode'])