from fastapi import Request


class AppRequest(Request):
	async def body(self) -> bytes:
		if not hasattr(self, '_body'):
			body = await super().body()
			'''manipulate the request body before it is 
			processed by your application'''
			self._body = body
		return self._body
