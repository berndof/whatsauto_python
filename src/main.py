import asyncio
from app.manager import Manager


async def main():
    manager = Manager()
    await manager.start()
    try:
        # Mantém o serviço rodando, escutando por eventos do socket e requisições do webserver
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        # Trata a interrupção pelo teclado para encerrar os serviços
        await manager.close()
    finally:
        # Encerra o loop de eventos
        asyncio.get_event_loop().close()

if __name__ == "__main__":
    asyncio.run(main())
