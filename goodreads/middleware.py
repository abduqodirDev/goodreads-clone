class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # So'rovni oldin
        print("So'rov qabul qilinyapdi")

        response = self.get_response(request)

        # Javobni keyin
        print("Javob berilyapdi")

        return response
