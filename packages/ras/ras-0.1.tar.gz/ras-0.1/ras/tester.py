from ras.RasHandler import RasHandler

if __name__ == "__main__":
    errorJson = {
        '_id': "831fa6b2-3e2b-4dc5-ae22-f95b55055555",
        'ts': 1585497690280,
        'status-code': 422,
        'tid': "831fa6b2-3e2b-4dc5-ae22-f95b55055555",
        'endpoint': "mdas_simulate",
        'message': "mdas_simulate failed.",
        'description': "Enqueue call returned a return code: 408 response",
        'internal-status-code': 408,
        'component': "plt-enqueue",
        'component-message': "job Time out=7200",
        'client': "iaasf",
        'batch': "PCRMIV"
    }

    rasHandler = RasHandler()
    rasHandler.insert('error', errorJson)