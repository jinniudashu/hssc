from django.dispatch import Signal


operand_started = Signal(providing_args=['pid', 'ocode', 'operator'])

operand_finished = Signal(providing_args=['pid', 'request', 'form_data', 'formset_data'])
