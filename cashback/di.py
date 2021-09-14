import logging

from dependency_injector import containers, providers

from cashback import database, config, services, storages


class Container(containers.DeclarativeContainer):
    logger = logging.getLogger(__name__)
    db = providers.Singleton(database.Database, database_url=config.database_url(), logger=logger)

    cashback_storage = providers.Singleton(storages.CashbackStorage, cashback_url=config.cashback_url())

    order_storage = providers.Factory(storages.OrderStorage, db=db)

    cashback_service = providers.Factory(
        services.CashbackService,
        cashback_storage=cashback_storage,
        order_storage=order_storage
    )
