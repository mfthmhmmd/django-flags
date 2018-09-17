from django.core.cache import cache
from django.test import TestCase

from flags.models import FlagState


class FlagStateTestCase(TestCase):

    def test_flag_str(self):
        state = FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        self.assertEqual(
            str(state),
            'MY_FLAG is enabled when boolean is True'
        )

    def test_save_signal_receiver(self):
        cache.set('flags_conditions_MY_FLAG', 'test value')
        self.assertIsNotNone(cache.get('flags_conditions_MY_FLAG'))
        FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        self.assertIsNone(cache.get('flags_conditions_MY_FLAG'))

    def test_delete_signal_receiver(self):
        state = FlagState.objects.create(
            name='MY_FLAG',
            condition='boolean',
            value='True'
        )
        cache.set('flags_conditions_MY_FLAG', 'test value')
        self.assertIsNotNone(cache.get('flags_conditions_MY_FLAG'))
        state.delete()
        self.assertIsNone(cache.get('flags_conditions_MY_FLAG'))
