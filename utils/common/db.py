from django.db import transaction


def delete_everything_created_in_transaction():
    transaction.set_rollback(True)
