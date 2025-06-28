class LivreIndisponibleError(Exception):
    def __init__(self,message="le livre demandé est indisponible"):
        super().__init__(message)
class QuotaEmpruntDepasseError(Exception):
    def __init__(self,message="impssible d'emprunter plus"):
        super().__init__(message)
class MembreInexistantError(Exception):
    def __init__(self,message="le membre recherché inexistant"):
        super().__init__(message)
class LivreInexistantError(Exception):
    def __init__(self,message="le livre recherché inexistant"):
        super().__init__(message)