from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken
from users.models import User

class ChatAppMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        params = parse_qs(query_string)
        token = params.get("token", [""])[0]
        
        scope["user"] = await self.get_user(token)
        return await super().__call__(scope, receive, send)
    
    @database_sync_to_async
    def get_user(self, token):
        try:
            untyped_token = UntypedToken(token)
            payload = untyped_token.payload
            
            user = User.objects.get(id=payload["user_id"])
            return user
        except InvalidToken:
            return AnonymousUser()
