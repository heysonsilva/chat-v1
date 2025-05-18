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
      "update_id": number,
      "message": {
        "message_id": number,
        "from": {
          "id": number,
          "is_bot": boolean,
          "first_name": string,
          "language_code": "pt-br"
        }
        },
    }
  ]
}


