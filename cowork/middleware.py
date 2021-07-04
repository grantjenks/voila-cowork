"""Middleware to wrap requests in a thread.

"""

import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor()


def thread_executor(get_response):

    def middleware(request):
        future = executor.submit(get_response, request)
        response = future.result()
        return response

    return middleware
