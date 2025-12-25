class EntityNotFoundError(Exception):
    """Сущность не найдена"""
    pass

class EntityHasDependenciesError(Exception):
    """Нельзя удалить, потому что есть связанные данные"""
    pass