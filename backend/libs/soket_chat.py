import asyncio
import websockets
import json

import asyncio
import websockets
import json

# Словарь для хранения активных соединений
connected_clients = {}

# Словарь для хранения чатов (id_user + id_worker -> chat_id)
chats = {}

async def open_websocket(user_id: str, worker_id: str, websocket):
    """
    Открывает веб-сокет для пользователя и сотрудника.

    :param user_id: Уникальный идентификатор пользователя.
    :param worker_id: Уникальный идентификатор сотрудника.
    :param websocket: Объект веб-сокета.
    """
    # Создаем уникальный идентификатор чата
    chat_id = f"{user_id}_{worker_id}"

    # Сохраняем соединение
    connected_clients[user_id] = websocket
    connected_clients[worker_id] = websocket
    chats[chat_id] = {"user_id": user_id, "worker_id": worker_id}

    print(f"Чат {chat_id} открыт для пользователя {user_id} и сотрудника {worker_id}")

    try:
        # Ожидаем сообщения от клиента
        async for message in websocket:
            data = json.loads(message)
            print(f"Получено сообщение в чате {chat_id}: {data}")

    except websockets.ConnectionClosed:
        print(f"Соединение в чате {chat_id} закрыто")
    
            
            
            
async def send_message(sender_id: str, recipient_id: str, message: str):
    """
    Пересылает сообщение от отправителя к получателю.

    :param sender_id: Уникальный идентификатор отправителя.
    :param recipient_id: Уникальный идентификатор получателя.
    :param message: Сообщение для отправки.
    """
    if recipient_id in connected_clients:
        websocket = connected_clients[recipient_id]
        try:
            await websocket.send(json.dumps({
                "type": "message",
                "from": sender_id,
                "text": message,
            }))
            print(f"Сообщение отправлено от {sender_id} к {recipient_id}")
        except websockets.ConnectionClosed:
            print(f"Не удалось отправить сообщение пользователю {recipient_id}: соединение закрыто")
    else:
        print(f"Пользователь {recipient_id} не найден")
        
async def handle_connection(websocket, path):
    """
    Обрабатывает подключение клиента.
    """
    try:
        # Получаем данные авторизации
        auth_data = await websocket.recv()
        auth_data = json.loads(auth_data)
        user_id = auth_data.get("user_id")
        worker_id = auth_data.get("worker_id")

        if not user_id or not worker_id:
            await websocket.close()
            return

        # Открываем веб-сокет для пользователя и сотрудника
        await open_websocket(user_id, worker_id, websocket)

    except websockets.ConnectionClosed:
        print("Соединение закрыто")

# Запуск сервера
start_server = websockets.serve(handle_connection, "localhost", 8765)


async def close_websocket(user_id: str, worker_id: str):
    """
    Закрывает веб-сокет для пользователя и сотрудника.

    :param user_id: Уникальный идентификатор пользователя.
    :param worker_id: Уникальный идентификатор сотрудника.
    """
    # Закрываем соединение для пользователя
    if user_id in connected_clients:
        websocket = connected_clients[user_id]
        await websocket.close()
        del connected_clients[user_id]
        print(f"Соединение для пользователя {user_id} закрыто")

    # Закрываем соединение для сотрудника
    if worker_id in connected_clients:
        websocket = connected_clients[worker_id]
        await websocket.close()
        del connected_clients[worker_id]
        print(f"Соединение для сотрудника {worker_id} закрыто")

    # Удаляем чат из словаря chats (если используется)
    chat_id = f"{user_id}_{worker_id}"
    if chat_id in chats:
        del chats[chat_id]
        print(f"Чат {chat_id} удален")
      
       

print("Сервер запущен на ws://localhost:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()