from django.dispatch import Signal


operand_started = Signal(providing_args=['operation_proc', 'ocode', 'operator'])

operand_finished = Signal(providing_args=['pid', 'ocode', 'field_values'])

