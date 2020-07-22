class TransactionMetadata(object):
    CURRENCY = 'BRL'
    PARTNER_ID = None
    SERVICE_TAGS = []

    def __init__(self, transaction_type=None):
        self._transaction_type = transaction_type

    def __new__(cls, transaction_type=None):
        variables_classes = {
            'uber_trip': UberTrip,
            'ifood_order': IFoodOrder,
            'play_store': GooglePlayStore
        }

        if cls is TransactionMetadata:
            return super(TransactionMetadata, cls).__new__(
                variables_classes[transaction_type]
            )

        return super(TransactionMetadata, cls). \
            __new__(cls, transaction_type)


class UberTrip(TransactionMetadata):
    PARTNER_ID = '001'
    SERVICE_TAGS = ['mobility', 'cars']


class IFoodOrder(TransactionMetadata):
    PARTNER_ID = '002'
    SERVICE_TAGS = ['food', 'buffets']


class GooglePlayStore(TransactionMetadata):
    PARTNER_ID = '003'
    SERVICE_TAGS = ['games', 'apps']


# How to use:

uber_trip = TransactionMetadata(transaction_type='uber_trip')
print(repr(uber_trip.SERVICE_TAGS))

ifood_order = TransactionMetadata(transaction_type='ifood_order')
print(repr(ifood_order.SERVICE_TAGS))

play_store_buy = TransactionMetadata(transaction_type='play_store')
print(repr(play_store_buy.SERVICE_TAGS))

