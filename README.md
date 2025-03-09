>> ANOTAÇÕES

API TOKEN: ...

NOME DO BOT: ...

ID do CHAT GROUP: ... 

ENDPOINT DO TELEGRAM:
https://api.telegram.org/bot<TOKEN>/


ESTRUTURAS DE REQUISIÇÕES 

============== JSON de Resposta do GET ==================

POST /bot<TOKEN>/sendMessage HTTP/1.1
Host: api.telegram.org
Content-Type: application/json
Content-Length: <TAMANHO_DO_CORPO>

{
    "chat_id": "<CHAT_ID>",
    "text": "Sua mensagem aqui"
}

=========================================================

=================== JSON Resposta =======================
{
  "ok": true,
  "result": [
    {
      "update_id": 372105685,
      "message": {
        "message_id": 2,
        "from": {
          "id": 5021057327,
          "is_bot": false,
          "first_name": "meclLove",
          "language_code": "pt-br"
        }
        },
    }
  ]
}


